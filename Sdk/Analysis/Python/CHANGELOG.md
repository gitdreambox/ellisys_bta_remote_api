# Changelog

All notable changes to `ellisys_analysis_automation` are recorded here. The format loosely follows
[Keep a Changelog](https://keepachangelog.com/); versions follow semantic versioning.

## 0.1.0

First cut covering the analyzer Remote Control API (every operation except the deprecated
`InsertComment` and the legacy `ExportAudio` -- see "Not wrapped" below).
Built on pre-generated `slice2py` bindings (`zeroc-ice~=3.8.2`) with an Ice-version preflight at
import. Fully type-hinted (ships a PEP 561 `py.typed` marker); zero Ice types cross the public API.

### Connection & recording
- `connect()` → `Analyzer` context manager (encoding 1.0, raised message-size limit, checked cast).
- `is_recording`, `start_recording()`, `stop_and_save()`, `abort_recording()`, and the
  `recording()` context manager.

### Overview navigation (bounded by construction)
- `analyzer.overview()` scope, `OverviewItem.cursor()` → `ChildCursor`, `search_cursor()` →
  `SearchCursor`, yielding bounded `Page`s. Per-page handle release by default keeps server memory
  at `O(page_size)`; `take()`/`cursor[a:b]`/`materialize()` raise `BoundExceeded` past `HARD_CAP`.
- Handle-free `ItemRecord` snapshots; `ScopeClosed` on stale use.
- Growth guard: a full traversal (`stream`/`stream_records`/`walk`/`iter_children`/`materialize`)
  of an overview that is still loading or recording raises `OverviewIncomplete` rather than
  silently stopping short. Opt in with `follow=True` (live-tail until growth stops or you `break`)
  or `snapshot=True` (just what exists now); bounded reads (`take`/`page`/`cursor[a:b]`) are exempt.

### Markers
- Typed `MarkerColor`; `add_marker_at_time()`, `add_marker_on_selected_overview_item()`,
  `OverviewItem.add_marker()`, and `markers()` → `Marker`.

### Exports
- Generic `export()` + `export_dry_run()`, typed wrappers for the base modes, typed option
  carriers (`FilteredTraceOptions`/`ThroughputOptions`/…) and a `BluetoothPacketLossMode` enum, a single
  centralized serializer, and a raw-mapping escape hatch for any current/future mode.

### Session / trace files / info
- Blocking `load()` (+ `start_loading`/`is_loading`/`wait_until_loaded`, `LoadTimeout`),
  `trace_file_info()`, `app_info()`, `recording_status()`, data sources, recording options,
  `is_modified`/`save_changes()`/`close_trace_file()`, `insert_message()`, `running_tasks()`,
  opaque `get_settings()`/`configure_settings()`, `cancel_user_interaction()`. Typed results
  (`AppInfo`, `RecordingStatus`, `TraceFileInfo`, `RunningTask`); `TraceFileInfo.started_at_utc`
  interprets the start time (milliseconds since 2000-01-01 UTC; raw `long` kept for reinterpretation).

### Logic signals
- `logic_signals_state()` (level bitmask) and `find_logic_signal_transition()` →
  `LogicSignalTransition` (with `LogicSignalTransitionType`).

### Product facets
- `analyzer.bluetooth` / `analyzer.wifi` / `analyzer.wpan` / `analyzer.usb30`, each acquired by
  `checkedCast` on the same communicator and raising `NotAvailable` if the connected analyzer
  isn't that product. Bluetooth: channel summaries, spectrum RSSI, device filter, link keys,
  "save & continue", typed Bluetooth exports. Wi-Fi: keys + device filter. WPAN: Thread/Zigbee
  key management. USB 3.0: link control + packet/symbol save. Shared `_ProductFacet` template.

### Not wrapped (intentionally)
- Deprecated `InsertComment` (use `insert_message`) and the legacy `ExportAudio` op (use the
  `bluetooth_audio` export mode via `analyzer.bluetooth.export_audio()`).
