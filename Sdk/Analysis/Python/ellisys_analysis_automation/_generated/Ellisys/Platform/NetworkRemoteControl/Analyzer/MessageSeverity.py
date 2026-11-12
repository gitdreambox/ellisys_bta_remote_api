# Copyright (c) ZeroC, Inc.

# slice2py version 3.8.2

from __future__ import annotations
import IcePy

from enum import Enum

class MessageSeverity(Enum):
    """
    Notes
    -----
        The Slice compiler generated this enum class from Slice enumeration ``::Ellisys::Platform::NetworkRemoteControl::Analyzer::MessageSeverity``.
    """

    Info = 1

    Warning = 2

    Error = 3

_Ellisys_Platform_NetworkRemoteControl_Analyzer_MessageSeverity_t = IcePy.defineEnum(
    "::Ellisys::Platform::NetworkRemoteControl::Analyzer::MessageSeverity",
    MessageSeverity,
    (),
    {
        1: MessageSeverity.Info,
        2: MessageSeverity.Warning,
        3: MessageSeverity.Error,
    }
)

__all__ = ["MessageSeverity", "_Ellisys_Platform_NetworkRemoteControl_Analyzer_MessageSeverity_t"]
