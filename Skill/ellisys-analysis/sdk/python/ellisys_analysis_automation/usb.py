"""The USB 3.0 product facet, reached as ``analyzer.usb30``.

Wraps ``Usb30AnalyzerRemoteControl``. Unlike the other products, USB 3.0 has no separate Ice
identity -- the *base* object implements the interface -- so the facet casts the base proxy
(identity ``AnalyzerRemoteControlIdentity``) to ``Usb30AnalyzerRemoteControlPrx``. Built on the
shared :class:`_ProductFacet`.
"""
from __future__ import annotations

import os

from ._facet import _ProductFacet

__all__ = ["Usb30Facet"]


class Usb30Facet(_ProductFacet):
    """USB 3.0-only operations on a connected analyzer. Obtain via ``analyzer.usb30``."""

    _PRODUCT_LABEL = "USB 3.0"
    _ATTR = "usb30"
    _SUBMODULE = None
    _IDENTITY = "AnalyzerRemoteControlIdentity"     # USB 3.0 shares the base object + identity
    _PRX = "Usb30AnalyzerRemoteControlPrx"

    def connect_link(self, disconnect_super_speed: bool = False) -> None:
        """Connect the analyzer's USB link to the device under test (-> ConnectLink).

        *disconnect_super_speed* keeps only the USB 2.0 link connected when ``True``.
        """
        self._call(self._proxy.ConnectLink, bool(disconnect_super_speed))

    def disconnect_link(self) -> None:
        """Disconnect the analyzer's USB link from the device under test (-> DisconnectLink)."""
        self._call(self._proxy.DisconnectLink)

    def save_usb20_packets(self, filename) -> None:
        """Save the captured USB 2.0 packets to *filename* on the analyzer (-> SaveUsb20Packets)."""
        self._call(self._proxy.SaveUsb20Packets, os.fspath(filename))

    def save_usb30_symbols(self, filename, upstream_symbols: bool) -> None:
        """Save captured USB 3.0 symbols to *filename* (-> SaveUsb30Symbols).

        *upstream_symbols* selects the upstream (``True``) or downstream (``False``) direction.
        """
        self._call(self._proxy.SaveUsb30Symbols, os.fspath(filename), bool(upstream_symbols))
