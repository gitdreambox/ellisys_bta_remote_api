"""Load a bundled Bluetooth trace, print some protocol items and per-channel statistics, and add a
Wi-Fi key -- using the SDK. This mirrors the C# Bluetooth sample.

The analyzer must be running with the Remote Control plugin enabled (default localhost:12345).
Install the dependencies first (from this directory):

    python -m pip install -r requirements.txt
"""
import os

import ellisys_analysis_automation as ea

# TODO: adapt to your setup
HOST = "localhost"
PORT = 12345

SAMPLE_TRACE = "A2dpMusicStreaming.btt"   # shipped alongside this script
SAMPLE_OVERVIEW = "BR/EDR"
TOP_ITEMS_COUNT = 3
MAX_DEPTH = 2


def print_items(item, print_count, max_depth, current_depth):
    """Recursively print up to *print_count* children of *item*, down to *max_depth*."""
    if current_depth >= max_depth:
        return
    for index in range(min(item.child_count, print_count)):
        child = item.child(index)
        print(" " * (4 * current_depth) + child.description)
        print_items(child, 16, max_depth, current_depth + 1)


def print_channels_statistics(analyzer):
    """Print the per-RF-channel packet tallies of the loaded trace."""
    print("{0:>8} {1:>8} {2:>8} {3:>8}".format("Channel", "OK", "Errors", "Retr"))
    for channel in analyzer.bluetooth.channels():
        summary = channel.summary
        print("{0:>8} {1:>8} {2:>8} {3:>8}".format(
            channel.rf_channel, summary.ok, summary.errors, summary.retransmitted))


with ea.connect(HOST, PORT) as analyzer:
    print("Remote control connection succeeded.")
    print()

    # Load the bundled sample trace (next to this script; load() blocks until it is loaded).
    trace_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), SAMPLE_TRACE)
    print("Open sample trace '{0}'".format(SAMPLE_TRACE))
    print()
    analyzer.load(trace_path)

    # Print some protocol items.
    with analyzer.overview(SAMPLE_OVERVIEW, protocol_layer="All Layers") as overview:
        print("Print the first {0} top items with a max depth of {1}".format(TOP_ITEMS_COUNT, MAX_DEPTH))
        print()
        print_items(overview.root, TOP_ITEMS_COUNT, MAX_DEPTH, 0)
        print()

        # Print channels statistics.
        print("Print channels statistics")
        print()
        print_channels_statistics(analyzer)

    # Add a Wi-Fi key.
    analyzer.wifi.add_wifi_key_by_ap_ssid("testSsid", "testKey")
