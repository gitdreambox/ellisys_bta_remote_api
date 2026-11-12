# Copyright (c) ZeroC, Inc.

# slice2py version 3.8.2

from __future__ import annotations
import IcePy

from Ellisys.Platform.NetworkRemoteControl.Generator.OperationFailed import OperationFailed
from Ellisys.Platform.NetworkRemoteControl.Generator.OperationFailed import _Ellisys_Platform_NetworkRemoteControl_Generator_OperationFailed_t

from dataclasses import dataclass


@dataclass
class AlreadyStopped(OperationFailed):
    """
    Notes
    -----
        The Slice compiler generated this exception dataclass from Slice exception ``::Ellisys::Platform::NetworkRemoteControl::Generator::AlreadyStopped``.
    """

    _ice_id = "::Ellisys::Platform::NetworkRemoteControl::Generator::AlreadyStopped"

_Ellisys_Platform_NetworkRemoteControl_Generator_AlreadyStopped_t = IcePy.defineException(
    "::Ellisys::Platform::NetworkRemoteControl::Generator::AlreadyStopped",
    AlreadyStopped,
    (),
    _Ellisys_Platform_NetworkRemoteControl_Generator_OperationFailed_t,
    ())

setattr(AlreadyStopped, '_ice_type', _Ellisys_Platform_NetworkRemoteControl_Generator_AlreadyStopped_t)

__all__ = ["AlreadyStopped", "_Ellisys_Platform_NetworkRemoteControl_Generator_AlreadyStopped_t"]
