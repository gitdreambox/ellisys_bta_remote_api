"""Internal: make the pre-generated Slice bindings importable and guard the Ice version.

The bindings under ``_generated/`` are produced by slice2py (see Plugins\\SliceAll.ps1) and are
version-coupled to the Ice runtime. We add ``_generated/`` to ``sys.path`` so the generated
``Ellisys`` package imports, and we check the installed zeroc-ice matches first -- a clear
error beats an obscure C-level failure on a mismatched runtime.
"""
import os
import sys

import Ice

_GENERATED = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_generated")
# Ice 3.8.x (Ice.intVersion() // 100). The bindings were generated with 3.8.2; the IcePy ABI
# the generated code binds to has historically changed across minor versions, not patches.
_EXPECTED_MAJOR_MINOR = 308
_module = None


def load():
    """Import and return the Analyzer bindings module (loaded once)."""
    global _module
    if _module is None:
        if Ice.intVersion() // 100 != _EXPECTED_MAJOR_MINOR:
            raise RuntimeError(
                "ellisys_analysis_automation's bindings were generated for Ice 3.8.x, but the "
                "installed zeroc-ice is %s. Install the matching runtime:\n"
                "    pip install \"zeroc-ice~=3.8.2\"" % Ice.stringVersion())
        if _GENERATED not in sys.path:
            sys.path.insert(0, _GENERATED)
        import Ellisys.Platform.NetworkRemoteControl.Analyzer as module
        _module = module
    return _module
