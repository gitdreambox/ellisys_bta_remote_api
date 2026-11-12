# Copyright (c) ZeroC, Inc.

# slice2py version 3.8.2

from __future__ import annotations
import IcePy

from Ellisys.Platform.NetworkRemoteControl.Analyzer.AddMarker import _Ellisys_Platform_NetworkRemoteControl_Analyzer_AddMarker_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.AnalyzerRemoteControl import AnalyzerRemoteControl
from Ellisys.Platform.NetworkRemoteControl.Analyzer.AnalyzerRemoteControl import AnalyzerRemoteControlPrx

from Ellisys.Platform.NetworkRemoteControl.Analyzer.AppInfo import _Ellisys_Platform_NetworkRemoteControl_Analyzer_AppInfo_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.ByteArray import _Ellisys_Platform_NetworkRemoteControl_Analyzer_ByteArray_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.ByteArrays import _Ellisys_Platform_NetworkRemoteControl_Analyzer_ByteArrays_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.ExportOptionArray import _Ellisys_Platform_NetworkRemoteControl_Analyzer_ExportOptionArray_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.GetMarkerArray import _Ellisys_Platform_NetworkRemoteControl_Analyzer_GetMarkerArray_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.HandleArray import _Ellisys_Platform_NetworkRemoteControl_Analyzer_HandleArray_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.LogicSignalTransitionType import _Ellisys_Platform_NetworkRemoteControl_Analyzer_LogicSignalTransitionType_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.MessageSeverity import _Ellisys_Platform_NetworkRemoteControl_Analyzer_MessageSeverity_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.OperationFailed import _Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.RecordingStatus import _Ellisys_Platform_NetworkRemoteControl_Analyzer_RecordingStatus_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.RunningTaskArray import _Ellisys_Platform_NetworkRemoteControl_Analyzer_RunningTaskArray_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.StringArray import _Ellisys_Platform_NetworkRemoteControl_Analyzer_StringArray_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.TimeArray import _Ellisys_Platform_NetworkRemoteControl_Analyzer_TimeArray_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.TraceFileInfo import _Ellisys_Platform_NetworkRemoteControl_Analyzer_TraceFileInfo_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.Usb30AnalyzerRemoteControl_forward import _Ellisys_Platform_NetworkRemoteControl_Analyzer_Usb30AnalyzerRemoteControlPrx_t

from Ice.ObjectPrx import checkedCast
from Ice.ObjectPrx import checkedCastAsync
from Ice.ObjectPrx import uncheckedCast

from Ice.OperationMode import OperationMode

from abc import ABC
from abc import abstractmethod

from typing import TYPE_CHECKING
from typing import overload

if TYPE_CHECKING:
    from Ellisys.Platform.NetworkRemoteControl.Analyzer.AddMarker import AddMarker
    from Ellisys.Platform.NetworkRemoteControl.Analyzer.AppInfo import AppInfo
    from Ellisys.Platform.NetworkRemoteControl.Analyzer.ExportOption import ExportOption
    from Ellisys.Platform.NetworkRemoteControl.Analyzer.GetMarker import GetMarker
    from Ellisys.Platform.NetworkRemoteControl.Analyzer.LogicSignalTransitionType import LogicSignalTransitionType
    from Ellisys.Platform.NetworkRemoteControl.Analyzer.MessageSeverity import MessageSeverity
    from Ellisys.Platform.NetworkRemoteControl.Analyzer.RecordingStatus import RecordingStatus
    from Ellisys.Platform.NetworkRemoteControl.Analyzer.RunningTask import RunningTask
    from Ellisys.Platform.NetworkRemoteControl.Analyzer.TraceFileInfo import TraceFileInfo
    from Ice.Current import Current
    from Ice.ObjectPrx import ObjectPrx
    from collections.abc import Awaitable
    from collections.abc import Buffer
    from collections.abc import Sequence


class Usb30AnalyzerRemoteControlPrx(AnalyzerRemoteControlPrx):
    """
    USB 3.0-specific capture remote-control operations.
    
    Notes
    -----
        The Slice compiler generated this proxy class from Slice interface ``::Ellisys::Platform::NetworkRemoteControl::Analyzer::Usb30AnalyzerRemoteControl``.
    """

    def ConnectLink(self, disconnectSuperSpeed: bool, context: dict[str, str] | None = None) -> None:
        """
        Connects the analyzer's USB link to the device under test.
        
        Parameters
        ----------
        disconnectSuperSpeed : bool
            if true, the SuperSpeed (USB 3.0) link is left disconnected, keeping
            only the USB 2.0 link connected.
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return Usb30AnalyzerRemoteControl._op_ConnectLink.invoke(self, ((disconnectSuperSpeed, ), context))

    def ConnectLinkAsync(self, disconnectSuperSpeed: bool, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Connects the analyzer's USB link to the device under test.
        
        Parameters
        ----------
        disconnectSuperSpeed : bool
            if true, the SuperSpeed (USB 3.0) link is left disconnected, keeping
            only the USB 2.0 link connected.
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return Usb30AnalyzerRemoteControl._op_ConnectLink.invokeAsync(self, ((disconnectSuperSpeed, ), context))

    def DisconnectLink(self, context: dict[str, str] | None = None) -> None:
        """
        Disconnects the analyzer's USB link from the device under test.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return Usb30AnalyzerRemoteControl._op_DisconnectLink.invoke(self, ((), context))

    def DisconnectLinkAsync(self, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Disconnects the analyzer's USB link from the device under test.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return Usb30AnalyzerRemoteControl._op_DisconnectLink.invokeAsync(self, ((), context))

    def SaveUsb20Packets(self, filename: str, context: dict[str, str] | None = None) -> None:
        """
        Saves the captured USB 2.0 packets to the specified file.
        
        Parameters
        ----------
        filename : str
            path to the file to be saved, based on the remote computer.
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return Usb30AnalyzerRemoteControl._op_SaveUsb20Packets.invoke(self, ((filename, ), context))

    def SaveUsb20PacketsAsync(self, filename: str, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Saves the captured USB 2.0 packets to the specified file.
        
        Parameters
        ----------
        filename : str
            path to the file to be saved, based on the remote computer.
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return Usb30AnalyzerRemoteControl._op_SaveUsb20Packets.invokeAsync(self, ((filename, ), context))

    def SaveUsb30Symbols(self, filename: str, upstreamSymbols: bool, context: dict[str, str] | None = None) -> None:
        """
        Saves the captured USB 3.0 symbols to the specified file.
        
        Parameters
        ----------
        filename : str
            path to the file to be saved, based on the remote computer.
        upstreamSymbols : bool
            if true, saves the upstream symbols; otherwise saves the downstream
            symbols.
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return Usb30AnalyzerRemoteControl._op_SaveUsb30Symbols.invoke(self, ((filename, upstreamSymbols), context))

    def SaveUsb30SymbolsAsync(self, filename: str, upstreamSymbols: bool, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Saves the captured USB 3.0 symbols to the specified file.
        
        Parameters
        ----------
        filename : str
            path to the file to be saved, based on the remote computer.
        upstreamSymbols : bool
            if true, saves the upstream symbols; otherwise saves the downstream
            symbols.
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return Usb30AnalyzerRemoteControl._op_SaveUsb30Symbols.invokeAsync(self, ((filename, upstreamSymbols), context))

    @staticmethod
    def checkedCast(
        proxy: ObjectPrx | None,
        facet: str | None = None,
        context: dict[str, str] | None = None
    ) -> Usb30AnalyzerRemoteControlPrx | None:
        return checkedCast(Usb30AnalyzerRemoteControlPrx, proxy, facet, context)

    @staticmethod
    def checkedCastAsync(
        proxy: ObjectPrx | None,
        facet: str | None = None,
        context: dict[str, str] | None = None
    ) -> Awaitable[Usb30AnalyzerRemoteControlPrx | None ]:
        return checkedCastAsync(Usb30AnalyzerRemoteControlPrx, proxy, facet, context)

    @overload
    @staticmethod
    def uncheckedCast(proxy: ObjectPrx, facet: str | None = None) -> Usb30AnalyzerRemoteControlPrx:
        ...

    @overload
    @staticmethod
    def uncheckedCast(proxy: None, facet: str | None = None) -> None:
        ...

    @staticmethod
    def uncheckedCast(proxy: ObjectPrx | None, facet: str | None = None) -> Usb30AnalyzerRemoteControlPrx | None:
        return uncheckedCast(Usb30AnalyzerRemoteControlPrx, proxy, facet)

    @staticmethod
    def ice_staticId() -> str:
        return "::Ellisys::Platform::NetworkRemoteControl::Analyzer::Usb30AnalyzerRemoteControl"

IcePy.defineProxy("::Ellisys::Platform::NetworkRemoteControl::Analyzer::Usb30AnalyzerRemoteControl", Usb30AnalyzerRemoteControlPrx)

class Usb30AnalyzerRemoteControl(AnalyzerRemoteControl, ABC):
    """
    USB 3.0-specific capture remote-control operations.
    
    Notes
    -----
        The Slice compiler generated this skeleton class from Slice interface ``::Ellisys::Platform::NetworkRemoteControl::Analyzer::Usb30AnalyzerRemoteControl``.
    """

    _ice_ids: Sequence[str] = ("::Ellisys::Platform::NetworkRemoteControl::Analyzer::AnalyzerRemoteControl", "::Ellisys::Platform::NetworkRemoteControl::Analyzer::Usb30AnalyzerRemoteControl", "::Ice::Object", )
    _op_ConnectLink: IcePy.Operation
    _op_DisconnectLink: IcePy.Operation
    _op_SaveUsb20Packets: IcePy.Operation
    _op_SaveUsb30Symbols: IcePy.Operation

    @staticmethod
    def ice_staticId() -> str:
        return "::Ellisys::Platform::NetworkRemoteControl::Analyzer::Usb30AnalyzerRemoteControl"

    @abstractmethod
    def ConnectLink(self, disconnectSuperSpeed: bool, current: Current) -> None | Awaitable[None]:
        """
        Connects the analyzer's USB link to the device under test.
        
        Parameters
        ----------
        disconnectSuperSpeed : bool
            if true, the SuperSpeed (USB 3.0) link is left disconnected, keeping
            only the USB 2.0 link connected.
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        None | Awaitable[None]
            None or an awaitable that completes when the dispatch completes.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def DisconnectLink(self, current: Current) -> None | Awaitable[None]:
        """
        Disconnects the analyzer's USB link from the device under test.
        
        Parameters
        ----------
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        None | Awaitable[None]
            None or an awaitable that completes when the dispatch completes.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def SaveUsb20Packets(self, filename: str, current: Current) -> None | Awaitable[None]:
        """
        Saves the captured USB 2.0 packets to the specified file.
        
        Parameters
        ----------
        filename : str
            path to the file to be saved, based on the remote computer.
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        None | Awaitable[None]
            None or an awaitable that completes when the dispatch completes.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def SaveUsb30Symbols(self, filename: str, upstreamSymbols: bool, current: Current) -> None | Awaitable[None]:
        """
        Saves the captured USB 3.0 symbols to the specified file.
        
        Parameters
        ----------
        filename : str
            path to the file to be saved, based on the remote computer.
        upstreamSymbols : bool
            if true, saves the upstream symbols; otherwise saves the downstream
            symbols.
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        None | Awaitable[None]
            None or an awaitable that completes when the dispatch completes.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

Usb30AnalyzerRemoteControl._op_ConnectLink = IcePy.Operation(
    "ConnectLink",
    "ConnectLink",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_bool, False, 0),),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

Usb30AnalyzerRemoteControl._op_DisconnectLink = IcePy.Operation(
    "DisconnectLink",
    "DisconnectLink",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

Usb30AnalyzerRemoteControl._op_SaveUsb20Packets = IcePy.Operation(
    "SaveUsb20Packets",
    "SaveUsb20Packets",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_string, False, 0),),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

Usb30AnalyzerRemoteControl._op_SaveUsb30Symbols = IcePy.Operation(
    "SaveUsb30Symbols",
    "SaveUsb30Symbols",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_string, False, 0), ((), IcePy._t_bool, False, 0)),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

__all__ = ["Usb30AnalyzerRemoteControl", "Usb30AnalyzerRemoteControlPrx", "_Ellisys_Platform_NetworkRemoteControl_Analyzer_Usb30AnalyzerRemoteControlPrx_t"]
