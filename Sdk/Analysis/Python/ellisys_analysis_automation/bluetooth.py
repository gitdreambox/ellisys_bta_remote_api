"""The Bluetooth product facet, reached as ``analyzer.bluetooth``.

Exposes the Bluetooth-only operations of ``BluetoothAnalyzerRemoteControl`` as a Pythonic
sub-namespace on a connected :class:`~ellisys_analysis_automation.Analyzer`. Built on the shared
:class:`~ellisys_analysis_automation._facet._ProductFacet` (attach/plumbing); it reuses the analyzer's
``_call`` and base ``export()`` and adds only the Bluetooth operations, typed results, and the
Bluetooth export modes/options. Zero Ice types cross the public surface.
"""
from __future__ import annotations

import datetime
import enum
import os
from collections.abc import Sequence
from dataclasses import dataclass

from ._facet import DeviceFilterMode, _ProductFacet, _check_addr48
from .exports import ExportMode, _to_ps, _validate_range

__all__ = [
    "DeviceFilterMode",   # re-exported (shared, defined in _facet)
    "BluetoothChannelSummary",
    "BluetoothChannelStat",
    "BluetoothSpectrumSample",
    "BluetoothSpectrumRange",
    "BluetoothPacketLossMode",
    "BluetoothExportModes",
    "BluetoothAudioOptions",
    "BluetoothChannelsOptions",
    "BluetoothAirtimeOptions",
    "format_bluetooth_bdaddr",
]

_INT64_MAX = 2**63 - 1


@dataclass(frozen=True, slots=True)
class BluetoothChannelSummary:
    """Per-RF-channel packet tallies (-> Slice struct ``ChannelSummary``)."""

    ok: int
    retransmitted: int
    payload_error: int
    header_error: int
    not_applicable: int

    @property
    def errors(self) -> int:
        """Header + payload errors."""
        return self.payload_error + self.header_error

    @property
    def total(self) -> int:
        """Classified packets on this channel (excludes ``not_applicable``)."""
        return self.ok + self.retransmitted + self.payload_error + self.header_error

    @property
    def error_rate(self) -> float | None:
        """Fraction of classified packets in error, or ``None`` if the channel had no data."""
        return self.errors / self.total if self.total else None

    @classmethod
    def _from_ice(cls, s) -> "BluetoothChannelSummary":
        return cls(ok=s.Ok, retransmitted=s.Retransmitted, payload_error=s.PayloadError,
                   header_error=s.HeaderError, not_applicable=s.NotApplicable)


@dataclass(frozen=True, slots=True)
class BluetoothChannelStat:
    """An (RF channel, summary) pair -- the explicit-index view of channel summaries."""

    rf_channel: int
    summary: BluetoothChannelSummary


@dataclass(frozen=True, slots=True)
class BluetoothSpectrumSample:
    """One RSSI sample (-> GetSpectrumRssi)."""

    rssi_dbm: float
    start_ps: int
    stop_ps: int

    @property
    def window(self) -> datetime.timedelta:
        """Length of the sampling window (``stop_ps - start_ps``) as a timedelta."""
        return datetime.timedelta(microseconds=(self.stop_ps - self.start_ps) / 1_000_000)


@dataclass(frozen=True, slots=True)
class BluetoothSpectrumRange:
    """A series of RSSI samples over a window (-> GetSpectrumRssiRange)."""

    rssi_dbm: tuple[float, ...]
    start_ps: int
    stop_ps: int

    def __len__(self) -> int:
        return len(self.rssi_dbm)

    @property
    def window(self) -> datetime.timedelta:
        """Length of the sampling window (``stop_ps - start_ps``) as a timedelta."""
        return datetime.timedelta(microseconds=(self.stop_ps - self.start_ps) / 1_000_000)

    @property
    def mean_dbm(self) -> float | None:
        """Mean RSSI across the samples in dBm, or ``None`` if there are none."""
        return sum(self.rssi_dbm) / len(self.rssi_dbm) if self.rssi_dbm else None

    @property
    def min_dbm(self) -> float | None:
        """Lowest RSSI sample in dBm, or ``None`` if there are none."""
        return min(self.rssi_dbm) if self.rssi_dbm else None

    @property
    def max_dbm(self) -> float | None:
        """Highest RSSI sample in dBm, or ``None`` if there are none."""
        return max(self.rssi_dbm) if self.rssi_dbm else None


def format_bluetooth_bdaddr(addr: int) -> str:
    """Format a 48-bit BDADDR int as ``"AA:BB:CC:DD:EE:FF"`` (a convenience; the API uses ints)."""
    value = int(addr)
    return ":".join("{0:02X}".format((value >> (8 * i)) & 0xFF) for i in range(5, -1, -1))


# -- Bluetooth export modes + option carriers (product-specific; see exports.ExportMode) ----------
class BluetoothPacketLossMode(enum.StrEnum):
    """``bluetooth_audio`` PacketLoss option; each member's value is the exact server token."""

    NEGATIVE_DC = "NegativeDC"          # fill gaps with a negative-DC value (easy to spot)
    SILENCE = "Silence"                 # fill gaps with silence, no smoothing
    SILENCE_SMOOTH = "SilenceSmooth"    # fill gaps with silence, smoothed to conceal the gap


class BluetoothExportModes:
    """Bluetooth export modes (valid only on a Bluetooth analyzer). Enumerate via :attr:`ALL`."""

    AUDIO = ExportMode("bluetooth_audio", "bluetooth", "Bluetooth audio extraction.")
    MOBILE_PHONE_DATA = ExportMode(
        "bluetooth_mobile_phone_data", "bluetooth", "Bluetooth mobile phone data.")
    CHANNELS = ExportMode("bluetooth_channels", "bluetooth", "Bluetooth per-channel statistics.")
    AIRTIME = ExportMode("airtime", "bluetooth", "Airtime usage.")

    #: All Bluetooth modes (documentation, not a capability gate).
    ALL = (AUDIO, MOBILE_PHONE_DATA, CHANNELS, AIRTIME)


@dataclass(frozen=True, slots=True)
class BluetoothAudioOptions:
    """Options for ``bluetooth_audio`` (Bluetooth analyzers only)."""

    add_raw_payload_files: bool | None = None        # AddRawPayloadFiles
    synchro_buffer_ms: int | None = None             # SynchroBufferMilliseconds
    force_isochronous_buffering: bool | None = None   # ForceIsochronousBuffering
    packet_loss: BluetoothPacketLossMode | None = None  # PacketLoss

    def as_options(self) -> dict[str, object]:
        """The ``{server OptionName: value}`` mapping for this mode (unset options are dropped)."""
        return {
            "AddRawPayloadFiles": self.add_raw_payload_files,
            "SynchroBufferMilliseconds": self.synchro_buffer_ms,
            "ForceIsochronousBuffering": self.force_isochronous_buffering,
            "PacketLoss": self.packet_loss,
        }

    def validate(self) -> None:
        """No range constraints to check."""


@dataclass(frozen=True, slots=True)
class BluetoothChannelsOptions:
    """Options for ``bluetooth_channels`` (Bluetooth analyzers only)."""

    range_start_time_ps: int | datetime.timedelta | None = None  # RangeStartTime
    range_end_time_ps: int | datetime.timedelta | None = None    # RangeEndTime

    def as_options(self) -> dict[str, object]:
        """The ``{server OptionName: value}`` mapping for this mode (unset options are dropped)."""
        return {"RangeStartTime": self.range_start_time_ps, "RangeEndTime": self.range_end_time_ps}

    def validate(self) -> None:
        """Validate the range -- raises :class:`ExportOptionError` if range end precedes start."""
        _validate_range(self.range_start_time_ps, self.range_end_time_ps)


@dataclass(frozen=True, slots=True)
class BluetoothAirtimeOptions:
    """Options for ``airtime`` (Bluetooth analyzers only)."""

    range_start_time_ps: int | datetime.timedelta | None = None  # RangeStartTime
    range_end_time_ps: int | datetime.timedelta | None = None    # RangeEndTime

    def as_options(self) -> dict[str, object]:
        """The ``{server OptionName: value}`` mapping for this mode (unset options are dropped)."""
        return {"RangeStartTime": self.range_start_time_ps, "RangeEndTime": self.range_end_time_ps}

    def validate(self) -> None:
        """Validate the range -- raises :class:`ExportOptionError` if range end precedes start."""
        _validate_range(self.range_start_time_ps, self.range_end_time_ps)


class BluetoothFacet(_ProductFacet):
    """Bluetooth-only operations on a connected analyzer. Obtain via ``analyzer.bluetooth``."""

    _PRODUCT_LABEL = "Bluetooth"
    _ATTR = "bluetooth"
    _SUBMODULE = None
    _IDENTITY = "BluetoothAnalyzerRemoteControlIdentity"
    _PRX = "BluetoothAnalyzerRemoteControlPrx"

    # -- recording -------------------------------------------------------------------
    def split_trace_and_continue(self, filename) -> None:
        """Save the current trace and keep recording -- "Save & Continue"
        (-> SplitTraceFileAndContinueRecording). *filename* is on the analyzer machine.
        """
        self._call(self._proxy.SplitTraceFileAndContinueRecording, os.fspath(filename))

    # -- spectrum / channels ---------------------------------------------------------
    def spectrum_rssi(self, time_ps, rf_channel: int) -> BluetoothSpectrumSample:
        """RSSI at *time_ps* on *rf_channel* (0-78) (-> GetSpectrumRssi).

        RF channels are 1 MHz apart: frequency = 2402 + *rf_channel* MHz (BR/EDR numbering;
        LE channels sit on a 2 MHz raster -- convert via frequency, e.g. Wi-Fi channel 11's
        2462 MHz center is rf_channel 60).
        """
        rssi, start, stop = self._call(self._proxy.GetSpectrumRssi, _to_ps(time_ps), int(rf_channel))
        return BluetoothSpectrumSample(rssi_dbm=rssi, start_ps=start, stop_ps=stop)

    def spectrum_rssi_range(self, from_time_ps, to_time_ps, rf_channel: int) -> BluetoothSpectrumRange:
        """RSSI samples across [*from_time_ps*, *to_time_ps*] on *rf_channel* (-> GetSpectrumRssiRange).

        Channel-to-frequency mapping as in :meth:`spectrum_rssi` (2402 + *rf_channel* MHz).
        Samples arrive at ~10 kHz; one call serves one channel, so sweeping a time/frequency
        grid means one call per cell -- keep grids coarse.
        """
        rssi, start, stop = self._call(self._proxy.GetSpectrumRssiRange,
                                       _to_ps(from_time_ps), _to_ps(to_time_ps), int(rf_channel))
        return BluetoothSpectrumRange(rssi_dbm=tuple(rssi), start_ps=start, stop_ps=stop)

    def channel_summaries(self, from_time_ps=0, to_time_ps=None) -> list[BluetoothChannelSummary]:
        """Per-RF-channel summaries; list index == RF channel (-> GetChannelsSummary).

        79 entries, 1 MHz apart: frequency = 2402 + index MHz (BR/EDR numbering; LE channels
        sit on a 2 MHz raster -- convert via frequency). Matches the Instant Channels view.
        Defaults to the whole trace (``from_time_ps=0``, ``to_time_ps=None`` -> trace end).
        """
        start = _to_ps(from_time_ps)
        stop = _INT64_MAX if to_time_ps is None else _to_ps(to_time_ps)
        return [BluetoothChannelSummary._from_ice(s)
                for s in self._call(self._proxy.GetChannelsSummary, start, stop)]

    def channels(self, from_time_ps=0, to_time_ps=None) -> list[BluetoothChannelStat]:
        """Per-channel summaries as explicit ``(rf_channel, summary)`` pairs."""
        return [BluetoothChannelStat(rf_channel=i, summary=s)
                for i, s in enumerate(self.channel_summaries(from_time_ps, to_time_ps))]

    # -- device filter / link keys ---------------------------------------------------
    def configure_device_filter(self, mode: DeviceFilterMode,
                                device_addrs: Sequence[int | str] = (), *,
                                wait: bool = True, timeout: float | None = 600.0) -> None:
        """Set which devices are kept/excluded (-> ConfigureDeviceFilter).

        *mode* is a :class:`DeviceFilterMode`; *device_addrs* are 48-bit BDADDRs -- ints or
        strings as the analyzer displays them (``"AA:BB:CC:DD:EE:FF"``); ignored for
        ``KEEP_ALL`` / ``EXCLUDE_BACKGROUND``. The analyzer re-filters in the background: by
        default this call **blocks** until that finishes (``wait=False`` returns immediately;
        settle later via :meth:`Analyzer.wait_until_idle`).
        """
        ice_mode = self._module.DeviceFilterMode(int(mode))     # SDK IntEnum -> Slice Enum
        addrs = [_check_addr48(a) for a in device_addrs]
        self._call(self._proxy.ConfigureDeviceFilter, ice_mode, addrs)
        if wait:
            self._analyzer.wait_until_idle(timeout=timeout)

    def add_link_key(self, bdaddr1: int | str, bdaddr2: int | str, link_key) -> None:
        """Add a 16-byte link key for the *bdaddr1*<->*bdaddr2* link (-> AddLinkKey).

        Addresses are 48-bit BDADDRs -- ints or strings (``"AA:BB:CC:DD:EE:FF"``).
        """
        key = bytes(link_key)
        if len(key) != 16:
            raise ValueError("link_key must be exactly 16 bytes, got {0}".format(len(key)))
        self._call(self._proxy.AddLinkKey, _check_addr48(bdaddr1), _check_addr48(bdaddr2), key)

    # -- exports (delegate to the base export pipeline; no new serialization) --------
    def export_audio(self, output, *, add_raw_payload_files=None, synchro_buffer_ms=None,
                     force_isochronous_buffering=None,
                     packet_loss: "BluetoothPacketLossMode | None" = None) -> None:
        """Export Bluetooth audio via the base ``Export`` pipeline (mode ``bluetooth_audio``).

        Builds the :class:`BluetoothAudioOptions` carrier and delegates to :meth:`Analyzer.export`.
        (The legacy dedicated ``ExportAudio`` op is intentionally not wrapped; this is the
        supported audio export.)
        """
        self._analyzer.export(output, BluetoothExportModes.AUDIO, options=BluetoothAudioOptions(
            add_raw_payload_files=add_raw_payload_files, synchro_buffer_ms=synchro_buffer_ms,
            force_isochronous_buffering=force_isochronous_buffering, packet_loss=packet_loss))

    def export_channels(self, output, *, range_start_time_ps=None, range_end_time_ps=None) -> None:
        """Export per-channel statistics (mode ``bluetooth_channels``)."""
        options = BluetoothChannelsOptions(range_start_time_ps=range_start_time_ps,
                                           range_end_time_ps=range_end_time_ps)
        options.validate()
        self._analyzer.export(output, BluetoothExportModes.CHANNELS, options=options)

    def export_airtime(self, output, *, range_start_time_ps=None, range_end_time_ps=None) -> None:
        """Export airtime usage (mode ``airtime``)."""
        options = BluetoothAirtimeOptions(range_start_time_ps=range_start_time_ps,
                                          range_end_time_ps=range_end_time_ps)
        options.validate()
        self._analyzer.export(output, BluetoothExportModes.AIRTIME, options=options)

    def export_mobile_phone_data(self, output) -> None:
        """Export Bluetooth mobile-phone data (mode ``bluetooth_mobile_phone_data``; no options)."""
        self._analyzer.export(output, BluetoothExportModes.MOBILE_PHONE_DATA)
