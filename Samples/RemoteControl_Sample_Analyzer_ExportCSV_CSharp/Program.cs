using System;
using System.IO;
using System.Xml;
using Ellisys.Analysis.Automation;

namespace RemoteControl_Analyzer_Sample;

class Program
{
	// TODO: Please adapt the following constants to your needs
	private const string HostIp = "localhost";
	private const int HostPort = 12345;

	private static void Main(string[] args)
	{
		using var analyzer = Analyzer.Connect(HostIp, HostPort);

		Console.WriteLine("Remote control connection succeeded.");

		Console.WriteLine("Creating CSV output from currently open trace...");

		// The scope targets the currently active overview and releases its item handles on Dispose.
		using var overview = analyzer.Overview();
		using var writer = File.CreateText("export.csv");

		Tools.ExportToCsv(overview, writer);
	}
}

static class Tools
{
	public static void ExportToCsv(OverviewScope overview, StreamWriter writer)
	{
		var first = true;
		var xmlDocument = new XmlDocument();

		// StreamRecords is the page-released full-scan extractor (server handles stay at O(pageSize),
		// unlike IterateChildren which is for bounded exploration); each record's Xml is the
		// filtered "Overview Columns" Details report.
		foreach (var record in overview.Root.Cursor().StreamRecords(xmlFilter: new XmlFilter("Overview Columns")))
		{
			if (string.IsNullOrEmpty(record.Xml))
			{
				continue; // this item has no Details report
			}

			xmlDocument.LoadXml(record.Xml);
			var item = xmlDocument["Details"]?["Item"];
			if (item == null)
			{
				continue;
			}

			if (first)
			{
				// Add title line
				foreach (XmlElement column in item)
				{
					writer.Write("\"");
					writer.Write(column.GetAttribute("name"));
					writer.Write("\",");
				}

				writer.WriteLine();

				first = false;
			}

			foreach (XmlElement column in item)
			{
				writer.Write("\"");
				writer.Write(column.GetAttribute("value"));
				writer.Write("\",");
			}

			writer.WriteLine();
		}
	}
}
