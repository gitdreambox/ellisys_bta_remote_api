# Copyright (c) ZeroC, Inc.

# slice2py version 3.8.2

from __future__ import annotations
import IcePy

from enum import Enum

class DeviceFilterMode(Enum):
    """
    Notes
    -----
        The Slice compiler generated this enum class from Slice enumeration ``::Ellisys::Platform::NetworkRemoteControl::Analyzer::Ethernet::DeviceFilterMode``.
    """

    KeepAll = 0

    ExcludeBackground = 1

    KeepOnly = 2

    KeepInvolving = 3

_Ellisys_Platform_NetworkRemoteControl_Analyzer_Ethernet_DeviceFilterMode_t = IcePy.defineEnum(
    "::Ellisys::Platform::NetworkRemoteControl::Analyzer::Ethernet::DeviceFilterMode",
    DeviceFilterMode,
    (),
    {
        0: DeviceFilterMode.KeepAll,
        1: DeviceFilterMode.ExcludeBackground,
        2: DeviceFilterMode.KeepOnly,
        3: DeviceFilterMode.KeepInvolving,
    }
)

__all__ = ["DeviceFilterMode", "_Ellisys_Platform_NetworkRemoteControl_Analyzer_Ethernet_DeviceFilterMode_t"]
