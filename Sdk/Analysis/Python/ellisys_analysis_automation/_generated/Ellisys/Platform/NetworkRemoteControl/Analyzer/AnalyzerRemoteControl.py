# Copyright (c) ZeroC, Inc.

# slice2py version 3.8.2

from __future__ import annotations
import IcePy

from Ellisys.Platform.NetworkRemoteControl.Analyzer.AddMarker import _Ellisys_Platform_NetworkRemoteControl_Analyzer_AddMarker_t

from Ellisys.Platform.NetworkRemoteControl.Analyzer.AnalyzerRemoteControl_forward import _Ellisys_Platform_NetworkRemoteControl_Analyzer_AnalyzerRemoteControlPrx_t

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
    from collections.abc import Awaitable
    from collections.abc import Buffer
    from collections.abc import Sequence


class AnalyzerRemoteControlPrx(ObjectPrx):
    """
    Generic remote-control operations common to every Ellisys analyzer.
    
    Notes
    -----
        The Slice compiler generated this proxy class from Slice interface ``::Ellisys::Platform::NetworkRemoteControl::Analyzer::AnalyzerRemoteControl``.
    """

    def GetAppInfo(self, context: dict[str, str] | None = None) -> AppInfo:
        """
        Returns information about the remote application, such as version, file extension, etc.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        AppInfo
            Application info.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_GetAppInfo.invoke(self, ((), context))

    def GetAppInfoAsync(self, context: dict[str, str] | None = None) -> Awaitable[AppInfo]:
        """
        Returns information about the remote application, such as version, file extension, etc.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[AppInfo]
            Application info.
        """
        return AnalyzerRemoteControl._op_GetAppInfo.invokeAsync(self, ((), context))

    def ExitApp(self, context: dict[str, str] | None = None) -> None:
        """
        Exits the remote application.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_ExitApp.invoke(self, ((), context))

    def ExitAppAsync(self, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Exits the remote application.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return AnalyzerRemoteControl._op_ExitApp.invokeAsync(self, ((), context))

    def GetAvailableDataSources(self, context: dict[str, str] | None = None) -> list[str]:
        """
        Returns the available analyzers accessible by the analysis software.
        
        Equivalent to list of the Record menu > Select analyzer dialog.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        list[str]
            Array of available data sources.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_GetAvailableDataSources.invoke(self, ((), context))

    def GetAvailableDataSourcesAsync(self, context: dict[str, str] | None = None) -> Awaitable[list[str]]:
        """
        Returns the available analyzers accessible by the analysis software.
        
        Equivalent to list of the Record menu > Select analyzer dialog.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[list[str]]
            Array of available data sources.
        """
        return AnalyzerRemoteControl._op_GetAvailableDataSources.invokeAsync(self, ((), context))

    def SelectDataSource(self, dataSourceUniqueId: str, context: dict[str, str] | None = None) -> None:
        """
        Select the active data source for capturing data. This is typically a string returned from the
        GetAvailableDataSources() function.
        
        Equivalent to selecting an analyzer from the Record menu > Select analyzer dialog.
        
        Parameters
        ----------
        dataSourceUniqueId : str
            unique ID of the data source to select
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_SelectDataSource.invoke(self, ((dataSourceUniqueId, ), context))

    def SelectDataSourceAsync(self, dataSourceUniqueId: str, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Select the active data source for capturing data. This is typically a string returned from the
        GetAvailableDataSources() function.
        
        Equivalent to selecting an analyzer from the Record menu > Select analyzer dialog.
        
        Parameters
        ----------
        dataSourceUniqueId : str
            unique ID of the data source to select
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return AnalyzerRemoteControl._op_SelectDataSource.invokeAsync(self, ((dataSourceUniqueId, ), context))

    def GetSelectedDataSource(self, context: dict[str, str] | None = None) -> str:
        """
        Returns the currently selected analyzers, if any.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        str
            Analyzer currently selected.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_GetSelectedDataSource.invoke(self, ((), context))

    def GetSelectedDataSourceAsync(self, context: dict[str, str] | None = None) -> Awaitable[str]:
        """
        Returns the currently selected analyzers, if any.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[str]
            Analyzer currently selected.
        """
        return AnalyzerRemoteControl._op_GetSelectedDataSource.invokeAsync(self, ((), context))

    def IsRecording(self, context: dict[str, str] | None = None) -> bool:
        """
        Indicates if a recording is currently running.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        bool
            true if the analyzer is currently capturing data following the call of the
            StartRecording() method, false otherwise
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_IsRecording.invoke(self, ((), context))

    def IsRecordingAsync(self, context: dict[str, str] | None = None) -> Awaitable[bool]:
        """
        Indicates if a recording is currently running.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[bool]
            true if the analyzer is currently capturing data following the call of the
            StartRecording() method, false otherwise
        """
        return AnalyzerRemoteControl._op_IsRecording.invokeAsync(self, ((), context))

    def GetRecordingStatus(self, context: dict[str, str] | None = None) -> RecordingStatus:
        """
        Returns information on the running recording, such as the analyzer, the duration and trace size.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        RecordingStatus
            Status of the recording
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_GetRecordingStatus.invoke(self, ((), context))

    def GetRecordingStatusAsync(self, context: dict[str, str] | None = None) -> Awaitable[RecordingStatus]:
        """
        Returns information on the running recording, such as the analyzer, the duration and trace size.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[RecordingStatus]
            Status of the recording
        """
        return AnalyzerRemoteControl._op_GetRecordingStatus.invokeAsync(self, ((), context))

    def StartRecording(self, context: dict[str, str] | None = None) -> None:
        """
        Starts the analyzer capture with the current settings. The settings can be either configured
        manually in the GUI software or configured with the ConfigureSettings() method.
        
        Equivalent to Record > Start recording in the GUI software.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_StartRecording.invoke(self, ((), context))

    def StartRecordingAsync(self, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Starts the analyzer capture with the current settings. The settings can be either configured
        manually in the GUI software or configured with the ConfigureSettings() method.
        
        Equivalent to Record > Start recording in the GUI software.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return AnalyzerRemoteControl._op_StartRecording.invokeAsync(self, ((), context))

    def StopRecordingAndSaveTraceFile(self, filename: str, overwrite: bool, context: dict[str, str] | None = None) -> None:
        """
        Stops the analyzer capture and save the resulting file to the specified filename.
        
        Equivalent to Record > Stop recording followed by File > Save in the GUI software.
        
        Parameters
        ----------
        filename : str
            path to the file to be saved, based on the remote computer
        overwrite : bool
            destination filename will be replaced if already exists
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_StopRecordingAndSaveTraceFile.invoke(self, ((filename, overwrite), context))

    def StopRecordingAndSaveTraceFileAsync(self, filename: str, overwrite: bool, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Stops the analyzer capture and save the resulting file to the specified filename.
        
        Equivalent to Record > Stop recording followed by File > Save in the GUI software.
        
        Parameters
        ----------
        filename : str
            path to the file to be saved, based on the remote computer
        overwrite : bool
            destination filename will be replaced if already exists
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return AnalyzerRemoteControl._op_StopRecordingAndSaveTraceFile.invokeAsync(self, ((filename, overwrite), context))

    def AbortRecordingAndDiscardTraceFile(self, context: dict[str, str] | None = None) -> None:
        """
        Aborts the ongoing capture and discard any captured data.
        
        Equivalent to Record > Stop recording followed by File > New in the GUI software.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_AbortRecordingAndDiscardTraceFile.invoke(self, ((), context))

    def AbortRecordingAndDiscardTraceFileAsync(self, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Aborts the ongoing capture and discard any captured data.
        
        Equivalent to Record > Stop recording followed by File > New in the GUI software.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return AnalyzerRemoteControl._op_AbortRecordingAndDiscardTraceFile.invokeAsync(self, ((), context))

    def GetRecordingOptions(self, relevantOnly: bool, context: dict[str, str] | None = None) -> str:
        """
        Retrieve the current recording options in JSON format.
        
        Equivalent to Record > Recording Options > Save in the GUI software.
        
        Parameters
        ----------
        relevantOnly : bool
            indicates if the function shall return only the fields which are set with
            non-default values, or if default values shall be returned as well.
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        str
            JSON formatted-string containing the recording options
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_GetRecordingOptions.invoke(self, ((relevantOnly, ), context))

    def GetRecordingOptionsAsync(self, relevantOnly: bool, context: dict[str, str] | None = None) -> Awaitable[str]:
        """
        Retrieve the current recording options in JSON format.
        
        Equivalent to Record > Recording Options > Save in the GUI software.
        
        Parameters
        ----------
        relevantOnly : bool
            indicates if the function shall return only the fields which are set with
            non-default values, or if default values shall be returned as well.
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[str]
            JSON formatted-string containing the recording options
        """
        return AnalyzerRemoteControl._op_GetRecordingOptions.invokeAsync(self, ((relevantOnly, ), context))

    def ConfigureRecordingOptions(self, options: str, context: dict[str, str] | None = None) -> None:
        """
        Configure the recording options of the data source. The provided settings can be saved from the
        Recording Options dialog of the GUI software or can be created manually.
        
        The format of the options string is a modified JSON format with the following customizations to
        the standard JSON format:
        
        - The root object braces can be omitted. For example, "{ field:value }" can optionally be
        expressed as "field:value" for brevity.
        - The name double quotes can be omitted. For example, "field":"value" can optionally be
        expressed as field: "value" for brevity.
        - Encapsulated parent objects having a single child object can use the '.' hierarchical
        notation. For example, "a:{ b:value }" can optionally be expressed as "a.b:value" for brevity.
        
        The provided string can contain only the fields to be updated.
        
        Equivalent to Record > Recording Options > Load in the GUI software.
        
        Parameters
        ----------
        options : str
            recording options in extended JSON format
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_ConfigureRecordingOptions.invoke(self, ((options, ), context))

    def ConfigureRecordingOptionsAsync(self, options: str, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Configure the recording options of the data source. The provided settings can be saved from the
        Recording Options dialog of the GUI software or can be created manually.
        
        The format of the options string is a modified JSON format with the following customizations to
        the standard JSON format:
        
        - The root object braces can be omitted. For example, "{ field:value }" can optionally be
        expressed as "field:value" for brevity.
        - The name double quotes can be omitted. For example, "field":"value" can optionally be
        expressed as field: "value" for brevity.
        - Encapsulated parent objects having a single child object can use the '.' hierarchical
        notation. For example, "a:{ b:value }" can optionally be expressed as "a.b:value" for brevity.
        
        The provided string can contain only the fields to be updated.
        
        Equivalent to Record > Recording Options > Load in the GUI software.
        
        Parameters
        ----------
        options : str
            recording options in extended JSON format
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return AnalyzerRemoteControl._op_ConfigureRecordingOptions.invokeAsync(self, ((options, ), context))

    def InsertMessage(self, severity: MessageSeverity, message: str, context: dict[str, str] | None = None) -> None:
        """
        Insert a message in the Message Log overview at the current time. This function can only be
        called during recording. The message can either be raw text, or hierarchically formatted text
        in JSON or XML.
        
        The JSON format is as follows:
        
        ----
        {
        fields:[
        { field:"field1", value:[
        { field:"field2", value:"value2" },
        { field:"field3", value:"value3" }
        ] }
        ]
        }
        ----
        
        The XML format is as follows:
        
        ----
        <fields>
        <field name="field1">
        <field name="field2">value2</field>
        <field name="field3">value3</field>
        </field>
        </fields>
        ----
        
        Parameters
        ----------
        severity : MessageSeverity
            indicates if this message is an information, a warning or an error
        message : str
            the message that will be inserted, either in raw text, JSON or XML
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_InsertMessage.invoke(self, ((severity, message), context))

    def InsertMessageAsync(self, severity: MessageSeverity, message: str, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Insert a message in the Message Log overview at the current time. This function can only be
        called during recording. The message can either be raw text, or hierarchically formatted text
        in JSON or XML.
        
        The JSON format is as follows:
        
        ----
        {
        fields:[
        { field:"field1", value:[
        { field:"field2", value:"value2" },
        { field:"field3", value:"value3" }
        ] }
        ]
        }
        ----
        
        The XML format is as follows:
        
        ----
        <fields>
        <field name="field1">
        <field name="field2">value2</field>
        <field name="field3">value3</field>
        </field>
        </fields>
        ----
        
        Parameters
        ----------
        severity : MessageSeverity
            indicates if this message is an information, a warning or an error
        message : str
            the message that will be inserted, either in raw text, JSON or XML
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return AnalyzerRemoteControl._op_InsertMessage.invokeAsync(self, ((severity, message), context))

    def IsLoading(self, context: dict[str, str] | None = None) -> bool:
        """
        Indicates if the software is loading a trace.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        bool
            true if the file is loading, false otherwise.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_IsLoading.invoke(self, ((), context))

    def IsLoadingAsync(self, context: dict[str, str] | None = None) -> Awaitable[bool]:
        """
        Indicates if the software is loading a trace.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[bool]
            true if the file is loading, false otherwise.
        """
        return AnalyzerRemoteControl._op_IsLoading.invokeAsync(self, ((), context))

    def StartLoading(self, filename: str, context: dict[str, str] | None = None) -> None:
        """
        Starts loading the specified filename.
        
        Equivalent to File > Open in the GUI software.
        
        Parameters
        ----------
        filename : str
            path to the file to be loaded, based on the remote computer
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_StartLoading.invoke(self, ((filename, ), context))

    def StartLoadingAsync(self, filename: str, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Starts loading the specified filename.
        
        Equivalent to File > Open in the GUI software.
        
        Parameters
        ----------
        filename : str
            path to the file to be loaded, based on the remote computer
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return AnalyzerRemoteControl._op_StartLoading.invokeAsync(self, ((filename, ), context))

    def GetTraceFileInfo(self, context: dict[str, str] | None = None) -> TraceFileInfo:
        """
        Returns information on the loaded trace file, such as the size, start date, analyzer used and
        software version.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        TraceFileInfo
            Information on the loaded trace file
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_GetTraceFileInfo.invoke(self, ((), context))

    def GetTraceFileInfoAsync(self, context: dict[str, str] | None = None) -> Awaitable[TraceFileInfo]:
        """
        Returns information on the loaded trace file, such as the size, start date, analyzer used and
        software version.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[TraceFileInfo]
            Information on the loaded trace file
        """
        return AnalyzerRemoteControl._op_GetTraceFileInfo.invokeAsync(self, ((), context))

    def CloseTraceFile(self, context: dict[str, str] | None = None) -> None:
        """
        Close the loaded trace file. Changes will be lost if any, unless saved explicitly with
        SaveChanges().
        
        Equivalent to File > New in the GUI software.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_CloseTraceFile.invoke(self, ((), context))

    def CloseTraceFileAsync(self, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Close the loaded trace file. Changes will be lost if any, unless saved explicitly with
        SaveChanges().
        
        Equivalent to File > New in the GUI software.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return AnalyzerRemoteControl._op_CloseTraceFile.invokeAsync(self, ((), context))

    def IsModified(self, context: dict[str, str] | None = None) -> bool:
        """
        Indicates if the open file has changes. The changes can be saved with SaveChanges().
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        bool
            true if the open file has changes, false otherwise
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_IsModified.invoke(self, ((), context))

    def IsModifiedAsync(self, context: dict[str, str] | None = None) -> Awaitable[bool]:
        """
        Indicates if the open file has changes. The changes can be saved with SaveChanges().
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[bool]
            true if the open file has changes, false otherwise
        """
        return AnalyzerRemoteControl._op_IsModified.invokeAsync(self, ((), context))

    def SaveChanges(self, context: dict[str, str] | None = None) -> None:
        """
        Save changes in the currently open file.
        
        Equivalent to File > Save in the GUI software.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_SaveChanges.invoke(self, ((), context))

    def SaveChangesAsync(self, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Save changes in the currently open file.
        
        Equivalent to File > Save in the GUI software.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return AnalyzerRemoteControl._op_SaveChanges.invokeAsync(self, ((), context))

    def AddMarkerOnSelectedOverviewItem(self, marker: AddMarker, context: dict[str, str] | None = None) -> None:
        """
        Adds a marker on the currently selected item in the Overview.
        
        Equivalent to main toolbar > Markers > Mark selected item in the GUI software.
        
        Parameters
        ----------
        marker : AddMarker
            information on the marker to be added
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_AddMarkerOnSelectedOverviewItem.invoke(self, ((marker, ), context))

    def AddMarkerOnSelectedOverviewItemAsync(self, marker: AddMarker, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Adds a marker on the currently selected item in the Overview.
        
        Equivalent to main toolbar > Markers > Mark selected item in the GUI software.
        
        Parameters
        ----------
        marker : AddMarker
            information on the marker to be added
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return AnalyzerRemoteControl._op_AddMarkerOnSelectedOverviewItem.invokeAsync(self, ((marker, ), context))

    def AddMarkerAtTime(self, timeInPicoseconds: int, marker: AddMarker, context: dict[str, str] | None = None) -> None:
        """
        Adds a marker at the specified time.
        
        Equivalent to Instant Timing > Right Click Menu > Add new marker here in the GUI software.
        
        Parameters
        ----------
        timeInPicoseconds : int
            the time in picoseconds of the marker to be added
        marker : AddMarker
            information on the marker to be added
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_AddMarkerAtTime.invoke(self, ((timeInPicoseconds, marker), context))

    def AddMarkerAtTimeAsync(self, timeInPicoseconds: int, marker: AddMarker, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Adds a marker at the specified time.
        
        Equivalent to Instant Timing > Right Click Menu > Add new marker here in the GUI software.
        
        Parameters
        ----------
        timeInPicoseconds : int
            the time in picoseconds of the marker to be added
        marker : AddMarker
            information on the marker to be added
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return AnalyzerRemoteControl._op_AddMarkerAtTime.invokeAsync(self, ((timeInPicoseconds, marker), context))

    def GetMarkers(self, context: dict[str, str] | None = None) -> list[GetMarker]:
        """
        Get all markers of the trace file.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        list[GetMarker]
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_GetMarkers.invoke(self, ((), context))

    def GetMarkersAsync(self, context: dict[str, str] | None = None) -> Awaitable[list[GetMarker]]:
        """
        Get all markers of the trace file.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[list[GetMarker]]
        """
        return AnalyzerRemoteControl._op_GetMarkers.invokeAsync(self, ((), context))

    def Export(self, outputFilename: str, exportName: str, exportOptions: Sequence[ExportOption], context: dict[str, str] | None = None) -> None:
        """
        Export the specified data to the output filename with the specified options. The options are
        optional and are specific to the export mode. The available export modes are described in the following entries.
        
        Parameters
        ----------
        outputFilename : str
        exportName : str
        exportOptions : Sequence[ExportOption]
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_Export.invoke(self, ((outputFilename, exportName, exportOptions), context))

    def ExportAsync(self, outputFilename: str, exportName: str, exportOptions: Sequence[ExportOption], context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Export the specified data to the output filename with the specified options. The options are
        optional and are specific to the export mode. The available export modes are described in the following entries.
        
        Parameters
        ----------
        outputFilename : str
        exportName : str
        exportOptions : Sequence[ExportOption]
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return AnalyzerRemoteControl._op_Export.invokeAsync(self, ((outputFilename, exportName, exportOptions), context))

    def GetAvailableOverviews(self, context: dict[str, str] | None = None) -> list[str]:
        """
        Get the list of available overviews.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        list[str]
            the list of available overviews
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_GetAvailableOverviews.invoke(self, ((), context))

    def GetAvailableOverviewsAsync(self, context: dict[str, str] | None = None) -> Awaitable[list[str]]:
        """
        Get the list of available overviews.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[list[str]]
            the list of available overviews
        """
        return AnalyzerRemoteControl._op_GetAvailableOverviews.invokeAsync(self, ((), context))

    def GetSelectedOverview(self, context: dict[str, str] | None = None) -> str:
        """
        Retrieve the active overview.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        str
            the name of the active overview
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_GetSelectedOverview.invoke(self, ((), context))

    def GetSelectedOverviewAsync(self, context: dict[str, str] | None = None) -> Awaitable[str]:
        """
        Retrieve the active overview.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[str]
            the name of the active overview
        """
        return AnalyzerRemoteControl._op_GetSelectedOverview.invokeAsync(self, ((), context))

    def SelectOverview(self, overviewName: str, context: dict[str, str] | None = None) -> None:
        """
        This method makes a given overview active. All the methods for navigating the overview tree
        structure will work in the active overview so it is required to first ensure the overview is
        active. For example SelectOverview("USB 3.0") will make the USB 3.0 Overview active.
        
        Parameters
        ----------
        overviewName : str
            Name of the overview to select
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_SelectOverview.invoke(self, ((overviewName, ), context))

    def SelectOverviewAsync(self, overviewName: str, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        This method makes a given overview active. All the methods for navigating the overview tree
        structure will work in the active overview so it is required to first ensure the overview is
        active. For example SelectOverview("USB 3.0") will make the USB 3.0 Overview active.
        
        Parameters
        ----------
        overviewName : str
            Name of the overview to select
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return AnalyzerRemoteControl._op_SelectOverview.invokeAsync(self, ((overviewName, ), context))

    def GetAvailableProtocolLayers(self, context: dict[str, str] | None = None) -> list[str]:
        """
        Get the list of available protocol layers.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        list[str]
            the list of available protocol layers
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_GetAvailableProtocolLayers.invoke(self, ((), context))

    def GetAvailableProtocolLayersAsync(self, context: dict[str, str] | None = None) -> Awaitable[list[str]]:
        """
        Get the list of available protocol layers.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[list[str]]
            the list of available protocol layers
        """
        return AnalyzerRemoteControl._op_GetAvailableProtocolLayers.invokeAsync(self, ((), context))

    def GetSelectedProtocolLayer(self, context: dict[str, str] | None = None) -> str:
        """
        Retrieve the current protocol layer in the active overview.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        str
            the selected protocol layer
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_GetSelectedProtocolLayer.invoke(self, ((), context))

    def GetSelectedProtocolLayerAsync(self, context: dict[str, str] | None = None) -> Awaitable[str]:
        """
        Retrieve the current protocol layer in the active overview.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[str]
            the selected protocol layer
        """
        return AnalyzerRemoteControl._op_GetSelectedProtocolLayer.invokeAsync(self, ((), context))

    def SelectProtocolLayer(self, protocolLayerName: str, context: dict[str, str] | None = None) -> None:
        """
        This method will switch the protocol layer in the active overview. It is equivalent to clicking
        the protocol layers buttons in the GUI.
        
        Parameters
        ----------
        protocolLayerName : str
            Name of the protocol layer to select, as displayed in the popup on the
            button in the GUI
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_SelectProtocolLayer.invoke(self, ((protocolLayerName, ), context))

    def SelectProtocolLayerAsync(self, protocolLayerName: str, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        This method will switch the protocol layer in the active overview. It is equivalent to clicking
        the protocol layers buttons in the GUI.
        
        Parameters
        ----------
        protocolLayerName : str
            Name of the protocol layer to select, as displayed in the popup on the
            button in the GUI
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return AnalyzerRemoteControl._op_SelectProtocolLayer.invokeAsync(self, ((protocolLayerName, ), context))

    def GetOverviewQuery(self, context: dict[str, str] | None = None) -> str:
        """
        Retrieve the current query in the active overview.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        str
            the current query if any, empty string otherwise
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_GetOverviewQuery.invoke(self, ((), context))

    def GetOverviewQueryAsync(self, context: dict[str, str] | None = None) -> Awaitable[str]:
        """
        Retrieve the current query in the active overview.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[str]
            the current query if any, empty string otherwise
        """
        return AnalyzerRemoteControl._op_GetOverviewQuery.invokeAsync(self, ((), context))

    def SetOverviewQuery(self, query: str, context: dict[str, str] | None = None) -> None:
        """
        Applies the specified query string to the active overview. This enables filtering the overview
        root items with the specified conditions.
        
        Equivalent to Search > Filter in the GUI software.
        
        Parameters
        ----------
        query : str
            the query to apply
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_SetOverviewQuery.invoke(self, ((query, ), context))

    def SetOverviewQueryAsync(self, query: str, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Applies the specified query string to the active overview. This enables filtering the overview
        root items with the specified conditions.
        
        Equivalent to Search > Filter in the GUI software.
        
        Parameters
        ----------
        query : str
            the query to apply
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return AnalyzerRemoteControl._op_SetOverviewQuery.invokeAsync(self, ((query, ), context))

    def OverviewRootItem(self, context: dict[str, str] | None = None) -> int:
        """
        The root item is a conceptual item that contains all the items displayed in the overview. The
        overview content is a tree structure where each item can have sub-items, called children. Fully
        traversing such a tree structure can be implemented as a recursive iteration. The root item is
        not a visible item and is just used of the purpose of iterating the tree structure.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        int
            handle to the active overview's root item
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_OverviewRootItem.invoke(self, ((), context))

    def OverviewRootItemAsync(self, context: dict[str, str] | None = None) -> Awaitable[int]:
        """
        The root item is a conceptual item that contains all the items displayed in the overview. The
        overview content is a tree structure where each item can have sub-items, called children. Fully
        traversing such a tree structure can be implemented as a recursive iteration. The root item is
        not a visible item and is just used of the purpose of iterating the tree structure.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[int]
            handle to the active overview's root item
        """
        return AnalyzerRemoteControl._op_OverviewRootItem.invokeAsync(self, ((), context))

    def GetOverviewItemDescription(self, itemHandle: int, context: dict[str, str] | None = None) -> str:
        """
        This method returns the string of the Item column for a given item handle.
        
        Parameters
        ----------
        itemHandle : int
            handle of the item, either from OverviewRootItem() or GetOverviewItemChild()
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        str
            string of the Item column for a given item handle
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_GetOverviewItemDescription.invoke(self, ((itemHandle, ), context))

    def GetOverviewItemDescriptionAsync(self, itemHandle: int, context: dict[str, str] | None = None) -> Awaitable[str]:
        """
        This method returns the string of the Item column for a given item handle.
        
        Parameters
        ----------
        itemHandle : int
            handle of the item, either from OverviewRootItem() or GetOverviewItemChild()
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[str]
            string of the Item column for a given item handle
        """
        return AnalyzerRemoteControl._op_GetOverviewItemDescription.invokeAsync(self, ((itemHandle, ), context))

    def GetOverviewItemsDescription(self, itemHandles: Sequence[int] | Buffer, context: dict[str, str] | None = None) -> list[str]:
        """
        This method returns the strings of the Item column for the specified item handles.
        
        Parameters
        ----------
        itemHandles : Sequence[int] | Buffer
            handles of the items
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        list[str]
            strings of the Item column for the specified item handles
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_GetOverviewItemsDescription.invoke(self, ((itemHandles, ), context))

    def GetOverviewItemsDescriptionAsync(self, itemHandles: Sequence[int] | Buffer, context: dict[str, str] | None = None) -> Awaitable[list[str]]:
        """
        This method returns the strings of the Item column for the specified item handles.
        
        Parameters
        ----------
        itemHandles : Sequence[int] | Buffer
            handles of the items
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[list[str]]
            strings of the Item column for the specified item handles
        """
        return AnalyzerRemoteControl._op_GetOverviewItemsDescription.invokeAsync(self, ((itemHandles, ), context))

    def GetOverviewItemTimeInPicoseconds(self, itemHandle: int, context: dict[str, str] | None = None) -> int:
        """
        This method returns the time in picoseconds for a given item handle.
        
        Parameters
        ----------
        itemHandle : int
            handle of the item, either from OverviewRootItem() or GetOverviewItemChild()
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        int
            time in picoseconds for a given item handle
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_GetOverviewItemTimeInPicoseconds.invoke(self, ((itemHandle, ), context))

    def GetOverviewItemTimeInPicosecondsAsync(self, itemHandle: int, context: dict[str, str] | None = None) -> Awaitable[int]:
        """
        This method returns the time in picoseconds for a given item handle.
        
        Parameters
        ----------
        itemHandle : int
            handle of the item, either from OverviewRootItem() or GetOverviewItemChild()
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[int]
            time in picoseconds for a given item handle
        """
        return AnalyzerRemoteControl._op_GetOverviewItemTimeInPicoseconds.invokeAsync(self, ((itemHandle, ), context))

    def GetOverviewItemsTimeInPicoseconds(self, itemHandles: Sequence[int] | Buffer, context: dict[str, str] | None = None) -> list[int]:
        """
        This method returns the times in picoseconds for the specified items handles.
        
        Parameters
        ----------
        itemHandles : Sequence[int] | Buffer
            handles of the items
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        list[int]
            time in picoseconds for the specified items handles
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_GetOverviewItemsTimeInPicoseconds.invoke(self, ((itemHandles, ), context))

    def GetOverviewItemsTimeInPicosecondsAsync(self, itemHandles: Sequence[int] | Buffer, context: dict[str, str] | None = None) -> Awaitable[list[int]]:
        """
        This method returns the times in picoseconds for the specified items handles.
        
        Parameters
        ----------
        itemHandles : Sequence[int] | Buffer
            handles of the items
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[list[int]]
            time in picoseconds for the specified items handles
        """
        return AnalyzerRemoteControl._op_GetOverviewItemsTimeInPicoseconds.invokeAsync(self, ((itemHandles, ), context))

    def GetOverviewItemData(self, itemHandle: int, context: dict[str, str] | None = None) -> bytes:
        """
        This method returns the data displayed in the Raw data view for the specified item handle.
        
        Parameters
        ----------
        itemHandle : int
            handle of the item, either from OverviewRootItem() or GetOverviewItemChild()
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        bytes
            data displayed in the Raw data view for the specified item handle
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_GetOverviewItemData.invoke(self, ((itemHandle, ), context))

    def GetOverviewItemDataAsync(self, itemHandle: int, context: dict[str, str] | None = None) -> Awaitable[bytes]:
        """
        This method returns the data displayed in the Raw data view for the specified item handle.
        
        Parameters
        ----------
        itemHandle : int
            handle of the item, either from OverviewRootItem() or GetOverviewItemChild()
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[bytes]
            data displayed in the Raw data view for the specified item handle
        """
        return AnalyzerRemoteControl._op_GetOverviewItemData.invokeAsync(self, ((itemHandle, ), context))

    def GetOverviewItemsData(self, itemHandles: Sequence[int] | Buffer, context: dict[str, str] | None = None) -> list[bytes]:
        """
        This method returns the data displayed in the Raw data view for the specified items handles.
        
        Parameters
        ----------
        itemHandles : Sequence[int] | Buffer
            handles of the items
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        list[bytes]
            data displayed in the Raw data view for the specified item handle
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_GetOverviewItemsData.invoke(self, ((itemHandles, ), context))

    def GetOverviewItemsDataAsync(self, itemHandles: Sequence[int] | Buffer, context: dict[str, str] | None = None) -> Awaitable[list[bytes]]:
        """
        This method returns the data displayed in the Raw data view for the specified items handles.
        
        Parameters
        ----------
        itemHandles : Sequence[int] | Buffer
            handles of the items
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[list[bytes]]
            data displayed in the Raw data view for the specified item handle
        """
        return AnalyzerRemoteControl._op_GetOverviewItemsData.invokeAsync(self, ((itemHandles, ), context))

    def GetOverviewItemXmlReport(self, itemHandle: int, context: dict[str, str] | None = None) -> str:
        """
        This method returns the content of the Details view as XML for the specified item handle. This
        XML can then be decoded by using any standard XML parser.
        
        Parameters
        ----------
        itemHandle : int
            handle of the item, either from OverviewRootItem() or GetOverviewItemChild()
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        str
            content of the Details view as XML for the specified item handle
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_GetOverviewItemXmlReport.invoke(self, ((itemHandle, ), context))

    def GetOverviewItemXmlReportAsync(self, itemHandle: int, context: dict[str, str] | None = None) -> Awaitable[str]:
        """
        This method returns the content of the Details view as XML for the specified item handle. This
        XML can then be decoded by using any standard XML parser.
        
        Parameters
        ----------
        itemHandle : int
            handle of the item, either from OverviewRootItem() or GetOverviewItemChild()
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[str]
            content of the Details view as XML for the specified item handle
        """
        return AnalyzerRemoteControl._op_GetOverviewItemXmlReport.invokeAsync(self, ((itemHandle, ), context))

    def GetOverviewItemsXmlReport(self, itemHandles: Sequence[int] | Buffer, context: dict[str, str] | None = None) -> list[str]:
        """
        This method returns the content of the Details view as XML for the specified items handles. This
        XML can then be decoded by using any standard XML parser.
        
        Parameters
        ----------
        itemHandles : Sequence[int] | Buffer
            handles of the items
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        list[str]
            content of the Details view as XML for the specified items handles
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_GetOverviewItemsXmlReport.invoke(self, ((itemHandles, ), context))

    def GetOverviewItemsXmlReportAsync(self, itemHandles: Sequence[int] | Buffer, context: dict[str, str] | None = None) -> Awaitable[list[str]]:
        """
        This method returns the content of the Details view as XML for the specified items handles. This
        XML can then be decoded by using any standard XML parser.
        
        Parameters
        ----------
        itemHandles : Sequence[int] | Buffer
            handles of the items
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[list[str]]
            content of the Details view as XML for the specified items handles
        """
        return AnalyzerRemoteControl._op_GetOverviewItemsXmlReport.invokeAsync(self, ((itemHandles, ), context))

    def GetOverviewItemXmlReportFiltered(self, itemHandle: int, fieldNameFilters: Sequence[str], context: dict[str, str] | None = None) -> str:
        """
        This method returns the content of the Details view as XML for the specified item handle as
        above, but only the fields matching the fieldNameFilters will be returned.
        
        Parameters
        ----------
        itemHandle : int
            handle of the item, either from OverviewRootItem() or GetOverviewItemChild()
        fieldNameFilters : Sequence[str]
            list of inclusion filters. The filters can be specific field names, and
            accept wildcards such as * and ? , or a regular expression, in which case the string shall start
            by regex: followed by the regular expression. More information about the supported regex format: https://learn.microsoft.com/en-us/dotnet/standard/base-types/regular-expression-language-quick-reference[.NET regular expression reference]
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        str
            content of the Details view as XML for the specified item handle
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_GetOverviewItemXmlReportFiltered.invoke(self, ((itemHandle, fieldNameFilters), context))

    def GetOverviewItemXmlReportFilteredAsync(self, itemHandle: int, fieldNameFilters: Sequence[str], context: dict[str, str] | None = None) -> Awaitable[str]:
        """
        This method returns the content of the Details view as XML for the specified item handle as
        above, but only the fields matching the fieldNameFilters will be returned.
        
        Parameters
        ----------
        itemHandle : int
            handle of the item, either from OverviewRootItem() or GetOverviewItemChild()
        fieldNameFilters : Sequence[str]
            list of inclusion filters. The filters can be specific field names, and
            accept wildcards such as * and ? , or a regular expression, in which case the string shall start
            by regex: followed by the regular expression. More information about the supported regex format: https://learn.microsoft.com/en-us/dotnet/standard/base-types/regular-expression-language-quick-reference[.NET regular expression reference]
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[str]
            content of the Details view as XML for the specified item handle
        """
        return AnalyzerRemoteControl._op_GetOverviewItemXmlReportFiltered.invokeAsync(self, ((itemHandle, fieldNameFilters), context))

    def GetOverviewItemsXmlReportFiltered(self, itemHandles: Sequence[int] | Buffer, fieldNameFilters: Sequence[str], context: dict[str, str] | None = None) -> list[str]:
        """
        This method returns the content of the Details view as XML for the specified items handles as
        above, but only the fields matching the fieldNameFilters will be returned.
        
        Parameters
        ----------
        itemHandles : Sequence[int] | Buffer
            handle of the items
        fieldNameFilters : Sequence[str]
            list of inclusion filters. The filters can be specific field names, and
            accept wildcards such as * and ? , or a regular expression, in which case the string shall start
            by regex: followed by the regular expression. More information about the supported regex format: https://learn.microsoft.com/en-us/dotnet/standard/base-types/regular-expression-language-quick-reference[.NET regular expression reference]
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        list[str]
            content of the Details view as XML for the specified items handles
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_GetOverviewItemsXmlReportFiltered.invoke(self, ((itemHandles, fieldNameFilters), context))

    def GetOverviewItemsXmlReportFilteredAsync(self, itemHandles: Sequence[int] | Buffer, fieldNameFilters: Sequence[str], context: dict[str, str] | None = None) -> Awaitable[list[str]]:
        """
        This method returns the content of the Details view as XML for the specified items handles as
        above, but only the fields matching the fieldNameFilters will be returned.
        
        Parameters
        ----------
        itemHandles : Sequence[int] | Buffer
            handle of the items
        fieldNameFilters : Sequence[str]
            list of inclusion filters. The filters can be specific field names, and
            accept wildcards such as * and ? , or a regular expression, in which case the string shall start
            by regex: followed by the regular expression. More information about the supported regex format: https://learn.microsoft.com/en-us/dotnet/standard/base-types/regular-expression-language-quick-reference[.NET regular expression reference]
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[list[str]]
            content of the Details view as XML for the specified items handles
        """
        return AnalyzerRemoteControl._op_GetOverviewItemsXmlReportFiltered.invokeAsync(self, ((itemHandles, fieldNameFilters), context))

    def GetOverviewItemChildCount(self, itemHandle: int, context: dict[str, str] | None = None) -> int:
        """
        This method returns the child count for the specified item handle.
        
        Parameters
        ----------
        itemHandle : int
            handle of the item, either from OverviewRootItem() or GetOverviewItemChild()
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        int
            child count for the specified item handle
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_GetOverviewItemChildCount.invoke(self, ((itemHandle, ), context))

    def GetOverviewItemChildCountAsync(self, itemHandle: int, context: dict[str, str] | None = None) -> Awaitable[int]:
        """
        This method returns the child count for the specified item handle.
        
        Parameters
        ----------
        itemHandle : int
            handle of the item, either from OverviewRootItem() or GetOverviewItemChild()
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[int]
            child count for the specified item handle
        """
        return AnalyzerRemoteControl._op_GetOverviewItemChildCount.invokeAsync(self, ((itemHandle, ), context))

    def GetOverviewItemChild(self, itemHandle: int, childIndex: int, context: dict[str, str] | None = None) -> int:
        """
        This method returns the child item handle corresponding to a given index for the specified item
        handle.
        
        Parameters
        ----------
        itemHandle : int
            handle of the item, either from OverviewRootItem() or GetOverviewItemChild()
        childIndex : int
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        int
            child item handle corresponding to a given index for the specified item handle
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_GetOverviewItemChild.invoke(self, ((itemHandle, childIndex), context))

    def GetOverviewItemChildAsync(self, itemHandle: int, childIndex: int, context: dict[str, str] | None = None) -> Awaitable[int]:
        """
        This method returns the child item handle corresponding to a given index for the specified item
        handle.
        
        Parameters
        ----------
        itemHandle : int
            handle of the item, either from OverviewRootItem() or GetOverviewItemChild()
        childIndex : int
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[int]
            child item handle corresponding to a given index for the specified item handle
        """
        return AnalyzerRemoteControl._op_GetOverviewItemChild.invokeAsync(self, ((itemHandle, childIndex), context))

    def GetOverviewItemChildren(self, itemHandle: int, childIndex: int, childCount: int, context: dict[str, str] | None = None) -> list[int]:
        """
        This method returns the quantity of requested children items handles starting from the specified
        index for the specified item handle.
        
        Parameters
        ----------
        itemHandle : int
            handle of the item, either from OverviewRootItem() or GetOverviewItemChild()
        childIndex : int
            index of the first child to be returned
        childCount : int
            count of children to be returned
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        list[int]
            child item handle corresponding to a given index for the specified item handle
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_GetOverviewItemChildren.invoke(self, ((itemHandle, childIndex, childCount), context))

    def GetOverviewItemChildrenAsync(self, itemHandle: int, childIndex: int, childCount: int, context: dict[str, str] | None = None) -> Awaitable[list[int]]:
        """
        This method returns the quantity of requested children items handles starting from the specified
        index for the specified item handle.
        
        Parameters
        ----------
        itemHandle : int
            handle of the item, either from OverviewRootItem() or GetOverviewItemChild()
        childIndex : int
            index of the first child to be returned
        childCount : int
            count of children to be returned
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[list[int]]
            child item handle corresponding to a given index for the specified item handle
        """
        return AnalyzerRemoteControl._op_GetOverviewItemChildren.invokeAsync(self, ((itemHandle, childIndex, childCount), context))

    def SearchOverviewItems(self, itemHandle: int, childIndex: int, childCount: int, maxDepth: int, descriptionFilters: Sequence[str], fieldNameFilters: Sequence[str], fieldValueFilters: Sequence[str], context: dict[str, str] | None = None) -> list[int]:
        """
        This method searches the specified filters in the children items of the specified parent item,
        going through the specified max depth. The value and field name filters can be used as follows:
        
        - If fieldNameFilters is null, then the item will be kept if any field value matches any value
        filter.
        - If fieldNameFilters is not null and fieldValueFilters is null, then the item will be kept if
        any field name matches any name filter.
        - If both fieldNameFilters and fieldValueFilters are not null, then both arrays must be of the
        same size. If a field matches a field name filter, the field's value will be matched against
        the corresponding index in the value filters. So in other terms, fieldNameFilters[0] is
        related to fieldValueFilters[0], fieldNameFilters[1] is related to fieldValueFilters[1], etc.
        The item will be retained if any field matches any filter.
        
        Parameters
        ----------
        itemHandle : int
            handle of the item, either from OverviewRootItem() or GetOverviewItemChild()
        childIndex : int
            index of the first child of the item to search from
        childCount : int
            quantity of children of the item to search into
        maxDepth : int
            maximum depth to go through the children. For example, a value of 1 will return
            only the direct children of the item.
        descriptionFilters : Sequence[str]
            inclusion filters matching the item description. The filters accepts
            wildcards such as * and ?, or a regular expression, in which case the string shall start by
            regex: followed by the regular expression. Can be null if no filtering is required.
        fieldNameFilters : Sequence[str]
            inclusion filters matching a fields names in the report. The filters
            accepts wildcards such as * and ?, or a regular expression, in which case the string shall start
            by regex: followed by the regular expression. Can be null if no filtering is required.
        fieldValueFilters : Sequence[str]
            inclusion filters matching fields values in the report. The filters
            accepts wildcards such as * and ?, or a regular expression, in which case the string shall start
            by regex: followed by the regular expression. Can be null if no filtering is required. More
            information about the supported regex format: https://learn.microsoft.com/en-us/dotnet/standard/base-types/regular-expression-language-quick-reference[.NET regular expression reference]
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        list[int]
            children items handles for the specified parent item handle, through the specified max
            depth, and matching the specified filters
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_SearchOverviewItems.invoke(self, ((itemHandle, childIndex, childCount, maxDepth, descriptionFilters, fieldNameFilters, fieldValueFilters), context))

    def SearchOverviewItemsAsync(self, itemHandle: int, childIndex: int, childCount: int, maxDepth: int, descriptionFilters: Sequence[str], fieldNameFilters: Sequence[str], fieldValueFilters: Sequence[str], context: dict[str, str] | None = None) -> Awaitable[list[int]]:
        """
        This method searches the specified filters in the children items of the specified parent item,
        going through the specified max depth. The value and field name filters can be used as follows:
        
        - If fieldNameFilters is null, then the item will be kept if any field value matches any value
        filter.
        - If fieldNameFilters is not null and fieldValueFilters is null, then the item will be kept if
        any field name matches any name filter.
        - If both fieldNameFilters and fieldValueFilters are not null, then both arrays must be of the
        same size. If a field matches a field name filter, the field's value will be matched against
        the corresponding index in the value filters. So in other terms, fieldNameFilters[0] is
        related to fieldValueFilters[0], fieldNameFilters[1] is related to fieldValueFilters[1], etc.
        The item will be retained if any field matches any filter.
        
        Parameters
        ----------
        itemHandle : int
            handle of the item, either from OverviewRootItem() or GetOverviewItemChild()
        childIndex : int
            index of the first child of the item to search from
        childCount : int
            quantity of children of the item to search into
        maxDepth : int
            maximum depth to go through the children. For example, a value of 1 will return
            only the direct children of the item.
        descriptionFilters : Sequence[str]
            inclusion filters matching the item description. The filters accepts
            wildcards such as * and ?, or a regular expression, in which case the string shall start by
            regex: followed by the regular expression. Can be null if no filtering is required.
        fieldNameFilters : Sequence[str]
            inclusion filters matching a fields names in the report. The filters
            accepts wildcards such as * and ?, or a regular expression, in which case the string shall start
            by regex: followed by the regular expression. Can be null if no filtering is required.
        fieldValueFilters : Sequence[str]
            inclusion filters matching fields values in the report. The filters
            accepts wildcards such as * and ?, or a regular expression, in which case the string shall start
            by regex: followed by the regular expression. Can be null if no filtering is required. More
            information about the supported regex format: https://learn.microsoft.com/en-us/dotnet/standard/base-types/regular-expression-language-quick-reference[.NET regular expression reference]
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[list[int]]
            children items handles for the specified parent item handle, through the specified max
            depth, and matching the specified filters
        """
        return AnalyzerRemoteControl._op_SearchOverviewItems.invokeAsync(self, ((itemHandle, childIndex, childCount, maxDepth, descriptionFilters, fieldNameFilters, fieldValueFilters), context))

    def ReleaseAllOverviewItemHandles(self, context: dict[str, str] | None = None) -> None:
        """
        This method releases all item handles allocated by GetOverviewItemChild() or
        GetOverviewItemChildren(). It is useful to release allocated handles after allocating a large
        quantity of handles to avoid excessive memory consumption in the analysis application.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_ReleaseAllOverviewItemHandles.invoke(self, ((), context))

    def ReleaseAllOverviewItemHandlesAsync(self, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        This method releases all item handles allocated by GetOverviewItemChild() or
        GetOverviewItemChildren(). It is useful to release allocated handles after allocating a large
        quantity of handles to avoid excessive memory consumption in the analysis application.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return AnalyzerRemoteControl._op_ReleaseAllOverviewItemHandles.invokeAsync(self, ((), context))

    def SelectOverviewItem(self, itemHandle: int, context: dict[str, str] | None = None) -> None:
        """
        Highlights the specified item in the active overview.
        
        Parameters
        ----------
        itemHandle : int
            Item to be highlighted
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_SelectOverviewItem.invoke(self, ((itemHandle, ), context))

    def SelectOverviewItemAsync(self, itemHandle: int, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Highlights the specified item in the active overview.
        
        Parameters
        ----------
        itemHandle : int
            Item to be highlighted
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return AnalyzerRemoteControl._op_SelectOverviewItem.invokeAsync(self, ((itemHandle, ), context))

    def GetSelectedOverviewItem(self, context: dict[str, str] | None = None) -> int:
        """
        Returns the selected overview item handle.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        int
            Item handle highlighted in the active overview
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_GetSelectedOverviewItem.invoke(self, ((), context))

    def GetSelectedOverviewItemAsync(self, context: dict[str, str] | None = None) -> Awaitable[int]:
        """
        Returns the selected overview item handle.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[int]
            Item handle highlighted in the active overview
        """
        return AnalyzerRemoteControl._op_GetSelectedOverviewItem.invokeAsync(self, ((), context))

    def GetLogicSignalsState(self, timeInPicoseconds: int, context: dict[str, str] | None = None) -> int:
        """
        This method returns the state of all logic signals at the specified time. The returned logic
        signals state contain the state of all signals. Bit 0 corresponds to logic signal 0, bit 1 to
        logic signal 1, etc.
        
        Parameters
        ----------
        timeInPicoseconds : int
            time at which the logic signals state shall be retrieved
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        int
        int
            state of all logic signals at the specified time
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_GetLogicSignalsState.invoke(self, ((timeInPicoseconds, ), context))

    def GetLogicSignalsStateAsync(self, timeInPicoseconds: int, context: dict[str, str] | None = None) -> Awaitable[int]:
        """
        This method returns the state of all logic signals at the specified time. The returned logic
        signals state contain the state of all signals. Bit 0 corresponds to logic signal 0, bit 1 to
        logic signal 1, etc.
        
        Parameters
        ----------
        timeInPicoseconds : int
            time at which the logic signals state shall be retrieved
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[int]
        int
            state of all logic signals at the specified time
        """
        return AnalyzerRemoteControl._op_GetLogicSignalsState.invokeAsync(self, ((timeInPicoseconds, ), context))

    def FindLogicSignalsTransition(self, fromTimeInPicoseconds: int, toTimeInPicoseconds: int, signalsMask: int, transitionType: LogicSignalTransitionType, context: dict[str, str] | None = None) -> tuple[int, int]:
        """
        This method searches a certain transition in the specified time range, for the specified
        signals. The desired signals should be set to 1 in the signalsMask to be included. For example
        if signals 0, 2, and 3 should be searched, the corresponding binary mask shall be 1101 (bits 0,
        2 and 3 set), which is 0xD in hexadecimal.
        
        Parameters
        ----------
        fromTimeInPicoseconds : int
            time from which to search for the logic transition
        toTimeInPicoseconds : int
            time to which to search for the logic transition
        signalsMask : int
            mask indicating which signals to search
        transitionType : LogicSignalTransitionType
            specifies if the searched transition is rising edge, falling edge, or any
            edge
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        tuple[int, int]
        
            A tuple containing:
                - int state of all logic signals at the specified time
                - int time at which the condition is found
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_FindLogicSignalsTransition.invoke(self, ((fromTimeInPicoseconds, toTimeInPicoseconds, signalsMask, transitionType), context))

    def FindLogicSignalsTransitionAsync(self, fromTimeInPicoseconds: int, toTimeInPicoseconds: int, signalsMask: int, transitionType: LogicSignalTransitionType, context: dict[str, str] | None = None) -> Awaitable[tuple[int, int]]:
        """
        This method searches a certain transition in the specified time range, for the specified
        signals. The desired signals should be set to 1 in the signalsMask to be included. For example
        if signals 0, 2, and 3 should be searched, the corresponding binary mask shall be 1101 (bits 0,
        2 and 3 set), which is 0xD in hexadecimal.
        
        Parameters
        ----------
        fromTimeInPicoseconds : int
            time from which to search for the logic transition
        toTimeInPicoseconds : int
            time to which to search for the logic transition
        signalsMask : int
            mask indicating which signals to search
        transitionType : LogicSignalTransitionType
            specifies if the searched transition is rising edge, falling edge, or any
            edge
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[tuple[int, int]]
        
            A tuple containing:
                - int state of all logic signals at the specified time
                - int time at which the condition is found
        """
        return AnalyzerRemoteControl._op_FindLogicSignalsTransition.invokeAsync(self, ((fromTimeInPicoseconds, toTimeInPicoseconds, signalsMask, transitionType), context))

    def GetRunningTasks(self, context: dict[str, str] | None = None) -> list[RunningTask]:
        """
        Returns the currently running tasks of the software, such as recording, saving, filtering,
        loading, etc.
        
        Equivalent to the Tasks view.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        list[RunningTask]
            Array of running tasks.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_GetRunningTasks.invoke(self, ((), context))

    def GetRunningTasksAsync(self, context: dict[str, str] | None = None) -> Awaitable[list[RunningTask]]:
        """
        Returns the currently running tasks of the software, such as recording, saving, filtering,
        loading, etc.
        
        Equivalent to the Tasks view.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[list[RunningTask]]
            Array of running tasks.
        """
        return AnalyzerRemoteControl._op_GetRunningTasks.invokeAsync(self, ((), context))

    def AbortRunningTask(self, name: str, context: dict[str, str] | None = None) -> None:
        """
        Aborts the specified task if running.
        
        Equivalent to canceling a task in the Tasks view.
        
        Parameters
        ----------
        name : str
            Name of the task to be aborted
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_AbortRunningTask.invoke(self, ((name, ), context))

    def AbortRunningTaskAsync(self, name: str, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Aborts the specified task if running.
        
        Equivalent to canceling a task in the Tasks view.
        
        Parameters
        ----------
        name : str
            Name of the task to be aborted
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return AnalyzerRemoteControl._op_AbortRunningTask.invokeAsync(self, ((name, ), context))

    def GetSettings(self, context: dict[str, str] | None = None) -> bytes:
        """
        Retrieve the current settings.
        
        Equivalent to File > Import and Export settings > Export settings in the GUI software.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        bytes
            Settings in binary form
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_GetSettings.invoke(self, ((), context))

    def GetSettingsAsync(self, context: dict[str, str] | None = None) -> Awaitable[bytes]:
        """
        Retrieve the current settings.
        
        Equivalent to File > Import and Export settings > Export settings in the GUI software.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[bytes]
            Settings in binary form
        """
        return AnalyzerRemoteControl._op_GetSettings.invokeAsync(self, ((), context))

    def ConfigureSettings(self, settings: Sequence[int] | bytes | Buffer, context: dict[str, str] | None = None) -> None:
        """
        Configure the software with the specified settings. The provided settings can be saved directly
        from the GUI software in order to create a few different configurations, or can be created
        dynamically.
        
        Equivalent to File > Import and Export settings > Import settings in the GUI software.
        
        Parameters
        ----------
        settings : Sequence[int] | bytes | Buffer
            content of a file created from File > Import and Export settings > Export
            settings
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_ConfigureSettings.invoke(self, ((settings, ), context))

    def ConfigureSettingsAsync(self, settings: Sequence[int] | bytes | Buffer, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Configure the software with the specified settings. The provided settings can be saved directly
        from the GUI software in order to create a few different configurations, or can be created
        dynamically.
        
        Equivalent to File > Import and Export settings > Import settings in the GUI software.
        
        Parameters
        ----------
        settings : Sequence[int] | bytes | Buffer
            content of a file created from File > Import and Export settings > Export
            settings
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return AnalyzerRemoteControl._op_ConfigureSettings.invokeAsync(self, ((settings, ), context))

    def CancelUserInteraction(self, context: dict[str, str] | None = None) -> None:
        """
        Cancels any message that might block the UI waiting for an user input.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_CancelUserInteraction.invoke(self, ((), context))

    def CancelUserInteractionAsync(self, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Cancels any message that might block the UI waiting for an user input.
        
        Parameters
        ----------
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return AnalyzerRemoteControl._op_CancelUserInteraction.invokeAsync(self, ((), context))

    def InsertComment(self, comment: str, overviewName: str, context: dict[str, str] | None = None) -> None:
        """
        Insert a comment item in the selected overview at the current time. This function can only be
        called during recording. *Obsolete:* This method is deprecated, use InsertMessage instead.
        
        Parameters
        ----------
        comment : str
            text of the comment
        overviewName : str
            name of the overview where the comment shall be inserted
        context : dict[str, str]
            The request context for the invocation.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        return AnalyzerRemoteControl._op_InsertComment.invoke(self, ((comment, overviewName), context))

    def InsertCommentAsync(self, comment: str, overviewName: str, context: dict[str, str] | None = None) -> Awaitable[None]:
        """
        Insert a comment item in the selected overview at the current time. This function can only be
        called during recording. *Obsolete:* This method is deprecated, use InsertMessage instead.
        
        Parameters
        ----------
        comment : str
            text of the comment
        overviewName : str
            name of the overview where the comment shall be inserted
        context : dict[str, str]
            The request context for the invocation.
        
        Returns
        -------
        Awaitable[None]
            An awaitable that is completed when the invocation completes.
        """
        return AnalyzerRemoteControl._op_InsertComment.invokeAsync(self, ((comment, overviewName), context))

    @staticmethod
    def checkedCast(
        proxy: ObjectPrx | None,
        facet: str | None = None,
        context: dict[str, str] | None = None
    ) -> AnalyzerRemoteControlPrx | None:
        return checkedCast(AnalyzerRemoteControlPrx, proxy, facet, context)

    @staticmethod
    def checkedCastAsync(
        proxy: ObjectPrx | None,
        facet: str | None = None,
        context: dict[str, str] | None = None
    ) -> Awaitable[AnalyzerRemoteControlPrx | None ]:
        return checkedCastAsync(AnalyzerRemoteControlPrx, proxy, facet, context)

    @overload
    @staticmethod
    def uncheckedCast(proxy: ObjectPrx, facet: str | None = None) -> AnalyzerRemoteControlPrx:
        ...

    @overload
    @staticmethod
    def uncheckedCast(proxy: None, facet: str | None = None) -> None:
        ...

    @staticmethod
    def uncheckedCast(proxy: ObjectPrx | None, facet: str | None = None) -> AnalyzerRemoteControlPrx | None:
        return uncheckedCast(AnalyzerRemoteControlPrx, proxy, facet)

    @staticmethod
    def ice_staticId() -> str:
        return "::Ellisys::Platform::NetworkRemoteControl::Analyzer::AnalyzerRemoteControl"

IcePy.defineProxy("::Ellisys::Platform::NetworkRemoteControl::Analyzer::AnalyzerRemoteControl", AnalyzerRemoteControlPrx)

class AnalyzerRemoteControl(Object, ABC):
    """
    Generic remote-control operations common to every Ellisys analyzer.
    
    Notes
    -----
        The Slice compiler generated this skeleton class from Slice interface ``::Ellisys::Platform::NetworkRemoteControl::Analyzer::AnalyzerRemoteControl``.
    """

    _ice_ids: Sequence[str] = ("::Ellisys::Platform::NetworkRemoteControl::Analyzer::AnalyzerRemoteControl", "::Ice::Object", )
    _op_GetAppInfo: IcePy.Operation
    _op_ExitApp: IcePy.Operation
    _op_GetAvailableDataSources: IcePy.Operation
    _op_SelectDataSource: IcePy.Operation
    _op_GetSelectedDataSource: IcePy.Operation
    _op_IsRecording: IcePy.Operation
    _op_GetRecordingStatus: IcePy.Operation
    _op_StartRecording: IcePy.Operation
    _op_StopRecordingAndSaveTraceFile: IcePy.Operation
    _op_AbortRecordingAndDiscardTraceFile: IcePy.Operation
    _op_GetRecordingOptions: IcePy.Operation
    _op_ConfigureRecordingOptions: IcePy.Operation
    _op_InsertMessage: IcePy.Operation
    _op_IsLoading: IcePy.Operation
    _op_StartLoading: IcePy.Operation
    _op_GetTraceFileInfo: IcePy.Operation
    _op_CloseTraceFile: IcePy.Operation
    _op_IsModified: IcePy.Operation
    _op_SaveChanges: IcePy.Operation
    _op_AddMarkerOnSelectedOverviewItem: IcePy.Operation
    _op_AddMarkerAtTime: IcePy.Operation
    _op_GetMarkers: IcePy.Operation
    _op_Export: IcePy.Operation
    _op_GetAvailableOverviews: IcePy.Operation
    _op_GetSelectedOverview: IcePy.Operation
    _op_SelectOverview: IcePy.Operation
    _op_GetAvailableProtocolLayers: IcePy.Operation
    _op_GetSelectedProtocolLayer: IcePy.Operation
    _op_SelectProtocolLayer: IcePy.Operation
    _op_GetOverviewQuery: IcePy.Operation
    _op_SetOverviewQuery: IcePy.Operation
    _op_OverviewRootItem: IcePy.Operation
    _op_GetOverviewItemDescription: IcePy.Operation
    _op_GetOverviewItemsDescription: IcePy.Operation
    _op_GetOverviewItemTimeInPicoseconds: IcePy.Operation
    _op_GetOverviewItemsTimeInPicoseconds: IcePy.Operation
    _op_GetOverviewItemData: IcePy.Operation
    _op_GetOverviewItemsData: IcePy.Operation
    _op_GetOverviewItemXmlReport: IcePy.Operation
    _op_GetOverviewItemsXmlReport: IcePy.Operation
    _op_GetOverviewItemXmlReportFiltered: IcePy.Operation
    _op_GetOverviewItemsXmlReportFiltered: IcePy.Operation
    _op_GetOverviewItemChildCount: IcePy.Operation
    _op_GetOverviewItemChild: IcePy.Operation
    _op_GetOverviewItemChildren: IcePy.Operation
    _op_SearchOverviewItems: IcePy.Operation
    _op_ReleaseAllOverviewItemHandles: IcePy.Operation
    _op_SelectOverviewItem: IcePy.Operation
    _op_GetSelectedOverviewItem: IcePy.Operation
    _op_GetLogicSignalsState: IcePy.Operation
    _op_FindLogicSignalsTransition: IcePy.Operation
    _op_GetRunningTasks: IcePy.Operation
    _op_AbortRunningTask: IcePy.Operation
    _op_GetSettings: IcePy.Operation
    _op_ConfigureSettings: IcePy.Operation
    _op_CancelUserInteraction: IcePy.Operation
    _op_InsertComment: IcePy.Operation

    @staticmethod
    def ice_staticId() -> str:
        return "::Ellisys::Platform::NetworkRemoteControl::Analyzer::AnalyzerRemoteControl"

    @abstractmethod
    def GetAppInfo(self, current: Current) -> AppInfo | Awaitable[AppInfo]:
        """
        Returns information about the remote application, such as version, file extension, etc.
        
        Parameters
        ----------
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        AppInfo | Awaitable[AppInfo]
            Application info.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def ExitApp(self, current: Current) -> None | Awaitable[None]:
        """
        Exits the remote application.
        
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
    def GetAvailableDataSources(self, current: Current) -> Sequence[str] | Awaitable[Sequence[str]]:
        """
        Returns the available analyzers accessible by the analysis software.
        
        Equivalent to list of the Record menu > Select analyzer dialog.
        
        Parameters
        ----------
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        Sequence[str] | Awaitable[Sequence[str]]
            Array of available data sources.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def SelectDataSource(self, dataSourceUniqueId: str, current: Current) -> None | Awaitable[None]:
        """
        Select the active data source for capturing data. This is typically a string returned from the
        GetAvailableDataSources() function.
        
        Equivalent to selecting an analyzer from the Record menu > Select analyzer dialog.
        
        Parameters
        ----------
        dataSourceUniqueId : str
            unique ID of the data source to select
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
    def GetSelectedDataSource(self, current: Current) -> str | Awaitable[str]:
        """
        Returns the currently selected analyzers, if any.
        
        Parameters
        ----------
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        str | Awaitable[str]
            Analyzer currently selected.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def IsRecording(self, current: Current) -> bool | Awaitable[bool]:
        """
        Indicates if a recording is currently running.
        
        Parameters
        ----------
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        bool | Awaitable[bool]
            true if the analyzer is currently capturing data following the call of the
            StartRecording() method, false otherwise
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def GetRecordingStatus(self, current: Current) -> RecordingStatus | Awaitable[RecordingStatus]:
        """
        Returns information on the running recording, such as the analyzer, the duration and trace size.
        
        Parameters
        ----------
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        RecordingStatus | Awaitable[RecordingStatus]
            Status of the recording
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def StartRecording(self, current: Current) -> None | Awaitable[None]:
        """
        Starts the analyzer capture with the current settings. The settings can be either configured
        manually in the GUI software or configured with the ConfigureSettings() method.
        
        Equivalent to Record > Start recording in the GUI software.
        
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
    def StopRecordingAndSaveTraceFile(self, filename: str, overwrite: bool, current: Current) -> None | Awaitable[None]:
        """
        Stops the analyzer capture and save the resulting file to the specified filename.
        
        Equivalent to Record > Stop recording followed by File > Save in the GUI software.
        
        Parameters
        ----------
        filename : str
            path to the file to be saved, based on the remote computer
        overwrite : bool
            destination filename will be replaced if already exists
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
    def AbortRecordingAndDiscardTraceFile(self, current: Current) -> None | Awaitable[None]:
        """
        Aborts the ongoing capture and discard any captured data.
        
        Equivalent to Record > Stop recording followed by File > New in the GUI software.
        
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
    def GetRecordingOptions(self, relevantOnly: bool, current: Current) -> str | Awaitable[str]:
        """
        Retrieve the current recording options in JSON format.
        
        Equivalent to Record > Recording Options > Save in the GUI software.
        
        Parameters
        ----------
        relevantOnly : bool
            indicates if the function shall return only the fields which are set with
            non-default values, or if default values shall be returned as well.
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        str | Awaitable[str]
            JSON formatted-string containing the recording options
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def ConfigureRecordingOptions(self, options: str, current: Current) -> None | Awaitable[None]:
        """
        Configure the recording options of the data source. The provided settings can be saved from the
        Recording Options dialog of the GUI software or can be created manually.
        
        The format of the options string is a modified JSON format with the following customizations to
        the standard JSON format:
        
        - The root object braces can be omitted. For example, "{ field:value }" can optionally be
        expressed as "field:value" for brevity.
        - The name double quotes can be omitted. For example, "field":"value" can optionally be
        expressed as field: "value" for brevity.
        - Encapsulated parent objects having a single child object can use the '.' hierarchical
        notation. For example, "a:{ b:value }" can optionally be expressed as "a.b:value" for brevity.
        
        The provided string can contain only the fields to be updated.
        
        Equivalent to Record > Recording Options > Load in the GUI software.
        
        Parameters
        ----------
        options : str
            recording options in extended JSON format
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
    def InsertMessage(self, severity: MessageSeverity, message: str, current: Current) -> None | Awaitable[None]:
        """
        Insert a message in the Message Log overview at the current time. This function can only be
        called during recording. The message can either be raw text, or hierarchically formatted text
        in JSON or XML.
        
        The JSON format is as follows:
        
        ----
        {
        fields:[
        { field:"field1", value:[
        { field:"field2", value:"value2" },
        { field:"field3", value:"value3" }
        ] }
        ]
        }
        ----
        
        The XML format is as follows:
        
        ----
        <fields>
        <field name="field1">
        <field name="field2">value2</field>
        <field name="field3">value3</field>
        </field>
        </fields>
        ----
        
        Parameters
        ----------
        severity : MessageSeverity
            indicates if this message is an information, a warning or an error
        message : str
            the message that will be inserted, either in raw text, JSON or XML
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
    def IsLoading(self, current: Current) -> bool | Awaitable[bool]:
        """
        Indicates if the software is loading a trace.
        
        Parameters
        ----------
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        bool | Awaitable[bool]
            true if the file is loading, false otherwise.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def StartLoading(self, filename: str, current: Current) -> None | Awaitable[None]:
        """
        Starts loading the specified filename.
        
        Equivalent to File > Open in the GUI software.
        
        Parameters
        ----------
        filename : str
            path to the file to be loaded, based on the remote computer
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
    def GetTraceFileInfo(self, current: Current) -> TraceFileInfo | Awaitable[TraceFileInfo]:
        """
        Returns information on the loaded trace file, such as the size, start date, analyzer used and
        software version.
        
        Parameters
        ----------
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        TraceFileInfo | Awaitable[TraceFileInfo]
            Information on the loaded trace file
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def CloseTraceFile(self, current: Current) -> None | Awaitable[None]:
        """
        Close the loaded trace file. Changes will be lost if any, unless saved explicitly with
        SaveChanges().
        
        Equivalent to File > New in the GUI software.
        
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
    def IsModified(self, current: Current) -> bool | Awaitable[bool]:
        """
        Indicates if the open file has changes. The changes can be saved with SaveChanges().
        
        Parameters
        ----------
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        bool | Awaitable[bool]
            true if the open file has changes, false otherwise
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def SaveChanges(self, current: Current) -> None | Awaitable[None]:
        """
        Save changes in the currently open file.
        
        Equivalent to File > Save in the GUI software.
        
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
    def AddMarkerOnSelectedOverviewItem(self, marker: AddMarker, current: Current) -> None | Awaitable[None]:
        """
        Adds a marker on the currently selected item in the Overview.
        
        Equivalent to main toolbar > Markers > Mark selected item in the GUI software.
        
        Parameters
        ----------
        marker : AddMarker
            information on the marker to be added
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
    def AddMarkerAtTime(self, timeInPicoseconds: int, marker: AddMarker, current: Current) -> None | Awaitable[None]:
        """
        Adds a marker at the specified time.
        
        Equivalent to Instant Timing > Right Click Menu > Add new marker here in the GUI software.
        
        Parameters
        ----------
        timeInPicoseconds : int
            the time in picoseconds of the marker to be added
        marker : AddMarker
            information on the marker to be added
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
    def GetMarkers(self, current: Current) -> Sequence[GetMarker] | Awaitable[Sequence[GetMarker]]:
        """
        Get all markers of the trace file.
        
        Parameters
        ----------
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        Sequence[GetMarker] | Awaitable[Sequence[GetMarker]]
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def Export(self, outputFilename: str, exportName: str, exportOptions: list[ExportOption], current: Current) -> None | Awaitable[None]:
        """
        Export the specified data to the output filename with the specified options. The options are
        optional and are specific to the export mode. The available export modes are described in the following entries.
        
        Parameters
        ----------
        outputFilename : str
        exportName : str
        exportOptions : list[ExportOption]
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
    def GetAvailableOverviews(self, current: Current) -> Sequence[str] | Awaitable[Sequence[str]]:
        """
        Get the list of available overviews.
        
        Parameters
        ----------
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        Sequence[str] | Awaitable[Sequence[str]]
            the list of available overviews
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def GetSelectedOverview(self, current: Current) -> str | Awaitable[str]:
        """
        Retrieve the active overview.
        
        Parameters
        ----------
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        str | Awaitable[str]
            the name of the active overview
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def SelectOverview(self, overviewName: str, current: Current) -> None | Awaitable[None]:
        """
        This method makes a given overview active. All the methods for navigating the overview tree
        structure will work in the active overview so it is required to first ensure the overview is
        active. For example SelectOverview("USB 3.0") will make the USB 3.0 Overview active.
        
        Parameters
        ----------
        overviewName : str
            Name of the overview to select
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
    def GetAvailableProtocolLayers(self, current: Current) -> Sequence[str] | Awaitable[Sequence[str]]:
        """
        Get the list of available protocol layers.
        
        Parameters
        ----------
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        Sequence[str] | Awaitable[Sequence[str]]
            the list of available protocol layers
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def GetSelectedProtocolLayer(self, current: Current) -> str | Awaitable[str]:
        """
        Retrieve the current protocol layer in the active overview.
        
        Parameters
        ----------
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        str | Awaitable[str]
            the selected protocol layer
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def SelectProtocolLayer(self, protocolLayerName: str, current: Current) -> None | Awaitable[None]:
        """
        This method will switch the protocol layer in the active overview. It is equivalent to clicking
        the protocol layers buttons in the GUI.
        
        Parameters
        ----------
        protocolLayerName : str
            Name of the protocol layer to select, as displayed in the popup on the
            button in the GUI
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
    def GetOverviewQuery(self, current: Current) -> str | Awaitable[str]:
        """
        Retrieve the current query in the active overview.
        
        Parameters
        ----------
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        str | Awaitable[str]
            the current query if any, empty string otherwise
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def SetOverviewQuery(self, query: str, current: Current) -> None | Awaitable[None]:
        """
        Applies the specified query string to the active overview. This enables filtering the overview
        root items with the specified conditions.
        
        Equivalent to Search > Filter in the GUI software.
        
        Parameters
        ----------
        query : str
            the query to apply
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
    def OverviewRootItem(self, current: Current) -> int | Awaitable[int]:
        """
        The root item is a conceptual item that contains all the items displayed in the overview. The
        overview content is a tree structure where each item can have sub-items, called children. Fully
        traversing such a tree structure can be implemented as a recursive iteration. The root item is
        not a visible item and is just used of the purpose of iterating the tree structure.
        
        Parameters
        ----------
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        int | Awaitable[int]
            handle to the active overview's root item
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def GetOverviewItemDescription(self, itemHandle: int, current: Current) -> str | Awaitable[str]:
        """
        This method returns the string of the Item column for a given item handle.
        
        Parameters
        ----------
        itemHandle : int
            handle of the item, either from OverviewRootItem() or GetOverviewItemChild()
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        str | Awaitable[str]
            string of the Item column for a given item handle
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def GetOverviewItemsDescription(self, itemHandles: list[int], current: Current) -> Sequence[str] | Awaitable[Sequence[str]]:
        """
        This method returns the strings of the Item column for the specified item handles.
        
        Parameters
        ----------
        itemHandles : list[int]
            handles of the items
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        Sequence[str] | Awaitable[Sequence[str]]
            strings of the Item column for the specified item handles
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def GetOverviewItemTimeInPicoseconds(self, itemHandle: int, current: Current) -> int | Awaitable[int]:
        """
        This method returns the time in picoseconds for a given item handle.
        
        Parameters
        ----------
        itemHandle : int
            handle of the item, either from OverviewRootItem() or GetOverviewItemChild()
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        int | Awaitable[int]
            time in picoseconds for a given item handle
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def GetOverviewItemsTimeInPicoseconds(self, itemHandles: list[int], current: Current) -> Sequence[int] | Buffer | Awaitable[Sequence[int] | Buffer]:
        """
        This method returns the times in picoseconds for the specified items handles.
        
        Parameters
        ----------
        itemHandles : list[int]
            handles of the items
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        Sequence[int] | Buffer | Awaitable[Sequence[int] | Buffer]
            time in picoseconds for the specified items handles
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def GetOverviewItemData(self, itemHandle: int, current: Current) -> Sequence[int] | bytes | Buffer | Awaitable[Sequence[int] | bytes | Buffer]:
        """
        This method returns the data displayed in the Raw data view for the specified item handle.
        
        Parameters
        ----------
        itemHandle : int
            handle of the item, either from OverviewRootItem() or GetOverviewItemChild()
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        Sequence[int] | bytes | Buffer | Awaitable[Sequence[int] | bytes | Buffer]
            data displayed in the Raw data view for the specified item handle
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def GetOverviewItemsData(self, itemHandles: list[int], current: Current) -> Sequence[Sequence[int] | bytes | Buffer] | Awaitable[Sequence[Sequence[int] | bytes | Buffer]]:
        """
        This method returns the data displayed in the Raw data view for the specified items handles.
        
        Parameters
        ----------
        itemHandles : list[int]
            handles of the items
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        Sequence[Sequence[int] | bytes | Buffer] | Awaitable[Sequence[Sequence[int] | bytes | Buffer]]
            data displayed in the Raw data view for the specified item handle
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def GetOverviewItemXmlReport(self, itemHandle: int, current: Current) -> str | Awaitable[str]:
        """
        This method returns the content of the Details view as XML for the specified item handle. This
        XML can then be decoded by using any standard XML parser.
        
        Parameters
        ----------
        itemHandle : int
            handle of the item, either from OverviewRootItem() or GetOverviewItemChild()
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        str | Awaitable[str]
            content of the Details view as XML for the specified item handle
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def GetOverviewItemsXmlReport(self, itemHandles: list[int], current: Current) -> Sequence[str] | Awaitable[Sequence[str]]:
        """
        This method returns the content of the Details view as XML for the specified items handles. This
        XML can then be decoded by using any standard XML parser.
        
        Parameters
        ----------
        itemHandles : list[int]
            handles of the items
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        Sequence[str] | Awaitable[Sequence[str]]
            content of the Details view as XML for the specified items handles
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def GetOverviewItemXmlReportFiltered(self, itemHandle: int, fieldNameFilters: list[str], current: Current) -> str | Awaitable[str]:
        """
        This method returns the content of the Details view as XML for the specified item handle as
        above, but only the fields matching the fieldNameFilters will be returned.
        
        Parameters
        ----------
        itemHandle : int
            handle of the item, either from OverviewRootItem() or GetOverviewItemChild()
        fieldNameFilters : list[str]
            list of inclusion filters. The filters can be specific field names, and
            accept wildcards such as * and ? , or a regular expression, in which case the string shall start
            by regex: followed by the regular expression. More information about the supported regex format: https://learn.microsoft.com/en-us/dotnet/standard/base-types/regular-expression-language-quick-reference[.NET regular expression reference]
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        str | Awaitable[str]
            content of the Details view as XML for the specified item handle
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def GetOverviewItemsXmlReportFiltered(self, itemHandles: list[int], fieldNameFilters: list[str], current: Current) -> Sequence[str] | Awaitable[Sequence[str]]:
        """
        This method returns the content of the Details view as XML for the specified items handles as
        above, but only the fields matching the fieldNameFilters will be returned.
        
        Parameters
        ----------
        itemHandles : list[int]
            handle of the items
        fieldNameFilters : list[str]
            list of inclusion filters. The filters can be specific field names, and
            accept wildcards such as * and ? , or a regular expression, in which case the string shall start
            by regex: followed by the regular expression. More information about the supported regex format: https://learn.microsoft.com/en-us/dotnet/standard/base-types/regular-expression-language-quick-reference[.NET regular expression reference]
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        Sequence[str] | Awaitable[Sequence[str]]
            content of the Details view as XML for the specified items handles
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def GetOverviewItemChildCount(self, itemHandle: int, current: Current) -> int | Awaitable[int]:
        """
        This method returns the child count for the specified item handle.
        
        Parameters
        ----------
        itemHandle : int
            handle of the item, either from OverviewRootItem() or GetOverviewItemChild()
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        int | Awaitable[int]
            child count for the specified item handle
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def GetOverviewItemChild(self, itemHandle: int, childIndex: int, current: Current) -> int | Awaitable[int]:
        """
        This method returns the child item handle corresponding to a given index for the specified item
        handle.
        
        Parameters
        ----------
        itemHandle : int
            handle of the item, either from OverviewRootItem() or GetOverviewItemChild()
        childIndex : int
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        int | Awaitable[int]
            child item handle corresponding to a given index for the specified item handle
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def GetOverviewItemChildren(self, itemHandle: int, childIndex: int, childCount: int, current: Current) -> Sequence[int] | Buffer | Awaitable[Sequence[int] | Buffer]:
        """
        This method returns the quantity of requested children items handles starting from the specified
        index for the specified item handle.
        
        Parameters
        ----------
        itemHandle : int
            handle of the item, either from OverviewRootItem() or GetOverviewItemChild()
        childIndex : int
            index of the first child to be returned
        childCount : int
            count of children to be returned
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        Sequence[int] | Buffer | Awaitable[Sequence[int] | Buffer]
            child item handle corresponding to a given index for the specified item handle
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def SearchOverviewItems(self, itemHandle: int, childIndex: int, childCount: int, maxDepth: int, descriptionFilters: list[str], fieldNameFilters: list[str], fieldValueFilters: list[str], current: Current) -> Sequence[int] | Buffer | Awaitable[Sequence[int] | Buffer]:
        """
        This method searches the specified filters in the children items of the specified parent item,
        going through the specified max depth. The value and field name filters can be used as follows:
        
        - If fieldNameFilters is null, then the item will be kept if any field value matches any value
        filter.
        - If fieldNameFilters is not null and fieldValueFilters is null, then the item will be kept if
        any field name matches any name filter.
        - If both fieldNameFilters and fieldValueFilters are not null, then both arrays must be of the
        same size. If a field matches a field name filter, the field's value will be matched against
        the corresponding index in the value filters. So in other terms, fieldNameFilters[0] is
        related to fieldValueFilters[0], fieldNameFilters[1] is related to fieldValueFilters[1], etc.
        The item will be retained if any field matches any filter.
        
        Parameters
        ----------
        itemHandle : int
            handle of the item, either from OverviewRootItem() or GetOverviewItemChild()
        childIndex : int
            index of the first child of the item to search from
        childCount : int
            quantity of children of the item to search into
        maxDepth : int
            maximum depth to go through the children. For example, a value of 1 will return
            only the direct children of the item.
        descriptionFilters : list[str]
            inclusion filters matching the item description. The filters accepts
            wildcards such as * and ?, or a regular expression, in which case the string shall start by
            regex: followed by the regular expression. Can be null if no filtering is required.
        fieldNameFilters : list[str]
            inclusion filters matching a fields names in the report. The filters
            accepts wildcards such as * and ?, or a regular expression, in which case the string shall start
            by regex: followed by the regular expression. Can be null if no filtering is required.
        fieldValueFilters : list[str]
            inclusion filters matching fields values in the report. The filters
            accepts wildcards such as * and ?, or a regular expression, in which case the string shall start
            by regex: followed by the regular expression. Can be null if no filtering is required. More
            information about the supported regex format: https://learn.microsoft.com/en-us/dotnet/standard/base-types/regular-expression-language-quick-reference[.NET regular expression reference]
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        Sequence[int] | Buffer | Awaitable[Sequence[int] | Buffer]
            children items handles for the specified parent item handle, through the specified max
            depth, and matching the specified filters
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def ReleaseAllOverviewItemHandles(self, current: Current) -> None | Awaitable[None]:
        """
        This method releases all item handles allocated by GetOverviewItemChild() or
        GetOverviewItemChildren(). It is useful to release allocated handles after allocating a large
        quantity of handles to avoid excessive memory consumption in the analysis application.
        
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
    def SelectOverviewItem(self, itemHandle: int, current: Current) -> None | Awaitable[None]:
        """
        Highlights the specified item in the active overview.
        
        Parameters
        ----------
        itemHandle : int
            Item to be highlighted
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
    def GetSelectedOverviewItem(self, current: Current) -> int | Awaitable[int]:
        """
        Returns the selected overview item handle.
        
        Parameters
        ----------
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        int | Awaitable[int]
            Item handle highlighted in the active overview
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def GetLogicSignalsState(self, timeInPicoseconds: int, current: Current) -> int | Awaitable[int]:
        """
        This method returns the state of all logic signals at the specified time. The returned logic
        signals state contain the state of all signals. Bit 0 corresponds to logic signal 0, bit 1 to
        logic signal 1, etc.
        
        Parameters
        ----------
        timeInPicoseconds : int
            time at which the logic signals state shall be retrieved
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        int | Awaitable[int]
        int
            state of all logic signals at the specified time
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def FindLogicSignalsTransition(self, fromTimeInPicoseconds: int, toTimeInPicoseconds: int, signalsMask: int, transitionType: LogicSignalTransitionType, current: Current) -> tuple[int, int] | Awaitable[tuple[int, int]]:
        """
        This method searches a certain transition in the specified time range, for the specified
        signals. The desired signals should be set to 1 in the signalsMask to be included. For example
        if signals 0, 2, and 3 should be searched, the corresponding binary mask shall be 1101 (bits 0,
        2 and 3 set), which is 0xD in hexadecimal.
        
        Parameters
        ----------
        fromTimeInPicoseconds : int
            time from which to search for the logic transition
        toTimeInPicoseconds : int
            time to which to search for the logic transition
        signalsMask : int
            mask indicating which signals to search
        transitionType : LogicSignalTransitionType
            specifies if the searched transition is rising edge, falling edge, or any
            edge
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        tuple[int, int] | Awaitable[tuple[int, int]]
        
            A tuple containing:
                - int state of all logic signals at the specified time
                - int time at which the condition is found
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def GetRunningTasks(self, current: Current) -> Sequence[RunningTask] | Awaitable[Sequence[RunningTask]]:
        """
        Returns the currently running tasks of the software, such as recording, saving, filtering,
        loading, etc.
        
        Equivalent to the Tasks view.
        
        Parameters
        ----------
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        Sequence[RunningTask] | Awaitable[Sequence[RunningTask]]
            Array of running tasks.
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def AbortRunningTask(self, name: str, current: Current) -> None | Awaitable[None]:
        """
        Aborts the specified task if running.
        
        Equivalent to canceling a task in the Tasks view.
        
        Parameters
        ----------
        name : str
            Name of the task to be aborted
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
    def GetSettings(self, current: Current) -> Sequence[int] | bytes | Buffer | Awaitable[Sequence[int] | bytes | Buffer]:
        """
        Retrieve the current settings.
        
        Equivalent to File > Import and Export settings > Export settings in the GUI software.
        
        Parameters
        ----------
        current : Ice.Current
            The Current object for the dispatch.
        
        Returns
        -------
        Sequence[int] | bytes | Buffer | Awaitable[Sequence[int] | bytes | Buffer]
            Settings in binary form
        
        Raises
        ------
        OperationFailed
            if the operation cannot be completed.
        """
        pass

    @abstractmethod
    def ConfigureSettings(self, settings: bytes, current: Current) -> None | Awaitable[None]:
        """
        Configure the software with the specified settings. The provided settings can be saved directly
        from the GUI software in order to create a few different configurations, or can be created
        dynamically.
        
        Equivalent to File > Import and Export settings > Import settings in the GUI software.
        
        Parameters
        ----------
        settings : bytes
            content of a file created from File > Import and Export settings > Export
            settings
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
    def CancelUserInteraction(self, current: Current) -> None | Awaitable[None]:
        """
        Cancels any message that might block the UI waiting for an user input.
        
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
    def InsertComment(self, comment: str, overviewName: str, current: Current) -> None | Awaitable[None]:
        """
        Insert a comment item in the selected overview at the current time. This function can only be
        called during recording. *Obsolete:* This method is deprecated, use InsertMessage instead.
        
        Parameters
        ----------
        comment : str
            text of the comment
        overviewName : str
            name of the overview where the comment shall be inserted
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

AnalyzerRemoteControl._op_GetAppInfo = IcePy.Operation(
    "GetAppInfo",
    "GetAppInfo",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_AppInfo_t, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_ExitApp = IcePy.Operation(
    "ExitApp",
    "ExitApp",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_GetAvailableDataSources = IcePy.Operation(
    "GetAvailableDataSources",
    "GetAvailableDataSources",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_StringArray_t, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_SelectDataSource = IcePy.Operation(
    "SelectDataSource",
    "SelectDataSource",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_string, False, 0),),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_GetSelectedDataSource = IcePy.Operation(
    "GetSelectedDataSource",
    "GetSelectedDataSource",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    ((), IcePy._t_string, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_IsRecording = IcePy.Operation(
    "IsRecording",
    "IsRecording",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    ((), IcePy._t_bool, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_GetRecordingStatus = IcePy.Operation(
    "GetRecordingStatus",
    "GetRecordingStatus",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_RecordingStatus_t, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_StartRecording = IcePy.Operation(
    "StartRecording",
    "StartRecording",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_StopRecordingAndSaveTraceFile = IcePy.Operation(
    "StopRecordingAndSaveTraceFile",
    "StopRecordingAndSaveTraceFile",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_string, False, 0), ((), IcePy._t_bool, False, 0)),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_AbortRecordingAndDiscardTraceFile = IcePy.Operation(
    "AbortRecordingAndDiscardTraceFile",
    "AbortRecordingAndDiscardTraceFile",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_GetRecordingOptions = IcePy.Operation(
    "GetRecordingOptions",
    "GetRecordingOptions",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_bool, False, 0),),
    (),
    ((), IcePy._t_string, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_ConfigureRecordingOptions = IcePy.Operation(
    "ConfigureRecordingOptions",
    "ConfigureRecordingOptions",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_string, False, 0),),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_InsertMessage = IcePy.Operation(
    "InsertMessage",
    "InsertMessage",
    OperationMode.Normal,
    None,
    (),
    (((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_MessageSeverity_t, False, 0), ((), IcePy._t_string, False, 0)),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_IsLoading = IcePy.Operation(
    "IsLoading",
    "IsLoading",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    ((), IcePy._t_bool, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_StartLoading = IcePy.Operation(
    "StartLoading",
    "StartLoading",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_string, False, 0),),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_GetTraceFileInfo = IcePy.Operation(
    "GetTraceFileInfo",
    "GetTraceFileInfo",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_TraceFileInfo_t, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_CloseTraceFile = IcePy.Operation(
    "CloseTraceFile",
    "CloseTraceFile",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_IsModified = IcePy.Operation(
    "IsModified",
    "IsModified",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    ((), IcePy._t_bool, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_SaveChanges = IcePy.Operation(
    "SaveChanges",
    "SaveChanges",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_AddMarkerOnSelectedOverviewItem = IcePy.Operation(
    "AddMarkerOnSelectedOverviewItem",
    "AddMarkerOnSelectedOverviewItem",
    OperationMode.Normal,
    None,
    (),
    (((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_AddMarker_t, False, 0),),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_AddMarkerAtTime = IcePy.Operation(
    "AddMarkerAtTime",
    "AddMarkerAtTime",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_long, False, 0), ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_AddMarker_t, False, 0)),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_GetMarkers = IcePy.Operation(
    "GetMarkers",
    "GetMarkers",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_GetMarkerArray_t, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_Export = IcePy.Operation(
    "Export",
    "Export",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_string, False, 0), ((), IcePy._t_string, False, 0), ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_ExportOptionArray_t, False, 0)),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_GetAvailableOverviews = IcePy.Operation(
    "GetAvailableOverviews",
    "GetAvailableOverviews",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_StringArray_t, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_GetSelectedOverview = IcePy.Operation(
    "GetSelectedOverview",
    "GetSelectedOverview",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    ((), IcePy._t_string, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_SelectOverview = IcePy.Operation(
    "SelectOverview",
    "SelectOverview",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_string, False, 0),),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_GetAvailableProtocolLayers = IcePy.Operation(
    "GetAvailableProtocolLayers",
    "GetAvailableProtocolLayers",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_StringArray_t, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_GetSelectedProtocolLayer = IcePy.Operation(
    "GetSelectedProtocolLayer",
    "GetSelectedProtocolLayer",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    ((), IcePy._t_string, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_SelectProtocolLayer = IcePy.Operation(
    "SelectProtocolLayer",
    "SelectProtocolLayer",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_string, False, 0),),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_GetOverviewQuery = IcePy.Operation(
    "GetOverviewQuery",
    "GetOverviewQuery",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    ((), IcePy._t_string, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_SetOverviewQuery = IcePy.Operation(
    "SetOverviewQuery",
    "SetOverviewQuery",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_string, False, 0),),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_OverviewRootItem = IcePy.Operation(
    "OverviewRootItem",
    "OverviewRootItem",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    ((), IcePy._t_int, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_GetOverviewItemDescription = IcePy.Operation(
    "GetOverviewItemDescription",
    "GetOverviewItemDescription",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_int, False, 0),),
    (),
    ((), IcePy._t_string, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_GetOverviewItemsDescription = IcePy.Operation(
    "GetOverviewItemsDescription",
    "GetOverviewItemsDescription",
    OperationMode.Normal,
    None,
    (),
    (((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_HandleArray_t, False, 0),),
    (),
    ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_StringArray_t, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_GetOverviewItemTimeInPicoseconds = IcePy.Operation(
    "GetOverviewItemTimeInPicoseconds",
    "GetOverviewItemTimeInPicoseconds",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_int, False, 0),),
    (),
    ((), IcePy._t_long, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_GetOverviewItemsTimeInPicoseconds = IcePy.Operation(
    "GetOverviewItemsTimeInPicoseconds",
    "GetOverviewItemsTimeInPicoseconds",
    OperationMode.Normal,
    None,
    (),
    (((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_HandleArray_t, False, 0),),
    (),
    ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_TimeArray_t, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_GetOverviewItemData = IcePy.Operation(
    "GetOverviewItemData",
    "GetOverviewItemData",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_int, False, 0),),
    (),
    ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_ByteArray_t, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_GetOverviewItemsData = IcePy.Operation(
    "GetOverviewItemsData",
    "GetOverviewItemsData",
    OperationMode.Normal,
    None,
    (),
    (((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_HandleArray_t, False, 0),),
    (),
    ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_ByteArrays_t, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_GetOverviewItemXmlReport = IcePy.Operation(
    "GetOverviewItemXmlReport",
    "GetOverviewItemXmlReport",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_int, False, 0),),
    (),
    ((), IcePy._t_string, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_GetOverviewItemsXmlReport = IcePy.Operation(
    "GetOverviewItemsXmlReport",
    "GetOverviewItemsXmlReport",
    OperationMode.Normal,
    None,
    (),
    (((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_HandleArray_t, False, 0),),
    (),
    ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_StringArray_t, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_GetOverviewItemXmlReportFiltered = IcePy.Operation(
    "GetOverviewItemXmlReportFiltered",
    "GetOverviewItemXmlReportFiltered",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_int, False, 0), ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_StringArray_t, False, 0)),
    (),
    ((), IcePy._t_string, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_GetOverviewItemsXmlReportFiltered = IcePy.Operation(
    "GetOverviewItemsXmlReportFiltered",
    "GetOverviewItemsXmlReportFiltered",
    OperationMode.Normal,
    None,
    (),
    (((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_HandleArray_t, False, 0), ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_StringArray_t, False, 0)),
    (),
    ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_StringArray_t, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_GetOverviewItemChildCount = IcePy.Operation(
    "GetOverviewItemChildCount",
    "GetOverviewItemChildCount",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_int, False, 0),),
    (),
    ((), IcePy._t_int, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_GetOverviewItemChild = IcePy.Operation(
    "GetOverviewItemChild",
    "GetOverviewItemChild",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_int, False, 0), ((), IcePy._t_int, False, 0)),
    (),
    ((), IcePy._t_int, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_GetOverviewItemChildren = IcePy.Operation(
    "GetOverviewItemChildren",
    "GetOverviewItemChildren",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_int, False, 0), ((), IcePy._t_int, False, 0), ((), IcePy._t_int, False, 0)),
    (),
    ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_HandleArray_t, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_SearchOverviewItems = IcePy.Operation(
    "SearchOverviewItems",
    "SearchOverviewItems",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_int, False, 0), ((), IcePy._t_int, False, 0), ((), IcePy._t_int, False, 0), ((), IcePy._t_int, False, 0), ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_StringArray_t, False, 0), ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_StringArray_t, False, 0), ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_StringArray_t, False, 0)),
    (),
    ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_HandleArray_t, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_ReleaseAllOverviewItemHandles = IcePy.Operation(
    "ReleaseAllOverviewItemHandles",
    "ReleaseAllOverviewItemHandles",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_SelectOverviewItem = IcePy.Operation(
    "SelectOverviewItem",
    "SelectOverviewItem",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_int, False, 0),),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_GetSelectedOverviewItem = IcePy.Operation(
    "GetSelectedOverviewItem",
    "GetSelectedOverviewItem",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    ((), IcePy._t_int, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_GetLogicSignalsState = IcePy.Operation(
    "GetLogicSignalsState",
    "GetLogicSignalsState",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_long, False, 0),),
    (((), IcePy._t_int, False, 0),),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_FindLogicSignalsTransition = IcePy.Operation(
    "FindLogicSignalsTransition",
    "FindLogicSignalsTransition",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_long, False, 0), ((), IcePy._t_long, False, 0), ((), IcePy._t_int, False, 0), ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_LogicSignalTransitionType_t, False, 0)),
    (((), IcePy._t_int, False, 0), ((), IcePy._t_long, False, 0)),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_GetRunningTasks = IcePy.Operation(
    "GetRunningTasks",
    "GetRunningTasks",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_RunningTaskArray_t, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_AbortRunningTask = IcePy.Operation(
    "AbortRunningTask",
    "AbortRunningTask",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_string, False, 0),),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_GetSettings = IcePy.Operation(
    "GetSettings",
    "GetSettings",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    ((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_ByteArray_t, False, 0),
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_ConfigureSettings = IcePy.Operation(
    "ConfigureSettings",
    "ConfigureSettings",
    OperationMode.Normal,
    None,
    (),
    (((), _Ellisys_Platform_NetworkRemoteControl_Analyzer_ByteArray_t, False, 0),),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_CancelUserInteraction = IcePy.Operation(
    "CancelUserInteraction",
    "CancelUserInteraction",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

AnalyzerRemoteControl._op_InsertComment = IcePy.Operation(
    "InsertComment",
    "InsertComment",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_string, False, 0), ((), IcePy._t_string, False, 0)),
    (),
    None,
    (_Ellisys_Platform_NetworkRemoteControl_Analyzer_OperationFailed_t,),
    False)

__all__ = ["AnalyzerRemoteControl", "AnalyzerRemoteControlPrx", "_Ellisys_Platform_NetworkRemoteControl_Analyzer_AnalyzerRemoteControlPrx_t"]
