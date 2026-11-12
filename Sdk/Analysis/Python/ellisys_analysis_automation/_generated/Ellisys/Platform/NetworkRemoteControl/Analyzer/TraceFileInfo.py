# Copyright (c) ZeroC, Inc.

# slice2py version 3.8.2

from __future__ import annotations
import IcePy

from dataclasses import dataclass


@dataclass(order=True, unsafe_hash=True)
class TraceFileInfo:
    """
    Notes
    -----
        The Slice compiler generated this dataclass from Slice struct ``::Ellisys::Platform::NetworkRemoteControl::Analyzer::TraceFileInfo``.
    """
    Path: str = ""
    FileSize: int = 0
    StartDateTimeUtc: int = 0
    SoftwareVersion: str = ""
    DataSource: str = ""
    UniqueId: str = ""
    RecordingOptions: str = ""

_Ellisys_Platform_NetworkRemoteControl_Analyzer_TraceFileInfo_t = IcePy.defineStruct(
    "::Ellisys::Platform::NetworkRemoteControl::Analyzer::TraceFileInfo",
    TraceFileInfo,
    (),
    (
        ("Path", (), IcePy._t_string),
        ("FileSize", (), IcePy._t_long),
        ("StartDateTimeUtc", (), IcePy._t_long),
        ("SoftwareVersion", (), IcePy._t_string),
        ("DataSource", (), IcePy._t_string),
        ("UniqueId", (), IcePy._t_string),
        ("RecordingOptions", (), IcePy._t_string)
    ))

__all__ = ["TraceFileInfo", "_Ellisys_Platform_NetworkRemoteControl_Analyzer_TraceFileInfo_t"]
