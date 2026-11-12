using IceEth = Ellisys.Platform.NetworkRemoteControl.Analyzer.Ethernet;

namespace Ellisys.Analysis.Automation;

/// <summary>Wi-Fi-only operations on a connected analyzer. Obtain via <c>analyzer.Wifi</c>.</summary>
public sealed class WifiFacet : ProductFacet
{
    private readonly IceEth.EthernetAnalyzerRemoteControlPrx _prx;

    internal WifiFacet(Analyzer owner) : base(owner) =>
        _prx = Attach(owner, IceEth.EthernetAnalyzerRemoteControlIdentity.value,
            p => IceEth.EthernetAnalyzerRemoteControlPrxHelper.checkedCast(p), "Wi-Fi");

    /// <summary>Add a Wi-Fi key for an access point identified by SSID.</summary>
    public void AddWifiKeyByApSsid(string apSsid, string key) =>
        Owner.Call(() => _prx.AddWifiKeyByApSsid(apSsid, key));

    /// <summary>Add a Wi-Fi key for an access point identified by its 48-bit MAC address.</summary>
    public void AddWifiKeyByApMac(long apMacAddress, string key) =>
        Owner.Call(() => _prx.AddWifiKeyByApMacAddr(CheckAddr48(apMacAddress), key));

    /// <summary>Add a Wi-Fi key for an access point, with the MAC as the analyzer displays it
    /// ("AA:BB:CC:DD:EE:FF").</summary>
    public void AddWifiKeyByApMac(string apMacAddress, string key) =>
        AddWifiKeyByApMac(ParseAddr48(apMacAddress), key);

    /// <summary>Set which devices are kept/excluded.</summary>
    public void ConfigureDeviceFilter(DeviceFilterMode mode, IReadOnlyList<long>? deviceAddresses = null,
        bool wait = true, TimeSpan? timeout = null)
    {
        var addrs = (deviceAddresses ?? Array.Empty<long>()).Select(CheckAddr48).ToArray();
        Owner.Call(() => _prx.ConfigureDeviceFilter((IceEth.DeviceFilterMode)(int)mode, addrs));
        if (wait)
        {
            Owner.WaitUntilIdle(timeout);
        }
    }

    /// <summary>Set which devices are kept/excluded, with addresses as the analyzer displays them
    /// ("AA:BB:CC:DD:EE:FF").</summary>
    public void ConfigureDeviceFilter(DeviceFilterMode mode, IReadOnlyList<string> deviceAddresses,
        bool wait = true, TimeSpan? timeout = null) =>
        ConfigureDeviceFilter(mode, deviceAddresses.Select(ParseAddr48).ToArray(), wait, timeout);
}

public sealed partial class Analyzer
{
    private WifiFacet? _wifi;

    /// <summary>Wi-Fi-only operations. Throws <see cref="NotAvailableException"/> if absent.</summary>
    public WifiFacet Wifi => _wifi ??= new WifiFacet(this);
}
