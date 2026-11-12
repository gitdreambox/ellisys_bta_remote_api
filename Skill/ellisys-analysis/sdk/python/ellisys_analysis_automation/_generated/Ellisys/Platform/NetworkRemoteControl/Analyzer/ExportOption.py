# Copyright (c) ZeroC, Inc.

# slice2py version 3.8.2

from __future__ import annotations
import IcePy

from dataclasses import dataclass


@dataclass(order=True, unsafe_hash=True)
class ExportOption:
    """
    Notes
    -----
        The Slice compiler generated this dataclass from Slice struct ``::Ellisys::Platform::NetworkRemoteControl::Analyzer::ExportOption``.
    """
    OptionName: str = ""
    OptionValue: str = ""

_Ellisys_Platform_NetworkRemoteControl_Analyzer_ExportOption_t = IcePy.defineStruct(
    "::Ellisys::Platform::NetworkRemoteControl::Analyzer::ExportOption",
    ExportOption,
    (),
    (
        ("OptionName", (), IcePy._t_string),
        ("OptionValue", (), IcePy._t_string)
    ))

__all__ = ["ExportOption", "_Ellisys_Platform_NetworkRemoteControl_Analyzer_ExportOption_t"]
