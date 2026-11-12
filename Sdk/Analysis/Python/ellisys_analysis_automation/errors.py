"""Exception hierarchy for the Ellisys Analysis Automation SDK.

Everything the SDK raises derives from :class:`RemoteControlError`, so callers can catch one
type. Transport problems surface as :class:`ConnectionFailed`; operations the analyzer rejects
surface as :class:`OperationError` (wrapping the Slice ``OperationFailed``).
"""


class RemoteControlError(Exception):
    """Base class for every error raised by the SDK."""


class ConnectionFailed(RemoteControlError):
    """The analyzer could not be reached or the connection was lost.

    Common causes: the Ellisys software is not running, the Remote Control plugin is not
    enabled, or the host/port is wrong.
    """


class OperationError(RemoteControlError):
    """The analyzer accepted the request but rejected the operation.

    Wraps the Slice ``OperationFailed`` exception; the message carries the analyzer's reason
    when one is available.
    """


class NotAvailable(RemoteControlError):
    """A requested product facet is not available on the connected analyzer.

    Raised by ``analyzer.bluetooth`` (and future product facets) when the endpoint is reachable
    and healthy but is a *different* product, so the product interface's ``checkedCast`` returns
    no proxy. Distinct from :class:`ConnectionFailed` (transport) and :class:`OperationError`
    (the server rejected an operation, e.g. a wrong-product ``export``); still catchable as
    :class:`RemoteControlError`.
    """


class LoadTimeout(OperationError):
    """A trace load did not finish within the timeout.

    Raised by :meth:`Analyzer.load` / :meth:`Analyzer.wait_until_loaded` when ``IsLoading``
    stays ``True`` past the deadline. Subclasses :class:`OperationError` so existing
    ``except OperationError`` handlers still catch it; the message carries the filename (when
    known), the elapsed time, and the timeout.
    """
