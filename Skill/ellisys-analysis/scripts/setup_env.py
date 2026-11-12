"""Bootstrap a virtual environment with the Ellisys Analysis Automation SDK (all platforms).

Run with any real Python 3.10+:
    Windows:      py scripts/setup_env.py
    Linux/macOS:  python3 scripts/setup_env.py

Creates ./.venv in the CURRENT directory (if absent) and installs the SDK in editable
mode. The SDK source is auto-located, in order:
  1. bundled inside this skill (<skill>/sdk/python -- present when the skill was installed
     from a release archive, making the skill folder fully self-contained);
  2. the release-archive / repo layout (<root>/Sdk/Analysis/Python, with the skill at <root>/Skill/...);
  3. an explicit path:  python3 scripts/setup_env.py /path/to/Sdk/Analysis/Python
Network access to PyPI is required (for the zeroc-ice dependency).
"""
import os
import subprocess
import sys
from pathlib import Path


def main() -> None:
    here = Path(__file__).resolve()
    if len(sys.argv) > 1:
        candidates = [Path(sys.argv[1]).resolve()]
    else:
        candidates = [
            here.parents[1] / "sdk" / "python",   # bundled in the skill (self-contained install)
            here.parents[3] / "Sdk" / "Analysis" / "Python",   # release archive / repo layout
        ]
    sdk = next((c for c in candidates if (c / "pyproject.toml").exists()), None)
    if sdk is None:
        sys.exit(
            "SDK not found (no pyproject.toml at "
            + " nor ".join(str(c) for c in candidates)
            + ").\nPass the path to the SDK source (the Sdk/Analysis/Python folder of the release archive)."
        )

    venv = Path.cwd() / ".venv"
    venv_python = venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not venv_python.exists():
        print(f"Creating {venv} ...")
        subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)

    print(f"Installing the SDK from {sdk} (needs network for zeroc-ice) ...")
    subprocess.run(
        [str(venv_python), "-m", "pip", "install", "--quiet",
         "--disable-pip-version-check", "-e", str(sdk)],
        check=True,
    )
    subprocess.run(
        [str(venv_python), "-c",
         "import ellisys_analysis_automation as e; "
         "print('OK ellisys_analysis_automation', e.__version__, '->', e.__file__)"],
        check=True,
    )
    print(f"Use this interpreter for all scripts: {venv_python}")


if __name__ == "__main__":
    main()
