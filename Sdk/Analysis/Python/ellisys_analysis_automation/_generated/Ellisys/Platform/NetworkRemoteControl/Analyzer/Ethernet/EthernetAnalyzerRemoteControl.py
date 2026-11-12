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

from Ellisys.Platform.NetworkRemoteControl.Analyzer.Ethernet.DeviceAddressArray import _Ellisys_Platform_NetworkRemoteControl_Analyzer_Ethernet_DeviceAddressArray_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.Ethernet.DeviceFilterMode import _Ellisys_Platform_NetworkRemoteControl_Analyzer_Ethernet_DeviceFilterMode_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.Ethernet.EthernetAnalyzerRemoteControl_forward import _Ellisys_Platform_NetworkRemoteControl_Analyzer_Ethernet_EthernetAnalyzerRemoteControlPrx_t

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
    from Ellisys.Platform.NetworkRemoteControl.Analyzer.Ethernet.DeviceFilterMode import DeviceFilterMode
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


class EthernetAnalyzerRemoteControlPrx(AnalyzerRemoteControlPrx):
    """
    Wi-Fi capture remote-control operations, available on analyzers that capture Wi-Fi.
    
    Notes
    -----
        The Slice compiler generated this proxy class from Slice interface ``::Ellisys::Platform::NetworkRemoteControl::Analyzer::Ethernet::EthernetAnalyzerRemoteControl``.
    """

    def AddWifiKeyByApSsid(self, apSsid: str, key: str, context: dict[str, str] | None = None) -> None:
        """
        Adds a Wi-Fi key for the access point identified by its SSID, so that traffic encrypted for that
        network can be decrypted.
        
        Parameters
        ----------
        apSsid : str
            SSID (network name) of the access point.
        key : str
            the Wi-Fi key (passphrase or hexadecimal key) for that network.
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return EthernetAnalyzerRemoteControl._op_AddWifiKeyByApSsid.invoke(self, ((apSsid, key), context))

    def AddWifiKeyByApSsidAsync(self, apSsid: str, key: str, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Adds a Wi-Fi key for the access point identified by its SSID, so that traffic encrypted for that
        network can be decrypted.
        
        Parameters
        ----------
        apSsid : str
            SSID (network name) of the access point.
        key : str
            the Wi-Fi key (passphrase or hexadecimal key) for that network.
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return EthernetAnalyzerRemoteControl._op_AddWifiKeyByApSsid.invokeAsync(self, ((apSsid, key), context))

    def AddWifiKeyByApMacAddr(self, apMacAddr: int, key: str, context: dict[str, str] | None = None) -> None:
        """
        Adds a Wi-Fi key for the access point identified by its MAC address (BSSID), so that traffic
        encrypted for that network can be decrypted.
        
        Parameters
        ----------
        apMacAddr : int
            MAC address (BSSID) of the access point.
        key : str
            the Wi-Fi key (passphrase or hexadecimal key) for that network.
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return EthernetAnalyzerRemoteControl._op_AddWifiKeyByApMacAddr.invoke(self, ((apMacAddr, key), context))

    def AddWifiKeyByApMacAddrAsync(self, apMacAddr: int, key: str, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Adds a Wi-Fi key for the access point identified by its MAC address (BSSID), so that traffic
        encrypted for that network can be decrypted.
        
        Parameters
        ----------
        apMacAddr : int
            MAC address (BSSID) of the access point.
        key : str
            the Wi-Fi key (passphrase or hexadecimal key) for that network.
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return EthernetAnalyzerRemoteControl._op_AddWifiKeyByApMacAddr.invokeAsync(self, ((apMacAddr, key), context))

    def ConfigureDeviceFilter(self, mode: DeviceFilterMode, deviceAddrs: Sequence[int] | Buffer, context: dict[str, str] | None = None) -> None:
        """
        This method sets the device filter. It is equivalent to specifying a device filter from the GUI.
        
        Parameters
        ----------
        mode : DeviceFilterMode
            specifies if the filter is keep all, exclude background, keep only or keep involving
        deviceAddrs : Sequence[int] | Buffer
            list of devices to keep. No device shall be specified in case of keep all and
            exclude background.
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return EthernetAnalyzerRemoteControl._op_ConfigureDeviceFilter.invoke(self, ((mode, deviceAddrs), context))

    def ConfigureDeviceFilterAsync(self, mode: DeviceFilterMode, deviceAddrs: Sequence[int] | Buffer, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        This method sets the device filter. It is equivalent to specifying a device filter from the GUI.
        
        Parameters
        ----------
        mode : DeviceFilterMode
            specifies if the filter is keep all, exclude background, keep only or keep involving
        deviceAddrs : Sequence[int] | Buffer
            list of devices to keep. No device shall be specified in case of keep all and
            exclude background.
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return EthernetAnalyzerRemoteControl._op_ConfigureDeviceFilter.invokeAsync(self, ((mode, deviceAddrs), context))

    @staticmethod
    def checkedCast(
        proxy: ObjectPrx | None,
        facet: str | None = None,
        context: dict[str, str] | None = None
    ) -> EthernetAnalyzerRemoteControlPrx | None:
        return checkedCast(EthernetAnalyzerRemoteControlPrx, proxy, facet, context)

    @staticmethod
    def checkedCastAsync(
        proxy: ObjectPrx | None,
        facet: str | None = None,
        context: dict[str, str] | None = None
    ) -> Awaitable[EthernetAnalyzerRemoteControlPrx | None ]:
        return checkedCastAsync(EthernetAnalyzerRemoteControlPrx, proxy, facet, context)

    @overload
    @staticmethod
    def uncheckedCast(proxy: ObjectPrx, facet: str | None = None) -> EthernetAnalyzerRemoteControlPrx:
        ...

    @overload
    @staticmethod
    def uncheckedCast(proxy: None, facet: str | None = None) -> None:
        ...

    @staticmethod
    def uncheckedCast(proxy: ObjectPrx | None, facet: str | None = None) -> EthernetAnalyzerRemoteControlPrx | None:
        return uncheckedCast(EthernetAnalyzerRemoteControlPrx, proxy, facet)

    @staticmethod
    def ice_staticId() -> str:
        return "::Ellisys::Platform::NetworkRemoteControl::Analyzer::Ethernet::EthernetAnalyzerRemoteControl"

IcePy.defineProxy("::Ellisys::Platform::NetworkRemoteControl::Analyzer::Ethernet::EthernetAnalyzerRemoteControl", EthernetAnalyzerRemoteControlPrx)

class EthernetAnalyzerRemoteControl(AnalyzerRemoteControl, ABC):
    """
    Wi-Fi capture remote-control operations, available on analyzers that capture Wi-Fi.
    
    Notes
    -----
        The Slice compiler generated this skeleton class from Slice interface ``::Ellisys::Platform::NetworkRemoteControl::Analyzer::Ethernet::EthernetAnalyzerRemoteControl``.
    """

    _ice_ids: Sequence[str] = ("::Ellisys::Platform::NetworkRemoteControl::Analyzer::AnalyzerRemoteControl", "::Ellisys::Platform::NetworkRemoteControl::Analyzer::Ethernet::EthernetAnalyzerRemoteControl", "::Ice::Object", )
    _op_AddWifiKeyByApSsid: IcePy.Operation
    _op_AddWifiKeyByApMacAddr: IcePy.Operation
    _op_ConfigureDeviceFilter: IcePy.Operation

    @staticmethod
    def ice_staticId() -> str:
        return "::Ellisys::Platform::NetworkRemoteControl::Analyzer::Ethernet::EthernetAnalyzerRemoteControl"

    @abstractmethod
    def AddWifiKeyByApSsid(self, apSsid: str, key: str, current: Current) -> None | Awaitable[None]:
        """
        Adds a Wi-Fi key for the access point identified by its SSID, so that traffic encrypted for that
        network can be decrypted.
        
        Parameters
        ----------
        apSsid : str
            SSID (network name) of the access point.
        key : str
            the Wi-Fi key (passphrase or hexadecimal key) for that network.
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
    def AddWifiKeyByApMacAddr(self, apMacAddr: int, key: str, current: Current) -> None | Awaitable[None]:
        """
        Adds a Wi-Fi key for the access point identified by its MAC address (BSSID), so that traffic
        encrypted for that network can be decrypted.
        
        Parameters
        ----------
        apMacAddr : int
            MAC address (BSSID) of the access point.
        key : str
            the Wi-Fi key (passphrase or hexadecimal key) for that network.
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
    def ConfigureDeviceFilter(self, mode: DeviceFilterMode, deviceAddrs: list[int], current: Current) -> None | Awaitable[None]:
        """
        This method sets the device filter. It is equivalent to specifying a device filter from the GUI.
        
        Parameters
        ----------
        mode : DeviceFilterMode
            specifies if the filter is keep all, exclude background, keep only or keep involving
        deviceAddrs : list[int]
            list of devices to keep. No device shall be specified in case of keep all and
            exclude background.
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

EthernetAnalyzerRemoteControl._op_AddWifiKeyByApSsid = IcePy.Operation(
    "AddWifiKeyByApSsid",
    "AddWifiKeyByApSsid",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_string, False, 0), ((), IcePy._t_string, False, 0)),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

EthernetAnalyzerRemoteControl._op_AddWifiKeyByApMacAddr = IcePy.Operation(
    "AddWifiKeyByApMacAddr",
    "AddWifiKeyByApMacAddr",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_long, False, 0), ((), IcePy._t_string, False, 0)),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

EthernetAnalyzerRemoteControl._op_ConfigureDeviceFilter = IcePy.Operation(
    "ConfigureDeviceFilter",
    "ConfigureDeviceFilter",
    OperationMode.Normal,
    None,
    (),
    (((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_Ethernet_DeviceFilterMode_t, False, 0), ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_Ethernet_DeviceAddressArray_t, False, 0)),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

__all__ = ["EthernetAnalyzerRemoteControl", "EthernetAnalyzerRemoteControlPrx", "_Ellisys_Platform_NetworkRemoteControl_Analyzer_Ethernet_EthernetAnalyzerRemoteControlPrx_t"]
