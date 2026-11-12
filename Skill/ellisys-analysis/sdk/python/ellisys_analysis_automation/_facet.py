"""Shared machinery for the per-product facets (``analyzer.bluetooth`` / ``.wifi`` / ``.wpan`` /
``.usb30``).

A product facet exposes a product interface's operations on a connected ``Analyzer``, reusing the
analyzer's communicator, ``_call`` (Ice->SDK error translation), and bindings module -- adding only
the product-specific operations. The invariant work (resolving the product bindings, the
identity + ``checkedCast`` attach, and the back-reference plumbing) lives here so each product
subclass only sets a few class attributes and adds its ops/results.

Acquisition notes (verified against a live analyzer):
- Most products have their own Ice identity (Bluetooth / Ethernet / Wpan); USB 3.0 shares the
  *base* object + identity (its proxy is the base proxy cast to ``Usb30AnalyzerRemoteControlPrx``).
- Bluetooth's types are flat in the base module; Ethernet's and Wpan's are in nested submodules
  (``Analyzer.Ethernet`` / ``Analyzer.Wpan``) imported on demand.
- ``checkedCast`` returns ``None`` when the object exists but is a different product, and raises
  ``ObjectNotExistException`` when no object exists at that identity -- both mean ``NotAvailable``.
"""
from __future__ import annotations

import enum
import importlib
from typing import TYPE_CHECKING

import Ice

from .errors import ConnectionFailed, NotAvailable

if TYPE_CHECKING:
    from .analyzer import Analyzer

__all__ = ["DeviceFilterMode"]

_GENERATED_ROOT = "Ellisys.Platform.NetworkRemoteControl.Analyzer"


class DeviceFilterMode(enum.IntEnum):
    """Device-filter policy (mirrors the Slice ``DeviceFilterMode`` enum; identical across products)."""

    KEEP_ALL = 0
    EXCLUDE_BACKGROUND = 1
    KEEP_ONLY = 2
    KEEP_INVOLVING = 3


def _check_addr48(addr: int | str) -> int:
    """Validate a 48-bit address (BDADDR / Wi-Fi BSSID); returns it as an int or raises ValueError.

    Accepts an int, or a string in the forms the analyzer itself displays (e.g. in the Overview's
    Communication column): ``"AA:BB:CC:DD:EE:FF"``, ``"AA-BB-CC-DD-EE-FF"``, ``"AABBCCDDEEFF"``,
    or ``"0x..."``. Exactly 12 hex digits always parse as hex (it's an address, even when all the
    digits are 0-9); any other plain-digit string stays decimal.
    """
    if isinstance(addr, str):
        s = addr.strip().replace(":", "").replace("-", "").replace(" ", "")
        try:
            if s.lower().startswith("0x") or len(s) == 12:
                value = int(s, 16)
            else:
                value = int(s)
        except ValueError:
            raise ValueError(f"not a 48-bit address: {addr!r} "
                             '(expected "AA:BB:CC:DD:EE:FF", 12 hex digits, 0x..., or an int)') from None
    else:
        value = int(addr)
    if not 0 <= value <= 0xFFFFFFFFFFFF:
        raise ValueError(
            "address must be a 48-bit value (0..0xFFFFFFFFFFFF), got {0:#x}".format(value))
    return value


class _ProductFacet:
    """Base for per-product facets. Subclasses set the five class attributes and add ops.

    Never constructed directly; minted by ``analyzer.<product>`` via :meth:`_attach`. It borrows
    the analyzer's ``_call`` and communicator through ``self._analyzer`` and uses ``self._module``
    (the product's bindings module) to construct any Ice enums/structs the product needs.
    """

    _PRODUCT_LABEL: str = "product"   # human label used in errors ("Bluetooth", "Wi-Fi", ...)
    _ATTR: str = "product"            # the analyzer attribute name ("bluetooth", "wifi", ...)
    _SUBMODULE: str | None = None     # nested submodule on the base module ("Ethernet"/"Wpan"), or None
    _IDENTITY: str = ""               # name of the identity const on the product module
    _PRX: str = ""                    # name of the proxy type on the product module

    def __init__(self, analyzer: "Analyzer", proxy, module) -> None:
        self._analyzer = analyzer
        self._proxy = proxy
        self._module = module         # the product's bindings module (for enum/struct construction)

    # -- attach ---------------------------------------------------------------------
    @classmethod
    def _product_module(cls, analyzer: "Analyzer"):
        """The Slice module holding this product's bindings (the base module, or a nested submodule)."""
        base = analyzer._bindings_module()
        if cls._SUBMODULE is None:
            return base
        sub = getattr(base, cls._SUBMODULE, None)
        if sub is None:               # real bindings: import the nested submodule, then re-read it off base
            importlib.import_module(_GENERATED_ROOT + "." + cls._SUBMODULE)
            sub = getattr(base, cls._SUBMODULE)
        return sub

    @classmethod
    def _attach(cls, analyzer: "Analyzer") -> "_ProductFacet":
        module = cls._product_module(analyzer)
        identity = Ice.stringToIdentity(getattr(module, cls._IDENTITY))
        based = analyzer._proxy.ice_identity(identity)    # same endpoint + communicator
        try:
            proxy = getattr(module, cls._PRX).checkedCast(based)
        except (Ice.ObjectNotExistException, Ice.FacetNotExistException) as exc:
            raise NotAvailable(cls._not_available_message()) from exc   # no such object -> wrong product
        except Ice.LocalException as exc:                 # genuine transport problem
            raise ConnectionFailed(
                "Lost the connection to the analyzer while attaching the {0} facet [{1}].".format(
                    cls._PRODUCT_LABEL, type(exc).__name__)) from exc
        if proxy is None:                                  # object exists, but a different product
            raise NotAvailable(cls._not_available_message())
        return cls(analyzer, proxy, module)

    @classmethod
    def _not_available_message(cls) -> str:
        return ("This analyzer is not a {0} analyzer; analyzer.{1} is unavailable on this "
                "endpoint.".format(cls._PRODUCT_LABEL, cls._ATTR))

    # -- borrowed plumbing ----------------------------------------------------------
    def _call(self, operation, *args):
        return self._analyzer._call(operation, *args)

    def __repr__(self) -> str:
        return "<{0} on {1!r}>".format(type(self).__name__, self._analyzer)
