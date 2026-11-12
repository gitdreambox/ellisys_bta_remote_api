# Copyright (c) ZeroC, Inc.

# slice2py version 3.8.2

from __future__ import annotations
import IcePy

from dataclasses import dataclass


@dataclass(order=True, unsafe_hash=True)
class RecordingStatus:
    """
    Notes
    -----
        The Slice compiler generated this dataclass from Slice struct ``::Ellisys::Platform::NetworkRemoteControl::Analyzer::RecordingStatus``.
    """
    DataSource: str = ""
    DurationSeconds: int = 0
    FileSize: int = 0

_Ellisys_Platform_NetworkRemoteControl_Analyzer_RecordingStatus_t = IcePy.defineStruct(
    "::Ellisys::Platform::NetworkRemoteControl::Analyzer::RecordingStatus",
    RecordingStatus,
    (),
    (
        ("DataSource", (), IcePy._t_string),
        ("DurationSeconds", (), IcePy._t_int),
        ("FileSize", (), IcePy._t_long)
    ))

__all__ = ["RecordingStatus", "_Ellisys_Platform_NetworkRemoteControl_Analyzer_RecordingStatus_t"]
