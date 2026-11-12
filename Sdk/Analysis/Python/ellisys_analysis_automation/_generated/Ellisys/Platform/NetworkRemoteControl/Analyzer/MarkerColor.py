# Copyright (c) ZeroC, Inc.

# slice2py version 3.8.2

from __future__ import annotations
import IcePy

from enum import Enum

class MarkerColor(Enum):
    """
    Notes
    -----
        The Slice compiler generated this enum class from Slice enumeration ``::Ellisys::Platform::NetworkRemoteControl::Analyzer::MarkerColor``.
    """

    Yellow = 0

    Blue = 1

    Red = 2

    Green = 3

    Orange = 4

    Purple = 5

_Ellisys_Platform_NetworkRemoteControl_Analyzer_MarkerColor_t = IcePy.defineEnum(
    "::Ellisys::Platform::NetworkRemoteControl::Analyzer::MarkerColor",
    MarkerColor,
    (),
    {
        0: MarkerColor.Yellow,
        1: MarkerColor.Blue,
        2: MarkerColor.Red,
        3: MarkerColor.Green,
        4: MarkerColor.Orange,
        5: MarkerColor.Purple,
    }
)

__all__ = ["MarkerColor", "_Ellisys_Platform_NetworkRemoteControl_Analyzer_MarkerColor_t"]
