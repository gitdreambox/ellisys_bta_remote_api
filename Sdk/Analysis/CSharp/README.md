# Ellisys Analysis Automation SDK (C#)

`Ellisys.Analysis.Automation` is an idiomatic C# client for the Ellisys analyzer Remote Control
automation API. It hides all ZeroC Ice setup (communicator, proxy, checked cast) behind a small,
synchronous, `IDisposable` surface and translates Ice exceptions into a catchable
`RemoteControlException` hierarchy. No ZeroC Ice type appears on the public surface.

It multi-targets **.NET 10** and **.NET Framework 4.8** and depends on `zeroc.ice.net` 3.7.x — the
same Ice runtime as the analyzer's own plug-ins, so it drops straight into existing C# solutions.

## Quick start

```csharp
using Ellisys.Analysis.Automation;

using var analyzer = Analyzer.Connect("localhost", 12345);
using (analyzer.Recording(@"C:\traces\session"))   // stops & saves when the block exits
{
    System.Console.WriteLine("Recording... press Enter to stop & save");
    System.Console.ReadLine();
}
```

## Overviews (bounded by design)

`Overview(...)` opens a scope; its cursors never let you read everything by accident:

```csharp
using var overview = analyzer.Overview("BR/EDR Overview");
foreach (var rec in overview.Root.Cursor().StreamRecords(new[] { ItemField.Time, ItemField.Description }))
    System.Console.WriteLine($"{rec.TimeSeconds}: {rec.Description}");
```

- `Stream()` / `StreamRecords(...)` are lazy and page-released (`O(pageSize)` server handles).
- `Take(n)`, `Page()`, slicing are explicit bounded reads; `Materialize()` throws past a cap.
- While a trace is **loading or recording** the overview grows, so full traversals throw
  `OverviewIncompleteException` unless you pass `follow: true` (tail items as they arrive) or
  `snapshot: true` (just what exists now).

## Exports (output paths are on the analyzer machine)

```csharp
analyzer.ExportFilteredTraceTimeRange(@"C:\out\first5s.btt",
    maxDurationPs: ExportOptions.PicosecondsFromTimeSpan(System.TimeSpan.FromSeconds(5)));
analyzer.ExportThroughput(@"C:\out\tput.csv");

analyzer.Bluetooth.ExportAudio(@"C:\out\audio",
    new BluetoothAudioOptions { PacketLoss = BluetoothPacketLossMode.SilenceSmooth });
```

Base modes live on `ExportModes`, Bluetooth modes on `BluetoothExportModes`; pass any raw token
string for modes newer than this SDK.

## Product facets

`analyzer.Bluetooth`, `.Wifi`, `.Wpan`, `.Usb30` expose product-specific operations and throw
`NotAvailableException` if the connected analyzer isn't that product:

```csharp
foreach (var ch in analyzer.Bluetooth.Channels())          // whole trace; index == RF channel
    if (ch.Summary.Total > 0)
        System.Console.WriteLine($"ch{ch.RfChannel}: ok={ch.Summary.Ok} err={ch.Summary.Errors}");
```

## Errors

All SDK errors derive from `RemoteControlException`:

- `ConnectionFailedException` — transport/connection problems (or the endpoint is not an analyzer).
- `OperationException` — the analyzer rejected the operation; subclasses include
  `LoadTimeoutException`, `ScopeClosedException`, `BoundExceededException`, `OverviewIncompleteException`.
- `NotAvailableException` — a facet/feature is not present on this analyzer.
- `ExportOptionException` — a bad export option, caught client-side.

## License

`GPL-2.0-only`. The SDK links ZeroC Ice, which is also `GPL-2.0-only`; see `LICENSE`. A commercial
Ice license from ZeroC is available if GPL terms do not suit your distribution.
