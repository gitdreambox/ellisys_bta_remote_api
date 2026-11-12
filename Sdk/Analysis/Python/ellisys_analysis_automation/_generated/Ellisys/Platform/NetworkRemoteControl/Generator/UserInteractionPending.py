# Copyright (c) ZeroC, Inc.

# slice2py version 3.8.2

from __future__ import annotations
import IcePy

from Ellisys.Platform.NetworkRemoteControl.Generator.OperationFailed import OperationFailed
from Ellisys.Platform.NetworkRemoteControl.Generator.OperationFailed import _Ellisys_Platform_NetworkRemoteControl_Generator_OperationFailed_t

from dataclasses import dataclass


@dataclass
class UserInteractionPending(OperationFailed):
    """
    Notes
    -----
        The Slice compiler generated this exception dataclass from Slice exception ``::Ellisys::Platform::NetworkRemoteControl::Generator::UserInteractionPending``.
    """

    _ice_id = "::Ellisys::Platform::NetworkRemoteControl::Generator::UserInteractionPending"

_Ellisys_Platform_NetworkRemoteControl_Generator_UserInteractionPending_t = IcePy.defineException(
    "::Ellisys::Platform::NetworkRemoteControl::Generator::UserInteractionPending",
    UserInteractionPending,
    (),
    _Ellisys_Platform_NetworkRemoteControl_Generator_OperationFailed_t,
    ())

setattr(UserInteractionPending, '_ice_type', _Ellisys_Platform_NetworkRemoteControl_Generator_UserInteractionPending_t)

__all__ = ["UserInteractionPending", "_Ellisys_Platform_NetworkRemoteControl_Generator_UserInteractionPending_t"]
