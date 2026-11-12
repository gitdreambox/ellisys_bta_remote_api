using System;
using System.IO;
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
		Console.WriteLine();

		//
		// Loading sample trace
		//
		const string SampleTrace = "A2dpMusicStreaming.btt";
		const string SampleOverview = "BR/EDR";

		Console.WriteLine($"Open sample trace '{SampleTrace}'");
		Console.WriteLine();

		var tracePath = Path.Combine(AppContext.BaseDirectory, SampleTrace);

		analyzer.Load(tracePath); // blocks until the trace is fully loaded

		//
		// Printing some protocol items
		//
		using var overview = analyzer.Overview(SampleOverview, protocolLayer: "All Layers");

		const int TopItemsCount = 3;
		const int MaxDepth = 2;

		Console.WriteLine($"Print the first {TopItemsCount} top items with a max depth of {MaxDepth}");
		Console.WriteLine();

		PrintItems(overview.Root, TopItemsCount, MaxDepth, 0);
		Console.WriteLine();

		//
		// Printing channels statistics
		//
		Console.WriteLine("Print channels statistics");
		Console.WriteLine();

		PrintChannelsStatistics(analyzer);

		//
		// Adding a WiFi key
		//
		analyzer.Wifi.AddWifiKeyByApSsid("testSsid", "testKey");
	}

	private static void PrintItems(OverviewItem item, int printCount, int maxDepth, int currentDepth)
	{
		if (currentDepth >= maxDepth)
		{
			return;
		}

		var childCount = Math.Min(item.ChildCount, printCount);

		for (var childIndex = 0; childIndex < childCount; childIndex++)
		{
			var child = item.Child(childIndex);

			Console.Write("".PadLeft(4 * currentDepth));
			Console.WriteLine(child.Description);

			PrintItems(child, 16, maxDepth, currentDepth + 1);
		}
	}

	private static void PrintChannelsStatistics(Analyzer analyzer)
	{
		Console.WriteLine("{0,8} {1,8} {2,8} {3,8}", "Channel", "OK", "Errors", "Retr");

		foreach (var channel in analyzer.Bluetooth.Channels())
		{
			var summary = channel.Summary;

			Console.WriteLine("{0,8} {1,8} {2,8} {3,8}", channel.RfChannel, summary.Ok, summary.Errors, summary.Retransmitted);
		}
	}
}
