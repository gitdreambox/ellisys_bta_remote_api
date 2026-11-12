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

from Ellisys.Platform.NetworkRemoteControl.Analyzer.Wpan.ByteArray import _Ellisys_Platform_NetworkRemoteControl_Analyzer_Wpan_ByteArray_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.Wpan.WpanAnalyzerRemoteControl_forward import _Ellisys_Platform_NetworkRemoteControl_Analyzer_Wpan_WpanAnalyzerRemoteControlPrx_t

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


class WpanAnalyzerRemoteControlPrx(AnalyzerRemoteControlPrx):
    """
    WPAN (IEEE 802.15.4) capture remote-control operations, including Thread and Zigbee key
    management.
    
    Notes
    -----
        The Slice compiler generated this proxy class from Slice interface ``::Ellisys::Platform::NetworkRemoteControl::Analyzer::Wpan::WpanAnalyzerRemoteControl``.
    """

    def AddThreadNetworkMasterKey(self, panId: int, key128: Sequence[int] | bytes | Buffer, sequenceCounter: int, context: dict[str, str] | None = None) -> None:
        """
        Adds a Thread network master key used to decrypt traffic of the specified Thread network.
        
        Parameters
        ----------
        panId : int
            PAN identifier of the Thread network.
        key128 : Sequence[int] | bytes | Buffer
            the 128-bit (16-byte) Thread master key.
        sequenceCounter : int
            key sequence counter associated with the master key.
        context : dict[str, str]
            The request context for the invocation.
        """
        return WpanAnalyzerRemoteControl._op_AddThreadNetworkMasterKey.invoke(self, ((panId, key128, sequenceCounter), context))

    def AddThreadNetworkMasterKeyAsync(self, panId: int, key128: Sequence[int] | bytes | Buffer, sequenceCounter: int, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Adds a Thread network master key used to decrypt traffic of the specified Thread network.
        
        Parameters
        ----------
        panId : int
            PAN identifier of the Thread network.
        key128 : Sequence[int] | bytes | Buffer
            the 128-bit (16-byte) Thread master key.
        sequenceCounter : int
            key sequence counter associated with the master key.
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return WpanAnalyzerRemoteControl._op_AddThreadNetworkMasterKey.invokeAsync(self, ((panId, key128, sequenceCounter), context))

    def RemoveThreadNetworkAllMasterKeys(self, context: dict[str, str] | None = None) -> None:
        """
        Removes all previously added Thread network master keys.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        """
        return WpanAnalyzerRemoteControl._op_RemoveThreadNetworkAllMasterKeys.invoke(self, ((), context))

    def RemoveThreadNetworkAllMasterKeysAsync(self, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Removes all previously added Thread network master keys.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return WpanAnalyzerRemoteControl._op_RemoveThreadNetworkAllMasterKeys.invokeAsync(self, ((), context))

    def RemoveThreadNetworkMasterKeys(self, panId: int, context: dict[str, str] | None = None) -> None:
        """
        Removes all Thread network master keys previously added for the specified PAN.
        
        Parameters
        ----------
        panId : int
            PAN identifier whose master keys are removed.
        context : dict[str, str]
            The request context for the invocation.
        """
        return WpanAnalyzerRemoteControl._op_RemoveThreadNetworkMasterKeys.invoke(self, ((panId, ), context))

    def RemoveThreadNetworkMasterKeysAsync(self, panId: int, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Removes all Thread network master keys previously added for the specified PAN.
        
        Parameters
        ----------
        panId : int
            PAN identifier whose master keys are removed.
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return WpanAnalyzerRemoteControl._op_RemoveThreadNetworkMasterKeys.invokeAsync(self, ((panId, ), context))

    def RemoveThreadNetworkMasterKey(self, panId: int, key128: Sequence[int] | bytes | Buffer, context: dict[str, str] | None = None) -> None:
        """
        Removes a specific Thread network master key previously added for the specified PAN.
        
        Parameters
        ----------
        panId : int
            PAN identifier of the Thread network.
        key128 : Sequence[int] | bytes | Buffer
            the 128-bit (16-byte) master key to remove.
        context : dict[str, str]
            The request context for the invocation.
        """
        return WpanAnalyzerRemoteControl._op_RemoveThreadNetworkMasterKey.invoke(self, ((panId, key128), context))

    def RemoveThreadNetworkMasterKeyAsync(self, panId: int, key128: Sequence[int] | bytes | Buffer, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Removes a specific Thread network master key previously added for the specified PAN.
        
        Parameters
        ----------
        panId : int
            PAN identifier of the Thread network.
        key128 : Sequence[int] | bytes | Buffer
            the 128-bit (16-byte) master key to remove.
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return WpanAnalyzerRemoteControl._op_RemoveThreadNetworkMasterKey.invokeAsync(self, ((panId, key128), context))

    def AddZigbeeApsKey(self, destinationAddress64: Sequence[int] | bytes | Buffer, sourceAddress64: Sequence[int] | bytes | Buffer, key128: Sequence[int] | bytes | Buffer, context: dict[str, str] | None = None) -> None:
        """
        Adds a Zigbee APS link key used to decrypt traffic between the two specified devices.
        
        Parameters
        ----------
        destinationAddress64 : Sequence[int] | bytes | Buffer
            64-bit IEEE address of the destination device.
        sourceAddress64 : Sequence[int] | bytes | Buffer
            64-bit IEEE address of the source device.
        key128 : Sequence[int] | bytes | Buffer
            the 128-bit (16-byte) APS link key.
        context : dict[str, str]
            The request context for the invocation.
        """
        return WpanAnalyzerRemoteControl._op_AddZigbeeApsKey.invoke(self, ((destinationAddress64, sourceAddress64, key128), context))

    def AddZigbeeApsKeyAsync(self, destinationAddress64: Sequence[int] | bytes | Buffer, sourceAddress64: Sequence[int] | bytes | Buffer, key128: Sequence[int] | bytes | Buffer, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Adds a Zigbee APS link key used to decrypt traffic between the two specified devices.
        
        Parameters
        ----------
        destinationAddress64 : Sequence[int] | bytes | Buffer
            64-bit IEEE address of the destination device.
        sourceAddress64 : Sequence[int] | bytes | Buffer
            64-bit IEEE address of the source device.
        key128 : Sequence[int] | bytes | Buffer
            the 128-bit (16-byte) APS link key.
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return WpanAnalyzerRemoteControl._op_AddZigbeeApsKey.invokeAsync(self, ((destinationAddress64, sourceAddress64, key128), context))

    def RemoveZigbeeApsAllKeys(self, context: dict[str, str] | None = None) -> None:
        """
        Removes all previously added Zigbee APS link keys.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        """
        return WpanAnalyzerRemoteControl._op_RemoveZigbeeApsAllKeys.invoke(self, ((), context))

    def RemoveZigbeeApsAllKeysAsync(self, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Removes all previously added Zigbee APS link keys.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return WpanAnalyzerRemoteControl._op_RemoveZigbeeApsAllKeys.invokeAsync(self, ((), context))

    def RemoveZigbeeApsKeys(self, destinationAddress64: Sequence[int] | bytes | Buffer, sourceAddress64: Sequence[int] | bytes | Buffer, context: dict[str, str] | None = None) -> None:
        """
        Removes all Zigbee APS link keys previously added for the specified device pair.
        
        Parameters
        ----------
        destinationAddress64 : Sequence[int] | bytes | Buffer
            64-bit IEEE address of the destination device.
        sourceAddress64 : Sequence[int] | bytes | Buffer
            64-bit IEEE address of the source device.
        context : dict[str, str]
            The request context for the invocation.
        """
        return WpanAnalyzerRemoteControl._op_RemoveZigbeeApsKeys.invoke(self, ((destinationAddress64, sourceAddress64), context))

    def RemoveZigbeeApsKeysAsync(self, destinationAddress64: Sequence[int] | bytes | Buffer, sourceAddress64: Sequence[int] | bytes | Buffer, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Removes all Zigbee APS link keys previously added for the specified device pair.
        
        Parameters
        ----------
        destinationAddress64 : Sequence[int] | bytes | Buffer
            64-bit IEEE address of the destination device.
        sourceAddress64 : Sequence[int] | bytes | Buffer
            64-bit IEEE address of the source device.
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return WpanAnalyzerRemoteControl._op_RemoveZigbeeApsKeys.invokeAsync(self, ((destinationAddress64, sourceAddress64), context))

    def RemoveZigbeeApsKey(self, destinationAddress64: Sequence[int] | bytes | Buffer, sourceAddress64: Sequence[int] | bytes | Buffer, key128: Sequence[int] | bytes | Buffer, context: dict[str, str] | None = None) -> None:
        """
        Removes a specific Zigbee APS link key previously added for the specified device pair.
        
        Parameters
        ----------
        destinationAddress64 : Sequence[int] | bytes | Buffer
            64-bit IEEE address of the destination device.
        sourceAddress64 : Sequence[int] | bytes | Buffer
            64-bit IEEE address of the source device.
        key128 : Sequence[int] | bytes | Buffer
            the 128-bit (16-byte) APS link key to remove.
        context : dict[str, str]
            The request context for the invocation.
        """
        return WpanAnalyzerRemoteControl._op_RemoveZigbeeApsKey.invoke(self, ((destinationAddress64, sourceAddress64, key128), context))

    def RemoveZigbeeApsKeyAsync(self, destinationAddress64: Sequence[int] | bytes | Buffer, sourceAddress64: Sequence[int] | bytes | Buffer, key128: Sequence[int] | bytes | Buffer, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Removes a specific Zigbee APS link key previously added for the specified device pair.
        
        Parameters
        ----------
        destinationAddress64 : Sequence[int] | bytes | Buffer
            64-bit IEEE address of the destination device.
        sourceAddress64 : Sequence[int] | bytes | Buffer
            64-bit IEEE address of the source device.
        key128 : Sequence[int] | bytes | Buffer
            the 128-bit (16-byte) APS link key to remove.
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return WpanAnalyzerRemoteControl._op_RemoveZigbeeApsKey.invokeAsync(self, ((destinationAddress64, sourceAddress64, key128), context))

    def AddZigbeeNetworkKey(self, panId: int, key128: Sequence[int] | bytes | Buffer, context: dict[str, str] | None = None) -> None:
        """
        Adds a Zigbee network key used to decrypt traffic of the specified Zigbee network.
        
        Parameters
        ----------
        panId : int
            PAN identifier of the Zigbee network.
        key128 : Sequence[int] | bytes | Buffer
            the 128-bit (16-byte) Zigbee network key.
        context : dict[str, str]
            The request context for the invocation.
        """
        return WpanAnalyzerRemoteControl._op_AddZigbeeNetworkKey.invoke(self, ((panId, key128), context))

    def AddZigbeeNetworkKeyAsync(self, panId: int, key128: Sequence[int] | bytes | Buffer, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Adds a Zigbee network key used to decrypt traffic of the specified Zigbee network.
        
        Parameters
        ----------
        panId : int
            PAN identifier of the Zigbee network.
        key128 : Sequence[int] | bytes | Buffer
            the 128-bit (16-byte) Zigbee network key.
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return WpanAnalyzerRemoteControl._op_AddZigbeeNetworkKey.invokeAsync(self, ((panId, key128), context))

    def RemoveZigbeeNetworkAllKeys(self, context: dict[str, str] | None = None) -> None:
        """
        Removes all previously added Zigbee network keys.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        """
        return WpanAnalyzerRemoteControl._op_RemoveZigbeeNetworkAllKeys.invoke(self, ((), context))

    def RemoveZigbeeNetworkAllKeysAsync(self, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Removes all previously added Zigbee network keys.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return WpanAnalyzerRemoteControl._op_RemoveZigbeeNetworkAllKeys.invokeAsync(self, ((), context))

    def RemoveZigbeeNetworkKeys(self, panId: int, context: dict[str, str] | None = None) -> None:
        """
        Removes all Zigbee network keys previously added for the specified PAN.
        
        Parameters
        ----------
        panId : int
            PAN identifier whose network keys are removed.
        context : dict[str, str]
            The request context for the invocation.
        """
        return WpanAnalyzerRemoteControl._op_RemoveZigbeeNetworkKeys.invoke(self, ((panId, ), context))

    def RemoveZigbeeNetworkKeysAsync(self, panId: int, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Removes all Zigbee network keys previously added for the specified PAN.
        
        Parameters
        ----------
        panId : int
            PAN identifier whose network keys are removed.
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return WpanAnalyzerRemoteControl._op_RemoveZigbeeNetworkKeys.invokeAsync(self, ((panId, ), context))

    def RemoveZigbeeNetworkKey(self, panId: int, key128: Sequence[int] | bytes | Buffer, context: dict[str, str] | None = None) -> None:
        """
        Removes a specific Zigbee network key previously added for the specified PAN.
        
        Parameters
        ----------
        panId : int
            PAN identifier of the Zigbee network.
        key128 : Sequence[int] | bytes | Buffer
            the 128-bit (16-byte) network key to remove.
        context : dict[str, str]
            The request context for the invocation.
        """
        return WpanAnalyzerRemoteControl._op_RemoveZigbeeNetworkKey.invoke(self, ((panId, key128), context))

    def RemoveZigbeeNetworkKeyAsync(self, panId: int, key128: Sequence[int] | bytes | Buffer, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Removes a specific Zigbee network key previously added for the specified PAN.
        
        Parameters
        ----------
        panId : int
            PAN identifier of the Zigbee network.
        key128 : Sequence[int] | bytes | Buffer
            the 128-bit (16-byte) network key to remove.
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return WpanAnalyzerRemoteControl._op_RemoveZigbeeNetworkKey.invokeAsync(self, ((panId, key128), context))

    @staticmethod
    def checkedCast(
        proxy: ObjectPrx | None,
        facet: str | None = None,
        context: dict[str, str] | None = None
    ) -> WpanAnalyzerRemoteControlPrx | None:
        return checkedCast(WpanAnalyzerRemoteControlPrx, proxy, facet, context)

    @staticmethod
    def checkedCastAsync(
        proxy: ObjectPrx | None,
        facet: str | None = None,
        context: dict[str, str] | None = None
    ) -> Awaitable[WpanAnalyzerRemoteControlPrx | None ]:
        return checkedCastAsync(WpanAnalyzerRemoteControlPrx, proxy, facet, context)

    @overload
    @staticmethod
    def uncheckedCast(proxy: ObjectPrx, facet: str | None = None) -> WpanAnalyzerRemoteControlPrx:
        ...

    @overload
    @staticmethod
    def uncheckedCast(proxy: None, facet: str | None = None) -> None:
        ...

    @staticmethod
    def uncheckedCast(proxy: ObjectPrx | None, facet: str | None = None) -> WpanAnalyzerRemoteControlPrx | None:
        return uncheckedCast(WpanAnalyzerRemoteControlPrx, proxy, facet)

    @staticmethod
    def ice_staticId() -> str:
        return "::Ellisys::Platform::NetworkRemoteControl::Analyzer::Wpan::WpanAnalyzerRemoteControl"

IcePy.defineProxy("::Ellisys::Platform::NetworkRemoteControl::Analyzer::Wpan::WpanAnalyzerRemoteControl", WpanAnalyzerRemoteControlPrx)

class WpanAnalyzerRemoteControl(AnalyzerRemoteControl, ABC):
    """
    WPAN (IEEE 802.15.4) capture remote-control operations, including Thread and Zigbee key
    management.
    
    Notes
    -----
        The Slice compiler generated this skeleton class from Slice interface ``::Ellisys::Platform::NetworkRemoteControl::Analyzer::Wpan::WpanAnalyzerRemoteControl``.
    """

    _ice_ids: Sequence[str] = ("::Ellisys::Platform::NetworkRemoteControl::Analyzer::AnalyzerRemoteControl", "::Ellisys::Platform::NetworkRemoteControl::Analyzer::Wpan::WpanAnalyzerRemoteControl", "::Ice::Object", )
    _op_AddThreadNetworkMasterKey: IcePy.Operation
    _op_RemoveThreadNetworkAllMasterKeys: IcePy.Operation
    _op_RemoveThreadNetworkMasterKeys: IcePy.Operation
    _op_RemoveThreadNetworkMasterKey: IcePy.Operation
    _op_AddZigbeeApsKey: IcePy.Operation
    _op_RemoveZigbeeApsAllKeys: IcePy.Operation
    _op_RemoveZigbeeApsKeys: IcePy.Operation
    _op_RemoveZigbeeApsKey: IcePy.Operation
    _op_AddZigbeeNetworkKey: IcePy.Operation
    _op_RemoveZigbeeNetworkAllKeys: IcePy.Operation
    _op_RemoveZigbeeNetworkKeys: IcePy.Operation
    _op_RemoveZigbeeNetworkKey: IcePy.Operation

    @staticmethod
    def ice_staticId() -> str:
        return "::Ellisys::Platform::NetworkRemoteControl::Analyzer::Wpan::WpanAnalyzerRemoteControl"

    @abstractmethod
    def AddThreadNetworkMasterKey(self, panId: int, key128: bytes, sequenceCounter: int, current: Current) -> None | Awaitable[None]:
        """
        Adds a Thread network master key used to decrypt traffic of the specified Thread network.
        
        Parameters
        ----------
        panId : int
            PAN identifier of the Thread network.
        key128 : bytes
            the 128-bit (16-byte) Thread master key.
        sequenceCounter : int
            key sequence counter associated with the master key.
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        None | Awaitable[None]
            None or an awaitable that completes when the dispatch completes.
        """
        pass

    @abstractmethod
    def RemoveThreadNetworkAllMasterKeys(self, current: Current) -> None | Awaitable[None]:
        """
        Removes all previously added Thread network master keys.
        
        Parameters
        ----------
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        None | Awaitable[None]
            None or an awaitable that completes when the dispatch completes.
        """
        pass

    @abstractmethod
    def RemoveThreadNetworkMasterKeys(self, panId: int, current: Current) -> None | Awaitable[None]:
        """
        Removes all Thread network master keys previously added for the specified PAN.
        
        Parameters
        ----------
        panId : int
            PAN identifier whose master keys are removed.
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        None | Awaitable[None]
            None or an awaitable that completes when the dispatch completes.
        """
        pass

    @abstractmethod
    def RemoveThreadNetworkMasterKey(self, panId: int, key128: bytes, current: Current) -> None | Awaitable[None]:
        """
        Removes a specific Thread network master key previously added for the specified PAN.
        
        Parameters
        ----------
        panId : int
            PAN identifier of the Thread network.
        key128 : bytes
            the 128-bit (16-byte) master key to remove.
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        None | Awaitable[None]
            None or an awaitable that completes when the dispatch completes.
        """
        pass

    @abstractmethod
    def AddZigbeeApsKey(self, destinationAddress64: bytes, sourceAddress64: bytes, key128: bytes, current: Current) -> None | Awaitable[None]:
        """
        Adds a Zigbee APS link key used to decrypt traffic between the two specified devices.
        
        Parameters
        ----------
        destinationAddress64 : bytes
            64-bit IEEE address of the destination device.
        sourceAddress64 : bytes
            64-bit IEEE address of the source device.
        key128 : bytes
            the 128-bit (16-byte) APS link key.
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        None | Awaitable[None]
            None or an awaitable that completes when the dispatch completes.
        """
        pass

    @abstractmethod
    def RemoveZigbeeApsAllKeys(self, current: Current) -> None | Awaitable[None]:
        """
        Removes all previously added Zigbee APS link keys.
        
        Parameters
        ----------
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        None | Awaitable[None]
            None or an awaitable that completes when the dispatch completes.
        """
        pass

    @abstractmethod
    def RemoveZigbeeApsKeys(self, destinationAddress64: bytes, sourceAddress64: bytes, current: Current) -> None | Awaitable[None]:
        """
        Removes all Zigbee APS link keys previously added for the specified device pair.
        
        Parameters
        ----------
        destinationAddress64 : bytes
            64-bit IEEE address of the destination device.
        sourceAddress64 : bytes
            64-bit IEEE address of the source device.
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        None | Awaitable[None]
            None or an awaitable that completes when the dispatch completes.
        """
        pass

    @abstractmethod
    def RemoveZigbeeApsKey(self, destinationAddress64: bytes, sourceAddress64: bytes, key128: bytes, current: Current) -> None | Awaitable[None]:
        """
        Removes a specific Zigbee APS link key previously added for the specified device pair.
        
        Parameters
        ----------
        destinationAddress64 : bytes
            64-bit IEEE address of the destination device.
        sourceAddress64 : bytes
            64-bit IEEE address of the source device.
        key128 : bytes
            the 128-bit (16-byte) APS link key to remove.
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        None | Awaitable[None]
            None or an awaitable that completes when the dispatch completes.
        """
        pass

    @abstractmethod
    def AddZigbeeNetworkKey(self, panId: int, key128: bytes, current: Current) -> None | Awaitable[None]:
        """
        Adds a Zigbee network key used to decrypt traffic of the specified Zigbee network.
        
        Parameters
        ----------
        panId : int
            PAN identifier of the Zigbee network.
        key128 : bytes
            the 128-bit (16-byte) Zigbee network key.
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        None | Awaitable[None]
            None or an awaitable that completes when the dispatch completes.
        """
        pass

    @abstractmethod
    def RemoveZigbeeNetworkAllKeys(self, current: Current) -> None | Awaitable[None]:
        """
        Removes all previously added Zigbee network keys.
        
        Parameters
        ----------
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        None | Awaitable[None]
            None or an awaitable that completes when the dispatch completes.
        """
        pass

    @abstractmethod
    def RemoveZigbeeNetworkKeys(self, panId: int, current: Current) -> None | Awaitable[None]:
        """
        Removes all Zigbee network keys previously added for the specified PAN.
        
        Parameters
        ----------
        panId : int
            PAN identifier whose network keys are removed.
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        None | Awaitable[None]
            None or an awaitable that completes when the dispatch completes.
        """
        pass

    @abstractmethod
    def RemoveZigbeeNetworkKey(self, panId: int, key128: bytes, current: Current) -> None | Awaitable[None]:
        """
        Removes a specific Zigbee network key previously added for the specified PAN.
        
        Parameters
        ----------
        panId : int
            PAN identifier of the Zigbee network.
        key128 : bytes
            the 128-bit (16-byte) network key to remove.
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        None | Awaitable[None]
            None or an awaitable that completes when the dispatch completes.
        """
        pass

WpanAnalyzerRemoteControl._op_AddThreadNetworkMasterKey = IcePy.Operation(
    "AddThreadNetworkMasterKey",
    "AddThreadNetworkMasterKey",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_int, False, 0), ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_Wpan_ByteArray_t, False, 0), ((), IcePy._t_long, False, 0)),
    (),
    None,
    (),
    False)

WpanAnalyzerRemoteControl._op_RemoveThreadNetworkAllMasterKeys = IcePy.Operation(
    "RemoveThreadNetworkAllMasterKeys",
    "RemoveThreadNetworkAllMasterKeys",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    None,
    (),
    False)

WpanAnalyzerRemoteControl._op_RemoveThreadNetworkMasterKeys = IcePy.Operation(
    "RemoveThreadNetworkMasterKeys",
    "RemoveThreadNetworkMasterKeys",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_int, False, 0),),
    (),
    None,
    (),
    False)

WpanAnalyzerRemoteControl._op_RemoveThreadNetworkMasterKey = IcePy.Operation(
    "RemoveThreadNetworkMasterKey",
    "RemoveThreadNetworkMasterKey",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_int, False, 0), ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_Wpan_ByteArray_t, False, 0)),
    (),
    None,
    (),
    False)

WpanAnalyzerRemoteControl._op_AddZigbeeApsKey = IcePy.Operation(
    "AddZigbeeApsKey",
    "AddZigbeeApsKey",
    OperationMode.Normal,
    None,
    (),
    (((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_Wpan_ByteArray_t, False, 0), ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_Wpan_ByteArray_t, False, 0), ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_Wpan_ByteArray_t, False, 0)),
    (),
    None,
    (),
    False)

WpanAnalyzerRemoteControl._op_RemoveZigbeeApsAllKeys = IcePy.Operation(
    "RemoveZigbeeApsAllKeys",
    "RemoveZigbeeApsAllKeys",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    None,
    (),
    False)

WpanAnalyzerRemoteControl._op_RemoveZigbeeApsKeys = IcePy.Operation(
    "RemoveZigbeeApsKeys",
    "RemoveZigbeeApsKeys",
    OperationMode.Normal,
    None,
    (),
    (((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_Wpan_ByteArray_t, False, 0), ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_Wpan_ByteArray_t, False, 0)),
    (),
    None,
    (),
    False)

WpanAnalyzerRemoteControl._op_RemoveZigbeeApsKey = IcePy.Operation(
    "RemoveZigbeeApsKey",
    "RemoveZigbeeApsKey",
    OperationMode.Normal,
    None,
    (),
    (((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_Wpan_ByteArray_t, False, 0), ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_Wpan_ByteArray_t, False, 0), ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_Wpan_ByteArray_t, False, 0)),
    (),
    None,
    (),
    False)

WpanAnalyzerRemoteControl._op_AddZigbeeNetworkKey = IcePy.Operation(
    "AddZigbeeNetworkKey",
    "AddZigbeeNetworkKey",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_int, False, 0), ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_Wpan_ByteArray_t, False, 0)),
    (),
    None,
    (),
    False)

WpanAnalyzerRemoteControl._op_RemoveZigbeeNetworkAllKeys = IcePy.Operation(
    "RemoveZigbeeNetworkAllKeys",
    "RemoveZigbeeNetworkAllKeys",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    None,
    (),
    False)

WpanAnalyzerRemoteControl._op_RemoveZigbeeNetworkKeys = IcePy.Operation(
    "RemoveZigbeeNetworkKeys",
    "RemoveZigbeeNetworkKeys",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_int, False, 0),),
    (),
    None,
    (),
    False)

WpanAnalyzerRemoteControl._op_RemoveZigbeeNetworkKey = IcePy.Operation(
    "RemoveZigbeeNetworkKey",
    "RemoveZigbeeNetworkKey",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_int, False, 0), ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_Wpan_ByteArray_t, False, 0)),
    (),
    None,
    (),
    False)

__all__ = ["WpanAnalyzerRemoteControl", "WpanAnalyzerRemoteControlPrx", "_Ellisys_Platform_NetworkRemoteControl_Analyzer_Wpan_WpanAnalyzerRemoteControlPrx_t"]
