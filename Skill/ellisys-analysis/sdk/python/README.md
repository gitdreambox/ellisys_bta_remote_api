# ellisys_analysis_automation

A Pythonic client for the Ellisys analyzer Remote Control automation API (ZeroC Ice based).
It hides the Ice machinery — connection setup, the Slice bindings, proxies, the communicator
lifecycle — behind a small, typed API.

## Install

```sh
python -m pip install -e .          # from this folder (Sdk/Analysis/Python)
```

Requires CPython 3.12–3.14 and `zeroc-ice~=3.8.2` (installed automatically). The bindings under
`ellisys_analysis_automation/_generated/` are pre-generated with `slice2py` and are **version-coupled**
to that Ice runtime — regenerate them with `Plugins\SliceAll.ps1` if the Ice version changes.
The SDK checks the installed Ice version at import and raises a clear error on a mismatch.

## Documentation

- **User guide + API reference** — the *Ellisys Analysis Automation SDK Guide (Python)*
  (Markdown/HTML/PDF), shipped in the Remote Control release archives: download
  [remote_api_analyzer.zip](https://downloads.ellisys.com/remote_api_analyzer.zip) (generic /
  Wi-Fi / WPAN / USB analyzers) or
  [bta_remote_api.zip](https://downloads.ellisys.com/bta_remote_api.zip) (Bluetooth analyzers);
  the guide is under `Sdk/Analysis/Python/`. Its API reference is generated from this package's
  docstrings, so `help(analyzer.<method>)` always has the authoritative, version-true answer.
- **For AI agents** — `llms.txt`: a dense, single-file usage guide (mental model + the rules the
  bounded API enforces). Installed with the package; locate it via
  `importlib.resources.files("ellisys_analysis_automation") / "llms.txt"`.

## Usage

```python
import ellisys_analysis_automation as ea

with ea.connect("localhost", 12345) as analyzer:
    with analyzer.recording(save_to=r"C:\traces\session"):   # path is on the analyzer machine
        input("Recording... press Enter to stop & save")
```

Navigate the Overview tree through a scope that owns the item handles and frees them on exit.
A trace can hold **millions** of items, so navigation is **bounded by construction**: you go
through a *cursor* that yields one bounded page at a time — there is no way to accidentally pull
everything.

```python
from ellisys_analysis_automation import ItemField, MarkerColor

with ea.connect("localhost", 12345) as analyzer:
    print(analyzer.overviews())                       # ['BR/EDR Overview', 'Low Energy Overview', ...]

    with analyzer.overview("BR/EDR Overview") as ov:
        print(ov.root.child_count)                    # cheap count, even at millions

        # Stream the whole tree in bounded, batched, page-released windows (safe at any size):
        for item in ov.root.cursor().stream():        # ~256 items/round-trip; O(page) memory
            print(item.time, item.description)        # served from each page's prefetch cache
            if done(item):
                break                                 # early break only fetched what you consumed

        # Bounded materialize (raises BoundExceeded past 100k); records are handle-free:
        first_50 = ov.root.cursor().take(50).records(ItemField.DESCRIPTION, ItemField.TIME)

        # Full handle-free extract for CSV/pandas — constant memory, page-released:
        for rec in ov.root.cursor().stream_records(ItemField.DESCRIPTION, ItemField.TIME):
            write_csv(rec.position, rec.time_seconds, rec.description)

        # Bounded search: glob/regex filters, finite default depth, observable progress:
        for hit in ov.search_cursor(description=["*Paging*"]).stream():
            hit.add_marker("found it", color=MarkerColor.RED)   # select + mark in one call
```

Markers (annotate the trace):

```python
from ellisys_analysis_automation import MarkerColor

analyzer.add_marker_at_time(6_391_402_625, "anomaly", color=MarkerColor.RED)  # time in picoseconds
for m in analyzer.markers():
    print(m.time, m.color.name, m.text)
```

Exports (output paths are on the **analyzer machine**):

```python
import datetime
from ellisys_analysis_automation import ExportModes, BluetoothExportModes, BluetoothAudioOptions, BluetoothPacketLossMode

# Typed base modes:
analyzer.export_filtered_trace_time_range(
    r"C:\out\first_5s.btt", max_duration_ps=datetime.timedelta(seconds=5), max_items=10_000)
analyzer.export_throughput(r"C:\out\tput.csv")

# Inspect the exact wire options offline before committing a long export:
print(analyzer.export_dry_run(r"C:\out\x", ExportModes.THROUGHPUT))   # [] (all server defaults)

# Any mode via the generic method + a typed carrier (or a raw {OptionName: value} mapping):
analyzer.export(r"C:\out\audio", BluetoothExportModes.AUDIO,
                options=BluetoothAudioOptions(packet_loss=BluetoothPacketLossMode.SILENCE_SMOOTH))
```

> A streaming cursor frees each page's handles by default (`release_mode="page"`), keeping
> server memory at `O(page_size)`. The trade: don't hold a live `OverviewItem` past its page —
> snapshot it to an `ItemRecord` (via `records()`/`stream_records()`), or use
> `cursor(release_mode="defer")` to retain handles for the scope.

> **Loading or recording?** The overview grows while a trace loads or the analyzer records, so a
> full traversal (`stream`/`stream_records`/`walk`/`iter_children`/`materialize`) raises
> `OverviewIncomplete` instead of silently stopping short. Either wait first
> (`load(wait=True)` / `wait_until_loaded()`), pass `follow=True` to tail items as they arrive
> (and `break` when your condition is met — handy during a live capture), or `snapshot=True` for
> just what exists now. Bounded reads (`take`/`page`/`cursor[a:b]`) are exempt.

Session & trace files (load is blocking by default; paths are on the analyzer machine):

```python
analyzer.load(r"C:\traces\capture.btt", timeout=300.0)   # blocks until loaded (raises LoadTimeout)
info = analyzer.trace_file_info()
print(info.path, f"{info.file_size:,} bytes", info.data_source)

print(analyzer.app_info().version)
for task in analyzer.running_tasks():
    print(task.name, task.progress)            # progress is None when the server says it's N/A

if analyzer.is_modified:
    analyzer.save_changes()
analyzer.close_trace_file()
```

Product facets expose product-specific operations — `analyzer.bluetooth`, `analyzer.wifi`,
`analyzer.wpan`, `analyzer.usb30` — each raising `NotAvailable` if the connected analyzer isn't
that product (a combo analyzer may expose several):

```python
from ellisys_analysis_automation import DeviceFilterMode, BluetoothPacketLossMode

bt = analyzer.bluetooth                                   # cached; NotAvailable if not Bluetooth
for ch, s in enumerate(bt.channel_summaries()):           # whole trace; index == RF channel
    if s.total:
        print(f"ch{ch}: ok={s.ok} err={s.errors} rate={s.error_rate:.1%}")

bt.configure_device_filter(DeviceFilterMode.KEEP_INVOLVING, [0x001122334455, 0xAABBCCDDEEFF])
bt.export_audio(r"C:\out\audio", packet_loss=BluetoothPacketLossMode.SILENCE_SMOOTH)   # via Export (bluetooth_audio)
```

Errors are Pythonic exceptions (`ConnectionFailed`, `OperationError`, `ScopeClosed` for a handle
used after its scope/page released it, and `BoundExceeded` when a materialize exceeds its cap).
No ZeroC Ice type crosses the API; the per-item escape hatches are `item.handle` /
`items.handles` (raw server handles).

## Status

- **Connection + recording lifecycle** — `connect()`, `recording()`, start/stop/abort.
- **Overview navigation** — scoped, bounded-by-construction cursors over the tree and over
  search, batch-by-default pages, and handle-free `ItemRecord` snapshots.
- **Markers** — typed `MarkerColor`, add at a time / on the selected (or any) overview item,
  and read all markers back as handle-free `Marker`s.
- **Exports** — generic `export()` + typed wrappers for the base modes, typed option carriers
  (with a `BluetoothPacketLossMode` enum), an offline `export_dry_run()`, and a raw-mapping escape hatch for
  any current/future mode.
- **Session / trace files / info** — blocking `load()` (+ `start_loading`/`is_loading`/
  `wait_until_loaded`), `trace_file_info()`/`app_info()`/`recording_status()` typed results,
  data sources, `save_changes`/`close_trace_file`, `insert_message`, running tasks, and an
  opaque settings round-trip.
- **Product facets** — `analyzer.bluetooth` (channel summaries, spectrum RSSI, device filter,
  link keys, "save & continue", typed Bluetooth exports), `analyzer.wifi` (Wi-Fi keys, device
  filter), `analyzer.wpan` (Thread/Zigbee key management), `analyzer.usb30` (link control,
  packet/symbol save). Each raises `NotAvailable` if the connected analyzer isn't that product.
- **Logic signals** — `logic_signals_state()` (level bitmask at a time) and
  `find_logic_signal_transition()` (masked edge search).

The SDK now wraps the analyzer Remote Control API — every operation except the deprecated
`InsertComment` and the legacy `ExportAudio` (superseded by the `bluetooth_audio` export mode).
