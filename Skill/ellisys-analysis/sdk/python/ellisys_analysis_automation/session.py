"""Typed results for the session / trace-file / info operations.

Frozen dataclasses mirroring the Slice structs (``AppInfo``, ``RecordingStatus``,
``TraceFileInfo``, ``RunningTask``) and the ``MessageSeverity`` enum. Each result has a private
``_from_ice`` classmethod that does the PascalCase->snake_case marshalling in one place.
"""
from __future__ import annotations

import datetime
import enum
from dataclasses import dataclass

__all__ = [
    "MessageSeverity",
    "AppInfo",
    "RecordingStatus",
    "RunningTask",
    "TraceFileInfo",
]

_UTC = datetime.timezone.utc


class MessageSeverity(enum.IntEnum):
    """Severity for :meth:`Analyzer.insert_message` (mirrors the Slice enum; 1-based)."""

    INFO = 1
    WARNING = 2
    ERROR = 3


@dataclass(frozen=True, slots=True)
class AppInfo:
    """Information about the remote application (-> GetAppInfo)."""

    id: str
    description: str
    version: str
    file_ext: str
    interactive: bool

    @classmethod
    def _from_ice(cls, s) -> "AppInfo":
        return cls(id=s.Id, description=s.Description, version=s.Version,
                   file_ext=s.FileExt, interactive=s.Interactive)


@dataclass(frozen=True, slots=True)
class RecordingStatus:
    """Status of the current recording (-> GetRecordingStatus)."""

    data_source: str
    duration_seconds: int
    file_size: int            # bytes

    @property
    def duration(self) -> datetime.timedelta:
        """``duration_seconds`` as a :class:`datetime.timedelta` (exact)."""
        return datetime.timedelta(seconds=self.duration_seconds)

    @classmethod
    def _from_ice(cls, s) -> "RecordingStatus":
        return cls(data_source=s.DataSource, duration_seconds=s.DurationSeconds, file_size=s.FileSize)


@dataclass(frozen=True, slots=True)
class RunningTask:
    """A background task running in the analyzer (-> GetRunningTasks)."""

    name: str
    progress_percent: int
    progress_applicable: bool

    @property
    def progress(self) -> int | None:
        """Percent complete, or ``None`` when the server says progress isn't meaningful."""
        return self.progress_percent if self.progress_applicable else None

    @classmethod
    def _from_ice(cls, s) -> "RunningTask":
        return cls(name=s.Name, progress_percent=s.ProgressPercent,
                   progress_applicable=s.ProgressApplicable)


@dataclass(frozen=True, slots=True)
class TraceFileInfo:
    """Information about the loaded trace file (-> GetTraceFileInfo)."""

    path: str
    file_size: int                  # bytes
    start_datetime_utc_raw: int     # raw Slice long: milliseconds since 2000-01-01 UTC (see started_at_utc)
    software_version: str
    data_source: str
    unique_id: str
    recording_options: str          # opaque blob (same string ConfigureRecordingOptions consumes)

    @property
    def started_at_utc(self) -> datetime.datetime | None:
        """The trace start time as a tz-aware UTC datetime, or ``None`` when the raw value is
        non-positive (unset). :attr:`start_datetime_utc_raw` is milliseconds since 2000-01-01 UTC
        (the epoch the analyzer's own trace indexer uses); reinterpret the raw value yourself if
        you ever need a different one.
        """
        raw = self.start_datetime_utc_raw
        if raw <= 0:
            return None
        return datetime.datetime(2000, 1, 1, tzinfo=_UTC) + datetime.timedelta(milliseconds=raw)

    @classmethod
    def _from_ice(cls, s) -> "TraceFileInfo":
        return cls(path=s.Path, file_size=s.FileSize, start_datetime_utc_raw=s.StartDateTimeUtc,
                   software_version=s.SoftwareVersion, data_source=s.DataSource,
                   unique_id=s.UniqueId, recording_options=s.RecordingOptions)
