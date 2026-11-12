# Copyright (c) ZeroC, Inc.

# slice2py version 3.8.2

from __future__ import annotations
import IcePy

from Ellisys.Platform.NetworkRemoteControl.Generator.GeneratorBufferArray import _Ellisys_Platform_NetworkRemoteControl_Generator_GeneratorBufferArray_t

from Ellisys.Platform.NetworkRemoteControl.Generator.GeneratorRemoteControl_forward import _Ellisys_Platform_NetworkRemoteControl_Generator_GeneratorRemoteControlPrx_t

from Ellisys.Platform.NetworkRemoteControl.Generator.GeneratorState import _Ellisys_Platform_NetworkRemoteControl_Generator_GeneratorState_t

from Ellisys.Platform.NetworkRemoteControl.Generator.GeneratorVariables import _Ellisys_Platform_NetworkRemoteControl_Generator_GeneratorVariables_t

from Ellisys.Platform.NetworkRemoteControl.Generator.OperationFailed import _Ellisys_Platform_NetworkRemoteControl_Generator_OperationFailed_t

from Ice.Object import Object

from Ice.ObjectPrx import ObjectPrx
from Ice.ObjectPrx import checkedCast
from Ice.ObjectPrx import checkedCastAsync
from Ice.ObjectPrx import uncheckedCast

from Ice.OperationMode import OperationMode

from abc import ABC
from abc import abstractmethod

from typing import TYPE_CHECKING
from typing import overload

if TYPE_CHECKING:
    from Ellisys.Platform.NetworkRemoteControl.Generator.GeneratorState import GeneratorState
    from Ice.Current import Current
    from collections.abc import Awaitable
    from collections.abc import Buffer
    from collections.abc import Mapping
    from collections.abc import Sequence


class GeneratorRemoteControlPrx(ObjectPrx):
    """
    Traffic-generator remote-control operations.
    
    Notes
    -----
        The Slice compiler generated this proxy class from Slice interface ``::Ellisys::Platform::NetworkRemoteControl::Generator::GeneratorRemoteControl``.
    """

    def RunFromFile(self, filename: str, context: dict[str, str] | None = None) -> None:
        """
        Starts the generator with the script located at the filename path. The path is relative to the
        computer running the GUI software, not the computer running the client software (if different).
        Can only be called if the generator is not running. The generator state can be determined with
        the GetGeneratorState() method.
        
        Parameters
        ----------
        filename : str
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return GeneratorRemoteControl._op_RunFromFile.invoke(self, ((filename, ), context))

    def RunFromFileAsync(self, filename: str, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Starts the generator with the script located at the filename path. The path is relative to the
        computer running the GUI software, not the computer running the client software (if different).
        Can only be called if the generator is not running. The generator state can be determined with
        the GetGeneratorState() method.
        
        Parameters
        ----------
        filename : str
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return GeneratorRemoteControl._op_RunFromFile.invokeAsync(self, ((filename, ), context))

    def Pause(self, context: dict[str, str] | None = None) -> None:
        """
        Pauses the generator at the current position. Can only be called if the generator is running.
        The generator state can be determined with the GetGeneratorState() method.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return GeneratorRemoteControl._op_Pause.invoke(self, ((), context))

    def PauseAsync(self, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Pauses the generator at the current position. Can only be called if the generator is running.
        The generator state can be determined with the GetGeneratorState() method.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return GeneratorRemoteControl._op_Pause.invokeAsync(self, ((), context))

    def Resume(self, context: dict[str, str] | None = None) -> None:
        """
        Resumes the generator when it is paused, either in a breakpoint of because of a call to the
        Pause() method. Can only be called if the generator is paused. The generator state can be
        determined with the GetGeneratorState() method.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return GeneratorRemoteControl._op_Resume.invoke(self, ((), context))

    def ResumeAsync(self, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Resumes the generator when it is paused, either in a breakpoint of because of a call to the
        Pause() method. Can only be called if the generator is paused. The generator state can be
        determined with the GetGeneratorState() method.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return GeneratorRemoteControl._op_Resume.invokeAsync(self, ((), context))

    def Stop(self, context: dict[str, str] | None = None) -> None:
        """
        Stops the generation. Can only be called if the generator is not stopped. The generator state
        can be determined with the GetGeneratorState() method.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return GeneratorRemoteControl._op_Stop.invoke(self, ((), context))

    def StopAsync(self, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Stops the generation. Can only be called if the generator is not stopped. The generator state
        can be determined with the GetGeneratorState() method.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return GeneratorRemoteControl._op_Stop.invokeAsync(self, ((), context))

    def ReadBuffer(self, offset: int, length: int, context: dict[str, str] | None = None) -> bytes:
        """
        Reads the generator buffer at the specified offset for the specified length. Can only be called
        if the generator is paused. The generator state can be determined with the GetGeneratorState()
        method.
        
        Parameters
        ----------
        offset : int
        length : int
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        bytes
        bytes
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return GeneratorRemoteControl._op_ReadBuffer.invoke(self, ((offset, length), context))

    def ReadBufferAsync(self, offset: int, length: int, context: dict[str, str] | None = None) -> Awaitable[bytes]:
        """
        Reads the generator buffer at the specified offset for the specified length. Can only be called
        if the generator is paused. The generator state can be determined with the GetGeneratorState()
        method.
        
        Parameters
        ----------
        offset : int
        length : int
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[bytes]
        bytes
        """
        return GeneratorRemoteControl._op_ReadBuffer.invokeAsync(self, ((offset, length), context))

    def ReadVariables(self, context: dict[str, str] | None = None) -> dict[str, int]:
        """
        Reads all generator variables. Can be called either when the generator is running or paused, but
        only global variables will be available when the generator is running. The generator state can
        be determined with the GetGeneratorState() method.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        dict[str, int]
        dict[str, int]
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return GeneratorRemoteControl._op_ReadVariables.invoke(self, ((), context))

    def ReadVariablesAsync(self, context: dict[str, str] | None = None) -> Awaitable[dict[str, int]]:
        """
        Reads all generator variables. Can be called either when the generator is running or paused, but
        only global variables will be available when the generator is running. The generator state can
        be determined with the GetGeneratorState() method.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[dict[str, int]]
        dict[str, int]
        """
        return GeneratorRemoteControl._op_ReadVariables.invokeAsync(self, ((), context))

    def WriteVariable(self, name: str, value: int, context: dict[str, str] | None = None) -> None:
        """
        Write the specified variable with the specified value. Can only be called if the generator is
        paused. The generator state can be determined with the GetGeneratorState() method.
        
        Parameters
        ----------
        name : str
        value : int
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return GeneratorRemoteControl._op_WriteVariable.invoke(self, ((name, value), context))

    def WriteVariableAsync(self, name: str, value: int, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Write the specified variable with the specified value. Can only be called if the generator is
        paused. The generator state can be determined with the GetGeneratorState() method.
        
        Parameters
        ----------
        name : str
        value : int
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return GeneratorRemoteControl._op_WriteVariable.invokeAsync(self, ((name, value), context))

    def GetGeneratorState(self, context: dict[str, str] | None = None) -> GeneratorState:
        """
        Returns the current generator state.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        GeneratorState
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return GeneratorRemoteControl._op_GetGeneratorState.invoke(self, ((), context))

    def GetGeneratorStateAsync(self, context: dict[str, str] | None = None) -> Awaitable[GeneratorState]:
        """
        Returns the current generator state.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[GeneratorState]
        """
        return GeneratorRemoteControl._op_GetGeneratorState.invokeAsync(self, ((), context))

    @staticmethod
    def checkedCast(
        proxy: ObjectPrx | None,
        facet: str | None = None,
        context: dict[str, str] | None = None
    ) -> GeneratorRemoteControlPrx | None:
        return checkedCast(GeneratorRemoteControlPrx, proxy, facet, context)

    @staticmethod
    def checkedCastAsync(
        proxy: ObjectPrx | None,
        facet: str | None = None,
        context: dict[str, str] | None = None
    ) -> Awaitable[GeneratorRemoteControlPrx | None ]:
        return checkedCastAsync(GeneratorRemoteControlPrx, proxy, facet, context)

    @overload
    @staticmethod
    def uncheckedCast(proxy: ObjectPrx, facet: str | None = None) -> GeneratorRemoteControlPrx:
        ...

    @overload
    @staticmethod
    def uncheckedCast(proxy: None, facet: str | None = None) -> None:
        ...

    @staticmethod
    def uncheckedCast(proxy: ObjectPrx | None, facet: str | None = None) -> GeneratorRemoteControlPrx | None:
        return uncheckedCast(GeneratorRemoteControlPrx, proxy, facet)

    @staticmethod
    def ice_staticId() -> str:
        return "::Ellisys::Platform::NetworkRemoteControl::Generator::GeneratorRemoteControl"

IcePy.defineProxy("::Ellisys::Platform::NetworkRemoteControl::Generator::GeneratorRemoteControl", GeneratorRemoteControlPrx)

class GeneratorRemoteControl(Object, ABC):
    """
    Traffic-generator remote-control operations.
    
    Notes
    -----
        The Slice compiler generated this skeleton class from Slice interface ``::Ellisys::Platform::NetworkRemoteControl::Generator::GeneratorRemoteControl``.
    """

    _ice_ids: Sequence[str] = ("::Ellisys::Platform::NetworkRemoteControl::Generator::GeneratorRemoteControl", "::Ice::Object", )
    _op_RunFromFile: IcePy.Operation
    _op_Pause: IcePy.Operation
    _op_Resume: IcePy.Operation
    _op_Stop: IcePy.Operation
    _op_ReadBuffer: IcePy.Operation
    _op_ReadVariables: IcePy.Operation
    _op_WriteVariable: IcePy.Operation
    _op_GetGeneratorState: IcePy.Operation

    @staticmethod
    def ice_staticId() -> str:
        return "::Ellisys::Platform::NetworkRemoteControl::Generator::GeneratorRemoteControl"

    @abstractmethod
    def RunFromFile(self, filename: str, current: Current) -> None | Awaitable[None]:
        """
        Starts the generator with the script located at the filename path. The path is relative to the
        computer running the GUI software, not the computer running the client software (if different).
        Can only be called if the generator is not running. The generator state can be determined with
        the GetGeneratorState() method.
        
        Parameters
        ----------
        filename : str
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
    def Pause(self, current: Current) -> None | Awaitable[None]:
        """
        Pauses the generator at the current position. Can only be called if the generator is running.
        The generator state can be determined with the GetGeneratorState() method.
        
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
    def Resume(self, current: Current) -> None | Awaitable[None]:
        """
        Resumes the generator when it is paused, either in a breakpoint of because of a call to the
        Pause() method. Can only be called if the generator is paused. The generator state can be
        determined with the GetGeneratorState() method.
        
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
    def Stop(self, current: Current) -> None | Awaitable[None]:
        """
        Stops the generation. Can only be called if the generator is not stopped. The generator state
        can be determined with the GetGeneratorState() method.
        
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
    def ReadBuffer(self, offset: int, length: int, current: Current) -> Sequence[int] | bytes | Buffer | Awaitable[Sequence[int] | bytes | Buffer]:
        """
        Reads the generator buffer at the specified offset for the specified length. Can only be called
        if the generator is paused. The generator state can be determined with the GetGeneratorState()
        method.
        
        Parameters
        ----------
        offset : int
        length : int
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        Sequence[int] | bytes | Buffer | Awaitable[Sequence[int] | bytes | Buffer]
        Sequence[int] | bytes | Buffer
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def ReadVariables(self, current: Current) -> Mapping[str, int] | Awaitable[Mapping[str, int]]:
        """
        Reads all generator variables. Can be called either when the generator is running or paused, but
        only global variables will be available when the generator is running. The generator state can
        be determined with the GetGeneratorState() method.
        
        Parameters
        ----------
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        Mapping[str, int] | Awaitable[Mapping[str, int]]
        Mapping[str, int]
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def WriteVariable(self, name: str, value: int, current: Current) -> None | Awaitable[None]:
        """
        Write the specified variable with the specified value. Can only be called if the generator is
        paused. The generator state can be determined with the GetGeneratorState() method.
        
        Parameters
        ----------
        name : str
        value : int
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
    def GetGeneratorState(self, current: Current) -> GeneratorState | Awaitable[GeneratorState]:
        """
        Returns the current generator state.
        
        Parameters
        ----------
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        GeneratorState | Awaitable[GeneratorState]
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

GeneratorRemoteControl._op_RunFromFile = IcePy.Operation(
    "RunFromFile",
    "RunFromFile",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_string, False, 0),),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Generator_OperationFailed_t,),
    False)

GeneratorRemoteControl._op_Pause = IcePy.Operation(
    "Pause",
    "Pause",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Generator_OperationFailed_t,),
    False)

GeneratorRemoteControl._op_Resume = IcePy.Operation(
    "Resume",
    "Resume",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Generator_OperationFailed_t,),
    False)

GeneratorRemoteControl._op_Stop = IcePy.Operation(
    "Stop",
    "Stop",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Generator_OperationFailed_t,),
    False)

GeneratorRemoteControl._op_ReadBuffer = IcePy.Operation(
    "ReadBuffer",
    "ReadBuffer",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_int, False, 0), ((), IcePy._t_int, False, 0)),
    (((), _Ellisys_Platform_NetworkRemoteControl_Generator_GeneratorBufferArray_t, False, 0),),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Generator_OperationFailed_t,),
    False)

GeneratorRemoteControl._op_ReadVariables = IcePy.Operation(
    "ReadVariables",
    "ReadVariables",
    OperationMode.Normal,
    None,
    (),
    (),
    (((), _Ellisys_Platform_NetworkRemoteControl_Generator_GeneratorVariables_t, False, 0),),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Generator_OperationFailed_t,),
    False)

GeneratorRemoteControl._op_WriteVariable = IcePy.Operation(
    "WriteVariable",
    "WriteVariable",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_string, False, 0), ((), IcePy._t_int, False, 0)),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Generator_OperationFailed_t,),
    False)

GeneratorRemoteControl._op_GetGeneratorState = IcePy.Operation(
    "GetGeneratorState",
    "GetGeneratorState",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    ((), _Ellisys_Platform_NetworkRemoteControl_Generator_GeneratorState_t, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Generator_OperationFailed_t,),
    False)

__all__ = ["GeneratorRemoteControl", "GeneratorRemoteControlPrx", "_Ellisys_Platform_NetworkRemoteControl_Generator_GeneratorRemoteControlPrx_t"]
