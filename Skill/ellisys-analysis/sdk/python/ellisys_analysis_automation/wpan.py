"""The WPAN (IEEE 802.15.4) product facet, reached as ``analyzer.wpan``.

Wraps ``WpanAnalyzerRemoteControl`` (in the nested ``Analyzer.Wpan`` module): Thread and Zigbee
decryption-key management. Built on the shared :class:`_ProductFacet`. Keys are 16 bytes and
64-bit IEEE addresses are 8 bytes (both ``bytes``); lengths are validated client-side.
"""
from __future__ import annotations

from ._facet import _ProductFacet

__all__ = ["WpanFacet"]


def _key128(key) -> bytes:
    data = bytes(key)
    if len(data) != 16:
        raise ValueError("key must be exactly 16 bytes (128-bit), got {0}".format(len(data)))
    return data


def _addr64(addr) -> bytes:
    data = bytes(addr)
    if len(data) != 8:
        raise ValueError("address must be exactly 8 bytes (64-bit), got {0}".format(len(data)))
    return data


def _pan_id(value) -> int:
    pan = int(value)
    if not 0 <= pan <= 0xFFFF:                  # PAN ids are 16-bit (avoids an Ice MarshalException)
        raise ValueError("PAN id must be a 16-bit value (0..0xFFFF), got {0:#x}".format(pan))
    return pan


class WpanFacet(_ProductFacet):
    """WPAN-only operations on a connected analyzer. Obtain via ``analyzer.wpan``."""

    _PRODUCT_LABEL = "WPAN"
    _ATTR = "wpan"
    _SUBMODULE = "Wpan"
    _IDENTITY = "WpanAnalyzerRemoteControlIdentity"
    _PRX = "WpanAnalyzerRemoteControlPrx"

    # -- Thread master keys ----------------------------------------------------------
    def add_thread_master_key(self, pan_id: int, key128, sequence_counter: int) -> None:
        """Add a Thread network master key (16 bytes) for *pan_id* (-> AddThreadNetworkMasterKey)."""
        self._call(self._proxy.AddThreadNetworkMasterKey,
                   _pan_id(pan_id), _key128(key128), int(sequence_counter))

    def remove_all_thread_master_keys(self) -> None:
        """Remove all Thread network master keys (-> RemoveThreadNetworkAllMasterKeys)."""
        self._call(self._proxy.RemoveThreadNetworkAllMasterKeys)

    def remove_thread_master_keys(self, pan_id: int) -> None:
        """Remove all Thread master keys for *pan_id* (-> RemoveThreadNetworkMasterKeys)."""
        self._call(self._proxy.RemoveThreadNetworkMasterKeys, _pan_id(pan_id))

    def remove_thread_master_key(self, pan_id: int, key128) -> None:
        """Remove one Thread master key for *pan_id* (-> RemoveThreadNetworkMasterKey)."""
        self._call(self._proxy.RemoveThreadNetworkMasterKey, _pan_id(pan_id), _key128(key128))

    # -- Zigbee APS link keys --------------------------------------------------------
    def add_zigbee_aps_key(self, destination_address64, source_address64, key128) -> None:
        """Add a Zigbee APS link key (16 bytes) for a device pair (-> AddZigbeeApsKey)."""
        self._call(self._proxy.AddZigbeeApsKey,
                   _addr64(destination_address64), _addr64(source_address64), _key128(key128))

    def remove_all_zigbee_aps_keys(self) -> None:
        """Remove all Zigbee APS link keys (-> RemoveZigbeeApsAllKeys)."""
        self._call(self._proxy.RemoveZigbeeApsAllKeys)

    def remove_zigbee_aps_keys(self, destination_address64, source_address64) -> None:
        """Remove all Zigbee APS link keys for a device pair (-> RemoveZigbeeApsKeys)."""
        self._call(self._proxy.RemoveZigbeeApsKeys,
                   _addr64(destination_address64), _addr64(source_address64))

    def remove_zigbee_aps_key(self, destination_address64, source_address64, key128) -> None:
        """Remove one Zigbee APS link key for a device pair (-> RemoveZigbeeApsKey)."""
        self._call(self._proxy.RemoveZigbeeApsKey,
                   _addr64(destination_address64), _addr64(source_address64), _key128(key128))

    # -- Zigbee network keys ---------------------------------------------------------
    def add_zigbee_network_key(self, pan_id: int, key128) -> None:
        """Add a Zigbee network key (16 bytes) for *pan_id* (-> AddZigbeeNetworkKey)."""
        self._call(self._proxy.AddZigbeeNetworkKey, _pan_id(pan_id), _key128(key128))

    def remove_all_zigbee_network_keys(self) -> None:
        """Remove all Zigbee network keys (-> RemoveZigbeeNetworkAllKeys)."""
        self._call(self._proxy.RemoveZigbeeNetworkAllKeys)

    def remove_zigbee_network_keys(self, pan_id: int) -> None:
        """Remove all Zigbee network keys for *pan_id* (-> RemoveZigbeeNetworkKeys)."""
        self._call(self._proxy.RemoveZigbeeNetworkKeys, _pan_id(pan_id))

    def remove_zigbee_network_key(self, pan_id: int, key128) -> None:
        """Remove one Zigbee network key for *pan_id* (-> RemoveZigbeeNetworkKey)."""
        self._call(self._proxy.RemoveZigbeeNetworkKey, _pan_id(pan_id), _key128(key128))
