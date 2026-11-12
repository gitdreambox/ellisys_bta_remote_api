namespace Ellisys.Analysis.Automation;

/// <summary>The Bluetooth export modes (valid only on a Bluetooth analyzer).</summary>
public static class BluetoothExportModes
{
    /// <summary>Bluetooth audio extraction.</summary>
    public static ExportMode Audio { get; } = new("bluetooth_audio", "bluetooth", "Bluetooth audio extraction.");

    /// <summary>Bluetooth mobile phone data.</summary>
    public static ExportMode MobilePhoneData { get; } = new("bluetooth_mobile_phone_data", "bluetooth", "Bluetooth mobile phone data.");

    /// <summary>Bluetooth per-channel statistics.</summary>
    public static ExportMode Channels { get; } = new("bluetooth_channels", "bluetooth", "Bluetooth per-channel statistics.");

    /// <summary>Airtime usage.</summary>
    public static ExportMode Airtime { get; } = new("airtime", "bluetooth", "Airtime usage.");

    /// <summary>All Bluetooth export modes.</summary>
    public static IReadOnlyList<ExportMode> All { get; } = new[] { Audio, MobilePhoneData, Channels, Airtime };
}

/// <summary>
/// How <c>bluetooth_audio</c> export fills gaps caused by packet loss (the <c>PacketLoss</c>
/// option). Bluetooth analyzers only. Each member maps to an exact server token.
/// </summary>
public enum BluetoothPacketLossMode
{
    /// <summary>Fill gaps with a negative-DC value (easy to spot). Wire token <c>NegativeDC</c>.</summary>
    NegativeDc,

    /// <summary>Fill gaps with silence, no smoothing. Wire token <c>Silence</c>.</summary>
    Silence,

    /// <summary>Fill gaps with silence, smoothed to conceal the gap. Wire token <c>SilenceSmooth</c>.</summary>
    SilenceSmooth,
}

/// <summary>Options for <see cref="BluetoothExportModes.Audio"/> (Bluetooth analyzers only).</summary>
public sealed class BluetoothAudioOptions : IExportOptions
{
    /// <summary>Also write raw payload files (<c>AddRawPayloadFiles</c>).</summary>
    public bool? AddRawPayloadFiles { get; init; }

    /// <summary>Synchronisation buffer, in milliseconds (<c>SynchroBufferMilliseconds</c>).</summary>
    public long? SynchroBufferMs { get; init; }

    /// <summary>Force isochronous buffering (<c>ForceIsochronousBuffering</c>).</summary>
    public bool? ForceIsochronousBuffering { get; init; }

    /// <summary>How to fill gaps caused by packet loss (<c>PacketLoss</c>).</summary>
    public BluetoothPacketLossMode? PacketLoss { get; init; }

    /// <inheritdoc/>
    public IReadOnlyDictionary<string, object?> AsOptions() => new Dictionary<string, object?>
    {
        ["AddRawPayloadFiles"] = AddRawPayloadFiles,
        ["SynchroBufferMilliseconds"] = SynchroBufferMs,
        ["ForceIsochronousBuffering"] = ForceIsochronousBuffering,
        ["PacketLoss"] = PacketLoss switch          // render the exact wire token here (Bluetooth-specific)
        {
            null => null,
            BluetoothPacketLossMode.NegativeDc => "NegativeDC",
            BluetoothPacketLossMode.Silence => "Silence",
            BluetoothPacketLossMode.SilenceSmooth => "SilenceSmooth",
            _ => throw new ExportOptionException($"unknown packet-loss mode: {PacketLoss}"),
        },
    };

    /// <summary>No range constraints to check.</summary>
    public void Validate() { }
}

/// <summary>Options for <see cref="BluetoothExportModes.Channels"/> (Bluetooth analyzers only).</summary>
public sealed class BluetoothChannelsOptions : IExportOptions
{
    /// <summary>Start of the range, in picoseconds (<c>RangeStartTime</c>).</summary>
    public long? RangeStartTimePs { get; init; }

    /// <summary>End of the range, in picoseconds (<c>RangeEndTime</c>).</summary>
    public long? RangeEndTimePs { get; init; }

    /// <inheritdoc/>
    public IReadOnlyDictionary<string, object?> AsOptions() => new Dictionary<string, object?>
    {
        ["RangeStartTime"] = RangeStartTimePs,
        ["RangeEndTime"] = RangeEndTimePs,
    };

    /// <summary>Validate the range — throws <see cref="ExportOptionException"/> if end precedes start.</summary>
    public void Validate() => ExportOptions.ValidateRange(RangeStartTimePs, RangeEndTimePs);
}

/// <summary>Options for <see cref="BluetoothExportModes.Airtime"/> (Bluetooth analyzers only).</summary>
public sealed class BluetoothAirtimeOptions : IExportOptions
{
    /// <summary>Start of the range, in picoseconds (<c>RangeStartTime</c>).</summary>
    public long? RangeStartTimePs { get; init; }

    /// <summary>End of the range, in picoseconds (<c>RangeEndTime</c>).</summary>
    public long? RangeEndTimePs { get; init; }

    /// <inheritdoc/>
    public IReadOnlyDictionary<string, object?> AsOptions() => new Dictionary<string, object?>
    {
        ["RangeStartTime"] = RangeStartTimePs,
        ["RangeEndTime"] = RangeEndTimePs,
    };

    /// <summary>Validate the range — throws <see cref="ExportOptionException"/> if end precedes start.</summary>
    public void Validate() => ExportOptions.ValidateRange(RangeStartTimePs, RangeEndTimePs);
}
