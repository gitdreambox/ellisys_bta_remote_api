# Copyright (c) ZeroC, Inc.

# slice2py version 3.8.2

from __future__ import annotations
import IcePy

from Ellisys.Platform.NetworkRemoteControl.Generator.OperationFailed import OperationFailed
from Ellisys.Platform.NetworkRemoteControl.Generator.OperationFailed import _Ellisys_Platform_NetworkRemoteControl_Generator_OperationFailed_t

from dataclasses import dataclass


@dataclass
class AlreadyRunning(OperationFailed):
    """
    Notes
    -----
        The Slice compiler generated this exception dataclass from Slice exception ``::Ellisys::Platform::NetworkRemoteControl::Generator::AlreadyRunning``.
    """

    _ice_id = "::Ellisys::Platform::NetworkRemoteControl::Generator::AlreadyRunning"

_Ellisys_Platform_NetworkRemoteControl_Generator_AlreadyRunning_t = IcePy.defineException(
    "::Ellisys::Platform::NetworkRemoteControl::Generator::AlreadyRunning",
    AlreadyRunning,
    (),
    _Ellisys_Platform_NetworkRemoteControl_Generator_OperationFailed_t,
    ())

setattr(AlreadyRunning, '_ice_type', _Ellisys_Platform_NetworkRemoteControl_Generator_AlreadyRunning_t)

__all__ = ["AlreadyRunning", "_Ellisys_Platform_NetworkRemoteControl_Generator_AlreadyRunning_t"]
