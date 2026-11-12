# Copyright (c) ZeroC, Inc.

# slice2py version 3.8.2

from __future__ import annotations
import IcePy

from Ellisys.Platform.NetworkRemoteControl.Analyzer.MarkerColor import MarkerColor
from Ellisys.Platform.NetworkRemoteControl.Analyzer.MarkerColor import _Ellisys_Platform_NetworkRemoteControl_Analyzer_MarkerColor_t

from dataclasses import dataclass


@dataclass(order=True, unsafe_hash=True)
class GetMarker:
    """
    Notes
    -----
        The Slice compiler generated this dataclass from Slice struct ``::Ellisys::Platform::NetworkRemoteControl::Analyzer::GetMarker``.
    """
    Color: MarkerColor = MarkerColor.Yellow
    Text: str = ""
    Time: int = 0

_Ellisys_Platform_NetworkRemoteControl_Analyzer_GetMarker_t = IcePy.defineStruct(
    "::Ellisys::Platform::NetworkRemoteControl::Analyzer::GetMarker",
    GetMarker,
    (),
    (
        ("Color", (), _Ellisys_Platform_NetworkRemoteControl_Analyzer_MarkerColor_t),
        ("Text", (), IcePy._t_string),
        ("Time", (), IcePy._t_long)
    ))

__all__ = ["GetMarker", "_Ellisys_Platform_NetworkRemoteControl_Analyzer_GetMarker_t"]
