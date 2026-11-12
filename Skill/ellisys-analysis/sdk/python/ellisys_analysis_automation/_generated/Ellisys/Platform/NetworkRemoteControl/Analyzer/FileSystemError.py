# Copyright (c) ZeroC, Inc.

# slice2py version 3.8.2

from __future__ import annotations
import IcePy

from Ellisys.Platform.NetworkRemoteControl.Analyzer.OperationFailed import OperationFailed
from Ellisys.Platform.NetworkRemoteControl.Analyzer.OperationFailed import _Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t

from dataclasses import dataclass


@dataclass
class FileSystemError(OperationFailed):
    """
    Notes
    -----
        The Slice compiler generated this exception dataclass from Slice exception ``::Ellisys::Platform::NetworkRemoteControl::Analyzer::FileSystemError``.
    """

    _ice_id = "::Ellisys::Platform::NetworkRemoteControl::Analyzer::FileSystemError"

_Ellisys_Platform_NetworkRemoteControl_Analyzer_FileSystemError_t = IcePy.defineException(
    "::Ellisys::Platform::NetworkRemoteControl::Analyzer::FileSystemError",
    FileSystemError,
    (),
    _Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,
    ())

setattr(FileSystemError, '_ice_type', _Ellisys_Platform_NetworkRemoteControl_Analyzer_FileSystemError_t)

__all__ = ["FileSystemError", "_Ellisys_Platform_NetworkRemoteControl_Analyzer_FileSystemError_t"]
