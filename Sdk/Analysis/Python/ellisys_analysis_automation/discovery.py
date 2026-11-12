"""Trace discovery -- fingerprint an unknown trace before scripting against it.

Three facts make discovery a required first step for any automated analysis:

* Overview **descriptions and field names are decoder-defined** -- close to, but not 1:1 with,
  the protocol specs -- so spec-derived keyword guesses fail (an A2DP trace says
  ``AVDTP Media Stream``; searching ``"*Streaming*"`` finds nothing).
* A Bluetooth capture contains **all nearby devices**, not only the devices of interest; the
  population must be known before narrowing with a device filter.
* **Overviews and protocol layers** are where traffic shows up, and the only way to know what a
  trace contains is counting root items across them (layer switches are instant).

:func:`explore` runs the whole pass and returns a readable report; the building blocks
(:func:`device_census`, :func:`find_position_at`, :func:`template`) are usable on their own.
"""
import html
import io
import re
from collections import Counter

__all__ = ["explore", "device_census", "find_position_at", "template"]

_ADDR_RX = re.compile(r"\b[0-9A-Fa-f]{2}(?::[0-9A-Fa-f]{2}){5}\b")
_NAMED_ADDR_RX = re.compile(r"'([^']*)'\s*((?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2})")
_COMM_RX = re.compile(r'name="Communication"[^>]*?value="([^"]*)"')


def template(description: str) -> str:
    """Normalize one item description into a reusable pattern.

    Quoted names become ``"<name>"``, 48-bit addresses ``<addr>``, hex literals ``<hex>`` and
    standalone numbers ``<n>`` -- while protocol identifiers like ``L2CAP`` are preserved.
    Counting templates over a sample yields the trace's vocabulary (the exact terms to use in
    searches and queries).
    """
    t = re.sub(r'"[^"]*"', '"<name>"', description)
    t = _ADDR_RX.sub("<addr>", t)
    t = re.sub(r"0x[0-9A-Fa-f]+", "<hex>", t)
    t = re.sub(r"(?<![A-Za-z0-9])\d+(\.\d+)?", "<n>", t)  # not inside identifiers (L2CAP)
    return t.strip()


def find_position_at(cursor, total: int, target_ps: int) -> int:
    """Binary-search chronological top-level items for the first at/after *target_ps*.

    *cursor* is a top-level :class:`~ellisys_analysis_automation.ChildCursor`; *total* its
    ``root.child_count``. ~17 bounded reads on a 100k-item overview.
    """
    lo, hi = 0, total - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if cursor[mid:mid + 1][0].time_ps < target_ps:
            lo = mid + 1
        else:
            hi = mid
    return lo


def device_census(analyzer, sample_per_overview: int = 90):
    """Sample the device population of the Bluetooth overviews.

    There is no list-devices operation in the API yet, so the population is probed from the
    Communication column of the BR/EDR and Low Energy overviews (head/middle/tail windows).
    Returns ``{overview_name: (Counter[address], {address: display_name})}`` with addresses in
    the displayed ``"AA:BB:CC:DD:EE:FF"`` form -- directly usable with
    :meth:`~ellisys_analysis_automation.bluetooth.BluetoothFacet.configure_device_filter`.
    """
    result = {}
    names = [n for n in analyzer.overviews() if n in ("BR/EDR Overview", "Low Energy Overview")]
    for name in names:
        devices: Counter[str] = Counter()
        labels: dict[str, str] = {}
        with analyzer.overview(name) as ov:
            total = ov.root.child_count
            cursor = ov.root.cursor()
            window = max(sample_per_overview // 3, 1)
            starts = sorted({0, max(total // 2 - window // 2, 0), max(total - window, 0)})
            for start in starts:
                for item in cursor[start:min(start + window, total)]:
                    m = _COMM_RX.search(item.xml_report())
                    blob = html.unescape(m.group(1)) if m else item.description
                    for label, addr in _NAMED_ADDR_RX.findall(blob):
                        labels[addr.upper()] = label
                    for addr in _ADDR_RX.findall(blob):
                        devices[addr.upper()] += 1
        result[name] = (devices, labels)
    return result


def explore(analyzer, *, trace=None, overview=None, at=None, marker=None,
            max_items=3000, max_reports=12, survey=True) -> str:
    """Run the full discovery pass and return a readable report.

    The report contains: a survey of all overviews and the target overview's protocol layers
    (root-item counts; layer switches are instant and the original layer is restored), the
    trace's markers, a census of description templates, the detail-report field names, and the
    Bluetooth device population. *trace* loads that file first (path on the analyzer machine);
    *at* (seconds) or *marker* (text, case-insensitive substring) anchor the template census
    around a time of interest and list the surrounding items.
    """
    out = io.StringIO()
    if trace:
        analyzer.load(trace)
    elif not analyzer.trace_file_info().path:
        return "No trace open on the analyzer. Pass trace=<path on the analyzer machine>."

    # 0. Survey: which overviews hold traffic? (their layer counts come once a scope is open)
    if survey:
        counts = {}
        for name in analyzer.overviews():
            with analyzer.overview(name) as ovs:
                counts[name] = ovs.root.child_count
        nonempty = {k: v for k, v in counts.items() if v}
        out.write(f"overviews with traffic ({len(nonempty)} of {len(counts)}):\n")
        for k, v in sorted(nonempty.items(), key=lambda kv: -kv[1]):
            out.write(f"  {v:>9}  {k}\n")

    # 1. Markers: the user's anchors; resolve a marker= request against them.
    markers = analyzer.markers()
    if markers:
        out.write(f"markers ({len(markers)}):\n")
        for mk in markers[:10]:
            out.write(f"  {mk.time_seconds:12.6f}s  [{mk.color.name}] {mk.text[:70]}\n")
    anchor_ps = None
    if marker:
        hit = next((m for m in markers if marker.lower() in m.text.lower()), None)
        if hit is None:
            return out.getvalue() + (
                f"no marker matching {marker!r}"
                + (f"; available: {[m.text for m in markers]}" if markers else " (trace has no markers)"))
        anchor_ps = hit.time_ps
        out.write(f"anchor: marker {hit.text!r} at {hit.time_seconds:.6f}s\n")
    elif at is not None:
        anchor_ps = int(at * 1e12)
        out.write(f"anchor: t={at}s\n")

    with analyzer.overview(overview) as ov:
        total = ov.root.child_count
        out.write(f"overview: {ov.name!r}, top-level items: {total}\n")

        # Protocol layers: instant per-protocol views; counts show what traffic is present.
        if survey:
            layers = ov.available_protocol_layers()
            if len(layers) > 1:
                original = ov.protocol_layer
                out.write(f"protocol layers ({len(layers)}; instant views of this overview):\n")
                for layer in layers:
                    ov.set_protocol_layer(layer)
                    out.write(f"  {ov.root.child_count:>9}  {layer}\n")
                ov.set_protocol_layer(original)

        cursor = ov.root.cursor()

        # 2. Description templates -- around the anchor when given, else head/middle/tail.
        census: Counter[str] = Counter()
        if anchor_ps is not None and total:
            pos = find_position_at(cursor, total, anchor_ps)
            lo, hi = max(pos - 10, 0), min(pos + 10, total)
            out.write(f"\nitems around the anchor (top-level positions {lo}..{hi - 1}):\n")
            for item in cursor[lo:hi]:
                mark = ">>" if item.position == pos else "  "
                out.write(f"  {mark} [{item.position}] {item.time}  {item.description[:78]}\n")
            w = max_items // 2
            for item in cursor[max(pos - w, 0):min(pos + w, total)]:
                census[template(item.description)] += 1
        else:
            head = max(max_items // 2, 1)
            for item in ov.root.walk(max_depth=2, snapshot=True):
                census[template(item.description)] += 1
                head -= 1
                if head <= 0:
                    break
            window = max((max_items - max_items // 2) // 2, 1)
            for start in (total // 2, max(total - window, 0)):
                stop = min(start + window, total)
                if stop > start:
                    for item in cursor[start:stop]:
                        census[template(item.description)] += 1
        out.write(f"\nsampled {sum(census.values())} items, "
                  f"{len(census)} distinct description templates\n")
        out.write("description templates (most common first):\n")
        for tpl, n in census.most_common(40):
            out.write(f"  {n:6d}  {tpl}\n")

        # 3. Field names: one detail report per distinct item kind.
        fields: Counter[str] = Counter()
        seen: set[str] = set()
        for item in ov.root.walk(max_depth=2, snapshot=True):
            tpl = template(item.description)
            if tpl in seen:
                continue
            seen.add(tpl)
            fields.update(re.findall(r'name="([^"]+)"', item.xml_report()))
            if len(seen) >= max_reports:
                break
        out.write(f"\ndetail-report field names ({len(fields)} distinct, from {len(seen)} item kinds):\n")
        out.write("  " + ", ".join(name for name, _ in fields.most_common(60)) + "\n")

    # 4. Bluetooth device population (both BT overviews).
    for name, (devices, labels) in device_census(analyzer).items():
        out.write(f"\ndevices seen in {name!r} (sampled; no list-devices API yet):\n")
        if not devices:
            out.write("  (none -- overview empty or items carry no addresses)\n")
        for addr, n in devices.most_common(12):
            label = f"  {labels[addr]!r}" if addr in labels else ""
            out.write(f"  {addr}  x{n}{label}\n")

    out.write(
        "\nScript against these EXACT terms: search_cursor(description=[...]) supports * "
        "wildcards; field searches use field_name=/field_value=; ov.set_query('Item = \"...\"') "
        "filters server-side (unknown names silently match nothing). Bluetooth: narrow busy "
        "captures with analyzer.bluetooth.configure_device_filter(DeviceFilterMode.KEEP_ONLY, "
        "['AA:BB:CC:DD:EE:FF', ...]).\n")
    return out.getvalue()
