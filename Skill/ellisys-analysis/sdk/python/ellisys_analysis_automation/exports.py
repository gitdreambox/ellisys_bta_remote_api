"""Typed export modes for the Ellisys analyzer.

The server exposes a single ``Export(outputFilename, exportName, exportOptions)`` op on the
BASE interface; ``exportName`` selects the mode and every option value travels as a string.
This module provides the base :class:`ExportMode` token (with metadata), the :class:`ExportModes`
catalogue of base modes, the typed option carriers, and the single serializer that renders them to
the wire. Product-specific modes/options live in their product module (e.g. ``bluetooth``).
``output`` paths are always interpreted on the ANALYZER machine (like :meth:`Analyzer.stop_and_save`).

See ``docs/export-design.md`` for the rationale.
"""
from __future__ import annotations

import datetime
import enum
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

__all__ = [
    "ExportMode",
    "ExportModes",
    "ExportOptions",
    "FilteredTraceOptions",
    "ThroughputOptions",
    "render_option_value",
    "ExportOptionError",
]

# Picoseconds-per-second; matches the *_ps / timedelta convention used by Marker.time.
_PS_PER_SECOND = 1_000_000_000_000


class ExportOptionError(ValueError):
    """A client-side export-option problem (bad value type, failed validation).

    Distinct from ``OperationError`` (server-side, e.g. a wrong-product mode) and
    ``ConnectionFailed``.
    """


@dataclass(frozen=True, slots=True, eq=False)
class ExportMode:
    """A known ``exportName`` token plus its metadata.

    ``value`` is the exact wire token; ``product`` is ``"base"`` / ``"bluetooth"`` / ``""``
    (unknown). Equality and hashing are by ``value`` only, and ``str(mode)`` is the token, so a
    mode compares equal to its raw string and methods accept ``str | ExportMode`` -- modes newer
    than this SDK stay reachable by passing the raw token. Use the :class:`ExportModes` (base) and
    product catalogues (e.g. ``BluetoothExportModes``) for the known ones.
    """

    value: str
    product: str = ""
    description: str = ""

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"ExportMode({self.value!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ExportMode):
            return self.value == other.value
        if isinstance(other, str):
            return self.value == other
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.value)


class ExportModes:
    """The base export modes (valid on any analyzer). Enumerate them via :attr:`ALL`."""

    FILTERED_TRACE_TIME_RANGE = ExportMode(
        "filtered_trace_time_range", "base", "Filtered trace, by time range.")
    FILTERED_TRACE_ACTIVE_OVERVIEW = ExportMode(
        "filtered_trace_active_overview", "base", "Filtered trace, by active overview.")
    THROUGHPUT = ExportMode("throughput", "base", "Throughput over a time range.")

    #: All base modes (there is no server op to enumerate; this is documentation, not a gate).
    ALL = (FILTERED_TRACE_TIME_RANGE, FILTERED_TRACE_ACTIVE_OVERVIEW, THROUGHPUT)


def _to_ps(value: int | datetime.timedelta) -> int:
    """Coerce an int (already picoseconds) or a timedelta to integer picoseconds."""
    if isinstance(value, datetime.timedelta):
        return round(value.total_seconds() * _PS_PER_SECOND)
    return int(value)


def render_option_value(value: object) -> str | None:
    """Render ONE typed option value to its exact wire string, or ``None`` to OMIT it.

    The single source of truth for the wire rules:
      * ``None``      -> ``None``  (unset; never sent, server default applies)
      * ``bool``      -> ``"true"`` / ``"false"``  (.NET ``bool.Parse`` form)
      * ``enum.Enum`` -> ``str(value.value)``      (exact token, e.g. ``"SilenceSmooth"``)
      * ``timedelta`` -> integer picoseconds as a decimal string
      * ``int``       -> decimal string
      * ``str``       -> verbatim

    ``bool`` is checked before ``int`` (``bool`` subclasses ``int``) and ``enum`` before ``int``
    (an ``IntEnum`` is an ``int``).
    """
    if value is None:
        return None
    if isinstance(value, bool):                 # MUST precede int
        return "true" if value else "false"
    if isinstance(value, enum.Enum):            # MUST precede int (IntEnum is int)
        return str(value.value)
    if isinstance(value, datetime.timedelta):
        return str(_to_ps(value))
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return value
    raise ExportOptionError(f"unsupported export option value type: {type(value).__name__}")


def _build_export_options(options: Mapping[str, object] | None, module) -> list:
    """Render ``{OptionName: typed value}`` into ``list[module.ExportOption]``, omitting None.

    The ONLY function that constructs Ice ``ExportOption`` structs (*module* is the slice2py
    bindings module from ``Analyzer._bindings_module()`` -- no Ice import lives here). Private:
    *module* is an internal lazy-binding detail.
    """
    rendered = []
    for name, value in (options or {}).items():
        wire = render_option_value(value)
        if wire is not None:                    # unset -> never sent
            rendered.append(module.ExportOption(OptionName=name, OptionValue=wire))
    return rendered


@runtime_checkable
class ExportOptions(Protocol):
    """Anything that can supply server-spelled option pairs (every carrier implements it)."""

    def as_options(self) -> dict[str, object]:
        """Return ``{ServerOptionName: typed value}`` (the snake->Pascal mapping lives here)."""
        ...

    def validate(self) -> None:
        """Validate the options, raising :class:`ExportOptionError` on a contradictory value (e.g.
        a time range whose end precedes its start). Carriers without constraints are a no-op."""
        ...


def _validate_range(start: int | datetime.timedelta | None,
                    end: int | datetime.timedelta | None) -> None:
    if start is not None and end is not None and _to_ps(end) < _to_ps(start):
        raise ExportOptionError("range end must be >= range start")


@dataclass(frozen=True, slots=True)
class FilteredTraceOptions:
    """Options for ``filtered_trace_time_range`` and ``filtered_trace_active_overview``."""

    start_time_ps: int | datetime.timedelta | None = None    # StartTime   (ps, default 0)
    max_size_bytes: int | None = None                        # MaxSize     (bytes, default full)
    max_duration_ps: int | datetime.timedelta | None = None  # MaxDuration (ps, default full)
    max_items: int | None = None                             # MaxItems    (count, default full)

    def as_options(self) -> dict[str, object]:
        """The ``{server OptionName: value}`` mapping for this mode (unset options are dropped)."""
        return {
            "StartTime": self.start_time_ps,
            "MaxSize": self.max_size_bytes,
            "MaxDuration": self.max_duration_ps,
            "MaxItems": self.max_items,
        }

    def validate(self) -> None:
        """No range constraints to check."""


@dataclass(frozen=True, slots=True)
class ThroughputOptions:
    """Options for ``throughput``."""

    range_start_time_ps: int | datetime.timedelta | None = None  # RangeStartTime
    range_end_time_ps: int | datetime.timedelta | None = None    # RangeEndTime

    def as_options(self) -> dict[str, object]:
        """The ``{server OptionName: value}`` mapping for this mode (unset options are dropped)."""
        return {"RangeStartTime": self.range_start_time_ps, "RangeEndTime": self.range_end_time_ps}

    def validate(self) -> None:
        """Validate the options -- raises :class:`ExportOptionError` if range end precedes start."""
        _validate_range(self.range_start_time_ps, self.range_end_time_ps)
