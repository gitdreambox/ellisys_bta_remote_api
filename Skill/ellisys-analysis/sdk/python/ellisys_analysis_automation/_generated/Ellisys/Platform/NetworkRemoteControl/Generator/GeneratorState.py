# Copyright (c) ZeroC, Inc.

# slice2py version 3.8.2

from __future__ import annotations
import IcePy

from enum import Enum

class GeneratorState(Enum):
    """
    Notes
    -----
        The Slice compiler generated this enum class from Slice enumeration ``::Ellisys::Platform::NetworkRemoteControl::Generator::GeneratorState``.
    """

    Stopped = 0

    Running = 1

    Pausing = 2

    Paused = 3

_Ellisys_Platform_NetworkRemoteControl_Generator_GeneratorState_t = IcePy.defineEnum(
    "::Ellisys::Platform::NetworkRemoteControl::Generator::GeneratorState",
    GeneratorState,
    (),
    {
        0: GeneratorState.Stopped,
        1: GeneratorState.Running,
        2: GeneratorState.Pausing,
        3: GeneratorState.Paused,
    }
)

__all__ = ["GeneratorState", "_Ellisys_Platform_NetworkRemoteControl_Generator_GeneratorState_t"]
