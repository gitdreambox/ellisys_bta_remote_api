using Ice;
using IceAnalyzer = Ellisys.Platform.NetworkRemoteControl.Analyzer;

namespace Ellisys.Analysis.Automation;

/// <summary>
/// A connected Ellisys analyzer. Obtain one with <see cref="Connect"/> and dispose it (a
/// <c>using</c> block) to disconnect. Every operation is synchronous.
/// </summary>
/// <remarks>
/// This hides all ZeroC Ice setup (communicator, proxy, checked cast) and translates Ice
/// exceptions into the <see cref="RemoteControlException"/> hierarchy. No ZeroC Ice type
/// appears on the public surface.
/// </remarks>
public sealed partial class Analyzer : IDisposable
{
    private readonly Communicator? _communicator;
    private bool _disposed;

    private Analyzer(Communicator communicator, IceAnalyzer.AnalyzerRemoteControlPrx proxy)
    {
        _communicator = communicator;
        Proxy = proxy;
    }

    /// <summary>Test seam: wrap a (mock) proxy with no communicator. Not for production use.</summary>
    internal Analyzer(IceAnalyzer.AnalyzerRemoteControlPrx proxy)
    {
        _communicator = null;
        Proxy = proxy;
    }

    /// <summary>The underlying Ice proxy (internal — used by the wrapped operations and the tests).</summary>
    internal IceAnalyzer.AnalyzerRemoteControlPrx Proxy { get; }

    /// <summary>
    /// Connect to a running Ellisys analyzer that has Remote Control enabled.
    /// </summary>
    /// <param name="host">Analyzer host name or IP.</param>
    /// <param name="port">Remote Control TCP port.</param>
    /// <param name="messageSizeMaxMb">Raises Ice's max message size so large Overview reads succeed.</param>
    /// <exception cref="ConnectionFailedException">The analyzer cannot be reached or the endpoint is not an analyzer.</exception>
    public static Analyzer Connect(string host = "localhost", int port = 12345, int messageSizeMaxMb = 256)
    {
        var initData = new InitializationData { properties = Util.createProperties() };
        initData.properties!.setProperty("Ice.Default.EncodingVersion", "1.0");   // the API requires Ice encoding 1.0
        initData.properties!.setProperty("Ice.MessageSizeMax", (messageSizeMaxMb * 1024).ToString());

        Communicator communicator;
        try
        {
            communicator = Util.initialize(initData);
        }
        catch (LocalException e)
        {
            throw new ConnectionFailedException($"Failed to initialize Ice: {e.Message}", e);
        }

        try
        {
            var proxyString = $"{IceAnalyzer.AnalyzerRemoteControlIdentity.value}:tcp -h {host} -p {port}";
            var proxy = IceAnalyzer.AnalyzerRemoteControlPrxHelper.checkedCast(communicator.stringToProxy(proxyString));
            if (proxy is null)
            {
                throw new ConnectionFailedException($"Endpoint {host}:{port} is not an Ellisys analyzer remote control.");
            }
            return new Analyzer(communicator, proxy);
        }
        catch (LocalException e)
        {
            communicator.destroy();
            throw new ConnectionFailedException($"Could not reach an analyzer at {host}:{port}: {e.Message}", e);
        }
        catch
        {
            communicator.destroy();
            throw;
        }
    }

    /// <summary>
    /// The single chokepoint for analyzer calls: runs <paramref name="operation"/> and translates
    /// Ice exceptions into the SDK hierarchy (declared failures to <see cref="OperationException"/>,
    /// transport failures to <see cref="ConnectionFailedException"/>).
    /// </summary>
    internal T Call<T>(Func<T> operation)
    {
        EnsureNotDisposed();
        try
        {
            return operation();
        }
        catch (UserException e)
        {
            throw new OperationException(DescribeUserException(e), e);
        }
        catch (LocalException e)
        {
            throw new ConnectionFailedException(e.Message, e);
        }
    }

    /// <summary>Void overload of <see cref="Call{T}"/>.</summary>
    internal void Call(Action operation) => Call<object?>(() => { operation(); return null; });

    private static string DescribeUserException(UserException e)
    {
        // The generated OperationFailed exception carries a public "Reason" field; fall back to
        // the exception type name when it isn't present.
        var type = e.GetType();
        var reason = type.GetField("Reason")?.GetValue(e) as string
                     ?? type.GetProperty("Reason")?.GetValue(e) as string;
        return string.IsNullOrEmpty(reason) ? type.Name : reason!;
    }

    private void EnsureNotDisposed()
    {
        if (_disposed)
        {
            throw new ObjectDisposedException(nameof(Analyzer));
        }
    }

    /// <summary>Disconnect from the analyzer and release the Ice communicator.</summary>
    public void Dispose()
    {
        if (_disposed)
        {
            return;
        }
        _disposed = true;
        try
        {
            _communicator?.destroy();
        }
        catch
        {
            // best effort -- nothing useful to do if teardown fails
        }
    }
}
