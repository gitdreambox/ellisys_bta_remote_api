# Copyright (c) ZeroC, Inc.

# slice2py version 3.8.2

from __future__ import annotations
import IcePy

from dataclasses import dataclass


@dataclass(order=True, unsafe_hash=True)
class RunningTask:
    """
    Notes
    -----
        The Slice compiler generated this dataclass from Slice struct ``::Ellisys::Platform::NetworkRemoteControl::Analyzer::RunningTask``.
    """
    Name: str = ""
    ProgressPercent: int = 0
    ProgressApplicable: bool = False

_Ellisys_Platform_NetworkRemoteControl_Analyzer_RunningTask_t = IcePy.defineStruct(
    "::Ellisys::Platform::NetworkRemoteControl::Analyzer::RunningTask",
    RunningTask,
    (),
    (
        ("Name", (), IcePy._t_string),
        ("ProgressPercent", (), IcePy._t_int),
        ("ProgressApplicable", (), IcePy._t_bool)
    ))

__all__ = ["RunningTask", "_Ellisys_Platform_NetworkRemoteControl_Analyzer_RunningTask_t"]
