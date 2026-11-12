using IceBase = Ellisys.Platform.NetworkRemoteControl.Analyzer;

namespace Ellisys.Analysis.Automation;

/// <summary>USB 3.0-only operations on a connected analyzer. Obtain via <c>analyzer.Usb30</c>.</summary>
public sealed class Usb30Facet : ProductFacet
{
    private readonly IceBase.Usb30AnalyzerRemoteControlPrx _prx;

    internal Usb30Facet(Analyzer owner) : base(owner) =>
        // USB 3.0 has no separate Ice identity -- the interface lives on the base analyzer object,
        // so cast the base proxy directly (null -> this isn't a USB 3.0 analyzer).
        _prx = Attach(owner, IceBase.AnalyzerRemoteControlIdentity.value,
            p => IceBase.Usb30AnalyzerRemoteControlPrxHelper.checkedCast(p), "USB 3.0");

    /// <summary>Connect the analyzer link.</summary>
    public void ConnectLink(bool disconnectSuperSpeed = false) =>
        Owner.Call(() => _prx.ConnectLink(disconnectSuperSpeed));

    /// <summary>Disconnect the analyzer link.</summary>
    public void DisconnectLink() =>
        Owner.Call(() => _prx.DisconnectLink());

    /// <summary>Save captured USB 2.0 packets to a file (on the analyzer machine).</summary>
    public void SaveUsb20Packets(string filename) =>
        Owner.Call(() => _prx.SaveUsb20Packets(filename));

    /// <summary>Save captured USB 3.0 symbols to a file (on the analyzer machine).</summary>
    public void SaveUsb30Symbols(string filename, bool upstreamSymbols) =>
        Owner.Call(() => _prx.SaveUsb30Symbols(filename, upstreamSymbols));
}

public sealed partial class Analyzer
{
    private Usb30Facet? _usb30;

    /// <summary>USB 3.0-only operations. Throws <see cref="NotAvailableException"/> if absent.</summary>
    public Usb30Facet Usb30 => _usb30 ??= new Usb30Facet(this);
}
