"""Export the active overview of the currently open trace to a CSV file, using the SDK.

The analyzer must be running with the Remote Control plugin enabled (default localhost:12345),
with a trace open. Install the dependencies first (from this directory):

    python -m pip install -r requirements.txt
"""
import csv
import xml.etree.ElementTree as ET

import ellisys_analysis_automation as ea
from ellisys_analysis_automation import ItemField

# TODO: adapt to your setup
HOST = "localhost"
PORT = 12345
OUTPUT = "export.csv"


def overview_columns(xml_report):
    """Yield (name, value) for each column in an item's 'Overview Columns' Details report."""
    root = ET.fromstring(xml_report)
    for column in root[0]:                      # root[0] is the 'Overview Columns' container
        yield column.attrib.get("name", ""), column.attrib.get("value", "")


with ea.connect(HOST, PORT) as analyzer:
    print("Creating CSV from the currently open trace...")
    with analyzer.overview() as overview:       # the active overview
        with open(OUTPUT, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            header_written = False
            # stream_records pages through the whole overview in bounded, page-released windows
            for record in overview.root.cursor().stream_records(ItemField.xml_filtered("Overview Columns")):
                columns = list(overview_columns(record.xml))
                if not header_written:
                    writer.writerow([name for name, _ in columns])
                    header_written = True
                writer.writerow([value for _, value in columns])
    print("Wrote '{0}'".format(OUTPUT))
