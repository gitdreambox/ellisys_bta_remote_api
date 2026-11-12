# Copyright (c) ZeroC, Inc.

# slice2py version 3.8.2

from __future__ import annotations
import IcePy

from Ellisys.Platform.NetworkRemoteControl.Analyzer.OperationFailed import OperationFailed
from Ellisys.Platform.NetworkRemoteControl.Analyzer.OperationFailed import _Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t

from dataclasses import dataclass


@dataclass
class IncorrectState(OperationFailed):
    """
    Notes
    -----
        The Slice compiler generated this exception dataclass from Slice exception ``::Ellisys::Platform::NetworkRemoteControl::Analyzer::IncorrectState``.
    """

    _ice_id = "::Ellisys::Platform::NetworkRemoteControl::Analyzer::IncorrectState"

_Ellisys_Platform_NetworkRemoteControl_Analyzer_IncorrectState_t = IcePy.defineException(
    "::Ellisys::Platform::NetworkRemoteControl::Analyzer::IncorrectState",
    IncorrectState,
    (),
    _Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,
    ())

setattr(IncorrectState, '_ice_type', _Ellisys_Platform_NetworkRemoteControl_Analyzer_IncorrectState_t)

__all__ = ["IncorrectState", "_Ellisys_Platform_NetworkRemoteControl_Analyzer_IncorrectState_t"]
