# Changelog

All notable changes to `Ellisys.Analysis.Automation` (C#) are documented here.

## 0.1.0 (unreleased)

Initial release — an idiomatic C# client for the Ellisys analyzer Remote Control API, mirroring the
Python SDK.

- **Connection & lifecycle**: `Analyzer.Connect(...)` / `IDisposable`; synchronous; all ZeroC Ice
  setup hidden and Ice exceptions translated to a `RemoteControlException` hierarchy. No Ice type on
  the public surface.
- **Overviews**: bounded traversal — scopes, cursors, pages, `Walk`/search, handle-free `ItemRecord`
  snapshots, page-released streaming, and a loading/recording growth guard
  (`OverviewIncompleteException`).
- **Product facets**: `Bluetooth`, `Wifi`, `Wpan`, `Usb30` (each `NotAvailableException` off-product).
- **Typed exports**: `ExportModes` / `BluetoothExportModes` catalogues + option carriers + an offline
  `ExportDryRun`.
- **Markers, session & trace-file info** (`TraceFileInfo.StartedAtUtc`), **logic signals**.
- Multi-targets `net48` and `net10.0`; strong-named with a dedicated key; `GPL-2.0-only`.
