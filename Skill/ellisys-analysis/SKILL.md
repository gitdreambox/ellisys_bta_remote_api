---
name: ellisys-analysis
description: Automate Ellisys protocol analyzers (Bluetooth/Wi-Fi/WPAN/USB) over the network via the Ellisys Remote Control API and its Python SDK. Use when the user asks to control an Ellisys analyzer, record or load a trace (.btt), navigate/search the Overview, add markers, export data (CSV, audio, channels, airtime, filtered traces), or otherwise drive an Ellisys analyzer programmatically.
---

# Ellisys Remote Control — agent skill

Control a **running Ellisys analyzer application** over TCP (default port **12345**). The
analyzer-side server is a plugin inside the Ellisys desktop application (Windows natively, or
Linux/macOS through the Ellisys-provided runtime); your code is a network client and runs on
**any platform** (Windows, Linux, macOS).
Primary tool: the **Python SDK** (`ellisys_analysis_automation`). A C# SDK with the same surface
exists for .NET integration; `eacli`/`btacli` (if bundled under `Binaries/`, with
win/linux/osx builds) offers quick no-code queries (`btacli --help`).

Below, `<python>` means a real Python 3.10+: `py` on Windows (bare `python` is often the
Microsoft Store stub), `python3` on Linux/macOS. `<venv-python>` means the venv interpreter:
`.venv\Scripts\python.exe` on Windows, `.venv/bin/python` on Linux/macOS.

## Workflow

1. **Probe connectivity first** — run [scripts/probe.py](scripts/probe.py):
   `<python> scripts/probe.py [host] [port]`. It diagnoses: TCP unreachable vs. SDK missing vs.
   connected (prints analyzer app info). Don't write task code against a dead endpoint.
2. **Ensure the environment** — if the SDK isn't installed, run
   `<python> scripts/setup_env.py` ([scripts/setup_env.py](scripts/setup_env.py)): creates
   `.venv` in the current directory and installs the SDK **bundled with this skill**
   (`sdk/python/`; falls back to a release archive's `Sdk/Analysis/Python`, or pass a path as an
   argument). Then run everything with `<venv-python>`.
3. **Read the SDK agent guide before writing code.** It is the authoritative, dense API
   reference with canonical recipes and the misuse rules the API enforces. Locate it via:
   ```
   <venv-python> -c "import ellisys_analysis_automation as e, pathlib; print(pathlib.Path(e.__file__).parent / 'llms.txt')"
   ```
   then Read that file. (Same content as `Sdk/Analysis/Python/ellisys_analysis_automation/llms.txt`.)
4. **Discover the trace's vocabulary, devices and anchors before scripting** — run
   [scripts/explore.py](scripts/explore.py):
   `<venv-python> scripts/explore.py [--trace <path-on-analyzer>] [--overview NAME]
   [--at SECONDS | --marker TEXT]`.
   Item descriptions and detail-report field names are **decoder-defined**, close to but not
   1:1 with the protocol spec (an A2DP trace says `AVDTP Media Stream`, so searching
   `"*Streaming*"` finds nothing). explore.py first **surveys all overviews and protocol
   layers** (root-item counts; layer switches are instant) — the quickest fingerprint of what
   traffic an unknown trace contains — then samples the overview (bounded) and prints the
   description templates + field names actually present, the user's **markers**, and (Bluetooth)
   the **device population** — script against those exact terms. When the user placed a marker
   ("look at the issue around my marker"), anchor the exploration with `--marker TEXT` (or
   `--at SECONDS`): it lists the items around that time and focuses the census there.
   (explore.py is a thin wrapper over the SDK's `discovery` module — `discovery.explore(analyzer)`
   is also callable from your own scripts.)
5. **Write the task as a script file** (don't pipe long code through `-c`), run it with
   `<venv-python>` **from the script's own directory** (a stray `ellisys_analysis_automation/`
   folder in the working directory shadows the installed package).

## Mental model (condensed — the llms.txt is the full version)

- `ea.connect(host, port)` → `Analyzer`, a context manager. Everything is synchronous.
- The Overview is a tree with potentially **millions of items**; there is deliberately no
  "all children" list. Traverse with **bounded cursors** (`.cursor().stream()`,
  `.stream_records(...)`, `.take(n)`, `page()`); `materialize()` raises `BoundExceeded` past 100k.
- Items are only valid inside their **`with analyzer.overview(name) as ov:`** scope, and (by
  default) only until their page is released — snapshot with `stream_records(...)` to keep data.
- While loading/recording the overview is **growing**: full traversals raise
  `OverviewIncomplete` unless you pass `follow=True` (tail live) or `snapshot=True`.
  Simplest: `analyzer.load(path)` blocks until loaded.
- Times are **picoseconds** (`.time_ps`) or `timedelta` (`.time`). File paths in `load`,
  `stop_and_save`, `export*` are resolved by the analyzer application on **its** machine, not
  the client: pass paths in the form that installation expects (e.g. `r"C:\traces\capture.btt"`
  on a Windows install), independent of the client's OS.
- Product features live on facets: `analyzer.bluetooth`, `.wifi`, `.wpan`, `.usb30`
  (`NotAvailable` if the connected product lacks them). Catch `RemoteControlError` as the base.
- **Queries are the efficient filter** — `ov.set_query('Item = "AVDTP*" && Status != "OK"')`
  filters the overview *inside the analyzer* on any column or Details field (full syntax in the
  SDK agent guide / "Overview queries" doc section). Use the column/field names discovered by
  explore.py: an **unknown name silently matches nothing**. `set_query` blocks until the filter
  is applied (`wait=False` to defer, then `analyzer.wait_until_idle()`); `set_query("")` clears.
- **A Bluetooth capture contains all nearby devices**, not only the devices of interest, and
  analyzing an unfiltered busy capture is inefficient to unworkable. Probe the device population
  first (explore.py reports it from the Communication column of the BR/EDR + Low Energy
  overviews; there is no list-devices API yet), then narrow:
  `analyzer.bluetooth.configure_device_filter(DeviceFilterMode.KEEP_ONLY, ["AA:BB:CC:DD:EE:FF", ...])`
  (`KEEP_INVOLVING` if the environment isn't too busy; `KEEP_ALL` restores). Addresses can be
  passed exactly as displayed. `configure_device_filter` blocks until the re-filtering finishes
  by default — re-open the overview scope afterwards (`wait=False` to defer).

## Starter pattern

```python
import ellisys_analysis_automation as ea
from ellisys_analysis_automation import ItemField, MarkerColor

with ea.connect("localhost", 12345) as analyzer:
    analyzer.load(r"C:\traces\capture.btt")          # blocks until fully loaded
    with analyzer.overview() as ov:                  # active overview; or overview("BR/EDR Overview")
        for rec in ov.root.cursor().stream_records(ItemField.TIME, ItemField.DESCRIPTION):
            ...                                      # rec.time_seconds, rec.description — handle-free
```

More canonical recipes (live follow, search + markers, exports incl. Bluetooth audio/channels/
airtime) are in the llms.txt from step 3 — prefer adapting those over inventing patterns.

## Troubleshooting

| Symptom | Cause → fix |
|---|---|
| TCP refused / `ConnectionFailed` | Ellisys app not running, Remote Control plugin not installed/enabled, or wrong port. See the *Remote Control User Guide* (in this archive) for server setup. |
| `python` exits 49 / opens MS Store (Windows) | Windows Store alias stub. Use the `py` launcher or the venv's `python.exe`. |
| `ModuleNotFoundError: ellisys_analysis_automation` | Wrong interpreter (use `<venv-python>`) or setup not run. |
| Import works but APIs missing | A stray local `ellisys_analysis_automation/` folder is shadowing the installed package — run from a clean directory. |
| `OverviewIncomplete` | Trace still loading/recording → `analyzer.load(path)` first, or pass `follow=True` / `snapshot=True`. |
| `ScopeClosed` | Item used after its overview scope closed or its page was released → keep work inside the `with`, snapshot via `stream_records`, or `cursor(release_mode="defer")`. |
| `BoundExceeded` | Asked to materialize >100k items → stream instead. |
| `NotAvailable` | Facet/feature not supported by the connected analyzer product. |
| Export/`load` can't find the file | Paths are resolved on the **analyzer machine** — use paths valid for that installation, not client-local paths. |

## Deeper documentation

Bundled with this skill (always available, wherever the skill folder was copied):

- **SDK agent guide (authoritative for code):** [sdk/python/ellisys_analysis_automation/llms.txt](sdk/python/ellisys_analysis_automation/llms.txt) — or locate the installed copy via step 3.
- **Python SDK Guide** (narrative + full API reference): [reference/analysis-sdk-python.md](reference/analysis-sdk-python.md).

In the release archive (when available):

- **C# SDK** (same surface, for .NET integration): `Sdk/Analysis/CSharp/` — guide + `Ellisys.Analysis.Automation/llms.txt`.
- **Remote Control User Guide** (server setup, raw language-neutral API): the `*Remote Control User Guide.md` at the archive root; HTML/PDF renditions of all guides.
