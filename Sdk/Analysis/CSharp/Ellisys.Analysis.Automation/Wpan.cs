using IceWpan = Ellisys.Platform.NetworkRemoteControl.Analyzer.Wpan;

namespace Ellisys.Analysis.Automation;

/// <summary>WPAN / 802.15.4-only operations on a connected analyzer. Obtain via <c>analyzer.Wpan</c>.</summary>
public sealed class WpanFacet : ProductFacet
{
    private readonly IceWpan.WpanAnalyzerRemoteControlPrx _prx;

    internal WpanFacet(Analyzer owner) : base(owner) =>
        _prx = Attach(owner, IceWpan.WpanAnalyzerRemoteControlIdentity.value,
            p => IceWpan.WpanAnalyzerRemoteControlPrxHelper.checkedCast(p), "WPAN");

    /// <summary>Add a Thread network master key for a PAN.</summary>
    public void AddThreadMasterKey(int panId, byte[] key, int sequenceCounter) =>
        Owner.Call(() => _prx.AddThreadNetworkMasterKey(CheckPanId(panId), CheckKey(key, 16), sequenceCounter));

    /// <summary>Remove every Thread network master key.</summary>
    public void RemoveAllThreadMasterKeys() =>
        Owner.Call(() => _prx.RemoveThreadNetworkAllMasterKeys());

    /// <summary>Remove all Thread master keys for a PAN.</summary>
    public void RemoveThreadMasterKeys(int panId) =>
        Owner.Call(() => _prx.RemoveThreadNetworkMasterKeys(CheckPanId(panId)));

    /// <summary>Remove a specific Thread master key.</summary>
    public void RemoveThreadMasterKey(int panId, byte[] key) =>
        Owner.Call(() => _prx.RemoveThreadNetworkMasterKey(CheckPanId(panId), CheckKey(key, 16)));

    /// <summary>Add a Zigbee APS link key between two 64-bit addresses.</summary>
    public void AddZigbeeApsKey(byte[] destinationAddress64, byte[] sourceAddress64, byte[] key) =>
        Owner.Call(() => _prx.AddZigbeeApsKey(CheckKey(destinationAddress64, 8), CheckKey(sourceAddress64, 8), CheckKey(key, 16)));

    /// <summary>Remove every Zigbee APS key.</summary>
    public void RemoveAllZigbeeApsKeys() =>
        Owner.Call(() => _prx.RemoveZigbeeApsAllKeys());

    /// <summary>Remove all Zigbee APS keys between two 64-bit addresses.</summary>
    public void RemoveZigbeeApsKeys(byte[] destinationAddress64, byte[] sourceAddress64) =>
        Owner.Call(() => _prx.RemoveZigbeeApsKeys(CheckKey(destinationAddress64, 8), CheckKey(sourceAddress64, 8)));

    /// <summary>Remove a specific Zigbee APS key.</summary>
    public void RemoveZigbeeApsKey(byte[] destinationAddress64, byte[] sourceAddress64, byte[] key) =>
        Owner.Call(() => _prx.RemoveZigbeeApsKey(CheckKey(destinationAddress64, 8), CheckKey(sourceAddress64, 8), CheckKey(key, 16)));

    /// <summary>Add a Zigbee network key for a PAN.</summary>
    public void AddZigbeeNetworkKey(int panId, byte[] key) =>
        Owner.Call(() => _prx.AddZigbeeNetworkKey(CheckPanId(panId), CheckKey(key, 16)));

    /// <summary>Remove every Zigbee network key.</summary>
    public void RemoveAllZigbeeNetworkKeys() =>
        Owner.Call(() => _prx.RemoveZigbeeNetworkAllKeys());

    /// <summary>Remove all Zigbee network keys for a PAN.</summary>
    public void RemoveZigbeeNetworkKeys(int panId) =>
        Owner.Call(() => _prx.RemoveZigbeeNetworkKeys(CheckPanId(panId)));

    /// <summary>Remove a specific Zigbee network key.</summary>
    public void RemoveZigbeeNetworkKey(int panId, byte[] key) =>
        Owner.Call(() => _prx.RemoveZigbeeNetworkKey(CheckPanId(panId), CheckKey(key, 16)));
}

public sealed partial class Analyzer
{
    private WpanFacet? _wpan;

    /// <summary>WPAN-only operations. Throws <see cref="NotAvailableException"/> if absent.</summary>
    public WpanFacet Wpan => _wpan ??= new WpanFacet(this);
}
