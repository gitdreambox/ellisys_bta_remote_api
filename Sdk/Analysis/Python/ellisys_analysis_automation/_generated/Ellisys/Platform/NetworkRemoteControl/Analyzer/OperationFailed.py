# Copyright (c) ZeroC, Inc.

# slice2py version 3.8.2

from __future__ import annotations
import IcePy

from Ice.UserException import UserException

from dataclasses import dataclass


@dataclass
class OperationFailed(UserException):
    """
    Notes
    -----
        The Slice compiler generated this exception dataclass from Slice exception ``::Ellisys::Platform::NetworkRemoteControl::Analyzer::OperationFailed``.
    """
    Reason: str = ""

    _ice_id = "::Ellisys::Platform::NetworkRemoteControl::Analyzer::OperationFailed"

_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t = IcePy.defineException(
    "::Ellisys::Platform::NetworkRemoteControl::Analyzer::OperationFailed",
    OperationFailed,
    (),
    None,
    (("Reason", (), IcePy._t_string, False, 0),))

setattr(OperationFailed, '_ice_type', _Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t)

__all__ = ["OperationFailed", "_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t"]
