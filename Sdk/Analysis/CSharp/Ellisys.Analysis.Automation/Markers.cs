using IceAnalyzer = Ellisys.Platform.NetworkRemoteControl.Analyzer;

namespace Ellisys.Analysis.Automation;

/// <summary>
/// A marker colour. Values match the analyzer's <c>MarkerColor</c> Slice enum.
/// </summary>
public enum MarkerColor
{
    /// <summary>Yellow.</summary>
    Yellow = 0,

    /// <summary>Blue.</summary>
    Blue = 1,

    /// <summary>Red.</summary>
    Red = 2,

    /// <summary>Green.</summary>
    Green = 3,

    /// <summary>Orange.</summary>
    Orange = 4,

    /// <summary>Purple.</summary>
    Purple = 5,
}

/// <summary>
/// A marker read from the trace (the result of <see cref="Analyzer.Markers"/>). Handle-free;
/// it is a snapshot, not a live reference to a marker on the analyzer.
/// </summary>
public sealed class Marker
{
    /// <summary>
    /// Creates a marker snapshot.
    /// </summary>
    /// <param name="color">The marker's colour.</param>
    /// <param name="text">The marker's label text.</param>
    /// <param name="timePs">The marker's time, in picoseconds.</param>
    public Marker(MarkerColor color, string text, long timePs)
    {
        Color = color;
        Text = text;
        TimePs = timePs;
    }

    /// <summary>The marker's colour.</summary>
    public MarkerColor Color { get; }

    /// <summary>The marker's label text.</summary>
    public string Text { get; }

    /// <summary>The marker's time, in picoseconds.</summary>
    public long TimePs { get; }

    /// <summary>The marker's time as a <see cref="TimeSpan"/> (100-nanosecond resolution).</summary>
    public TimeSpan Time => OverviewTime.ToTimeSpan(TimePs);

    /// <summary>The marker's time in seconds.</summary>
    public double TimeSeconds => TimePs / 1e12;
}

public sealed partial class Analyzer
{
    /// <summary>
    /// Adds a marker at a given time (-> <c>AddMarkerAtTime</c>).
    /// </summary>
    /// <param name="timePs">The marker time, in picoseconds.</param>
    /// <param name="text">The marker's label text.</param>
    /// <param name="color">The marker's colour. Defaults to <see cref="MarkerColor.Yellow"/>.</param>
    /// <exception cref="OperationException">The analyzer rejected the request.</exception>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public void AddMarkerAtTime(long timePs, string text, MarkerColor color = MarkerColor.Yellow)
    {
        Call(() => Proxy.AddMarkerAtTime(timePs, MakeAddMarker(color, text)));
    }

    /// <summary>
    /// Adds a marker on the currently selected overview item (-> <c>AddMarkerOnSelectedOverviewItem</c>).
    /// </summary>
    /// <param name="text">The marker's label text.</param>
    /// <param name="color">The marker's colour. Defaults to <see cref="MarkerColor.Yellow"/>.</param>
    /// <exception cref="OperationException">The analyzer rejected the request.</exception>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public void AddMarkerOnSelectedOverviewItem(string text, MarkerColor color = MarkerColor.Yellow)
    {
        Call(() => Proxy.AddMarkerOnSelectedOverviewItem(MakeAddMarker(color, text)));
    }

    /// <summary>
    /// Every marker in the trace, as handle-free <see cref="Marker"/> snapshots (-> <c>GetMarkers</c>).
    /// </summary>
    /// <returns>The markers currently in the trace.</returns>
    /// <exception cref="OperationException">The analyzer rejected the request.</exception>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public IReadOnlyList<Marker> Markers()
    {
        var markers = Call(() => Proxy.GetMarkers());
        var result = new Marker[markers.Length];
        for (var i = 0; i < markers.Length; i++)
        {
            var m = markers[i];
            result[i] = new Marker((MarkerColor)m.Color, m.Text, m.Time);
        }
        return result;
    }

    /// <summary>Builds the Ice <c>AddMarker</c> struct from an SDK colour + text.</summary>
    private static IceAnalyzer.AddMarker MakeAddMarker(MarkerColor color, string text) =>
        new IceAnalyzer.AddMarker((IceAnalyzer.MarkerColor)color, text);
}
