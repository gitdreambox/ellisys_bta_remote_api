using System.Globalization;
using IceAnalyzer = Ellisys.Platform.NetworkRemoteControl.Analyzer;

namespace Ellisys.Analysis.Automation;

/// <summary>
/// A client-side export-option problem (a bad value type, or a failed validation such as a
/// range whose end precedes its start).
/// </summary>
/// <remarks>
/// Distinct from <see cref="OperationException"/> (a server-side failure, e.g. a wrong-product
/// mode) and <see cref="ConnectionFailedException"/>; derives from <see cref="ArgumentException"/>
/// so it reads as a bad-argument error to callers.
/// </remarks>
public sealed class ExportOptionException : ArgumentException
{
    /// <summary>Create an export-option error with a message.</summary>
    public ExportOptionException(string message)
        : base(message) { }

    /// <summary>Create an export-option error with a message and inner exception.</summary>
    public ExportOptionException(string message, Exception? innerException)
        : base(message, innerException) { }
}

/// <summary>
/// An export mode: the exact <c>exportName</c> wire token plus its <see cref="Product"/> and a
/// <see cref="Description"/>. Named modes live in <see cref="ExportModes"/> (base) and each product's
/// holder (e.g. <c>BluetoothExportModes</c>); a raw string can also be passed wherever a mode is
/// expected, so modes newer than this SDK remain reachable. Equality is by token only.
/// </summary>
public readonly struct ExportMode : IEquatable<ExportMode>
{
    /// <summary>The exact wire token (the server <c>exportName</c>).</summary>
    public string Value { get; }

    /// <summary>The product that supports the mode (<c>"base"</c> or e.g. <c>"bluetooth"</c>; empty for a raw token).</summary>
    public string Product { get; }

    /// <summary>A human-readable description (empty for a raw token).</summary>
    public string Description { get; }

    /// <summary>Wrap a raw <c>exportName</c> token (no metadata); allows modes newer than this SDK.</summary>
    public ExportMode(string value) : this(value, "", "") { }

    internal ExportMode(string value, string product, string description)
    {
        Value = value ?? throw new ArgumentNullException(nameof(value));
        Product = product;
        Description = description;
    }

    /// <summary>Implicitly wrap any raw token, so a string can be passed wherever a mode is expected.</summary>
    public static implicit operator ExportMode(string value) => new(value);

    /// <summary>The wire token.</summary>
    public override string ToString() => Value ?? string.Empty;

    /// <inheritdoc/>
    public bool Equals(ExportMode other) => string.Equals(Value, other.Value, StringComparison.Ordinal);

    /// <inheritdoc/>
    public override bool Equals(object? obj) => obj is ExportMode other && Equals(other);

    /// <inheritdoc/>
    public override int GetHashCode() => Value is null ? 0 : StringComparer.Ordinal.GetHashCode(Value);

    /// <summary>Token equality.</summary>
    public static bool operator ==(ExportMode left, ExportMode right) => left.Equals(right);

    /// <summary>Token inequality.</summary>
    public static bool operator !=(ExportMode left, ExportMode right) => !left.Equals(right);
}

/// <summary>
/// The base export modes (valid on any analyzer). There is no server operation to enumerate modes,
/// so these are also the documentation catalogue. Product modes live on their product's holder
/// (e.g. <c>BluetoothExportModes</c>).
/// </summary>
public static class ExportModes
{
    /// <summary>Filtered trace, by time range.</summary>
    public static ExportMode FilteredTraceTimeRange { get; } =
        new("filtered_trace_time_range", "base", "Filtered trace, by time range.");

    /// <summary>Filtered trace, by active overview.</summary>
    public static ExportMode FilteredTraceActiveOverview { get; } =
        new("filtered_trace_active_overview", "base", "Filtered trace, by active overview.");

    /// <summary>Throughput over a time range.</summary>
    public static ExportMode Throughput { get; } =
        new("throughput", "base", "Throughput over a time range.");

    /// <summary>All base export modes.</summary>
    public static IReadOnlyList<ExportMode> All { get; } =
        new[] { FilteredTraceTimeRange, FilteredTraceActiveOverview, Throughput };
}

/// <summary>
/// Anything that can supply server-spelled export-option pairs. Every typed option carrier
/// implements it; the snake-to-Pascal name mapping lives in each carrier's <see cref="AsOptions"/>.
/// </summary>
public interface IExportOptions
{
    /// <summary>
    /// Return the <c>{ServerOptionName: typed value}</c> mapping for this mode. Unset (<c>null</c>)
    /// values are dropped by the serializer and never sent (the server default then applies).
    /// </summary>
    IReadOnlyDictionary<string, object?> AsOptions();

    /// <summary>
    /// Validate the options, throwing <see cref="ExportOptionException"/> on a contradictory value
    /// (e.g. a time range whose end precedes its start). Carriers without constraints implement this
    /// as a no-op.
    /// </summary>
    void Validate();
}

/// <summary>
/// Options for <see cref="ExportModes.FilteredTraceTimeRange"/> and
/// <see cref="ExportModes.FilteredTraceActiveOverview"/>.
/// </summary>
/// <remarks>
/// <c>*Ps</c> values are picoseconds (use <see cref="ExportOptions.PicosecondsFromTimeSpan"/> to
/// convert a <see cref="TimeSpan"/>). <c>null</c> omits the option, applying the server default
/// (StartTime 0; the rest = full trace).
/// </remarks>
public sealed class FilteredTraceOptions : IExportOptions
{
    /// <summary>Start of the range, in picoseconds (<c>StartTime</c>; default 0).</summary>
    public long? StartTimePs { get; init; }

    /// <summary>Maximum output size, in bytes (<c>MaxSize</c>; default = full).</summary>
    public long? MaxSizeBytes { get; init; }

    /// <summary>Maximum duration, in picoseconds (<c>MaxDuration</c>; default = full).</summary>
    public long? MaxDurationPs { get; init; }

    /// <summary>Maximum number of items (<c>MaxItems</c>; default = full).</summary>
    public long? MaxItems { get; init; }

    /// <inheritdoc/>
    public IReadOnlyDictionary<string, object?> AsOptions() => new Dictionary<string, object?>
    {
        ["StartTime"] = StartTimePs,
        ["MaxSize"] = MaxSizeBytes,
        ["MaxDuration"] = MaxDurationPs,
        ["MaxItems"] = MaxItems,
    };

    /// <summary>No range constraints to check.</summary>
    public void Validate() { }
}

/// <summary>Options for <see cref="ExportModes.Throughput"/>.</summary>
public sealed class ThroughputOptions : IExportOptions
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

/// <summary>
/// The export-option wire machinery: the value renderer, the option-to-wire serializer, and the
/// range validator. (Export modes carry their own metadata on <see cref="ExportMode"/>.)
/// </summary>
public static class ExportOptions
{
    /// <summary>Picoseconds per second; matches the picosecond convention used elsewhere in the SDK.</summary>
    public const long PicosecondsPerSecond = 1_000_000_000_000L;

    /// <summary>Convert a <see cref="TimeSpan"/> to integer picoseconds (rounded).</summary>
    public static long PicosecondsFromTimeSpan(TimeSpan value) =>
        (long)Math.Round(value.TotalSeconds * PicosecondsPerSecond);

    /// <summary>
    /// Render ONE typed option value to its exact wire string, or <c>null</c> to OMIT it.
    /// </summary>
    /// <remarks>
    /// The wire rules (the single source of truth):
    /// <list type="bullet">
    ///   <item><description><c>null</c> → <c>null</c> (unset; never sent, server default applies)</description></item>
    ///   <item><description><see cref="bool"/> → <c>"true"</c> / <c>"false"</c> (.NET <c>bool.Parse</c> form)</description></item>
    ///   <item><description><see cref="TimeSpan"/> → integer picoseconds as a decimal string</description></item>
    ///   <item><description>integral types (<see cref="long"/>/<see cref="int"/>) → decimal string</description></item>
    ///   <item><description><see cref="string"/> → verbatim (carriers pre-render any token strings)</description></item>
    /// </list>
    /// </remarks>
    /// <exception cref="ExportOptionException">The value is of an unsupported type.</exception>
    public static string? RenderOptionValue(object? value) => value switch
    {
        null => null,
        bool b => b ? "true" : "false",
        Enum e => Convert.ToString(Convert.ChangeType(e, e.GetTypeCode(), CultureInfo.InvariantCulture), CultureInfo.InvariantCulture),
        TimeSpan ts => PicosecondsFromTimeSpan(ts).ToString(CultureInfo.InvariantCulture),
        long l => l.ToString(CultureInfo.InvariantCulture),
        int i => i.ToString(CultureInfo.InvariantCulture),
        short s => s.ToString(CultureInfo.InvariantCulture),
        byte by => by.ToString(CultureInfo.InvariantCulture),
        string str => str,
        _ => throw new ExportOptionException($"unsupported export option value type: {value.GetType().Name}"),
    };

    /// <summary>
    /// Render a <c>{OptionName: typed value}</c> mapping into the Ice <c>ExportOption[]</c> wire array,
    /// omitting any entry whose value renders to <c>null</c> (unset). The only function that
    /// constructs Ice <c>ExportOption</c> structs.
    /// </summary>
    internal static IceAnalyzer.ExportOption[] BuildExportOptions(IReadOnlyDictionary<string, object?>? options)
    {
        if (options is null || options.Count == 0)
        {
            return Array.Empty<IceAnalyzer.ExportOption>();
        }

        var rendered = new List<IceAnalyzer.ExportOption>(options.Count);
        foreach (var (name, value) in options)
        {
            var wire = RenderOptionValue(value);
            if (wire is not null)
            {
                rendered.Add(new IceAnalyzer.ExportOption(name, wire));
            }
        }
        return rendered.ToArray();
    }

    internal static void ValidateRange(long? start, long? end)
    {
        if (start is not null && end is not null && end < start)
        {
            throw new ExportOptionException("range end must be >= range start");
        }
    }
}

public sealed partial class Analyzer
{
    /// <summary>
    /// Run any export mode (the generic primary method, and an escape hatch for modes newer than
    /// this SDK).
    /// </summary>
    /// <remarks>
    /// <paramref name="output"/> is a path on the <b>analyzer machine</b> (like <c>StopAndSave</c>).
    /// <paramref name="mode"/> is the server <c>exportName</c> — a named member of
    /// <see cref="ExportModes"/> / a product holder, or any raw string. <paramref name="options"/> is
    /// a typed carrier (e.g. <see cref="BluetoothAudioOptions"/>) or <c>null</c>. A product mode used
    /// on the wrong analyzer raises <see cref="OperationException"/> at call time.
    /// </remarks>
    /// <param name="output">Output path on the analyzer machine.</param>
    /// <param name="mode">The export mode (server <c>exportName</c>).</param>
    /// <param name="options">Typed option carrier, or <c>null</c> for no options.</param>
    /// <exception cref="OperationException">The analyzer rejected the export (e.g. a wrong-product mode).</exception>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public void Export(string output, ExportMode mode, IExportOptions? options = null)
    {
        var raw = options?.AsOptions();
        var wire = ExportOptions.BuildExportOptions(raw);
        Call(() => Proxy.Export(output, mode.ToString(), wire));
    }

    /// <summary>
    /// Render the exact <c>(OptionName, OptionValue)</c> wire pairs that <see cref="Export"/> would
    /// send, <b>without</b> contacting the analyzer (offline).
    /// </summary>
    /// <remarks>
    /// Calls <see cref="IExportOptions.Validate"/> on <paramref name="options"/> first, then returns
    /// the rendered pairs. Makes no proxy call — useful for tests and for inspecting omit-null /
    /// bool / picosecond rendering before committing a long export. <paramref name="output"/> and
    /// <paramref name="mode"/> are accepted for signature symmetry with <see cref="Export"/>.
    /// </remarks>
    /// <exception cref="ExportOptionException">The options failed validation or held an unsupported value type.</exception>
    public IReadOnlyList<(string OptionName, string OptionValue)> ExportDryRun(
        string output, ExportMode mode, IExportOptions? options = null)
    {
        _ = output;
        _ = mode;
        options?.Validate();
        var raw = options?.AsOptions();
        var wire = ExportOptions.BuildExportOptions(raw);
        var pairs = new (string, string)[wire.Length];
        for (var i = 0; i < wire.Length; i++)
        {
            pairs[i] = (wire[i].OptionName, wire[i].OptionValue);
        }
        return pairs;
    }

    /// <summary>
    /// Export a filtered trace by time range (BASE; valid on any analyzer).
    /// </summary>
    /// <remarks>
    /// <c>*Ps</c> values are picoseconds (use <see cref="ExportOptions.PicosecondsFromTimeSpan"/> to
    /// convert a <see cref="TimeSpan"/>); <paramref name="maxSizeBytes"/> is a byte count. <c>null</c>
    /// omits the option (server defaults: StartTime 0, the rest = full trace).
    /// </remarks>
    public void ExportFilteredTraceTimeRange(
        string output,
        long? startTimePs = null,
        long? maxSizeBytes = null,
        long? maxDurationPs = null,
        long? maxItems = null) =>
        Export(output, ExportModes.FilteredTraceTimeRange, new FilteredTraceOptions
        {
            StartTimePs = startTimePs,
            MaxSizeBytes = maxSizeBytes,
            MaxDurationPs = maxDurationPs,
            MaxItems = maxItems,
        });

    /// <summary>
    /// Export a filtered trace by the active overview (BASE; valid on any analyzer). Same options as
    /// the time-range form.
    /// </summary>
    public void ExportFilteredTraceActiveOverview(
        string output,
        long? startTimePs = null,
        long? maxSizeBytes = null,
        long? maxDurationPs = null,
        long? maxItems = null) =>
        Export(output, ExportModes.FilteredTraceActiveOverview, new FilteredTraceOptions
        {
            StartTimePs = startTimePs,
            MaxSizeBytes = maxSizeBytes,
            MaxDurationPs = maxDurationPs,
            MaxItems = maxItems,
        });

    /// <summary>
    /// Export throughput over a time range (BASE; valid on any analyzer). <c>null</c> uses the server
    /// default (trace start/end).
    /// </summary>
    /// <exception cref="ExportOptionException">The range end precedes its start.</exception>
    public void ExportThroughput(
        string output,
        long? rangeStartTimePs = null,
        long? rangeEndTimePs = null)
    {
        var options = new ThroughputOptions
        {
            RangeStartTimePs = rangeStartTimePs,
            RangeEndTimePs = rangeEndTimePs,
        };
        options.Validate();
        Export(output, ExportModes.Throughput, options);
    }
}
