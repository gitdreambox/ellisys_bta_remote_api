# Copyright (c) ZeroC, Inc.

# slice2py version 3.8.2

from __future__ import annotations
import IcePy

from Ellisys.Platform.NetworkRemoteControl.Analyzer.AddMarker import _Ellisys_Platform_NetworkRemoteControl_Analyzer_AddMarker_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.AnalyzerRemoteControl import AnalyzerRemoteControl
from Ellisys.Platform.NetworkRemoteControl.Analyzer.AnalyzerRemoteControl import AnalyzerRemoteControlPrx

from Ellisys.Platform.NetworkRemoteControl.Analyzer.AppInfo import _Ellisys_Platform_NetworkRemoteControl_Analyzer_AppInfo_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.BluetoothAnalyzerRemoteControl_forward import _Ellisys_Platform_NetworkRemoteControl_Analyzer_BluetoothAnalyzerRemoteControlPrx_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.ByteArray import _Ellisys_Platform_NetworkRemoteControl_Analyzer_ByteArray_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.ByteArrays import _Ellisys_Platform_NetworkRemoteControl_Analyzer_ByteArrays_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.ChannelsSummary import _Ellisys_Platform_NetworkRemoteControl_Analyzer_ChannelsSummary_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.DeviceAddressArray import _Ellisys_Platform_NetworkRemoteControl_Analyzer_DeviceAddressArray_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.DeviceFilterMode import _Ellisys_Platform_NetworkRemoteControl_Analyzer_DeviceFilterMode_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.ExportOptionArray import _Ellisys_Platform_NetworkRemoteControl_Analyzer_ExportOptionArray_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.GetMarkerArray import _Ellisys_Platform_NetworkRemoteControl_Analyzer_GetMarkerArray_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.HandleArray import _Ellisys_Platform_NetworkRemoteControl_Analyzer_HandleArray_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.LinkKeyByteArray import _Ellisys_Platform_NetworkRemoteControl_Analyzer_LinkKeyByteArray_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.LogicSignalTransitionType import _Ellisys_Platform_NetworkRemoteControl_Analyzer_LogicSignalTransitionType_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.MessageSeverity import _Ellisys_Platform_NetworkRemoteControl_Analyzer_MessageSeverity_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.OperationFailed import _Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.RecordingStatus import _Ellisys_Platform_NetworkRemoteControl_Analyzer_RecordingStatus_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.RssiArray import _Ellisys_Platform_NetworkRemoteControl_Analyzer_RssiArray_t

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
    from Ellisys.Platform.NetworkRemoteControl.Analyzer.ChannelSummary import ChannelSummary
    from Ellisys.Platform.NetworkRemoteControl.Analyzer.DeviceFilterMode import DeviceFilterMode
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


class BluetoothAnalyzerRemoteControlPrx(AnalyzerRemoteControlPrx):
    """
    Bluetooth-specific remote-control operations, available while capturing Bluetooth.
    
    Notes
    -----
        The Slice compiler generated this proxy class from Slice interface ``::Ellisys::Platform::NetworkRemoteControl::Analyzer::BluetoothAnalyzerRemoteControl``.
    """

    def SplitTraceFileAndContinueRecording(self, filename: str, context: dict[str, str] | None = None) -> None:
        """
        This method will save the ongoing trace to the specific file path and will continue recording.
        It is equivalent to clicking the "Save & Continue" button in the GUI.
        
        Parameters
        ----------
        filename : str
            path to the file to be saved, based on the remote computer
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return BluetoothAnalyzerRemoteControl._op_SplitTraceFileAndContinueRecording.invoke(self, ((filename, ), context))

    def SplitTraceFileAndContinueRecordingAsync(self, filename: str, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        This method will save the ongoing trace to the specific file path and will continue recording.
        It is equivalent to clicking the "Save & Continue" button in the GUI.
        
        Parameters
        ----------
        filename : str
            path to the file to be saved, based on the remote computer
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return BluetoothAnalyzerRemoteControl._op_SplitTraceFileAndContinueRecording.invokeAsync(self, ((filename, ), context))

    def AddLinkKey(self, bdaddr1: int, bdaddr2: int, linkKey: Sequence[int] | bytes | Buffer, context: dict[str, str] | None = None) -> None:
        """
        This method will add the specified link key to the devices database for the specified
        connection. The views will not reload after the call of this function. If a loaded trace is
        affected by this new link key, it shall be reloaded manually.
        
        Parameters
        ----------
        bdaddr1 : int
            BDADDR of the first device
        bdaddr2 : int
            BDADDR of the second device
        linkKey : Sequence[int] | bytes | Buffer
            16 bytes composing the link key
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return BluetoothAnalyzerRemoteControl._op_AddLinkKey.invoke(self, ((bdaddr1, bdaddr2, linkKey), context))

    def AddLinkKeyAsync(self, bdaddr1: int, bdaddr2: int, linkKey: Sequence[int] | bytes | Buffer, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        This method will add the specified link key to the devices database for the specified
        connection. The views will not reload after the call of this function. If a loaded trace is
        affected by this new link key, it shall be reloaded manually.
        
        Parameters
        ----------
        bdaddr1 : int
            BDADDR of the first device
        bdaddr2 : int
            BDADDR of the second device
        linkKey : Sequence[int] | bytes | Buffer
            16 bytes composing the link key
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return BluetoothAnalyzerRemoteControl._op_AddLinkKey.invokeAsync(self, ((bdaddr1, bdaddr2, linkKey), context))

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
        return BluetoothAnalyzerRemoteControl._op_ConfigureDeviceFilter.invoke(self, ((mode, deviceAddrs), context))

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
        return BluetoothAnalyzerRemoteControl._op_ConfigureDeviceFilter.invokeAsync(self, ((mode, deviceAddrs), context))

    def GetSpectrumRssi(self, timeInPicoseconds: int, rfChannelNumber: int, context: dict[str, str] | None = None) -> tuple[float, int, int]:
        """
        This method returns the RSSI level in the captured spectrum at the specified time and on the
        specified channel. The RSSI value is in dBm.
        
        Parameters
        ----------
        timeInPicoseconds : int
            Time at which the spectrum RSSI shall be retrieved
        rfChannelNumber : int
            RF channel number, from 0 to 78
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        tuple[float, int, int]
        
            A tuple containing:
                - float Signal strength in dBm
                - int Start time in picoseconds of the RSSI sample
                - int Stop time in picoseconds of the RSSI sample
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return BluetoothAnalyzerRemoteControl._op_GetSpectrumRssi.invoke(self, ((timeInPicoseconds, rfChannelNumber), context))

    def GetSpectrumRssiAsync(self, timeInPicoseconds: int, rfChannelNumber: int, context: dict[str, str] | None = None) -> Awaitable[tuple[float, int, int]]:
        """
        This method returns the RSSI level in the captured spectrum at the specified time and on the
        specified channel. The RSSI value is in dBm.
        
        Parameters
        ----------
        timeInPicoseconds : int
            Time at which the spectrum RSSI shall be retrieved
        rfChannelNumber : int
            RF channel number, from 0 to 78
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[tuple[float, int, int]]
        
            A tuple containing:
                - float Signal strength in dBm
                - int Start time in picoseconds of the RSSI sample
                - int Stop time in picoseconds of the RSSI sample
        """
        return BluetoothAnalyzerRemoteControl._op_GetSpectrumRssi.invokeAsync(self, ((timeInPicoseconds, rfChannelNumber), context))

    def GetSpectrumRssiRange(self, fromTimeInPicoseconds: int, toTimeInPicoseconds: int, rfChannelNumber: int, context: dict[str, str] | None = None) -> tuple[list[float], int, int]:
        """
        This method returns the RSSI level in the captured spectrum in the specified time range and on
        the specified channel.
        
        Parameters
        ----------
        fromTimeInPicoseconds : int
            time from which to get RSSI samples
        toTimeInPicoseconds : int
            time to which to get RSSI samples
        rfChannelNumber : int
            RF channel number, from 0 to 78
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        tuple[list[float], int, int]
        
            A tuple containing:
                - list[float] Array of signal strength samples in dBm
                - int Start time in picoseconds of the first RSSI sample
                - int Stop time in picoseconds of last RSSI sample
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return BluetoothAnalyzerRemoteControl._op_GetSpectrumRssiRange.invoke(self, ((fromTimeInPicoseconds, toTimeInPicoseconds, rfChannelNumber), context))

    def GetSpectrumRssiRangeAsync(self, fromTimeInPicoseconds: int, toTimeInPicoseconds: int, rfChannelNumber: int, context: dict[str, str] | None = None) -> Awaitable[tuple[list[float], int, int]]:
        """
        This method returns the RSSI level in the captured spectrum in the specified time range and on
        the specified channel.
        
        Parameters
        ----------
        fromTimeInPicoseconds : int
            time from which to get RSSI samples
        toTimeInPicoseconds : int
            time to which to get RSSI samples
        rfChannelNumber : int
            RF channel number, from 0 to 78
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[tuple[list[float], int, int]]
        
            A tuple containing:
                - list[float] Array of signal strength samples in dBm
                - int Start time in picoseconds of the first RSSI sample
                - int Stop time in picoseconds of last RSSI sample
        """
        return BluetoothAnalyzerRemoteControl._op_GetSpectrumRssiRange.invokeAsync(self, ((fromTimeInPicoseconds, toTimeInPicoseconds, rfChannelNumber), context))

    def GetChannelsSummary(self, fromTimeInPicoseconds: int, toTimeInPicoseconds: int, context: dict[str, str] | None = None) -> list[ChannelSummary]:
        """
        This method returns the Bluetooth channels summary as displayed in the Instant Channels view for
        the specified time range.
        
        Parameters
        ----------
        fromTimeInPicoseconds : int
            time from which to get channels summary
        toTimeInPicoseconds : int
            time to which to get channels summary
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        list[ChannelSummary]
            Bluetooth channels summary as displayed in the Instant Channels view
        """
        return BluetoothAnalyzerRemoteControl._op_GetChannelsSummary.invoke(self, ((fromTimeInPicoseconds, toTimeInPicoseconds), context))

    def GetChannelsSummaryAsync(self, fromTimeInPicoseconds: int, toTimeInPicoseconds: int, context: dict[str, str] | None = None) -> Awaitable[list[ChannelSummary]]:
        """
        This method returns the Bluetooth channels summary as displayed in the Instant Channels view for
        the specified time range.
        
        Parameters
        ----------
        fromTimeInPicoseconds : int
            time from which to get channels summary
        toTimeInPicoseconds : int
            time to which to get channels summary
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[list[ChannelSummary]]
            Bluetooth channels summary as displayed in the Instant Channels view
        """
        return BluetoothAnalyzerRemoteControl._op_GetChannelsSummary.invokeAsync(self, ((fromTimeInPicoseconds, toTimeInPicoseconds), context))

    def ExportAudio(self, outputDirectory: str, context: dict[str, str] | None = None) -> None:
        """
        This method exports all audio available in the trace to the specified directory. It is
        equivalent to the File menu > Export > Bluetooth Audio function in the GUI. See the xref:op_AnalyzerRemoteControl_Export[Export()] function for more
        options on the audio export parameters.
        
        Parameters
        ----------
        outputDirectory : str
            path to the directory to export audio files, based on the remote computer
        context : dict[str, str]
            The request context for the invocation.
        """
        return BluetoothAnalyzerRemoteControl._op_ExportAudio.invoke(self, ((outputDirectory, ), context))

    def ExportAudioAsync(self, outputDirectory: str, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        This method exports all audio available in the trace to the specified directory. It is
        equivalent to the File menu > Export > Bluetooth Audio function in the GUI. See the xref:op_AnalyzerRemoteControl_Export[Export()] function for more
        options on the audio export parameters.
        
        Parameters
        ----------
        outputDirectory : str
            path to the directory to export audio files, based on the remote computer
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return BluetoothAnalyzerRemoteControl._op_ExportAudio.invokeAsync(self, ((outputDirectory, ), context))

    @staticmethod
    def checkedCast(
        proxy: ObjectPrx | None,
        facet: str | None = None,
        context: dict[str, str] | None = None
    ) -> BluetoothAnalyzerRemoteControlPrx | None:
        return checkedCast(BluetoothAnalyzerRemoteControlPrx, proxy, facet, context)

    @staticmethod
    def checkedCastAsync(
        proxy: ObjectPrx | None,
        facet: str | None = None,
        context: dict[str, str] | None = None
    ) -> Awaitable[BluetoothAnalyzerRemoteControlPrx | None ]:
        return checkedCastAsync(BluetoothAnalyzerRemoteControlPrx, proxy, facet, context)

    @overload
    @staticmethod
    def uncheckedCast(proxy: ObjectPrx, facet: str | None = None) -> BluetoothAnalyzerRemoteControlPrx:
        ...

    @overload
    @staticmethod
    def uncheckedCast(proxy: None, facet: str | None = None) -> None:
        ...

    @staticmethod
    def uncheckedCast(proxy: ObjectPrx | None, facet: str | None = None) -> BluetoothAnalyzerRemoteControlPrx | None:
        return uncheckedCast(BluetoothAnalyzerRemoteControlPrx, proxy, facet)

    @staticmethod
    def ice_staticId() -> str:
        return "::Ellisys::Platform::NetworkRemoteControl::Analyzer::BluetoothAnalyzerRemoteControl"

IcePy.defineProxy("::Ellisys::Platform::NetworkRemoteControl::Analyzer::BluetoothAnalyzerRemoteControl", BluetoothAnalyzerRemoteControlPrx)

class BluetoothAnalyzerRemoteControl(AnalyzerRemoteControl, ABC):
    """
    Bluetooth-specific remote-control operations, available while capturing Bluetooth.
    
    Notes
    -----
        The Slice compiler generated this skeleton class from Slice interface ``::Ellisys::Platform::NetworkRemoteControl::Analyzer::BluetoothAnalyzerRemoteControl``.
    """

    _ice_ids: Sequence[str] = ("::Ellisys::Platform::NetworkRemoteControl::Analyzer::AnalyzerRemoteControl", "::Ellisys::Platform::NetworkRemoteControl::Analyzer::BluetoothAnalyzerRemoteControl", "::Ice::Object", )
    _op_SplitTraceFileAndContinueRecording: IcePy.Operation
    _op_AddLinkKey: IcePy.Operation
    _op_ConfigureDeviceFilter: IcePy.Operation
    _op_GetSpectrumRssi: IcePy.Operation
    _op_GetSpectrumRssiRange: IcePy.Operation
    _op_GetChannelsSummary: IcePy.Operation
    _op_ExportAudio: IcePy.Operation

    @staticmethod
    def ice_staticId() -> str:
        return "::Ellisys::Platform::NetworkRemoteControl::Analyzer::BluetoothAnalyzerRemoteControl"

    @abstractmethod
    def SplitTraceFileAndContinueRecording(self, filename: str, current: Current) -> None | Awaitable[None]:
        """
        This method will save the ongoing trace to the specific file path and will continue recording.
        It is equivalent to clicking the "Save & Continue" button in the GUI.
        
        Parameters
        ----------
        filename : str
            path to the file to be saved, based on the remote computer
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
    def AddLinkKey(self, bdaddr1: int, bdaddr2: int, linkKey: bytes, current: Current) -> None | Awaitable[None]:
        """
        This method will add the specified link key to the devices database for the specified
        connection. The views will not reload after the call of this function. If a loaded trace is
        affected by this new link key, it shall be reloaded manually.
        
        Parameters
        ----------
        bdaddr1 : int
            BDADDR of the first device
        bdaddr2 : int
            BDADDR of the second device
        linkKey : bytes
            16 bytes composing the link key
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

    @abstractmethod
    def GetSpectrumRssi(self, timeInPicoseconds: int, rfChannelNumber: int, current: Current) -> tuple[float, int, int] | Awaitable[tuple[float, int, int]]:
        """
        This method returns the RSSI level in the captured spectrum at the specified time and on the
        specified channel. The RSSI value is in dBm.
        
        Parameters
        ----------
        timeInPicoseconds : int
            Time at which the spectrum RSSI shall be retrieved
        rfChannelNumber : int
            RF channel number, from 0 to 78
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        tuple[float, int, int] | Awaitable[tuple[float, int, int]]
        
            A tuple containing:
                - float Signal strength in dBm
                - int Start time in picoseconds of the RSSI sample
                - int Stop time in picoseconds of the RSSI sample
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def GetSpectrumRssiRange(self, fromTimeInPicoseconds: int, toTimeInPicoseconds: int, rfChannelNumber: int, current: Current) -> tuple[Sequence[float] | Buffer, int, int] | Awaitable[tuple[Sequence[float] | Buffer, int, int]]:
        """
        This method returns the RSSI level in the captured spectrum in the specified time range and on
        the specified channel.
        
        Parameters
        ----------
        fromTimeInPicoseconds : int
            time from which to get RSSI samples
        toTimeInPicoseconds : int
            time to which to get RSSI samples
        rfChannelNumber : int
            RF channel number, from 0 to 78
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        tuple[Sequence[float] | Buffer, int, int] | Awaitable[tuple[Sequence[float] | Buffer, int, int]]
        
            A tuple containing:
                - Sequence[float] | Buffer Array of signal strength samples in dBm
                - int Start time in picoseconds of the first RSSI sample
                - int Stop time in picoseconds of last RSSI sample
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def GetChannelsSummary(self, fromTimeInPicoseconds: int, toTimeInPicoseconds: int, current: Current) -> Sequence[ChannelSummary] | Awaitable[Sequence[ChannelSummary]]:
        """
        This method returns the Bluetooth channels summary as displayed in the Instant Channels view for
        the specified time range.
        
        Parameters
        ----------
        fromTimeInPicoseconds : int
            time from which to get channels summary
        toTimeInPicoseconds : int
            time to which to get channels summary
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        Sequence[ChannelSummary] | Awaitable[Sequence[ChannelSummary]]
            Bluetooth channels summary as displayed in the Instant Channels view
        """
        pass

    @abstractmethod
    def ExportAudio(self, outputDirectory: str, current: Current) -> None | Awaitable[None]:
        """
        This method exports all audio available in the trace to the specified directory. It is
        equivalent to the File menu > Export > Bluetooth Audio function in the GUI. See the xref:op_AnalyzerRemoteControl_Export[Export()] function for more
        options on the audio export parameters.
        
        Parameters
        ----------
        outputDirectory : str
            path to the directory to export audio files, based on the remote computer
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        None | Awaitable[None]
            None or an awaitable that completes when the dispatch completes.
        """
        pass

BluetoothAnalyzerRemoteControl._op_SplitTraceFileAndContinueRecording = IcePy.Operation(
    "SplitTraceFileAndContinueRecording",
    "SplitTraceFileAndContinueRecording",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_string, False, 0),),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

BluetoothAnalyzerRemoteControl._op_AddLinkKey = IcePy.Operation(
    "AddLinkKey",
    "AddLinkKey",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_long, False, 0), ((), IcePy._t_long, False, 0), ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_LinkKeyByteArray_t, False, 0)),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

BluetoothAnalyzerRemoteControl._op_ConfigureDeviceFilter = IcePy.Operation(
    "ConfigureDeviceFilter",
    "ConfigureDeviceFilter",
    OperationMode.Normal,
    None,
    (),
    (((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_DeviceFilterMode_t, False, 0), ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_DeviceAddressArray_t, False, 0)),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

BluetoothAnalyzerRemoteControl._op_GetSpectrumRssi = IcePy.Operation(
    "GetSpectrumRssi",
    "GetSpectrumRssi",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_long, False, 0), ((), IcePy._t_int, False, 0)),
    (((), IcePy._t_double, False, 0), ((), IcePy._t_long, False, 0), ((), IcePy._t_long, False, 0)),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

BluetoothAnalyzerRemoteControl._op_GetSpectrumRssiRange = IcePy.Operation(
    "GetSpectrumRssiRange",
    "GetSpectrumRssiRange",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_long, False, 0), ((), IcePy._t_long, False, 0), ((), IcePy._t_int, False, 0)),
    (((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_RssiArray_t, False, 0), ((), IcePy._t_long, False, 0), ((), IcePy._t_long, False, 0)),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

BluetoothAnalyzerRemoteControl._op_GetChannelsSummary = IcePy.Operation(
    "GetChannelsSummary",
    "GetChannelsSummary",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_long, False, 0), ((), IcePy._t_long, False, 0)),
    (),
    ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_ChannelsSummary_t, False, 0),
    (),
    False)

BluetoothAnalyzerRemoteControl._op_ExportAudio = IcePy.Operation(
    "ExportAudio",
    "ExportAudio",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_string, False, 0),),
    (),
    None,
    (),
    False)

__all__ = ["BluetoothAnalyzerRemoteControl", "BluetoothAnalyzerRemoteControlPrx", "_Ellisys_Platform_NetworkRemoteControl_Analyzer_BluetoothAnalyzerRemoteControlPrx_t"]
