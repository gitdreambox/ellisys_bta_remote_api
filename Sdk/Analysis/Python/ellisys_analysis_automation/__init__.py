r"""Ellisys Analysis Automation SDK -- a Pythonic client for the Ellisys analyzer automation API.

Quick start::

    import ellisys_analysis_automation as ea

    with ea.connect("localhost", 12345) as analyzer:
        with analyzer.recording(save_to=r"C:\traces\session"):
            input("Recording... press Enter to stop & save")

No ZeroC Ice details leak out: connection setup, the Slice bindings, the proxy and the
communicator lifecycle are all handled for you. The bindings under ``_generated/`` are
pre-generated (slice2py) and pinned to a matching ``zeroc-ice`` runtime.
"""
from . import discovery, exports
from .analyzer import Analyzer, connect
from .bluetooth import (
    BluetoothAirtimeOptions,
    BluetoothAudioOptions,
    BluetoothChannelsOptions,
    BluetoothChannelStat,
    BluetoothChannelSummary,
    BluetoothExportModes,
    BluetoothPacketLossMode,
    BluetoothSpectrumRange,
    BluetoothSpectrumSample,
    DeviceFilterMode,
    format_bluetooth_bdaddr,
)
from .errors import ConnectionFailed, LoadTimeout, NotAvailable, OperationError, RemoteControlError
from .exports import (
    ExportMode,
    ExportModes,
    ExportOptionError,
    ExportOptions,
    FilteredTraceOptions,
    ThroughputOptions,
)
from .markers import Marker, MarkerColor
from .session import AppInfo, MessageSeverity, RecordingStatus, RunningTask, TraceFileInfo
from .signals import LogicSignalTransition, LogicSignalTransitionType
from .overview import (
    BoundExceeded,
    ChildCursor,
    ItemField,
    ItemRecord,
    OverviewIncomplete,
    OverviewItem,
    OverviewItemList,
    OverviewScope,
    Page,
    ScopeClosed,
    SearchCursor,
    XmlFilter,
)

__all__ = [
    "connect",
    "Analyzer",
    "RemoteControlError",
    "ConnectionFailed",
    "OperationError",
    "LoadTimeout",
    "NotAvailable",
    # overview navigation
    "OverviewScope",
    "OverviewItem",
    "OverviewItemList",
    "Page",
    "ChildCursor",
    "SearchCursor",
    "ItemRecord",
    "ItemField",
    "XmlFilter",
    "ScopeClosed",
    "BoundExceeded",
    "OverviewIncomplete",
    # markers
    "Marker",
    "MarkerColor",
    # exports
    "exports",
    "discovery",
    "ExportMode",
    "ExportModes",
    "ExportOptions",
    "FilteredTraceOptions",
    "ThroughputOptions",
    "ExportOptionError",
    # session / trace-file / info
    "AppInfo",
    "RecordingStatus",
    "TraceFileInfo",
    "RunningTask",
    "MessageSeverity",
    # logic signals
    "LogicSignalTransitionType",
    "LogicSignalTransition",
    # bluetooth facet (the facet itself is reached only via analyzer.bluetooth)
    "DeviceFilterMode",
    "BluetoothChannelSummary",
    "BluetoothChannelStat",
    "BluetoothSpectrumSample",
    "BluetoothSpectrumRange",
    "BluetoothPacketLossMode",
    "BluetoothExportModes",
    "BluetoothAudioOptions",
    "BluetoothChannelsOptions",
    "BluetoothAirtimeOptions",
    "format_bluetooth_bdaddr",
]

__version__ = "0.1.0"
