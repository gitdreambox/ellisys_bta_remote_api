# Copyright (c) ZeroC, Inc.

# slice2py version 3.8.2

from __future__ import annotations
import IcePy

from Ellisys.Platform.NetworkRemoteControl.Generator.OperationFailed import OperationFailed
from Ellisys.Platform.NetworkRemoteControl.Generator.OperationFailed import _Ellisys_Platform_NetworkRemoteControl_Generator_OperationFailed_t

from dataclasses import dataclass


@dataclass
class GeneratorNotFound(OperationFailed):
    """
    Notes
    -----
        The Slice compiler generated this exception dataclass from Slice exception ``::Ellisys::Platform::NetworkRemoteControl::Generator::GeneratorNotFound``.
    """

    _ice_id = "::Ellisys::Platform::NetworkRemoteControl::Generator::GeneratorNotFound"

_Ellisys_Platform_NetworkRemoteControl_Generator_GeneratorNotFound_t = IcePy.defineException(
    "::Ellisys::Platform::NetworkRemoteControl::Generator::GeneratorNotFound",
    GeneratorNotFound,
    (),
    _Ellisys_Platform_NetworkRemoteControl_Generator_OperationFailed_t,
    ())

setattr(GeneratorNotFound, '_ice_type', _Ellisys_Platform_NetworkRemoteControl_Generator_GeneratorNotFound_t)

__all__ = ["GeneratorNotFound", "_Ellisys_Platform_NetworkRemoteControl_Generator_GeneratorNotFound_t"]
