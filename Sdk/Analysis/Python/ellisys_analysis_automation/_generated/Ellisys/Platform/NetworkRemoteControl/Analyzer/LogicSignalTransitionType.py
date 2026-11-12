# Copyright (c) ZeroC, Inc.

# slice2py version 3.8.2

from __future__ import annotations
import IcePy

from enum import Enum

class LogicSignalTransitionType(Enum):
    """
    Notes
    -----
        The Slice compiler generated this enum class from Slice enumeration ``::Ellisys::Platform::NetworkRemoteControl::Analyzer::LogicSignalTransitionType``.
    """

    Any = 0

    RisingEdge = 1

    FallingEdge = 2

_Ellisys_Platform_NetworkRemoteControl_Analyzer_LogicSignalTransitionType_t = IcePy.defineEnum(
    "::Ellisys::Platform::NetworkRemoteControl::Analyzer::LogicSignalTransitionType",
    LogicSignalTransitionType,
    (),
    {
        0: LogicSignalTransitionType.Any,
        1: LogicSignalTransitionType.RisingEdge,
        2: LogicSignalTransitionType.FallingEdge,
    }
)

__all__ = ["LogicSignalTransitionType", "_Ellisys_Platform_NetworkRemoteControl_Analyzer_LogicSignalTransitionType_t"]
