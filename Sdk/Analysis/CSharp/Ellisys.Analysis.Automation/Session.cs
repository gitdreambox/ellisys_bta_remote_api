using System.Diagnostics;
using IceAnalyzer = Ellisys.Platform.NetworkRemoteControl.Analyzer;

namespace Ellisys.Analysis.Automation;

/// <summary>
/// Severity for <see cref="Analyzer.InsertMessage"/> (mirrors the Slice enum; 1-based).
/// </summary>
public enum MessageSeverity
{
    /// <summary>An informational message.</summary>
    Info = 1,

    /// <summary>A warning message.</summary>
    Warning = 2,

    /// <summary>An error message.</summary>
    Error = 3,
}

/// <summary>Information about the remote application (from <c>GetAppInfo</c>).</summary>
public sealed class AppInfo
{
    /// <summary>Creates an <see cref="AppInfo"/>.</summary>
    public AppInfo(string id, string description, string version, string fileExt, bool interactive)
    {
        Id = id;
        Description = description;
        Version = version;
        FileExt = fileExt;
        Interactive = interactive;
    }

    /// <summary>The application identifier.</summary>
    public string Id { get; }

    /// <summary>A human-readable description of the application.</summary>
    public string Description { get; }

    /// <summary>The application version.</summary>
    public string Version { get; }

    /// <summary>The trace file extension this application uses.</summary>
    public string FileExt { get; }

    /// <summary>Whether the application is running interactively (with a UI).</summary>
    public bool Interactive { get; }

    internal static AppInfo FromIce(IceAnalyzer.AppInfo s) =>
        new(s.Id, s.Description, s.Version, s.FileExt, s.Interactive);
}

/// <summary>Status of the current recording (from <c>GetRecordingStatus</c>).</summary>
public sealed class RecordingStatus
{
    /// <summary>Creates a <see cref="RecordingStatus"/>.</summary>
    public RecordingStatus(string dataSource, int durationSeconds, long fileSize)
    {
        DataSource = dataSource;
        DurationSeconds = durationSeconds;
        FileSize = fileSize;
    }

    /// <summary>The data source being recorded.</summary>
    public string DataSource { get; }

    /// <summary>How long the recording has been running, in seconds.</summary>
    public int DurationSeconds { get; }

    /// <summary>The current trace size, in bytes.</summary>
    public long FileSize { get; }

    /// <summary><see cref="DurationSeconds"/> as a <see cref="TimeSpan"/> (exact).</summary>
    public TimeSpan Duration => TimeSpan.FromSeconds(DurationSeconds);

    internal static RecordingStatus FromIce(IceAnalyzer.RecordingStatus s) =>
        new(s.DataSource, s.DurationSeconds, s.FileSize);
}

/// <summary>A background task running in the analyzer (from <c>GetRunningTasks</c>).</summary>
public sealed class RunningTask
{
    /// <summary>Creates a <see cref="RunningTask"/>.</summary>
    public RunningTask(string name, int progressPercent, bool progressApplicable)
    {
        Name = name;
        ProgressPercent = progressPercent;
        ProgressApplicable = progressApplicable;
    }

    /// <summary>The task name.</summary>
    public string Name { get; }

    /// <summary>The raw progress percentage (only meaningful when <see cref="ProgressApplicable"/> is <c>true</c>).</summary>
    public int ProgressPercent { get; }

    /// <summary>Whether <see cref="ProgressPercent"/> is meaningful for this task.</summary>
    public bool ProgressApplicable { get; }

    /// <summary>Percent complete, or <c>null</c> when the server says progress isn't meaningful.</summary>
    public int? Progress => ProgressApplicable ? ProgressPercent : null;

    internal static RunningTask FromIce(IceAnalyzer.RunningTask t) =>
        new(t.Name, t.ProgressPercent, t.ProgressApplicable);
}

/// <summary>Information about the loaded trace file (from <c>GetTraceFileInfo</c>).</summary>
public sealed class TraceFileInfo
{
    private static readonly DateTime Ellisys2000Epoch = new(2000, 1, 1, 0, 0, 0, DateTimeKind.Utc);

    /// <summary>Creates a <see cref="TraceFileInfo"/>.</summary>
    public TraceFileInfo(string path, long fileSize, long startDateTimeUtcRaw, string softwareVersion,
        string dataSource, string uniqueId, string recordingOptions)
    {
        Path = path;
        FileSize = fileSize;
        StartDateTimeUtcRaw = startDateTimeUtcRaw;
        SoftwareVersion = softwareVersion;
        DataSource = dataSource;
        UniqueId = uniqueId;
        RecordingOptions = recordingOptions;
    }

    /// <summary>The trace file path (on the analyzer machine).</summary>
    public string Path { get; }

    /// <summary>The trace file size, in bytes.</summary>
    public long FileSize { get; }

    /// <summary>The raw Slice <c>long</c> start time (milliseconds since 2000-01-01 UTC); see <see cref="StartedAtUtc"/>.</summary>
    public long StartDateTimeUtcRaw { get; }

    /// <summary>The analyzer software version that produced the trace.</summary>
    public string SoftwareVersion { get; }

    /// <summary>The data source that was recorded.</summary>
    public string DataSource { get; }

    /// <summary>A unique identifier for the trace.</summary>
    public string UniqueId { get; }

    /// <summary>The opaque recording-options blob (the same string <c>ConfigureRecordingOptions</c> consumes).</summary>
    public string RecordingOptions { get; }

    /// <summary>
    /// The trace start time as a UTC <see cref="DateTime"/>, or <c>null</c> when the raw value is
    /// non-positive (unset). <see cref="StartDateTimeUtcRaw"/> is milliseconds since 2000-01-01 UTC
    /// (the epoch the analyzer's own trace indexer uses); reinterpret the raw value yourself if you
    /// ever need a different one.
    /// </summary>
    public DateTime? StartedAtUtc =>
        StartDateTimeUtcRaw > 0 ? Ellisys2000Epoch.AddMilliseconds(StartDateTimeUtcRaw) : null;

    internal static TraceFileInfo FromIce(IceAnalyzer.TraceFileInfo s) =>
        new(s.Path, s.FileSize, s.StartDateTimeUtc, s.SoftwareVersion, s.DataSource, s.UniqueId, s.RecordingOptions);
}

public sealed partial class Analyzer
{
    //
    // recording
    //
    /// <summary><c>true</c> while a capture is in progress (<c>IsRecording</c>).</summary>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public bool IsRecording => Call(() => Proxy.IsRecording());

    /// <summary>Starts a capture (equivalent to Record &gt; Start in the GUI; <c>StartRecording</c>).</summary>
    /// <exception cref="OperationException">The analyzer rejected the request.</exception>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public void StartRecording() => Call(() => Proxy.StartRecording());

    /// <summary>
    /// Stops the capture and saves the trace to <paramref name="filename"/> (<c>StopRecordingAndSaveTraceFile</c>).
    /// </summary>
    /// <remarks>
    /// The path is interpreted on the <b>analyzer machine</b>, not the client running this code.
    /// </remarks>
    /// <param name="filename">The destination path on the analyzer machine.</param>
    /// <param name="overwrite">Set <c>true</c> to replace an existing file.</param>
    /// <exception cref="OperationException">The analyzer rejected the request.</exception>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public void StopAndSave(string filename, bool overwrite = false) =>
        Call(() => Proxy.StopRecordingAndSaveTraceFile(filename, overwrite));

    /// <summary>Stops the capture and discards the trace — nothing is saved (<c>AbortRecordingAndDiscardTraceFile</c>).</summary>
    /// <exception cref="OperationException">The analyzer rejected the request.</exception>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public void AbortRecording() => Call(() => Proxy.AbortRecordingAndDiscardTraceFile());

    /// <summary>
    /// Starts a capture and returns a handle that stops and saves the trace to <paramref name="saveTo"/>
    /// when disposed.
    /// </summary>
    /// <remarks>
    /// Intended for a <c>using</c> block: the trace is saved when the block exits (best effort even if
    /// the body throws — a capture is rarely worth losing because the code that triggered it failed).
    /// </remarks>
    /// <param name="saveTo">The destination path on the analyzer machine.</param>
    /// <param name="overwrite">Set <c>true</c> to replace an existing file.</param>
    /// <returns>An <see cref="IDisposable"/> that stops and saves on dispose.</returns>
    /// <exception cref="OperationException">The analyzer rejected the request to start recording.</exception>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public IDisposable Recording(string saveTo, bool overwrite = false)
    {
        StartRecording();
        return new RecordingScope(this, saveTo, overwrite);
    }

    private sealed class RecordingScope : IDisposable
    {
        private readonly Analyzer _analyzer;
        private readonly string _saveTo;
        private readonly bool _overwrite;
        private bool _stopped;

        public RecordingScope(Analyzer analyzer, string saveTo, bool overwrite)
        {
            _analyzer = analyzer;
            _saveTo = saveTo;
            _overwrite = overwrite;
        }

        public void Dispose()
        {
            if (_stopped)
            {
                return;
            }
            _stopped = true;
            _analyzer.StopAndSave(_saveTo, _overwrite);
        }
    }

    //

    // trace file

    //
    /// <summary><c>true</c> while a trace file is loading (<c>IsLoading</c>).</summary>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public bool IsLoading => Call(() => Proxy.IsLoading());

    /// <summary>
    /// Begins loading <paramref name="filename"/> and returns immediately (<c>StartLoading</c>).
    /// </summary>
    /// <remarks>
    /// Loading is asynchronous: poll <see cref="IsLoading"/> (or use <see cref="WaitUntilLoaded"/> /
    /// <see cref="Load"/>) to know when it finishes. <paramref name="filename"/> is a path on the
    /// analyzer machine.
    /// </remarks>
    /// <param name="filename">The trace file path on the analyzer machine.</param>
    /// <exception cref="OperationException">The analyzer rejected the request.</exception>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public void StartLoading(string filename) => Call(() => Proxy.StartLoading(filename));

    /// <summary>
    /// Blocks until <see cref="IsLoading"/> is <c>false</c>, polling against a deadline.
    /// </summary>
    /// <param name="timeout">
    /// Maximum time to wait. Defaults to two minutes. Pass <see cref="System.Threading.Timeout.InfiniteTimeSpan"/>
    /// (or any negative value) to wait forever.
    /// </param>
    /// <param name="pollInterval">How often to poll. Must be &gt; 0. Defaults to 250 ms.</param>
    /// <exception cref="LoadTimeoutException">Loading did not finish within <paramref name="timeout"/>.</exception>
    /// <exception cref="ArgumentOutOfRangeException"><paramref name="pollInterval"/> is not positive.</exception>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public void WaitUntilLoaded(TimeSpan? timeout = null, TimeSpan? pollInterval = null)
    {
        var poll = pollInterval ?? TimeSpan.FromMilliseconds(250);
        if (poll <= TimeSpan.Zero)
        {
            throw new ArgumentOutOfRangeException(nameof(pollInterval), "pollInterval must be > 0");
        }
        var limit = timeout ?? TimeSpan.FromMinutes(2);
        var waitForever = limit < TimeSpan.Zero;

        var stopwatch = Stopwatch.StartNew();
        while (IsLoading)
        {
            if (!waitForever)
            {
                var remaining = limit - stopwatch.Elapsed;
                if (remaining <= TimeSpan.Zero)
                {
                    throw new LoadTimeoutException(
                        $"trace load did not finish within {limit.TotalSeconds:0.###}s");
                }
                Thread.Sleep(remaining < poll ? remaining : poll);
            }
            else
            {
                Thread.Sleep(poll);
            }
        }
    }

    /// <summary>
    /// Loads a trace file (<c>StartLoading</c>); by default blocks until it finishes.
    /// </summary>
    /// <remarks>
    /// The primary entry point: it calls <see cref="StartLoading"/> and then, unless
    /// <paramref name="wait"/> is <c>false</c>, <see cref="WaitUntilLoaded"/>, so the next statement
    /// can use <see cref="TraceFileInfo()"/>. The path is on the analyzer machine.
    /// </remarks>
    /// <param name="filename">The trace file path on the analyzer machine.</param>
    /// <param name="wait">When <c>true</c> (the default), block until loading finishes.</param>
    /// <param name="timeout">
    /// Maximum time to wait when <paramref name="wait"/> is <c>true</c>. Defaults to two minutes;
    /// pass a negative <see cref="TimeSpan"/> to wait forever.
    /// </param>
    /// <param name="pollInterval">How often to poll. Must be &gt; 0. Defaults to 250 ms.</param>
    /// <exception cref="LoadTimeoutException">Loading exceeded <paramref name="timeout"/>.</exception>
    /// <exception cref="OperationException">The analyzer rejected the request.</exception>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public void Load(string filename, bool wait = true, TimeSpan? timeout = null, TimeSpan? pollInterval = null)
    {
        StartLoading(filename);
        if (!wait)
        {
            return;
        }
        try
        {
            WaitUntilLoaded(timeout, pollInterval);
        }
        catch (LoadTimeoutException e)
        {
            var limit = timeout ?? TimeSpan.FromMinutes(2);
            throw new LoadTimeoutException(
                $"loading '{filename}' did not finish within {limit.TotalSeconds:0.###}s", e);
        }
    }

    /// <summary>Returns information about the loaded trace file (<c>GetTraceFileInfo</c>).</summary>
    /// <returns>The <see cref="TraceFileInfo"/> for the loaded trace.</returns>
    /// <exception cref="OperationException">The analyzer rejected the request.</exception>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public TraceFileInfo TraceFileInfo() =>
        Call(() => Automation.TraceFileInfo.FromIce(Proxy.GetTraceFileInfo()));

    /// <summary>Closes the loaded trace file (<c>CloseTraceFile</c>).</summary>
    /// <exception cref="OperationException">The analyzer rejected the request.</exception>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public void CloseTraceFile() => Call(() => Proxy.CloseTraceFile());

    /// <summary><c>true</c> if the trace has unsaved changes (<c>IsModified</c>).</summary>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public bool IsModified => Call(() => Proxy.IsModified());

    /// <summary>Saves changes to the loaded trace file (<c>SaveChanges</c>).</summary>
    /// <exception cref="OperationException">The analyzer rejected the request.</exception>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public void SaveChanges() => Call(() => Proxy.SaveChanges());

    //

    // app / info

    //
    /// <summary>Returns information about the remote application (<c>GetAppInfo</c>).</summary>
    /// <returns>The <see cref="Automation.AppInfo"/> for the remote application.</returns>
    /// <exception cref="OperationException">The analyzer rejected the request.</exception>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public AppInfo AppInfo() => Call(() => Automation.AppInfo.FromIce(Proxy.GetAppInfo()));

    /// <summary>Asks the remote application to exit (<c>ExitApp</c>).</summary>
    /// <exception cref="OperationException">The analyzer rejected the request.</exception>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public void ExitApp() => Call(() => Proxy.ExitApp());

    /// <summary>Returns the status of the current recording (<c>GetRecordingStatus</c>).</summary>
    /// <remarks>
    /// Only valid while a recording is active; the analyzer rejects it otherwise (surfacing as
    /// <see cref="OperationException"/>). Gate it on <see cref="IsRecording"/>.
    /// </remarks>
    /// <returns>The current <see cref="Automation.RecordingStatus"/>.</returns>
    /// <exception cref="OperationException">No recording is active, or the analyzer rejected the request.</exception>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public RecordingStatus RecordingStatus() =>
        Call(() => Automation.RecordingStatus.FromIce(Proxy.GetRecordingStatus()));

    /// <summary>Returns the recording options as an opaque string (<c>GetRecordingOptions</c>).</summary>
    /// <param name="relevantOnly">When <c>true</c>, return only the options relevant to the current setup.</param>
    /// <returns>The opaque recording-options blob.</returns>
    /// <exception cref="OperationException">The analyzer rejected the request.</exception>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public string GetRecordingOptions(bool relevantOnly = false) =>
        Call(() => Proxy.GetRecordingOptions(relevantOnly));

    /// <summary>Applies recording options from an opaque string (<c>ConfigureRecordingOptions</c>).</summary>
    /// <param name="options">The opaque recording-options blob (as returned by <see cref="GetRecordingOptions"/>).</param>
    /// <exception cref="OperationException">The analyzer rejected the request.</exception>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public void ConfigureRecordingOptions(string options) =>
        Call(() => Proxy.ConfigureRecordingOptions(options));

    //

    // data sources

    //
    /// <summary>Returns the available data source unique IDs (<c>GetAvailableDataSources</c>).</summary>
    /// <returns>The available data source unique IDs.</returns>
    /// <exception cref="OperationException">The analyzer rejected the request.</exception>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public IReadOnlyList<string> DataSources() => Call(() => Proxy.GetAvailableDataSources());

    /// <summary>Selects the data source by its unique ID (<c>SelectDataSource</c>).</summary>
    /// <param name="dataSourceUniqueId">The unique ID of the data source to select.</param>
    /// <exception cref="OperationException">The analyzer rejected the request.</exception>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public void SelectDataSource(string dataSourceUniqueId) =>
        Call(() => Proxy.SelectDataSource(dataSourceUniqueId));

    /// <summary>Returns the selected data source unique ID, or <c>null</c> (<c>GetSelectedDataSource</c>).</summary>
    /// <returns>The selected data source unique ID, or <c>null</c> if none is selected.</returns>
    /// <exception cref="OperationException">The analyzer rejected the request.</exception>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public string? SelectedDataSource() =>
        Call(() =>
        {
            var id = Proxy.GetSelectedDataSource();
            return string.IsNullOrEmpty(id) ? null : id;
        });

    //

    // messages / tasks / settings

    //
    /// <summary>Inserts a message in the Message Log (<c>InsertMessage</c>).</summary>
    /// <param name="severity">The message severity.</param>
    /// <param name="message">The message text.</param>
    /// <exception cref="OperationException">The analyzer rejected the request.</exception>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public void InsertMessage(MessageSeverity severity, string message) =>
        Call(() => Proxy.InsertMessage((IceAnalyzer.MessageSeverity)severity, message));

    /// <summary>
    /// Blocks until no background task is running (polls <c>GetRunningTasks</c>).
    /// </summary>
    /// <remarks>
    /// Filter changes (overview queries, device filters) re-process the trace in the background,
    /// reported as a running task (e.g. "Filtering data") while <see cref="IsLoading"/> stays
    /// <c>false</c> -- so this, not <see cref="WaitUntilLoaded"/>, is the wait that matches them.
    /// </remarks>
    /// <param name="timeout">Maximum time to wait. Defaults to ten minutes. Pass
    /// <see cref="System.Threading.Timeout.InfiniteTimeSpan"/> (or any negative value) to wait forever.</param>
    /// <param name="pollInterval">How often to poll. Must be &gt; 0. Defaults to 250 ms.</param>
    /// <param name="settlePeriod">How long idleness must persist before it is trusted (the background
    /// task can take a moment to appear after the triggering call). Defaults to 1 s.</param>
    /// <exception cref="OperationException">Tasks were still running after <paramref name="timeout"/>.</exception>
    /// <exception cref="ArgumentOutOfRangeException"><paramref name="pollInterval"/> is not positive.</exception>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public void WaitUntilIdle(TimeSpan? timeout = null, TimeSpan? pollInterval = null, TimeSpan? settlePeriod = null)
    {
        var poll = pollInterval ?? TimeSpan.FromMilliseconds(250);
        if (poll <= TimeSpan.Zero)
        {
            throw new ArgumentOutOfRangeException(nameof(pollInterval), "pollInterval must be > 0");
        }
        var limit = timeout ?? TimeSpan.FromMinutes(10);
        var waitForever = limit < TimeSpan.Zero;
        // The background task can take a moment to APPEAR after the triggering call, so idleness
        // must persist for the settle period before we trust it.
        var settle = settlePeriod ?? TimeSpan.FromSeconds(1);

        var stopwatch = Stopwatch.StartNew();
        TimeSpan? idleSince = null;
        while (true)
        {
            if (RunningTasks().Count > 0)
            {
                idleSince = null;
            }
            else
            {
                idleSince ??= stopwatch.Elapsed;
                if (stopwatch.Elapsed - idleSince >= settle)
                {
                    return;
                }
            }
            if (!waitForever)
            {
                var remaining = limit - stopwatch.Elapsed;
                if (remaining <= TimeSpan.Zero)
                {
                    throw new OperationException(
                        $"background tasks still running after {limit.TotalSeconds:0.###}s");
                }
                Thread.Sleep(remaining < poll ? remaining : poll);
            }
            else
            {
                Thread.Sleep(poll);
            }
        }
    }

    /// <summary>Returns the background tasks currently running (<c>GetRunningTasks</c>).</summary>
    /// <returns>The currently running <see cref="Automation.RunningTask"/>s.</returns>
    /// <exception cref="OperationException">The analyzer rejected the request.</exception>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public IReadOnlyList<RunningTask> RunningTasks() =>
        Call(() => Array.ConvertAll(Proxy.GetRunningTasks(), RunningTask.FromIce));

    /// <summary>Aborts the running task named <paramref name="name"/> (<c>AbortRunningTask</c>).</summary>
    /// <param name="name">The name of the task to abort.</param>
    /// <exception cref="OperationException">The analyzer rejected the request.</exception>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public void AbortRunningTask(string name) => Call(() => Proxy.AbortRunningTask(name));

    /// <summary>Returns the application settings as an opaque byte blob (<c>GetSettings</c>).</summary>
    /// <returns>The opaque settings blob.</returns>
    /// <exception cref="OperationException">The analyzer rejected the request.</exception>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public byte[] GetSettings() => Call(() => Proxy.GetSettings());

    /// <summary>Applies an opaque settings byte blob (<c>ConfigureSettings</c>).</summary>
    /// <param name="settings">The opaque settings blob (as returned by <see cref="GetSettings"/>).</param>
    /// <exception cref="OperationException">The analyzer rejected the request.</exception>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public void ConfigureSettings(byte[] settings) => Call(() => Proxy.ConfigureSettings(settings));

    /// <summary>Cancels a pending user interaction on the analyzer (<c>CancelUserInteraction</c>).</summary>
    /// <exception cref="OperationException">The analyzer rejected the request.</exception>
    /// <exception cref="ConnectionFailedException">The analyzer could not be reached.</exception>
    public void CancelUserInteraction() => Call(() => Proxy.CancelUserInteraction());
}
