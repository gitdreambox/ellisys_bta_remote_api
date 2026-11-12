using IceBase = Ellisys.Platform.NetworkRemoteControl.Analyzer;

namespace Ellisys.Analysis.Automation;

/// <summary>Per-RF-channel packet tallies (-> Slice struct <c>ChannelSummary</c>).</summary>
public sealed record BluetoothChannelSummary(long Ok, long Retransmitted, long PayloadError, long HeaderError, long NotApplicable)
{
    /// <summary>Header + payload errors.</summary>
    public long Errors => PayloadError + HeaderError;

    /// <summary>Classified packets on this channel (excludes <see cref="NotApplicable"/>).</summary>
    public long Total => Ok + Retransmitted + PayloadError + HeaderError;

    /// <summary>Fraction of classified packets in error, or <c>null</c> if the channel had no data.</summary>
    public double? ErrorRate => Total > 0 ? (double)Errors / Total : null;

    internal static BluetoothChannelSummary FromIce(IceBase.ChannelSummary s) =>
        new(s.Ok, s.Retransmitted, s.PayloadError, s.HeaderError, s.NotApplicable);
}

/// <summary>An (RF channel, summary) pair -- the explicit-index view of channel summaries.</summary>
public sealed record BluetoothChannelStat(int RfChannel, BluetoothChannelSummary Summary);

/// <summary>One RSSI sample (-> GetSpectrumRssi).</summary>
public sealed record BluetoothSpectrumSample(double RssiDbm, long StartPs, long StopPs)
{
    /// <summary>Length of the sampling window as a <see cref="TimeSpan"/>.</summary>
    public TimeSpan Window => TimeSpan.FromTicks((StopPs - StartPs) / 100_000);
}

/// <summary>A series of RSSI samples over a window (-> GetSpectrumRssiRange).</summary>
public sealed record BluetoothSpectrumRange(IReadOnlyList<double> RssiDbm, long StartPs, long StopPs)
{
    /// <summary>Number of samples.</summary>
    public int Count => RssiDbm.Count;

    /// <summary>Length of the sampling window as a <see cref="TimeSpan"/>.</summary>
    public TimeSpan Window => TimeSpan.FromTicks((StopPs - StartPs) / 100_000);

    /// <summary>Mean RSSI across the samples in dBm, or <c>null</c> if there are none.</summary>
    public double? MeanDbm => RssiDbm.Count > 0 ? RssiDbm.Average() : null;

    /// <summary>Lowest RSSI sample in dBm, or <c>null</c> if there are none.</summary>
    public double? MinDbm => RssiDbm.Count > 0 ? RssiDbm.Min() : null;

    /// <summary>Highest RSSI sample in dBm, or <c>null</c> if there are none.</summary>
    public double? MaxDbm => RssiDbm.Count > 0 ? RssiDbm.Max() : null;
}

/// <summary>Helper to format a 48-bit BDADDR.</summary>
public static class BluetoothBdAddr
{
    /// <summary>Format a 48-bit BDADDR as "AA:BB:CC:DD:EE:FF".</summary>
    public static string Format(long address) =>
        string.Join(":", Enumerable.Range(0, 6).Reverse().Select(i => $"{(address >> (8 * i)) & 0xFF:X2}"));
}

/// <summary>Bluetooth-only operations on a connected analyzer. Obtain via <c>analyzer.Bluetooth</c>.</summary>
public sealed class BluetoothFacet : ProductFacet
{
    private const long Int64Max = long.MaxValue;
    private readonly IceBase.BluetoothAnalyzerRemoteControlPrx _prx;

    internal BluetoothFacet(Analyzer owner) : base(owner) =>
        _prx = Attach(owner, IceBase.BluetoothAnalyzerRemoteControlIdentity.value,
            p => IceBase.BluetoothAnalyzerRemoteControlPrxHelper.checkedCast(p), "Bluetooth");

    /// <summary>Save the current trace and keep recording -- "Save &amp; Continue".</summary>
    public void SplitTraceAndContinue(string filename) =>
        Owner.Call(() => _prx.SplitTraceFileAndContinueRecording(filename));

    /// <summary>RSSI at <paramref name="timePs"/> on <paramref name="rfChannel"/> (0-78).</summary>
    /// <remarks>RF channels are 1 MHz apart: frequency = 2402 + <paramref name="rfChannel"/> MHz
    /// (BR/EDR numbering; LE channels sit on a 2 MHz raster -- convert via frequency, e.g.
    /// Wi-Fi channel 11's 2462 MHz center is RF channel 60).</remarks>
    public BluetoothSpectrumSample SpectrumRssi(long timePs, int rfChannel) => Owner.Call(() =>
    {
        _prx.GetSpectrumRssi(timePs, rfChannel, out var rssi, out var start, out var stop);
        return new BluetoothSpectrumSample(rssi, start, stop);
    });

    /// <summary>RSSI samples across [<paramref name="fromTimePs"/>, <paramref name="toTimePs"/>] on a channel.</summary>
    /// <remarks>Channel-to-frequency mapping as in <see cref="SpectrumRssi"/> (2402 + channel MHz).
    /// Samples arrive at ~10 kHz; one call serves one channel, so sweeping a time/frequency grid
    /// means one call per cell -- keep grids coarse.</remarks>
    public BluetoothSpectrumRange SpectrumRssiRange(long fromTimePs, long toTimePs, int rfChannel) => Owner.Call(() =>
    {
        _prx.GetSpectrumRssiRange(fromTimePs, toTimePs, rfChannel, out var rssi, out var start, out var stop);
        return new BluetoothSpectrumRange(rssi, start, stop);
    });

    /// <summary>Per-RF-channel summaries; list index == RF channel. Defaults to the whole trace.</summary>
    /// <remarks>79 entries, 1 MHz apart: frequency = 2402 + index MHz (BR/EDR numbering; LE
    /// channels sit on a 2 MHz raster -- convert via frequency). Matches the Instant Channels
    /// view.</remarks>
    public IReadOnlyList<BluetoothChannelSummary> ChannelSummaries(long fromTimePs = 0, long? toTimePs = null) =>
        Owner.Call(() => _prx.GetChannelsSummary(fromTimePs, toTimePs ?? Int64Max))
            .Select(BluetoothChannelSummary.FromIce).ToList();

    /// <summary>Per-channel summaries as explicit (RF channel, summary) pairs.</summary>
    public IReadOnlyList<BluetoothChannelStat> Channels(long fromTimePs = 0, long? toTimePs = null) =>
        ChannelSummaries(fromTimePs, toTimePs).Select((s, i) => new BluetoothChannelStat(i, s)).ToList();

    /// <summary>Set which devices are kept/excluded.</summary>
    public void ConfigureDeviceFilter(DeviceFilterMode mode, IReadOnlyList<long>? deviceAddresses = null,
        bool wait = true, TimeSpan? timeout = null)
    {
        var addrs = (deviceAddresses ?? Array.Empty<long>()).Select(CheckAddr48).ToArray();
        Owner.Call(() => _prx.ConfigureDeviceFilter((IceBase.DeviceFilterMode)(int)mode, addrs));
        if (wait)
        {
            Owner.WaitUntilIdle(timeout);
        }
    }

    /// <summary>Set which devices are kept/excluded, with addresses as the analyzer displays them
    /// (e.g. from the Overview's Communication column: "AA:BB:CC:DD:EE:FF").</summary>
    public void ConfigureDeviceFilter(DeviceFilterMode mode, IReadOnlyList<string> deviceAddresses,
        bool wait = true, TimeSpan? timeout = null) =>
        ConfigureDeviceFilter(mode, deviceAddresses.Select(ParseAddr48).ToArray(), wait, timeout);

    /// <summary>Add a 16-byte link key for the <paramref name="bdAddr1"/>&lt;-&gt;<paramref name="bdAddr2"/> link.</summary>
    public void AddLinkKey(long bdAddr1, long bdAddr2, byte[] linkKey) =>
        Owner.Call(() => _prx.AddLinkKey(CheckAddr48(bdAddr1), CheckAddr48(bdAddr2), CheckKey(linkKey, 16)));

    /// <summary>Add a 16-byte link key, with the BDADDRs as the analyzer displays them ("AA:BB:CC:DD:EE:FF").</summary>
    public void AddLinkKey(string bdAddr1, string bdAddr2, byte[] linkKey) =>
        AddLinkKey(ParseAddr48(bdAddr1), ParseAddr48(bdAddr2), linkKey);

    /// <summary>Export Bluetooth audio (mode <c>bluetooth_audio</c>; the supported audio export).</summary>
    public void ExportAudio(string output, BluetoothAudioOptions? options = null) =>
        Owner.Export(output, BluetoothExportModes.Audio, options);

    /// <summary>Export per-channel statistics (mode <c>bluetooth_channels</c>).</summary>
    public void ExportChannels(string output, BluetoothChannelsOptions? options = null) =>
        Owner.Export(output, BluetoothExportModes.Channels, options);

    /// <summary>Export airtime usage (mode <c>airtime</c>).</summary>
    public void ExportAirtime(string output, BluetoothAirtimeOptions? options = null) =>
        Owner.Export(output, BluetoothExportModes.Airtime, options);

    /// <summary>Export Bluetooth mobile-phone data (mode <c>bluetooth_mobile_phone_data</c>).</summary>
    public void ExportMobilePhoneData(string output) =>
        Owner.Export(output, BluetoothExportModes.MobilePhoneData);
}

public sealed partial class Analyzer
{
    private BluetoothFacet? _bluetooth;

    /// <summary>Bluetooth-only operations. Throws <see cref="NotAvailableException"/> if absent.</summary>
    public BluetoothFacet Bluetooth => _bluetooth ??= new BluetoothFacet(this);
}
