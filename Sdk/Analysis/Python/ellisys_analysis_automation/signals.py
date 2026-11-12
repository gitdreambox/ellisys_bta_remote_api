"""Logic-signal queries: the signal-state bitmask and transition search.

Logic signals are the analyzer's digital I/O lines. State is returned as an ``int`` bitmask
where bit N is the level of logic signal N. These are base ``Analyzer`` operations (available
on analyzers that capture logic signals), not a product facet.
"""
from __future__ import annotations

import datetime
import enum
from dataclasses import dataclass

__all__ = ["LogicSignalTransitionType", "LogicSignalTransition"]


class LogicSignalTransitionType(enum.IntEnum):
    """Which edge to search for (mirrors the Slice ``LogicSignalTransitionType`` enum)."""

    ANY = 0
    RISING_EDGE = 1
    FALLING_EDGE = 2


@dataclass(frozen=True, slots=True)
class LogicSignalTransition:
    """A found logic-signal transition (-> FindLogicSignalsTransition)."""

    state: int        # bitmask of all signal levels at the transition (bit N == signal N)
    time_ps: int      # time of the transition, in picoseconds

    @property
    def time(self) -> datetime.timedelta:
        """The transition time as a :class:`datetime.timedelta` (microsecond resolution)."""
        return datetime.timedelta(microseconds=self.time_ps / 1_000_000)
