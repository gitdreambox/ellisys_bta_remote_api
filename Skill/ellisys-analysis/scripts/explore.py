"""Discover a trace's overviews/layers, vocabulary, devices and anchors -- run BEFORE scripting.

Thin CLI over :mod:`ellisys_analysis_automation.discovery` (the SDK's discovery module -- see
its docs for what each section means and why discovery is a required first step).

Usage (run with the venv interpreter):
    python explore.py [--host H] [--port P] [--trace PATH] [--overview NAME]
                      [--at SECONDS | --marker TEXT] [--max-items N] [--no-survey]
--trace loads that file first (path on the ANALYZER machine); otherwise the currently open
trace is profiled. --at/--marker anchor the exploration around a time of interest (e.g. a
marker placed by the user). Read-only apart from the optional load.
"""
import argparse
import sys

import ellisys_analysis_automation as ea
from ellisys_analysis_automation import discovery


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--host", default="localhost")
    ap.add_argument("--port", type=int, default=12345)
    ap.add_argument("--trace", help="trace file to load first (path on the analyzer machine)")
    ap.add_argument("--overview", help="overview name (default: the active overview)")
    ap.add_argument("--at", type=float, metavar="SECONDS",
                    help="anchor the exploration around this trace time")
    ap.add_argument("--marker", metavar="TEXT",
                    help="anchor around the first marker whose text contains TEXT (case-insensitive)")
    ap.add_argument("--max-items", type=int, default=3000, help="sampling budget (default 3000)")
    ap.add_argument("--max-reports", type=int, default=12,
                    help="detail reports to sample for field names (default 12)")
    ap.add_argument("--no-survey", action="store_true",
                    help="skip the overview / protocol-layer survey")
    args = ap.parse_args()
    if args.at is not None and args.marker:
        ap.error("--at and --marker are mutually exclusive")

    with ea.connect(args.host, args.port) as analyzer:
        print(discovery.explore(analyzer, trace=args.trace, overview=args.overview,
                                at=args.at, marker=args.marker, max_items=args.max_items,
                                max_reports=args.max_reports, survey=not args.no_survey), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
