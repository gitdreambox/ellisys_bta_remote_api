"""The Wi-Fi product facet, reached as ``analyzer.wifi``.

Wraps ``EthernetAnalyzerRemoteControl`` (the Slice interface for Wi-Fi capture, in the nested
``Analyzer.Ethernet`` module). Built on the shared :class:`_ProductFacet`.
"""
from __future__ import annotations

from collections.abc import Sequence

from ._facet import DeviceFilterMode, _ProductFacet, _check_addr48

__all__ = ["WifiFacet"]


class WifiFacet(_ProductFacet):
    """Wi-Fi-only operations on a connected analyzer. Obtain via ``analyzer.wifi``."""

    _PRODUCT_LABEL = "Wi-Fi"
    _ATTR = "wifi"
    _SUBMODULE = "Ethernet"
    _IDENTITY = "EthernetAnalyzerRemoteControlIdentity"
    _PRX = "EthernetAnalyzerRemoteControlPrx"

    def add_wifi_key_by_ap_ssid(self, ap_ssid: str, key: str) -> None:
        """Add a Wi-Fi key for the access point with SSID *ap_ssid* (-> AddWifiKeyByApSsid)."""
        self._call(self._proxy.AddWifiKeyByApSsid, ap_ssid, key)

    def add_wifi_key_by_ap_mac(self, ap_mac_addr: int | str, key: str) -> None:
        """Add a Wi-Fi key for the access point with BSSID *ap_mac_addr* -- a 48-bit int or a
        string like ``"AA:BB:CC:DD:EE:FF"`` (-> AddWifiKeyByApMacAddr)."""
        self._call(self._proxy.AddWifiKeyByApMacAddr, _check_addr48(ap_mac_addr), key)

    def configure_device_filter(self, mode: DeviceFilterMode,
                                device_addrs: Sequence[int | str] = (), *,
                                wait: bool = True, timeout: float | None = 600.0) -> None:
        """Set which devices are kept/excluded (-> ConfigureDeviceFilter).

        *mode* is a :class:`~ellisys_analysis_automation.DeviceFilterMode`; *device_addrs* are 48-bit
        MACs -- ints or strings (``"AA:BB:CC:DD:EE:FF"``); ignored for ``KEEP_ALL`` /
        ``EXCLUDE_BACKGROUND``. The analyzer re-filters in the background: by default this call
        **blocks** until that finishes (``wait=False`` returns immediately).
        """
        ice_mode = self._module.DeviceFilterMode(int(mode))     # SDK IntEnum -> Slice Enum
        addrs = [_check_addr48(a) for a in device_addrs]
        self._call(self._proxy.ConfigureDeviceFilter, ice_mode, addrs)
        if wait:
            self._analyzer.wait_until_idle(timeout=timeout)
