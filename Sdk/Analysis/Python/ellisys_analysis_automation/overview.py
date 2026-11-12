"""Pythonic, bounded navigation of the analyzer's Overview tree.

The server exposes the Overview as a tree of items addressed by opaque ``int`` handles, with
edges this module hides safely. A trace can hold MILLIONS of items, so "never read all" is a
**structural** guarantee here, not advice:

* You reach children/matches only through a **cursor** (:meth:`OverviewItem.cursor`,
  :meth:`OverviewScope.search_cursor`) that yields one bounded :class:`Page` at a time. No
  object can represent "all items"; the whole-set batch readers live only on a ``Page``,
  whose size is capped by construction (``PAGE_MAX``).
* Every round-trip is bounded by a default page size; the page-size argument is clamped to
  ``PAGE_MAX``. Materializing into memory (``take``/``[a:b]``/``materialize``) is an explicit
  opt-in that **raises** :class:`BoundExceeded` past ``HARD_CAP`` -- never a silent pull.
* Server handle memory is bounded **by default**: a page-streaming cursor releases each page's
  handles at the page boundary (``release_mode="page"``), so a full scan keeps the server's
  handle high-water mark at ``O(page_size)``.
* A full traversal of an overview that is still **growing** (a trace loading, or the analyzer
  recording) raises :class:`OverviewIncomplete` rather than silently stopping short. Pass
  ``follow=True`` to tail it as items arrive, or ``snapshot=True`` for just what exists now.

Handles cannot be freed individually (``ReleaseAllOverviewItemHandles`` is global), so the
unit of lifetime is an :class:`OverviewScope` (see :meth:`Analyzer.overview`). Using a handle
after its scope closed -- or after a page-release invalidated it -- raises :class:`ScopeClosed`
before any network call. Everything routes through ``Analyzer._call``; no Ice type leaks out.

See ``docs/bounded-access-design.md`` for the full rationale.
"""
from __future__ import annotations

import datetime
import enum
import time
import xml.etree.ElementTree as ET
from collections.abc import Callable, Iterator, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

from .errors import OperationError
from .markers import MarkerColor

if TYPE_CHECKING:  # avoid a runtime import cycle (analyzer imports this module)
    from .analyzer import Analyzer

__all__ = [
    "ScopeClosed",
    "BoundExceeded",
    "ItemField",
    "XmlFilter",
    "ItemRecord",
    "OverviewScope",
    "OverviewItem",
    "OverviewItemList",
    "Page",
    "ChildCursor",
    "SearchCursor",
    "OverviewIncomplete",
]

_UNSET: object = object()  # sentinel: distinguishes "not fetched yet" from a real None/""

#: Per-round-trip page for cursors/streams.
PAGE_DEFAULT: int = 256
#: Hard ceiling on any single page / batch round-trip (clamps caller-supplied page sizes).
PAGE_MAX: int = 4096
#: Ceiling on an explicit materialize (take / finite slice / materialize). Exceeding it raises.
HARD_CAP: int = 100_000
#: Default recursion depth for search_cursor (finite on purpose -- NOT the whole subtree).
DEFAULT_SEARCH_DEPTH: int = 8
#: How many of the base's direct children a search window covers per round-trip.
DEFAULT_SEARCH_FANOUT: int = 16
#: Default ceiling on total search matches before search raises.
DEFAULT_RESULT_CAP: int = 100_000
#: Default poll interval (seconds) for follow= traversals while the overview is still growing.
_FOLLOW_POLL: float = 0.25

#: SearchOverviewItems maxDepth for "whole subtree" (Slice int32 max; the server saturates at
#: the tree's real depth). NOTE: the .ice docs say maxDepth=1 returns only the direct children,
#: but a live analyzer empirically treats maxDepth=0 as "direct children" and -1 as "nothing"
#: (verified) -- so we never pass -1.
_UNBOUNDED_DEPTH: int = 2**31 - 1


class ScopeClosed(OperationError):
    """A handle was used after its :class:`OverviewScope` released it.

    Raised when an item/page is touched after its scope exited, after
    :meth:`OverviewScope.release_handles`, or after a page-streaming cursor released the page
    that minted it. Subclasses :class:`~ellisys_analysis_automation.errors.OperationError`, so
    existing ``except OperationError`` handlers still catch it.
    """


class BoundExceeded(OperationError):
    """A bounded read was asked to materialize more than its cap.

    Raised by ``take(n)`` / ``cursor[a:b]`` / ``materialize(cap=)`` / search ``result_cap``
    when the requested or discovered size would exceed the limit, and by constructing a
    :class:`Page` larger than ``HARD_CAP``. Fail-loud by design: there is no silent truncation.
    """


class OverviewIncomplete(OperationError):
    """A full traversal was attempted while the overview is still being populated.

    The overview grows while a trace is **loading** or while the analyzer is **recording**, so a
    plain ``stream`` / ``stream_records`` / ``walk`` / ``iter_children`` / ``materialize`` would
    stop at whatever count happened to exist when it started and silently drop the rest. Rather
    than truncate quietly, those ops raise this unless the caller says how to handle the growth:

    * wait until it is complete first (``analyzer.load(wait=True)`` / ``wait_until_loaded()``),
    * pass ``follow=True`` to keep traversing as items arrive (live-tail), or
    * pass ``snapshot=True`` to deliberately traverse only what exists right now.

    Bounded reads (``take(n)`` / ``page()`` / ``cursor[a:b]``) are exempt -- they are explicitly
    partial by request, so nothing is lost silently. Subclasses ``OperationError``.
    """


class ItemField(enum.Enum):
    """Selects which batch operation a reader issues. One member == one plural Ice op."""

    DESCRIPTION = "description"   # GetOverviewItemsDescription
    TIME = "time"                # GetOverviewItemsTimeInPicoseconds
    DATA = "data"                # GetOverviewItemsData
    XML = "xml"                  # GetOverviewItemsXmlReport

    @staticmethod
    def xml_filtered(*field_names: str) -> "XmlFilter":
        """Filtered Details XML (-> GetOverviewItemsXmlReportFiltered)."""
        return XmlFilter(tuple(field_names))


@dataclass(frozen=True)
class XmlFilter:
    """A request for the filtered Details XML of the given field names."""

    field_names: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ItemRecord:
    """A pure-data, handle-FREE snapshot of one item -- safe to keep after the scope closes.

    Only the fields you requested are populated; the rest stay ``None``. ``position`` is the
    item's index within its parent / result set (for traceability) -- it is *not* a handle.
    """

    position: int
    description: str | None = None
    time_ps: int | None = None
    data: bytes | None = None
    xml: str | None = None

    @property
    def time(self) -> datetime.timedelta | None:
        """``time_ps`` as a :class:`datetime.timedelta` (microsecond resolution), or ``None``."""
        return None if self.time_ps is None else _ps_to_timedelta(self.time_ps)

    @property
    def time_seconds(self) -> float | None:
        """``time_ps`` in seconds as a float, or ``None``."""
        return None if self.time_ps is None else self.time_ps / 1e12


#: Fields a Page prefetches on construction (the two columns analysts read most). Override per
#: call with the ``prefetch=`` argument; pass ``prefetch=()`` to skip.
DEFAULT_PREFETCH: tuple[ItemField, ...] = (ItemField.DESCRIPTION, ItemField.TIME)


def _ps_to_timedelta(picoseconds: int) -> datetime.timedelta:
    return datetime.timedelta(microseconds=picoseconds / 1_000_000)


def _clamp_page(size: int | None) -> int:
    """Clamp a caller-supplied page size into ``[1, PAGE_MAX]`` (defaulting when ``None``)."""
    if size is None:
        return PAGE_DEFAULT
    return max(1, min(int(size), PAGE_MAX))


def _column(scope: "OverviewScope", handles: list[int], field: ItemField | XmlFilter) -> list:
    """One bounded batch round-trip for *field* across *handles*; returns the column in order."""
    if not handles:
        return []
    if len(handles) > HARD_CAP:  # defensive: no single batch may exceed the hard ceiling
        raise BoundExceeded(f"batch of {len(handles):,} handles exceeds HARD_CAP={HARD_CAP:,}.")
    if isinstance(field, XmlFilter):
        return list(scope._op("GetOverviewItemsXmlReportFiltered", handles, list(field.field_names)))
    if field is ItemField.DESCRIPTION:
        return list(scope._op("GetOverviewItemsDescription", handles))
    if field is ItemField.TIME:
        return list(scope._op("GetOverviewItemsTimeInPicoseconds", handles))
    if field is ItemField.DATA:
        return list(scope._op("GetOverviewItemsData", handles))
    if field is ItemField.XML:
        return list(scope._op("GetOverviewItemsXmlReport", handles))
    raise TypeError(f"unsupported field selector: {field!r}")


def _record_at(position: int, fields: Sequence[ItemField | XmlFilter], cols: dict, idx: int) -> ItemRecord:
    """Assemble one ItemRecord from pre-fetched columns at row *idx*."""
    kw: dict = {}
    for field in fields:
        value = cols[field][idx]
        if isinstance(field, XmlFilter) or field is ItemField.XML:
            kw["xml"] = value
        elif field is ItemField.DESCRIPTION:
            kw["description"] = value
        elif field is ItemField.TIME:
            kw["time_ps"] = value
        elif field is ItemField.DATA:
            kw["data"] = value
    return ItemRecord(position=position, **kw)


def _parse_detail_fields(xml_text: str) -> dict[str, str]:
    """Best-effort name->value map from a Details XML report.

    Real Details XML nests ``<Item name="..." value="..."/>`` elements; we map each element
    that carries a name (``name``/``Name``) to its value (``value``/``Value`` or element text).
    """
    fields: dict[str, str] = {}
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return fields
    for element in root.iter():
        name = element.get("name") or element.get("Name")
        if name is None:
            continue
        value = element.get("value")
        if value is None:
            value = element.get("Value")
        if value is None:
            value = (element.text or "").strip()
        fields[name] = value
    return fields


class OverviewItem:
    """A lazy, scope-bound wrapper around one opaque handle.

    Constructing one is free. Each single-item field property does one Ice call on first access
    then caches it. For many items, navigate with :meth:`cursor` (bounded) or stream with
    :meth:`iter_children` / :meth:`walk`.

    ``_path`` is the item's index path from the overview root (e.g. ``(3, 7)`` == root's child
    3, its child 7). It lets a page-releasing cursor re-acquire the item after a global release.
    Items whose path is unknown (search results, the selected item) carry ``None`` and cannot
    be re-seated.
    """

    __slots__ = ("_scope", "_handle", "_position", "_path", "_gen", "_depth",
                 "_desc", "_time_ps", "_data", "_xml", "_child_count")

    def __init__(self, scope: "OverviewScope", handle: int, *, position: int = 0,
                 path: tuple[int, ...] | None = None) -> None:
        self._scope = scope
        self._handle = handle
        self._position = position
        self._path = path
        self._gen = scope._generation
        self._depth = 0
        self._desc: object = _UNSET
        self._time_ps: object = _UNSET
        self._data: object = _UNSET
        self._xml: object = _UNSET
        self._child_count: object = _UNSET

    # -- liveness -------------------------------------------------------------------
    def _check(self) -> None:
        self._scope._ensure_live()
        if self._gen != self._scope._generation:
            raise ScopeClosed(
                "this overview item's handles were released; re-navigate from scope.root.")

    @property
    def handle(self) -> int:
        """The raw server handle -- an escape hatch for ops the SDK doesn't wrap yet."""
        self._check()
        return self._handle

    @property
    def position(self) -> int:
        """Index of this item within its parent / result set."""
        return self._position

    @property
    def depth(self) -> int:
        """Depth relative to where a :meth:`walk` started (0 for that level's children)."""
        return self._depth

    # -- single-item field accessors (one round-trip each, cached) -------------------
    @property
    def description(self) -> str:
        """Text of the Item column (-> GetOverviewItemDescription)."""
        self._check()  # always: a cached value must not outlive its scope (use ItemRecord for that)
        if self._desc is _UNSET:
            self._desc = self._scope._op("GetOverviewItemDescription", self._handle)
        return self._desc  # type: ignore[return-value]

    @property
    def time_ps(self) -> int:
        """Timestamp in picoseconds, lossless 64-bit (-> GetOverviewItemTimeInPicoseconds)."""
        self._check()
        if self._time_ps is _UNSET:
            self._time_ps = self._scope._op("GetOverviewItemTimeInPicoseconds", self._handle)
        return self._time_ps  # type: ignore[return-value]

    @property
    def time(self) -> datetime.timedelta:
        """Timestamp as a :class:`datetime.timedelta` (microsecond resolution)."""
        return _ps_to_timedelta(self.time_ps)

    @property
    def data(self) -> bytes:
        """Bytes shown in the Raw data view (-> GetOverviewItemData)."""
        self._check()
        if self._data is _UNSET:
            self._data = self._scope._op("GetOverviewItemData", self._handle)
        return self._data  # type: ignore[return-value]

    def xml_report(self, *, fields: Sequence[str] | None = None) -> str:
        """Details view as XML (-> GetOverviewItemXmlReport / ...Filtered)."""
        self._check()
        if fields is not None:
            return self._scope._op("GetOverviewItemXmlReportFiltered", self._handle, list(fields))
        if self._xml is _UNSET:
            self._xml = self._scope._op("GetOverviewItemXmlReport", self._handle)
        return self._xml  # type: ignore[return-value]

    # -- traversal ------------------------------------------------------------------
    @property
    def child_count(self) -> int:
        """Number of direct children (-> GetOverviewItemChildCount, cached). Cheap even at millions."""
        self._check()
        if self._child_count is _UNSET:
            self._child_count = self._scope._op("GetOverviewItemChildCount", self._handle)
        return self._child_count  # type: ignore[return-value]

    def cursor(self, *, page_size: int = PAGE_DEFAULT,
               prefetch: Sequence[ItemField] | None = DEFAULT_PREFETCH,
               release_mode: Literal["page", "defer"] = "page") -> "ChildCursor":
        """A bounded cursor over this item's children (replaces the old unbounded ``children()``).

        The cursor yields one :class:`Page` at a time. ``page_size`` is clamped to ``PAGE_MAX``.
        With ``release_mode="page"`` (default) each page's handles are freed at the page
        boundary, so a full scan keeps server memory at ``O(page_size)`` -- at the cost that a
        live item must not be held across a page boundary (it raises :class:`ScopeClosed`; use
        :meth:`ChildCursor.stream_records` to keep data). Use ``release_mode="defer"`` to retain
        handles (e.g. while holding live items or running concurrent cursors).
        """
        self._check()
        return ChildCursor(self, page_size=page_size, prefetch=prefetch, release_mode=release_mode)

    def child(self, index: int) -> "OverviewItem":
        """The single child at *index* (-> GetOverviewItemChild)."""
        self._check()
        handle = self._scope._op("GetOverviewItemChild", self._handle, index)
        path = None if self._path is None else self._path + (index,)
        return OverviewItem(self._scope, handle, position=index, path=path)

    def iter_children(self, *, batch_size: int = PAGE_DEFAULT, follow: bool = False,
                      snapshot: bool = False,
                      poll_interval: float = _FOLLOW_POLL) -> Iterator["OverviewItem"]:
        """Lazily page through direct children (``ceil(N/batch_size)`` calls, not N).

        A true generator for *bounded* exploration: break early and only fetched pages cost
        round-trips. It does NOT release handles per page (it yields live items), so for a full
        multi-million-item scan prefer :meth:`ChildCursor.stream_records`, which is page-released.

        While the overview is growing (loading/recording) this raises :class:`OverviewIncomplete`
        unless you pass ``follow=True`` (live-tail the children as they arrive) or
        ``snapshot=True`` (only the children that exist now).
        """
        self._check()
        self._scope._guard_growing(follow, snapshot)
        size = _clamp_page(batch_size)
        start = 0
        while True:
            if follow:
                self._child_count = _UNSET      # force a fresh count each pass
            total = self.child_count
            while start < total:
                take = min(size, total - start)
                handles = self._scope._op("GetOverviewItemChildren", self._handle, start, take)
                for offset, handle in enumerate(handles):
                    path = None if self._path is None else self._path + (start + offset,)
                    yield OverviewItem(self._scope, handle, position=start + offset, path=path)
                start += take
            if not follow or not self._scope._is_growing():
                break
            time.sleep(poll_interval)

    def walk(self, *, max_depth: int | None = None, batch_size: int = PAGE_DEFAULT,
             follow: bool = False, snapshot: bool = False,
             poll_interval: float = _FOLLOW_POLL) -> Iterator["OverviewItem"]:
        """Lazy depth-first walk of descendants; sets each item's :attr:`depth`.

        Yields this item's children at depth 0, their children at depth 1, etc. *max_depth*
        limits the levels (``None`` = unbounded). Built on :meth:`iter_children` (no per-page
        release, since it holds ancestors while descending) -- intended for bounded exploration
        with early ``break``, not for materializing a whole huge tree.

        On a growing overview this raises :class:`OverviewIncomplete` unless you pass
        ``snapshot=True`` (walk what exists now) or ``follow=True`` (wait until loading /
        recording stops, then walk the complete tree -- live-tailing a recursive walk is not
        well-defined, so ``follow`` here means "let it finish first").
        """
        self._check()
        self._scope._guard_growing(follow, snapshot)
        if follow:
            while self._scope._is_growing():
                time.sleep(poll_interval)

        def _recurse(item: "OverviewItem", depth: int) -> Iterator["OverviewItem"]:
            # the policy was resolved at the top; iterate children unguarded (snapshot=True)
            for child in item.iter_children(batch_size=batch_size, snapshot=True):
                child._depth = depth
                yield child
                if max_depth is None or depth + 1 < max_depth:
                    yield from _recurse(child, depth + 1)

        yield from _recurse(self, 0)

    # -- selection / snapshot -------------------------------------------------------
    def select(self) -> None:
        """Highlight this item in the analyzer GUI (-> SelectOverviewItem)."""
        self._check()
        self._scope._op("SelectOverviewItem", self._handle)

    def add_marker(self, text: str, *, color: MarkerColor = MarkerColor.YELLOW) -> None:
        """Select this item and drop a marker on it (-> SelectOverviewItem + AddMarkerOnSelectedOverviewItem)."""
        self.select()
        self._scope._analyzer.add_marker_on_selected_overview_item(text, color=color)

    def record(self, *fields: ItemField | XmlFilter) -> ItemRecord:
        """Snapshot this item to a handle-free :class:`ItemRecord` (single-item ops)."""
        self._check()
        selected = fields or (ItemField.DESCRIPTION, ItemField.TIME)
        kw: dict = {}
        for field in selected:
            if isinstance(field, XmlFilter):
                kw["xml"] = self.xml_report(fields=field.field_names)
            elif field is ItemField.XML:
                kw["xml"] = self.xml_report()
            elif field is ItemField.DESCRIPTION:
                kw["description"] = self.description
            elif field is ItemField.TIME:
                kw["time_ps"] = self.time_ps
            elif field is ItemField.DATA:
                kw["data"] = self.data
        return ItemRecord(position=self._position, **kw)

    def __repr__(self) -> str:  # never does I/O -- safe to log
        if self._desc is not _UNSET:
            return f"<OverviewItem #{self._position} {self._desc!r}>"
        return f"<OverviewItem #{self._position} in {self._scope._name!r}>"


class OverviewItemList(Sequence[OverviewItem]):
    """An ordered, scope-bound, batch-backed sequence of :class:`OverviewItem` (base of :class:`Page`).

    No longer constructed directly by users -- a bounded :class:`Page` is what cursors hand out.
    ``len`` / indexing / slicing / iteration are pure-local; each batch reader is one bounded
    round-trip over the list's handles. Construction is capped at ``HARD_CAP``.
    """

    def __init__(
        self,
        scope: "OverviewScope",
        handles: Sequence[int],
        *,
        start: int = 0,
        prefetch: Sequence[ItemField] | None = None,
        base_path: tuple[int, ...] | None = None,
    ) -> None:
        if len(handles) > HARD_CAP:
            raise BoundExceeded(f"{len(handles):,} items exceed HARD_CAP={HARD_CAP:,}.")
        self._scope = scope
        self._gen = scope._generation
        self._items = [
            OverviewItem(scope, h, position=start + i,
                         path=(None if base_path is None else base_path + (start + i,)))
            for i, h in enumerate(handles)
        ]
        fields = DEFAULT_PREFETCH if prefetch is None else tuple(prefetch)
        if self._items and fields:
            hs = [it._handle for it in self._items]
            for field in fields:
                self._seed(field, _column(scope, hs, field))

    @classmethod
    def _from_items(cls, scope: "OverviewScope", items: Sequence[OverviewItem]) -> "OverviewItemList":
        """Build a list reusing existing item objects (and their caches); no round-trip."""
        obj = cls.__new__(cls)
        obj._scope = scope
        obj._gen = scope._generation
        obj._items = list(items)
        return obj

    def _check(self) -> None:
        self._scope._ensure_live()
        if self._gen != self._scope._generation:
            raise ScopeClosed(
                "this page's handles were released; fetch a fresh page from the cursor.")

    def _seed(self, field: ItemField | XmlFilter, column: list) -> None:
        attr = {
            ItemField.DESCRIPTION: "_desc",
            ItemField.TIME: "_time_ps",
            ItemField.DATA: "_data",
            ItemField.XML: "_xml",
        }.get(field if isinstance(field, ItemField) else None)  # type: ignore[arg-type]
        if attr is None:
            return  # filtered XML is not cached on the item (the filter varies)
        for item, value in zip(self._items, column):
            setattr(item, attr, value)

    # -- pure-local sequence protocol (zero round-trips) ----------------------------
    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, index):  # int -> OverviewItem; slice -> OverviewItemList
        if isinstance(index, slice):
            return OverviewItemList._from_items(self._scope, self._items[index])
        return self._items[index]

    def __iter__(self) -> Iterator[OverviewItem]:
        return iter(self._items)

    @property
    def handles(self) -> tuple[int, ...]:
        """The raw handles, in order (escape hatch)."""
        self._check()
        return tuple(it._handle for it in self._items)

    # -- batch readers (one bounded round-trip each; also seed item caches) ----------
    def descriptions(self) -> list[str]:
        """Item-column text for every item (-> GetOverviewItemsDescription)."""
        return self._read(ItemField.DESCRIPTION)

    def times_ps(self) -> list[int]:
        """Timestamps in picoseconds (-> GetOverviewItemsTimeInPicoseconds)."""
        return self._read(ItemField.TIME)

    def times(self) -> list[datetime.timedelta]:
        """Timestamps as timedeltas (microsecond resolution)."""
        return [_ps_to_timedelta(ps) for ps in self.times_ps()]

    def data(self) -> list[bytes]:
        """Raw-data-view bytes for every item (-> GetOverviewItemsData)."""
        return self._read(ItemField.DATA)

    def xml_reports(self, *, fields: Sequence[str] | None = None) -> list[str]:
        """Details XML for every item (-> GetOverviewItemsXmlReport / ...Filtered)."""
        self._check()
        field: ItemField | XmlFilter = ItemField.XML if fields is None else XmlFilter(tuple(fields))
        column = _column(self._scope, [it._handle for it in self._items], field)
        self._seed(field, column)
        return list(column)

    def _read(self, field: ItemField) -> list:
        self._check()
        column = _column(self._scope, [it._handle for it in self._items], field)
        self._seed(field, column)
        return list(column)

    # -- snapshots / convenience ----------------------------------------------------
    def records(self, *fields: ItemField | XmlFilter) -> list[ItemRecord]:
        """Snapshot the whole list to handle-free records (one batch per requested field)."""
        self._check()
        selected = fields or (ItemField.DESCRIPTION, ItemField.TIME)
        hs = [it._handle for it in self._items]
        cols = {field: _column(self._scope, hs, field) for field in selected}
        return [_record_at(it._position, selected, cols, i) for i, it in enumerate(self._items)]

    def to_rows(self, *field_names: str) -> list[dict[str, str]]:
        """Filtered Details fields parsed into dicts (for pandas / CSV)."""
        records = self.records(ItemField.xml_filtered(*field_names))
        return [{name: _parse_detail_fields(r.xml or "").get(name, "") for name in field_names}
                for r in records]

    def filter(self, predicate: Callable[[OverviewItem], bool]) -> "OverviewItemList":
        """A new list of the items matching *predicate* (reuses the same item objects)."""
        self._check()
        return OverviewItemList._from_items(self._scope, [it for it in self._items if predicate(it)])

    def __repr__(self) -> str:  # no I/O
        return f"<{type(self).__name__} n={len(self._items)} in {self._scope._name!r}>"


class Page(OverviewItemList):
    """One bounded window of children/matches -- the only object carrying whole-set readers.

    A ``Page`` is an :class:`OverviewItemList` (so it has the batch readers / slicing / filter)
    whose length is capped by construction (``<= PAGE_MAX`` for a streamed page, ``<= HARD_CAP``
    for a ``take``/slice result). It also knows its ``position`` in the parent and whether more
    follow (:attr:`has_more`).
    """

    def __init__(self, scope: "OverviewScope", handles: Sequence[int], *, position: int,
                 page_size: int, total: int, prefetch: Sequence[ItemField] | None = None,
                 cursor: "ChildCursor | None" = None,
                 base_path: tuple[int, ...] | None = None) -> None:
        super().__init__(scope, handles, start=position, prefetch=prefetch, base_path=base_path)
        self.position = position
        self.page_size = page_size
        self.total = total
        self.has_more = position + len(self._items) < total
        self._cursor = cursor

    def next_page(self) -> "Page | None":
        """Advance the owning cursor and return the next page (``None`` at the end)."""
        if self._cursor is None:
            return None
        return self._cursor.next_page()


class ChildCursor:
    """A bounded, page-at-a-time cursor over one item's children. Built by :meth:`OverviewItem.cursor`.

    Streaming (:meth:`stream`, :meth:`stream_records`) and manual paging (:meth:`page`,
    :meth:`next_page`, :meth:`seek`, :meth:`reset`) page in windows of ``page_size`` (clamped to
    ``PAGE_MAX``). Materializing (:meth:`take`, ``cursor[a:b]``, :meth:`materialize`) is bounded
    and raises :class:`BoundExceeded` past ``HARD_CAP``. It is NOT a ``Sequence``; ``total`` is
    the cheap count, not a fetch of items.
    """

    def __init__(self, parent: OverviewItem, *, page_size: int,
                 prefetch: Sequence[ItemField] | None, release_mode: Literal["page", "defer"]) -> None:
        self._scope = parent._scope
        self._parent_path = parent._path
        self._parent_h = parent._handle
        self._parent_gen = parent._gen
        self._page_size = _clamp_page(page_size)
        self._prefetch = prefetch
        # page-release needs a path to re-seat the parent after a global release; fall back to
        # "defer" when the parent is not addressable (e.g. a search result).
        self._release_mode = "page" if (release_mode == "page" and parent._path is not None) else "defer"
        self._position = 0
        self._last_len = 0
        self._total: int | None = None

    # -- re-seating after a global release ------------------------------------------
    def _parent_handle(self) -> int:
        self._scope._ensure_live()
        if self._parent_gen == self._scope._generation:
            return self._parent_h
        if self._parent_path is None:
            raise ScopeClosed("cursor parent handle was released and cannot be re-seated.")
        handle = self._scope._root_handle()
        for index in self._parent_path:
            handle = self._scope._op("GetOverviewItemChild", handle, index)
        self._parent_h, self._parent_gen = handle, self._scope._generation
        return handle

    def _release_prior(self) -> None:
        if self._release_mode == "page":
            self._scope.release_handles()   # global ReleaseAll + generation bump

    @property
    def total(self) -> int:
        """Number of children (-> GetOverviewItemChildCount). Cheap; not a fetch of items."""
        if self._total is None:
            self._total = self._scope._op("GetOverviewItemChildCount", self._parent_handle())
        return self._total

    @property
    def position(self) -> int:
        """Index of the next unread child."""
        return self._position

    def __iter__(self):
        raise TypeError(
            "a ChildCursor is not directly iterable (that would invite reading all items); "
            "use stream(), stream_records(), take(n), page(), or a finite cursor[a:b] slice.")

    # -- internal fetch -------------------------------------------------------------
    def _window(self, start: int, size: int, prefetch: Sequence[ItemField] | None) -> Page:
        size = _clamp_page(size)
        total = self.total
        start = max(0, min(start, total))
        count = min(size, total - start)
        handles: list[int] = []
        if count > 0:
            handles = list(self._scope._op("GetOverviewItemChildren", self._parent_handle(), start, count))
        self._last_len = len(handles)
        return Page(self._scope, handles, position=start, page_size=size, total=total,
                    prefetch=prefetch, cursor=self, base_path=self._parent_path)

    def _collect(self, start: int, want: int) -> list[int]:
        """Accumulate up to *want* handles from *start* in PAGE_MAX chunks (no release; retained)."""
        handles: list[int] = []
        total = self.total
        pos = start
        while len(handles) < want and pos < total:
            chunk = self._scope._op("GetOverviewItemChildren", self._parent_handle(),
                                    pos, min(PAGE_MAX, want - len(handles)))
            chunk = list(chunk)
            if not chunk:
                break
            handles.extend(chunk)
            pos += len(chunk)
        return handles[:want]

    # -- manual paging --------------------------------------------------------------
    def page(self, size: int | None = None) -> Page:
        """The page at the current position (peek; does not advance). ``size`` clamped to PAGE_MAX."""
        return self._window(self._position, self._page_size if size is None else size, self._prefetch)

    def next_page(self) -> Page | None:
        """Advance past the current page (releasing it if ``release_mode='page'``); ``None`` at end."""
        self._position += self._last_len
        self._release_prior()
        if self._position >= self.total:
            self._last_len = 0
            return None
        return self._window(self._position, self._page_size, self._prefetch)

    def reset(self) -> None:
        """Release any live page and seek back to the start."""
        self._release_prior()
        self._position = 0
        self._last_len = 0

    def seek(self, index: int) -> None:
        """Release any live page and jump the position to *index*."""
        self._release_prior()
        self._position = max(0, index)
        self._last_len = 0

    # -- streaming ------------------------------------------------------------------
    def stream(self, *, prefetch: Sequence[ItemField] | None = None,
               follow: bool = False, snapshot: bool = False,
               poll_interval: float = _FOLLOW_POLL) -> Iterator[OverviewItem]:
        """Yield children one at a time, paging under the hood (batched, bounded, page-released).

        The obvious loop on a 10M-child node: ``O(page_size)`` handles in flight, ~3 ops/page,
        early ``break`` stops fetching. With ``release_mode='page'`` an item must be consumed
        within its page -- don't stash live items across iterations (use ``stream_records``).

        While the overview is still growing (loading/recording) this raises
        :class:`OverviewIncomplete` unless you pass ``follow=True`` (re-read the count at the end
        and keep yielding new items as they arrive, until growth stops or you ``break``) or
        ``snapshot=True`` (traverse only the items that exist now).
        """
        pf = self._prefetch if prefetch is None else prefetch
        self._scope._guard_growing(follow, snapshot)
        pos = self._position
        first = True
        while True:
            if follow:
                self._total = None              # force a fresh count each pass
            total = self.total
            while pos < total:
                if not first:
                    self._release_prior()       # release the PREVIOUS page before the next
                first = False
                page = self._window(pos, self._page_size, pf)
                if len(page) == 0:
                    break
                yield from page
                pos += len(page)
                self._position = pos
            if not follow or not self._scope._is_growing():
                break
            time.sleep(poll_interval)

    def stream_records(self, *fields: ItemField | XmlFilter,
                       page_size: int | None = None, follow: bool = False,
                       snapshot: bool = False,
                       poll_interval: float = _FOLLOW_POLL) -> Iterator[ItemRecord]:
        """Yield handle-free :class:`ItemRecord`\\ s, page by page, releasing each page.

        The safe full-scan extractor: constant client memory, ``O(page_size)`` server handles,
        batched (one round-trip per field per page). Records survive the per-page release.
        Defaults to description + time. ``follow`` / ``snapshot`` behave as in :meth:`stream`
        (a growing overview otherwise raises :class:`OverviewIncomplete`).
        """
        selected = fields or (ItemField.DESCRIPTION, ItemField.TIME)
        size = _clamp_page(page_size if page_size is not None else self._page_size)
        self._scope._guard_growing(follow, snapshot)
        pos = self._position
        first = True
        while True:
            if follow:
                self._total = None              # force a fresh count each pass
            total = self.total
            while pos < total:
                if not first:
                    self._release_prior()
                first = False
                handles = list(self._scope._op("GetOverviewItemChildren", self._parent_handle(),
                                               pos, min(size, total - pos)))
                if not handles:
                    break
                cols = {field: _column(self._scope, handles, field) for field in selected}
                for i in range(len(handles)):
                    yield _record_at(pos + i, selected, cols, i)
                pos += len(handles)
                self._position = pos
            if not follow or not self._scope._is_growing():
                break
            time.sleep(poll_interval)
        self._release_prior()  # records are handle-free, so releasing the last page is safe

    # -- bounded materialize (all RAISE past the cap) -------------------------------
    def take(self, n: int) -> Page:
        """A :class:`Page` of the first ``min(n, total)`` children. Raises if ``n > HARD_CAP``."""
        if n > HARD_CAP:
            raise BoundExceeded(
                f"take(n={n:,}) exceeds HARD_CAP={HARD_CAP:,}; stream() or raise the cap deliberately.")
        want = min(max(0, n), self.total)
        handles = self._collect(0, want)
        return Page(self._scope, handles, position=0, page_size=len(handles), total=self.total,
                    prefetch=self._prefetch, cursor=self, base_path=self._parent_path)

    def __getitem__(self, key: slice) -> Page:
        """``cursor[a:b]`` -> a :class:`Page` of that finite window. Open/over-cap slices raise."""
        if not isinstance(key, slice):
            raise TypeError("cursor supports slicing only (cursor[a:b]); use take()/page() otherwise.")
        if key.step not in (None, 1):
            raise ValueError("step slicing is not supported.")
        if key.start is None or key.stop is None:
            raise ValueError("open-ended slices are not allowed; give both bounds, e.g. cursor[a:b].")
        start, stop = key.start, key.stop
        if start < 0 or stop < 0:
            raise ValueError("negative slice bounds are not supported.")
        span = stop - start
        if span > HARD_CAP:
            raise BoundExceeded(f"slice span {span:,} exceeds HARD_CAP={HARD_CAP:,}.")
        handles = self._collect(start, max(0, span))
        return Page(self._scope, handles, position=start, page_size=len(handles), total=self.total,
                    prefetch=self._prefetch, cursor=self, base_path=self._parent_path)

    def materialize(self, *, cap: int = HARD_CAP,
                    fields: Sequence[ItemField | XmlFilter] = DEFAULT_PREFETCH,
                    follow: bool = False, snapshot: bool = False,
                    poll_interval: float = _FOLLOW_POLL) -> list[ItemRecord]:
        """All children as handle-free records (page-released). Raises if ``total > cap``.

        On a growing overview this raises :class:`OverviewIncomplete` unless you pass
        ``snapshot=True`` (materialize what exists now) or ``follow=True`` (wait until loading /
        recording stops, then materialize the complete set -- so do not ``follow`` an open-ended
        live recording here; use :meth:`stream` and ``break`` for that).
        """
        self._scope._guard_growing(follow, snapshot)
        if follow:
            while self._scope._is_growing():
                time.sleep(poll_interval)
            self._total = None                  # fresh count now that growth has stopped
        total = self.total
        if total > cap:
            raise BoundExceeded(
                f"{total:,} items exceed cap={cap:,}; raise cap or use stream_records().")
        selected = tuple(fields) or (ItemField.DESCRIPTION, ItemField.TIME)
        out: list[ItemRecord] = []
        pos = 0
        first = True
        while pos < total:
            if not first:
                self._release_prior()
            first = False
            handles = list(self._scope._op("GetOverviewItemChildren", self._parent_handle(),
                                           pos, min(PAGE_MAX, total - pos)))
            if not handles:
                break
            cols = {field: _column(self._scope, handles, field) for field in selected}
            for i in range(len(handles)):
                out.append(_record_at(pos + i, selected, cols, i))
            pos += len(handles)
        self._release_prior()
        return out

    def to_table(self, *field_names: str, cap: int = HARD_CAP,
                 follow: bool = False, snapshot: bool = False) -> list[dict[str, str]]:
        """All children's filtered Details fields as dicts (for pandas / CSV). Raises if over *cap*.

        ``follow`` / ``snapshot`` are forwarded to :meth:`materialize` (a growing overview
        otherwise raises :class:`OverviewIncomplete`).
        """
        records = self.materialize(cap=cap, fields=(ItemField.xml_filtered(*field_names),),
                                   follow=follow, snapshot=snapshot)
        return [{name: _parse_detail_fields(r.xml or "").get(name, "") for name in field_names}
                for r in records]


class SearchCursor:
    """A bounded cursor over search matches. Built by :meth:`OverviewScope.search_cursor`.

    ``SearchOverviewItems`` has no result paging, so this bounds the search SPACE: it windows
    the base's DIRECT children in steps of ``search_fanout``, issuing one search per window and
    (by default) releasing each window's match handles before the next. ``max_depth`` is finite
    by default; ``result_cap`` raises :class:`BoundExceeded` if total matches exceed it.
    ``scanned`` / ``found`` expose progress.

    Residual risk (inherent to the server): a single windowed child whose subtree alone holds
    millions of matches still returns them in one array; ``max_depth`` and ``result_cap`` cap
    the damage to a loud raise rather than an OOM, but cannot subdivide one subtree.
    """

    def __init__(self, scope: "OverviewScope", base: OverviewItem, *,
                 description: Sequence[str], field_name: Sequence[str], field_value: Sequence[str],
                 search_fanout: int, max_depth: int | None, result_cap: int,
                 prefetch: Sequence[ItemField] | None) -> None:
        self._scope = scope
        self._base_path = base._path
        self._base_h = base._handle
        self._base_gen = base._gen
        self._desc = list(description)
        self._name = list(field_name)
        self._val = list(field_value)
        self._fanout = max(1, search_fanout)
        self._max_depth = _UNBOUNDED_DEPTH if max_depth is None else max_depth
        self._result_cap = result_cap
        self._prefetch = prefetch
        self._window_index = 0
        self._scanned = 0
        self._found = 0
        self._base_total: int | None = None

    @property
    def scanned(self) -> int:
        """Direct children of the base searched so far."""
        return self._scanned

    @property
    def found(self) -> int:
        """Matches yielded so far."""
        return self._found

    def _base_handle(self) -> int:
        self._scope._ensure_live()
        if self._base_gen == self._scope._generation:
            return self._base_h
        if self._base_path is None:
            raise ScopeClosed("search base handle was released and cannot be re-seated.")
        handle = self._scope._root_handle()
        for index in self._base_path:
            handle = self._scope._op("GetOverviewItemChild", handle, index)
        self._base_h, self._base_gen = handle, self._scope._generation
        return handle

    def _base_children(self) -> int:
        if self._base_total is None:
            self._base_total = self._scope._op("GetOverviewItemChildCount", self._base_handle())
        return self._base_total

    def _search_window(self, start: int, count: int) -> list[int]:
        return list(self._scope._op("SearchOverviewItems", self._base_handle(), start, count,
                                    self._max_depth, self._desc, self._name, self._val))

    def next_window(self) -> Page | None:
        """The next window's matches as a :class:`Page` (``None`` when the search space is exhausted)."""
        total = self._base_children()
        if self._window_index >= total:
            return None
        if self._window_index > 0:
            self._scope.release_handles()      # release prior window before the next
        fanout = min(self._fanout, total - self._window_index)
        handles = self._search_window(self._window_index, fanout)
        window_start = self._window_index
        self._window_index += fanout
        self._scanned += fanout
        remaining = self._result_cap - self._found
        if len(handles) > remaining:
            raise BoundExceeded(
                f"search exceeded result_cap={self._result_cap:,} (>= {self._found + len(handles):,} matches); "
                f"narrow the filter, lower max_depth, or raise result_cap.")
        if len(handles) > HARD_CAP:
            raise BoundExceeded(
                f"a single search window returned {len(handles):,} matches (> HARD_CAP={HARD_CAP:,}); "
                f"narrow the filter or reduce max_depth / search_fanout.")
        self._found += len(handles)
        return Page(self._scope, handles, position=window_start, page_size=len(handles),
                    total=total, prefetch=self._prefetch, cursor=None, base_path=None)

    def stream(self, *, snapshot: bool = False) -> Iterator[OverviewItem]:
        """Yield matches one at a time, windowing the search space (consume within each window).

        Like the other full traversals this raises :class:`OverviewIncomplete` while the overview
        is loading or recording: the searched child count is captured once, so a live search would
        silently miss later arrivals. Pass ``snapshot=True`` to search just what exists now.
        """
        self._scope._guard_growing(False, snapshot)
        while True:
            page = self.next_window()
            if page is None:
                break
            yield from page

    def reset(self) -> None:
        """Release matches and restart the search from the first window."""
        self._scope.release_handles()
        self._window_index = 0
        self._scanned = 0
        self._found = 0

    def take(self, n: int) -> Page:
        """A :class:`Page` of the first ``min(n, matches)`` matches. Raises if ``n > HARD_CAP``."""
        if n > HARD_CAP:
            raise BoundExceeded(
                f"take(n={n:,}) exceeds HARD_CAP={HARD_CAP:,}; stream() or raise the cap deliberately.")
        total = self._base_children()
        collected: list[int] = []
        wi = 0
        while wi < total and len(collected) < n:
            fanout = min(self._fanout, total - wi)
            collected.extend(self._search_window(wi, fanout))
            wi += fanout
            if len(collected) > HARD_CAP:
                raise BoundExceeded(
                    f"search accumulated > HARD_CAP={HARD_CAP:,} matches; narrow the filter.")
        kept = collected[:n]
        self._scanned = wi
        self._found = len(kept)
        return Page(self._scope, kept, position=0, page_size=len(kept), total=len(kept),
                    prefetch=self._prefetch, cursor=None, base_path=None)

    def materialize(self, *, cap: int = HARD_CAP,
                    fields: Sequence[ItemField | XmlFilter] = DEFAULT_PREFETCH,
                    snapshot: bool = False) -> list[ItemRecord]:
        """All matches as handle-free records (window-released). Raises if matches exceed *cap*.

        Raises :class:`OverviewIncomplete` while loading or recording; pass ``snapshot=True`` to
        materialize just what exists now.
        """
        self._scope._guard_growing(False, snapshot)
        selected = tuple(fields) or (ItemField.DESCRIPTION, ItemField.TIME)
        total = self._base_children()
        out: list[ItemRecord] = []
        wi = 0
        first = True
        while wi < total:
            if not first:
                self._scope.release_handles()
            first = False
            fanout = min(self._fanout, total - wi)
            handles = self._search_window(wi, fanout)
            wi += fanout
            self._scanned = wi
            if len(out) + len(handles) > cap:
                raise BoundExceeded(
                    f"search results exceed cap={cap:,}; narrow the filter or raise cap.")
            if handles:
                cols = {field: _column(self._scope, handles, field) for field in selected}
                base = len(out)
                for i in range(len(handles)):
                    out.append(_record_at(base + i, selected, cols, i))
            self._found = len(out)
        self._scope.release_handles()
        return out


class OverviewScope:
    """Owns one server-side handle session for one active overview.

    Constructed only by :meth:`Analyzer.overview` -- never directly. It is the single place that
    calls ``ReleaseAllOverviewItemHandles`` (on exit, via :meth:`release_handles`, or at a
    page-streaming cursor's page boundaries). Every item / page / cursor it mints checks the
    scope is live before any network call.
    """

    def __init__(self, analyzer: "Analyzer", name: str | None) -> None:
        self._analyzer = analyzer
        self._name = name
        self._live = True
        self._generation = 0
        self._root: OverviewItem | None = None

    # -- internal plumbing ----------------------------------------------------------
    def _ensure_live(self) -> None:
        if not self._live:
            raise ScopeClosed("the overview scope has closed; its item handles were released.")

    def _op(self, _operation: str, *args):
        """Invoke an Ice op by name through the analyzer's error-translating chokepoint."""
        self._ensure_live()
        analyzer = self._analyzer
        return analyzer._call(getattr(analyzer._proxy, _operation), *args)

    def _root_handle(self) -> int:
        """A fresh root handle in the current generation (-> OverviewRootItem)."""
        self._ensure_live()
        return self._op("OverviewRootItem")

    def _invalidate(self) -> None:
        """Mark every handle minted so far stale (next use raises ScopeClosed)."""
        self._generation += 1
        self._root = None

    # -- growth guard (loading / recording) -----------------------------------------
    def _is_growing(self) -> bool:
        """True while the overview may still be growing -- a trace is loading or recording."""
        return self._analyzer.is_loading or self._analyzer.is_recording

    def _guard_growing(self, follow: bool, snapshot: bool) -> None:
        """Gate a full traversal when the overview is still being populated.

        Raises :class:`OverviewIncomplete` if a trace is loading / recording and the caller did
        not opt in via ``follow`` or ``snapshot``. A no-op once growth has stopped.
        """
        if follow and snapshot:
            raise ValueError("pass at most one of follow= / snapshot=.")
        if not (follow or snapshot) and self._is_growing():
            raise OverviewIncomplete(
                "the overview is still being populated (a trace is loading or the analyzer is "
                "recording), so a full traversal would stop short and silently drop the rest. "
                "Wait until it is complete (analyzer.wait_until_loaded() / load(wait=True)), or "
                "pass follow=True to traverse as items arrive, or snapshot=True to traverse only "
                "what exists now.")

    # -- identity / context ---------------------------------------------------------
    @property
    def name(self) -> str | None:
        """The overview this scope is bound to."""
        return self._name

    @property
    def closed(self) -> bool:
        """``True`` once the scope has exited."""
        return not self._live

    @property
    def root(self) -> OverviewItem:
        """The active overview's root item (-> OverviewRootItem; re-fetched if released)."""
        self._ensure_live()
        if self._root is None:
            self._root = OverviewItem(self, self._root_handle(), position=0, path=())
        return self._root

    # -- stateful settings (mutate the tree; invalidate existing handles) -----------
    @property
    def query(self) -> str:
        """The active overview's filter query (-> GetOverviewQuery)."""
        return self._op("GetOverviewQuery")

    def set_query(self, query: str, *, wait: bool = True, timeout: float | None = 600.0) -> None:
        """Apply a filter query (-> SetOverviewQuery). Invalidates existing handles.

        Queries filter the overview, inside the analyzer, on any overview column or Details
        field -- e.g. ``Item = "AVDTP*" && Status != "OK"``. Comparators ``= != < > <= >=``;
        comma-separated alternative values; ``!`` before a value for NOT; ``&&``/``||`` and
        parentheses; numbers (``123``, ``0xABCD``, ``0b0101``, inclusive ranges ``7..10``); data
        patterns ``0x[A1 ## *]`` (``##`` = any byte, trailing ``*`` = any rest); ``RegEx("...")``;
        ``ByteAt(Field, n)``. The analyzer re-filters the overview in the background (a
        "Filtering data" running task; ``is_loading`` stays ``False``): by default this call
        **blocks** until that finishes. Pass ``wait=False`` to return immediately and settle
        later via :meth:`Analyzer.wait_until_idle`. A malformed query raises
        :class:`OperationError` ("Invalid query"); an unknown field name silently matches
        *nothing*. ``""`` clears the filter. See the SDK guide's "Overview queries" section.
        """
        self._op("SetOverviewQuery", query)
        self._invalidate()
        if wait:
            self._analyzer.wait_until_idle(timeout=timeout)

    @property
    def protocol_layer(self) -> str:
        """The active overview's protocol layer (-> GetSelectedProtocolLayer)."""
        return self._op("GetSelectedProtocolLayer")

    def set_protocol_layer(self, layer: str) -> None:
        """Switch the protocol layer (-> SelectProtocolLayer). Invalidates existing handles.

        Protocol layers are per-protocol *views* of the overview; switching is instant (no
        background re-processing, unlike queries/device filters). Iterating
        :meth:`available_protocol_layers` and reading ``root.child_count`` per layer is the
        quickest way to fingerprint what traffic a trace contains.
        """
        self._op("SelectProtocolLayer", layer)
        self._invalidate()

    def available_protocol_layers(self) -> list[str]:
        """Protocol layers selectable on the active overview (-> GetAvailableProtocolLayers)."""
        return list(self._op("GetAvailableProtocolLayers"))

    # -- search ---------------------------------------------------------------------
    def search_cursor(
        self,
        *,
        description: Sequence[str] = (),
        field_name: Sequence[str] = (),
        field_value: Sequence[str] = (),
        within: OverviewItem | None = None,
        search_fanout: int = DEFAULT_SEARCH_FANOUT,
        max_depth: int | None = DEFAULT_SEARCH_DEPTH,
        result_cap: int = DEFAULT_RESULT_CAP,
        prefetch: Sequence[ItemField] | None = DEFAULT_PREFETCH,
    ) -> SearchCursor:
        """A bounded cursor over matches under *within* (default: the scope root).

        Filters are **glob patterns** (``*`` / ``?``) or a .NET regex prefixed ``regex:``; a
        bare literal must match the *whole* value. ``field_name`` / ``field_value`` filter the
        Details fields, pairing by index when both are given. ``max_depth`` defaults to a finite
        ``DEFAULT_SEARCH_DEPTH`` (pass ``None`` for the whole subtree); ``result_cap`` bounds the
        total matches before :class:`BoundExceeded`.
        """
        self._ensure_live()
        base = within if within is not None else self.root
        base._check()
        return SearchCursor(self, base, description=description, field_name=field_name,
                            field_value=field_value, search_fanout=search_fanout,
                            max_depth=max_depth, result_cap=result_cap, prefetch=prefetch)

    # -- selection ------------------------------------------------------------------
    @property
    def selected(self) -> OverviewItem | None:
        """The item highlighted in the GUI, or ``None`` (-> GetSelectedOverviewItem)."""
        self._ensure_live()
        handle = self._op("GetSelectedOverviewItem")
        if handle <= 0:        # GetSelectedOverviewItem returns 0/invalid when nothing is selected
            return None
        return OverviewItem(self, handle, position=0, path=None)

    def select(self, item: OverviewItem) -> None:
        """Highlight *item* in the GUI (-> SelectOverviewItem)."""
        item._check()
        self._op("SelectOverviewItem", item._handle)

    # -- mid-scope reclamation ------------------------------------------------------
    def release_handles(self) -> None:
        """Free *all* item handles now without closing the scope (-> ReleaseAllOverviewItemHandles).

        Global by nature -- there is no per-handle release. Every live item/page minted in this
        scope raises :class:`ScopeClosed` on next use; already-extracted :class:`ItemRecord`\\ s
        stay valid. This is also the primitive a page-streaming cursor uses at page boundaries.
        """
        self._op("ReleaseAllOverviewItemHandles")
        self._invalidate()
