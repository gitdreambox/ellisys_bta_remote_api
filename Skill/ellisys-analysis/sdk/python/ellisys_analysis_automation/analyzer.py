"""High-level, Pythonic client for the Ellisys Analyzer Remote Control API.

The goal: connect and drive an analyzer without touching ZeroC Ice. :func:`connect` hides the
encoding/message-size setup, the proxy string and the checked cast; :class:`Analyzer` exposes
operations as snake_case methods, translates Ice errors into the SDK's exceptions, and manages
the communicator lifecycle (use it as a context manager).
"""
import contextlib
import os
import time

import Ice

from . import _bindings, overview
from .errors import ConnectionFailed, LoadTimeout, OperationError
from .exports import ExportModes, FilteredTraceOptions, ThroughputOptions, _to_ps, _build_export_options
from .markers import Marker, MarkerColor
from .signals import LogicSignalTransition, LogicSignalTransitionType
from .session import AppInfo, MessageSeverity, RecordingStatus, RunningTask, TraceFileInfo


def connect(host="localhost", port=12345, *, message_size_max_mb=256):
    """Connect to a running Ellisys analyzer that has Remote Control enabled.

    Hides all ZeroC Ice setup: it loads the pre-generated bindings, forces the mandatory Ice
    encoding 1.0, raises the message-size limit, builds the proxy and performs the checked
    cast. Returns an :class:`Analyzer`; use it as a context manager or call ``close()``.

    Raises :class:`~ellisys_analysis_automation.errors.ConnectionFailed` if the analyzer cannot be
    reached or the endpoint is not an analyzer.
    """
    module = _bindings.load()

    properties = Ice.createProperties([])
    properties.setProperty("Ice.Default.EncodingVersion", "1.0")              # the API requires 1.0
    properties.setProperty("Ice.MessageSizeMax", str(int(message_size_max_mb) * 1024))  # KB
    init_data = Ice.InitializationData()
    init_data.properties = properties
    communicator = Ice.initialize(initData=init_data)

    try:
        endpoint = "{0}:tcp -h {1} -p {2}".format(module.AnalyzerRemoteControlIdentity, host, port)
        proxy = module.AnalyzerRemoteControlPrx.checkedCast(communicator.stringToProxy(endpoint))
        if proxy is None:
            raise ConnectionFailed(
                "Reached {0}:{1} but it is not an Analyzer Remote Control endpoint "
                "(is the Remote Control plugin enabled?).".format(host, port))
    except Ice.LocalException as exc:
        communicator.destroy()
        raise ConnectionFailed(
            "Could not connect to the analyzer at {0}:{1}. Is the Ellisys software running "
            "with Remote Control enabled on that port? [{2}]".format(host, port, type(exc).__name__)) from exc
    except BaseException:
        communicator.destroy()
        raise

    return Analyzer(communicator, proxy, module)


class Analyzer:
    """A connected Ellisys analyzer. Obtain one from :func:`connect`.

    Supports the context-manager protocol; leaving the ``with`` block disconnects.
    """

    def __init__(self, communicator, proxy, module=None):
        self._communicator = communicator
        self._proxy = proxy
        self._module = module       # the Slice bindings module (for constructing Ice structs/enums)
        self._active_scope = None   # at most one overview scope at a time (handles are global)
        self._bluetooth = None      # cached product facets (one each per Analyzer)
        self._wifi = None
        self._wpan = None
        self._usb30 = None

    def __repr__(self):
        return "<Analyzer {0}>".format("closed" if self._communicator is None else "connected")

    # ------------------------------------------------------------------ recording
    @property
    def is_recording(self):
        """``True`` while a capture is in progress."""
        return self._call(self._proxy.IsRecording)

    def start_recording(self):
        """Start a capture (equivalent to Record > Start in the GUI)."""
        self._call(self._proxy.StartRecording)

    def stop_and_save(self, filename, *, overwrite=False):
        """Stop the capture and save the trace to *filename*.

        The path is interpreted on the **analyzer machine**, not the client running this
        script. Set ``overwrite=True`` to replace an existing file.
        """
        self._call(self._proxy.StopRecordingAndSaveTraceFile, filename, bool(overwrite))

    def abort_recording(self):
        """Stop the capture and discard the trace (nothing is saved)."""
        self._call(self._proxy.AbortRecordingAndDiscardTraceFile)

    @contextlib.contextmanager
    def recording(self, save_to, *, overwrite=False):
        """Record for the duration of the ``with`` block, then stop and save to *save_to*.

        On a normal exit the trace is saved. If the body raises, the trace is still saved
        (best effort) and the original exception propagates -- a capture is rarely worth
        losing because the script that triggered it failed.
        """
        self.start_recording()
        try:
            yield self
        except BaseException:
            with contextlib.suppress(Exception):
                self.stop_and_save(save_to, overwrite=overwrite)
            raise
        else:
            self.stop_and_save(save_to, overwrite=overwrite)

    # ------------------------------------------------------------------ overview
    def overviews(self):
        """Names of the available overviews (-> GetAvailableOverviews). No scope needed."""
        return list(self._call(self._proxy.GetAvailableOverviews))

    def active_overview(self):
        """Name of the currently selected overview, or ``None`` (-> GetSelectedOverview)."""
        return self._call(self._proxy.GetSelectedOverview) or None

    @contextlib.contextmanager
    def overview(self, name=None, *, query=None, protocol_layer=None, restore_active=True):
        """Open a navigation scope on *name* (or the already-active overview if ``None``).

        Mirrors :meth:`recording`: on entry it snapshots the active overview, selects *name*,
        and optionally applies *query* / *protocol_layer*; it yields an
        :class:`~ellisys_analysis_automation.overview.OverviewScope` for navigating the tree. On
        exit it frees all item handles once (``ReleaseAllOverviewItemHandles``) and, unless
        ``restore_active=False``, re-selects the previously active overview.

        Only one scope may be open at a time -- handle release is global, so a nested scope
        would free this one's handles. Opening a second raises
        :class:`~ellisys_analysis_automation.errors.OperationError`.
        """
        if self._active_scope is not None and not self._active_scope.closed:
            raise OperationError(
                "an overview scope is already open; close it first -- "
                "ReleaseAllOverviewItemHandles is global and would free its handles.")

        prior = self._call(self._proxy.GetSelectedOverview) or None
        target = name if name is not None else prior
        if name is not None:
            self._call(self._proxy.SelectOverview, name)
        if query is not None:
            self._call(self._proxy.SetOverviewQuery, query)
        if protocol_layer is not None:
            self._call(self._proxy.SelectProtocolLayer, protocol_layer)

        scope = overview.OverviewScope(self, target)
        self._active_scope = scope
        try:
            yield scope
        finally:
            scope._live = False                       # dead BEFORE release: stale use raises locally
            self._active_scope = None
            with contextlib.suppress(Exception):      # cleanup never masks the body's error
                self._call(self._proxy.ReleaseAllOverviewItemHandles)
            if restore_active and prior is not None and prior != target:
                with contextlib.suppress(Exception):
                    self._call(self._proxy.SelectOverview, prior)

    # ------------------------------------------------------------------ markers
    def add_marker_at_time(self, time_ps, text, *, color=MarkerColor.YELLOW):
        """Add a marker at *time_ps* picoseconds (-> AddMarkerAtTime).

        *color* is a :class:`~ellisys_analysis_automation.MarkerColor` (or its int value).
        """
        self._call(self._proxy.AddMarkerAtTime, _to_ps(time_ps), self._make_add_marker(color, text))

    def add_marker_on_selected_overview_item(self, text, *, color=MarkerColor.YELLOW):
        """Add a marker on the currently selected overview item (-> AddMarkerOnSelectedOverviewItem)."""
        self._call(self._proxy.AddMarkerOnSelectedOverviewItem, self._make_add_marker(color, text))

    def markers(self):
        """Every marker in the trace as handle-free :class:`~ellisys_analysis_automation.Marker`\\ s (-> GetMarkers)."""
        return [Marker(color=MarkerColor(m.Color.value), text=m.Text, time_ps=m.Time)
                for m in self._call(self._proxy.GetMarkers)]

    def _make_add_marker(self, color, text):
        """Build the Ice ``AddMarker`` struct from an SDK colour + text."""
        module = self._bindings_module()
        return module.AddMarker(Color=module.MarkerColor(int(color)), Text=str(text))

    def _bindings_module(self):
        """The Slice bindings module (lazily loaded), used to construct Ice structs/enums."""
        if self._module is None:
            self._module = _bindings.load()
        return self._module

    # ------------------------------------------------------------------ exports
    def export(self, output, mode, *, options=None):
        """Run any export mode (-> Export). Generic primary method AND escape hatch.

        *output* is a path on the **analyzer machine** (like :meth:`stop_and_save`). *mode* is
        the server ``exportName`` -- an :class:`~ellisys_analysis_automation.ExportMode` member or any
        raw string (including modes newer than this SDK). *options* is a typed carrier (e.g.
        :class:`~ellisys_analysis_automation.BluetoothAudioOptions`) or a raw ``{OptionName: value}``
        mapping keyed by the EXACT server tokens (PascalCase). Values may be ``int``, ``bool``,
        ``str``, :class:`datetime.timedelta`, or an ``Enum``; ``None`` values are omitted. A
        product mode used on the wrong analyzer raises
        :class:`~ellisys_analysis_automation.errors.OperationError`.
        """
        if hasattr(options, "validate"):
            options.validate()
        module = self._bindings_module()
        raw = options.as_options() if hasattr(options, "as_options") else options
        self._call(self._proxy.Export, os.fspath(output), str(mode), _build_export_options(raw, module))

    def export_dry_run(self, output, mode, *, options=None):
        """Render the exact ``(OptionName, OptionValue)`` wire pairs WITHOUT sending (offline).

        Calls ``options.validate()`` if present, then returns what :meth:`export` would send.
        Makes no proxy call -- useful for tests and for inspecting omit-None / bool / enum /
        picosecond rendering before committing a long export. (*output* is accepted for
        signature symmetry with :meth:`export`; it is not part of the option pairs.)
        """
        if hasattr(options, "validate"):
            options.validate()
        module = self._bindings_module()
        raw = options.as_options() if hasattr(options, "as_options") else options
        return [(o.OptionName, o.OptionValue) for o in _build_export_options(raw, module)]

    def export_filtered_trace_time_range(self, output, *, start_time_ps=None, max_size_bytes=None,
                                         max_duration_ps=None, max_items=None):
        """Export a filtered trace by time range (BASE; any analyzer).

        ``*_ps`` accept int picoseconds or a :class:`datetime.timedelta`; ``max_size_bytes`` is a
        byte count. ``None`` omits the option (server defaults: StartTime 0, the rest = full trace).
        """
        self.export(output, ExportModes.FILTERED_TRACE_TIME_RANGE, options=FilteredTraceOptions(
            start_time_ps=start_time_ps, max_size_bytes=max_size_bytes,
            max_duration_ps=max_duration_ps, max_items=max_items))

    def export_filtered_trace_active_overview(self, output, *, start_time_ps=None, max_size_bytes=None,
                                              max_duration_ps=None, max_items=None):
        """Export a filtered trace by the active overview (BASE). Same options as the time-range form."""
        self.export(output, ExportModes.FILTERED_TRACE_ACTIVE_OVERVIEW, options=FilteredTraceOptions(
            start_time_ps=start_time_ps, max_size_bytes=max_size_bytes,
            max_duration_ps=max_duration_ps, max_items=max_items))

    def export_throughput(self, output, *, range_start_time_ps=None, range_end_time_ps=None):
        """Export throughput over a time range (BASE). ``None`` -> server default (trace start/end)."""
        opts = ThroughputOptions(range_start_time_ps=range_start_time_ps, range_end_time_ps=range_end_time_ps)
        opts.validate()
        self.export(output, ExportModes.THROUGHPUT, options=opts)

    # ------------------------------------------------------------------ app / info
    def app_info(self):
        """Information about the remote application (-> GetAppInfo)."""
        return AppInfo._from_ice(self._call(self._proxy.GetAppInfo))

    def exit_app(self):
        """Ask the remote application to exit (-> ExitApp)."""
        self._call(self._proxy.ExitApp)

    def recording_status(self):
        """Status of the current recording (-> GetRecordingStatus).

        Only valid while a recording is active; the analyzer rejects it otherwise (surfacing as
        :class:`~ellisys_analysis_automation.errors.OperationError`). Gate it on :attr:`is_recording`.
        """
        return RecordingStatus._from_ice(self._call(self._proxy.GetRecordingStatus))

    def get_recording_options(self, *, relevant_only=False):
        """The recording options as an opaque string (-> GetRecordingOptions)."""
        return self._call(self._proxy.GetRecordingOptions, bool(relevant_only))

    def configure_recording_options(self, options):
        """Apply recording options from an opaque string (-> ConfigureRecordingOptions)."""
        self._call(self._proxy.ConfigureRecordingOptions, options)

    # ------------------------------------------------------------------ data sources
    def data_sources(self):
        """Available data source unique IDs (-> GetAvailableDataSources)."""
        return list(self._call(self._proxy.GetAvailableDataSources))

    def select_data_source(self, data_source_unique_id):
        """Select the data source by its unique ID (-> SelectDataSource)."""
        self._call(self._proxy.SelectDataSource, data_source_unique_id)

    def selected_data_source(self):
        """The selected data source unique ID, or ``None`` (-> GetSelectedDataSource)."""
        return self._call(self._proxy.GetSelectedDataSource) or None

    # ------------------------------------------------------------------ trace file
    @property
    def is_loading(self):
        """``True`` while a trace file is loading (-> IsLoading)."""
        return self._call(self._proxy.IsLoading)

    def start_loading(self, filename):
        """Begin loading *filename* and return immediately (-> StartLoading).

        Loading is asynchronous: poll :attr:`is_loading` (or use :meth:`wait_until_loaded` /
        :meth:`load`) to know when it finishes. *filename* is a path on the analyzer machine.
        """
        self._call(self._proxy.StartLoading, os.fspath(filename))

    def wait_until_loaded(self, *, timeout=120.0, poll_interval=0.25):
        """Block until :attr:`is_loading` is ``False`` (raises :class:`LoadTimeout` on timeout).

        Polls every *poll_interval* seconds against a monotonic deadline. ``timeout=None`` waits
        forever. *poll_interval* must be > 0.
        """
        if poll_interval <= 0:
            raise ValueError("poll_interval must be > 0")
        deadline = None if timeout is None else time.monotonic() + timeout
        while self.is_loading:
            if deadline is not None:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise LoadTimeout("trace load did not finish within {0:g}s".format(timeout))
                time.sleep(min(poll_interval, remaining))
            else:
                time.sleep(poll_interval)

    def load(self, filename, *, wait=True, timeout=120.0, poll_interval=0.25):
        """Load a trace file (-> StartLoading); by default blocks until it finishes.

        The primary entry point: it calls :meth:`start_loading` and then, unless ``wait=False``,
        :meth:`wait_until_loaded`, so the next statement can use :meth:`trace_file_info`.
        Raises :class:`LoadTimeout` if loading exceeds *timeout* (``None`` waits forever). The
        path is on the analyzer machine.
        """
        self.start_loading(filename)
        if wait:
            try:
                self.wait_until_loaded(timeout=timeout, poll_interval=poll_interval)
            except LoadTimeout as exc:
                raise LoadTimeout("loading {0!r} did not finish within {1:g}s".format(
                    os.fspath(filename), timeout)) from exc

    def trace_file_info(self):
        """Information about the loaded trace file (-> GetTraceFileInfo)."""
        return TraceFileInfo._from_ice(self._call(self._proxy.GetTraceFileInfo))

    def close_trace_file(self):
        """Close the loaded trace file (-> CloseTraceFile)."""
        self._call(self._proxy.CloseTraceFile)

    @property
    def is_modified(self):
        """``True`` if the trace has unsaved changes (-> IsModified)."""
        return self._call(self._proxy.IsModified)

    def save_changes(self):
        """Save changes to the loaded trace file (-> SaveChanges)."""
        self._call(self._proxy.SaveChanges)

    # ------------------------------------------------------------------ messages / tasks / settings
    def insert_message(self, severity, message):
        """Insert a message in the Message Log (-> InsertMessage).

        *severity* is a :class:`~ellisys_analysis_automation.MessageSeverity` (or its int value).
        """
        self._call(self._proxy.InsertMessage, self._make_severity(severity), message)

    # NOTE: the Slice ``InsertComment`` op is deprecated (use InsertMessage); intentionally not wrapped.

    def running_tasks(self):
        """Background tasks currently running (-> GetRunningTasks)."""
        return [RunningTask._from_ice(t) for t in self._call(self._proxy.GetRunningTasks)]

    def wait_until_idle(self, *, timeout=600.0, poll_interval=0.25, settle=1.0):
        """Block until no background task is running (polls -> GetRunningTasks).

        Filter changes (overview queries, device filters) re-process the trace in the
        background, reported as a running task (e.g. ``"Filtering data"``) while
        :attr:`is_loading` stays ``False`` -- so this, not :meth:`wait_until_loaded`, is the
        wait that matches them. The background task can take a moment to *appear* after the
        triggering call, so idleness must persist for *settle* seconds before this returns
        (``settle=0`` returns on the first idle observation). ``timeout=None`` waits forever;
        raises :class:`OperationError` on timeout. *poll_interval* must be > 0.
        """
        if poll_interval <= 0:
            raise ValueError("poll_interval must be > 0")
        deadline = None if timeout is None else time.monotonic() + timeout
        idle_since = None
        while True:
            if self.running_tasks():
                idle_since = None
            else:
                now = time.monotonic()
                if idle_since is None:
                    idle_since = now
                if now - idle_since >= settle:
                    return
            if deadline is not None and time.monotonic() > deadline:
                raise OperationError(
                    "background tasks still running after {0} s".format(timeout))
            time.sleep(poll_interval)

    def abort_running_task(self, name):
        """Abort the running task named *name* (-> AbortRunningTask)."""
        self._call(self._proxy.AbortRunningTask, name)

    def get_settings(self):
        """The application settings as an opaque ``bytes`` blob (-> GetSettings)."""
        return self._call(self._proxy.GetSettings)

    def configure_settings(self, settings):
        """Apply an opaque settings ``bytes`` blob (-> ConfigureSettings)."""
        self._call(self._proxy.ConfigureSettings, settings)

    def cancel_user_interaction(self):
        """Cancel a pending user interaction on the analyzer (-> CancelUserInteraction)."""
        self._call(self._proxy.CancelUserInteraction)

    def _make_severity(self, severity):
        """Build the Ice ``MessageSeverity`` enumerator from an SDK severity."""
        return self._bindings_module().MessageSeverity(int(severity))

    # ------------------------------------------------------------------ logic signals
    def logic_signals_state(self, time_ps):
        """Bitmask of all logic-signal levels at *time_ps* (bit N == signal N) (-> GetLogicSignalsState)."""
        return self._call(self._proxy.GetLogicSignalsState, _to_ps(time_ps))

    def find_logic_signal_transition(self, from_time_ps, to_time_ps, signals_mask,
                                     transition_type=LogicSignalTransitionType.ANY):
        """Search [*from_time_ps*, *to_time_ps*] for a transition on the masked signals.

        *signals_mask* selects signals by bit (set bit N to include signal N); *transition_type*
        is a :class:`~ellisys_analysis_automation.LogicSignalTransitionType`. Returns a
        :class:`~ellisys_analysis_automation.LogicSignalTransition` (state bitmask + time). Raises
        :class:`~ellisys_analysis_automation.errors.OperationError` if no matching transition is found.
        (-> FindLogicSignalsTransition)
        """
        ice_type = self._bindings_module().LogicSignalTransitionType(int(transition_type))
        state, found_time_ps = self._call(self._proxy.FindLogicSignalsTransition,
                                          _to_ps(from_time_ps), _to_ps(to_time_ps),
                                          int(signals_mask), ice_type)
        return LogicSignalTransition(state=state, time_ps=found_time_ps)

    # ------------------------------------------------------------------ product facets
    @property
    def bluetooth(self):
        """The Bluetooth-specific facet (-> BluetoothAnalyzerRemoteControl), cached per analyzer.

        Valid only on a Bluetooth analyzer; raises
        :class:`~ellisys_analysis_automation.errors.NotAvailable` if the connected analyzer is a
        different product.
        """
        if self._bluetooth is None:
            from .bluetooth import BluetoothFacet
            self._bluetooth = BluetoothFacet._attach(self)
        return self._bluetooth

    @property
    def wifi(self):
        """The Wi-Fi facet (-> EthernetAnalyzerRemoteControl), cached; ``NotAvailable`` if not a Wi-Fi analyzer."""
        if self._wifi is None:
            from .wifi import WifiFacet
            self._wifi = WifiFacet._attach(self)
        return self._wifi

    @property
    def wpan(self):
        """The WPAN facet (-> WpanAnalyzerRemoteControl), cached; ``NotAvailable`` if not a WPAN analyzer."""
        if self._wpan is None:
            from .wpan import WpanFacet
            self._wpan = WpanFacet._attach(self)
        return self._wpan

    @property
    def usb30(self):
        """The USB 3.0 facet (-> Usb30AnalyzerRemoteControl), cached; ``NotAvailable`` if not a USB 3.0 analyzer."""
        if self._usb30 is None:
            from .usb import Usb30Facet
            self._usb30 = Usb30Facet._attach(self)
        return self._usb30

    # ------------------------------------------------------------------ lifecycle
    def close(self):
        """Disconnect and release the Ice communicator. Idempotent."""
        if self._communicator is not None:
            self._communicator.destroy()
            self._communicator = None

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()

    # ------------------------------------------------------------------ internal
    def _call(self, operation, *args):
        """Invoke an Ice operation, translating Ice errors into SDK exceptions."""
        try:
            return operation(*args)
        except Ice.UserException as exc:        # declared Slice exceptions, e.g. OperationFailed
            raise OperationError(_describe(exc)) from exc
        except Ice.LocalException as exc:       # transport-level: connection lost, timeout, ...
            raise ConnectionFailed("Lost the connection to the analyzer [{0}].".format(type(exc).__name__)) from exc


def _describe(user_exception):
    """Best-effort human message from a Slice exception."""
    for attr in ("Reason", "reason", "message", "description"):  # Slice OperationFailed field is 'Reason'
        value = getattr(user_exception, attr, None)
        if value:
            return str(value)
    text = str(user_exception).strip()
    return text or type(user_exception).__name__
