# Copyright (c) ZeroC, Inc.

# slice2py version 3.8.2

from __future__ import annotations
import IcePy

from dataclasses import dataclass


@dataclass(order=True, unsafe_hash=True)
class ChannelSummary:
    """
    Notes
    -----
        The Slice compiler generated this dataclass from Slice struct ``::Ellisys::Platform::NetworkRemoteControl::Analyzer::ChannelSummary``.
    """
    Ok: int = 0
    Retransmitted: int = 0
    PayloadError: int = 0
    HeaderError: int = 0
    NotApplicable: int = 0

_Ellisys_Platform_NetworkRemoteControl_Analyzer_ChannelSummary_t = IcePy.defineStruct(
    "::Ellisys::Platform::NetworkRemoteControl::Analyzer::ChannelSummary",
    ChannelSummary,
    (),
    (
        ("Ok", (), IcePy._t_long),
        ("Retransmitted", (), IcePy._t_long),
        ("PayloadError", (), IcePy._t_long),
        ("HeaderError", (), IcePy._t_long),
        ("NotApplicable", (), IcePy._t_long)
    ))

__all__ = ["ChannelSummary", "_Ellisys_Platform_NetworkRemoteControl_Analyzer_ChannelSummary_t"]
