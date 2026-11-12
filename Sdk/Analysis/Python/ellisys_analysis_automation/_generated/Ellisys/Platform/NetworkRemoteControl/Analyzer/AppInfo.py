# Copyright (c) ZeroC, Inc.

# slice2py version 3.8.2

from __future__ import annotations
import IcePy

from dataclasses import dataclass


@dataclass(order=True, unsafe_hash=True)
class AppInfo:
    """
    Notes
    -----
        The Slice compiler generated this dataclass from Slice struct ``::Ellisys::Platform::NetworkRemoteControl::Analyzer::AppInfo``.
    """
    Id: str = ""
    Description: str = ""
    Version: str = ""
    FileExt: str = ""
    Interactive: bool = False

_Ellisys_Platform_NetworkRemoteControl_Analyzer_AppInfo_t = IcePy.defineStruct(
    "::Ellisys::Platform::NetworkRemoteControl::Analyzer::AppInfo",
    AppInfo,
    (),
    (
        ("Id", (), IcePy._t_string),
        ("Description", (), IcePy._t_string),
        ("Version", (), IcePy._t_string),
        ("FileExt", (), IcePy._t_string),
        ("Interactive", (), IcePy._t_bool)
    ))

__all__ = ["AppInfo", "_Ellisys_Platform_NetworkRemoteControl_Analyzer_AppInfo_t"]
