using IceAnalyzer = Ellisys.Platform.NetworkRemoteControl.Analyzer;

namespace Ellisys.Analysis.Automation;

/// <summary>
/// Which edge to search for (mirrors the Slice <c>LogicSignalTransitionType</c> enum).
/// </summary>
public enum LogicSignalTransitionType
{
    /// <summary>Match either a rising or a falling edge.</summary>
    Any = 0,

    /// <summary>Match a low-to-high transition.</summary>
    RisingEdge = 1,

    /// <summary>Match a high-to-low transition.</summary>
    FallingEdge = 2,
}

/// <summary>
/// A found logic-signal transition (the result of
/// <see cref="Analyzer.FindLogicSignalTransition"/>).
/// </summary>
/// <remarks>
/// Logic signals are the analyzer's digital I/O lines. <see cref="State"/> is a bitmask where
/// bit N is the level of logic signal N at the moment of the transition.
/// </remarks>
public sealed class LogicSignalTransition
{
    /// <summary>
    /// Creates a transition result.
    /// </summary>
    /// <param name="state">Bitmask of all signal levels at the transition (bit N == signal N).</param>
    /// <param name="timePs">Time of the transition, in picoseconds.</param>
    public LogicSignalTransition(int state, long timePs)
    {
        State = state;
        TimePs = timePs;
    }

    /// <summary>Bitmask of all signal levels at the transition (bit N is the level of signal N).</summary>
    public int State { get; }

    /// <summary>Time of the transition, in picoseconds.</summary>
    public long TimePs { get; }

    /// <summary>The transition time as a <see cref="TimeSpan"/> (100-nanosecond resolution).</summary>
    public TimeSpan Time => OverviewTime.ToTimeSpan(TimePs);
}

public sealed partial class Analyzer
{
    /// <summary>
    /// Reads the logic-signal state at a given time, as a bitmask where bit N is the level of
    /// logic signal N.
    /// </summary>
    /// <param name="timePs">The time to sample, in picoseconds.</param>
    /// <returns>The signal-state bitmask at <paramref name="timePs"/>.</returns>
    /// <exception cref="OperationException">The analyzer rejected the request.</exception>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public int LogicSignalsState(long timePs)
    {
        return Call(() =>
        {
            Proxy.GetLogicSignalsState(timePs, out var state);
            return state;
        });
    }

    /// <summary>
    /// Searches for the next logic-signal transition within a time range.
    /// </summary>
    /// <param name="fromTimePs">Start of the search range, in picoseconds (inclusive).</param>
    /// <param name="toTimePs">End of the search range, in picoseconds.</param>
    /// <param name="signalsMask">
    /// Bitmask selecting which signals to watch (bit N selects logic signal N).
    /// </param>
    /// <param name="transitionType">Which edge to match. Defaults to <see cref="LogicSignalTransitionType.Any"/>.</param>
    /// <returns>The matching <see cref="LogicSignalTransition"/>.</returns>
    /// <exception cref="OperationException">No transition was found, or the analyzer rejected the request.</exception>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public LogicSignalTransition FindLogicSignalTransition(
        long fromTimePs,
        long toTimePs,
        int signalsMask,
        LogicSignalTransitionType transitionType = LogicSignalTransitionType.Any)
    {
        return Call(() =>
        {
            Proxy.FindLogicSignalsTransition(
                fromTimePs,
                toTimePs,
                signalsMask,
                (IceAnalyzer.LogicSignalTransitionType)transitionType,
                out var foundState,
                out var foundTimePs);
            return new LogicSignalTransition(foundState, foundTimePs);
        });
    }
}
