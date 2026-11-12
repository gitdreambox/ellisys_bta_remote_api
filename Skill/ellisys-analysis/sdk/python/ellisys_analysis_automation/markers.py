"""Typed markers for annotating a trace.

:class:`MarkerColor` mirrors the analyzer's marker palette; :class:`Marker` is a handle-free
snapshot of a marker read back from the trace. The :class:`~ellisys_analysis_automation.Analyzer`
methods ``add_marker_at_time`` / ``add_marker_on_selected_overview_item`` / ``markers`` (and
:meth:`OverviewItem.add_marker`) bridge these to the Ice ``AddMarker`` / ``GetMarker`` types.
"""
from __future__ import annotations

import datetime
import enum
from dataclasses import dataclass

__all__ = ["MarkerColor", "Marker"]


class MarkerColor(enum.IntEnum):
    """A marker colour (values match the analyzer's ``MarkerColor`` Slice enum)."""

    YELLOW = 0
    BLUE = 1
    RED = 2
    GREEN = 3
    ORANGE = 4
    PURPLE = 5


@dataclass(frozen=True, slots=True)
class Marker:
    """A marker read from the trace (-> GetMarkers). Handle-free; ``time_ps`` is picoseconds."""

    color: MarkerColor
    text: str
    time_ps: int

    @property
    def time(self) -> datetime.timedelta:
        """``time_ps`` as a :class:`datetime.timedelta` (microsecond resolution)."""
        return datetime.timedelta(microseconds=self.time_ps / 1_000_000)

    @property
    def time_seconds(self) -> float:
        """``time_ps`` in seconds as a float."""
        return self.time_ps / 1e12
