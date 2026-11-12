namespace Ellisys.Analysis.Automation;

/// <summary>Base type for every error raised by the SDK. Catch this to catch them all.</summary>
public class RemoteControlException : Exception
{
    /// <summary>Create a remote-control error with a message and optional inner exception.</summary>
    public RemoteControlException(string message, Exception? innerException = null)
        : base(message, innerException) { }
}

/// <summary>The analyzer could not be reached, or the endpoint is not an Ellisys analyzer.</summary>
public sealed class ConnectionFailedException : RemoteControlException
{
    /// <summary>Create a connection failure.</summary>
    public ConnectionFailedException(string message, Exception? innerException = null)
        : base(message, innerException) { }
}

/// <summary>The analyzer rejected the operation (a server-side failure, e.g. a wrong-product call).</summary>
public class OperationException : RemoteControlException
{
    /// <summary>Create an operation failure.</summary>
    public OperationException(string message, Exception? innerException = null)
        : base(message, innerException) { }
}

/// <summary>A trace did not finish loading within the allotted time.</summary>
public sealed class LoadTimeoutException : OperationException
{
    /// <summary>Create a load-timeout failure.</summary>
    public LoadTimeoutException(string message, Exception? innerException = null)
        : base(message, innerException) { }
}

/// <summary>A requested product facet or feature is not available on this analyzer.</summary>
public sealed class NotAvailableException : RemoteControlException
{
    /// <summary>Create a not-available failure.</summary>
    public NotAvailableException(string message, Exception? innerException = null)
        : base(message, innerException) { }
}
