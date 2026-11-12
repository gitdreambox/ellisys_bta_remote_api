using System.Xml;
using IceAnalyzer = Ellisys.Platform.NetworkRemoteControl.Analyzer;

namespace Ellisys.Analysis.Automation;

// =====================================================================================
// Bounded, safe navigation of the analyzer's Overview tree.
//
// The server exposes the Overview as a tree of items addressed by opaque int handles. A
// trace can hold MILLIONS of items, so "never read all" is a STRUCTURAL guarantee here,
// not advice:
//
//   * You reach children/matches only through a cursor (OverviewItem.Cursor,
//     OverviewScope.SearchCursor) that yields one bounded Page at a time. No object can
//     represent "all items"; the whole-set batch readers live only on a Page, whose size
//     is capped by construction (PageMax).
//   * Every round-trip is bounded by a default page size; the page-size argument is
//     clamped to PageMax. Materializing into memory (Take / [a..b] / Materialize) is an
//     explicit opt-in that THROWS BoundExceededException past HardCap -- never a silent pull.
//   * Server handle memory is bounded BY DEFAULT: a page-streaming cursor releases each
//     page's handles at the page boundary (ReleaseMode.Page), so a full scan keeps the
//     server's handle high-water mark at O(pageSize).
//   * A full traversal of an overview that is still GROWING (a trace loading, or the
//     analyzer recording) throws OverviewIncompleteException rather than silently stopping
//     short. Pass follow:true to tail it as items arrive, or snapshot:true for just what
//     exists now.
//
// Handles cannot be freed individually (ReleaseAllOverviewItemHandles is global), so the
// unit of lifetime is an OverviewScope (see Analyzer.Overview). Using a handle after its
// scope closed -- or after a page-release invalidated it -- throws ScopeClosedException
// before any network call. Everything routes through Analyzer.Call; no Ice type leaks out.
// =====================================================================================

/// <summary>A handle was used after its <see cref="OverviewScope"/> released it.</summary>
/// <remarks>
/// Thrown when an item/page is touched after its scope exited, after
/// <see cref="OverviewScope.ReleaseHandles"/>, or after a page-streaming cursor released the
/// page that minted it. Subclasses <see cref="OperationException"/>, so existing
/// <c>catch (OperationException)</c> handlers still catch it.
/// </remarks>
public sealed class ScopeClosedException : OperationException
{
    /// <summary>Create a scope-closed failure.</summary>
    public ScopeClosedException(string message, Exception? innerException = null)
        : base(message, innerException) { }
}

/// <summary>A bounded read was asked to materialize more than its cap.</summary>
/// <remarks>
/// Thrown by <c>Take(n)</c> / <c>cursor[a..b]</c> / <c>Materialize(cap:)</c> / search
/// <c>resultCap</c> when the requested or discovered size would exceed the limit, and by
/// constructing a <see cref="Page"/> larger than <see cref="OverviewLimits.HardCap"/>.
/// Fail-loud by design: there is no silent truncation.
/// </remarks>
public sealed class BoundExceededException : OperationException
{
    /// <summary>Create a bound-exceeded failure.</summary>
    public BoundExceededException(string message, Exception? innerException = null)
        : base(message, innerException) { }
}

/// <summary>A full traversal was attempted while the overview is still being populated.</summary>
/// <remarks>
/// The overview grows while a trace is <b>loading</b> or while the analyzer is
/// <b>recording</b>, so a plain stream / record-stream / walk / iterate-children / materialize
/// would stop at whatever count happened to exist when it started and silently drop the rest.
/// Rather than truncate quietly, those operations throw this unless the caller says how to
/// handle the growth: wait until it is complete first (<see cref="Analyzer.WaitUntilLoaded"/>),
/// pass <c>follow:true</c> to keep traversing as items arrive (live-tail), or pass
/// <c>snapshot:true</c> to deliberately traverse only what exists right now. Bounded reads
/// (<c>Take(n)</c> / <c>Page()</c> / <c>cursor[a..b]</c>) are exempt -- they are explicitly
/// partial by request, so nothing is lost silently. Subclasses <see cref="OperationException"/>.
/// </remarks>
public sealed class OverviewIncompleteException : OperationException
{
    /// <summary>Create an overview-incomplete failure.</summary>
    public OverviewIncompleteException(string message, Exception? innerException = null)
        : base(message, innerException) { }
}

/// <summary>The structural caps that make bounded access a guarantee rather than advice.</summary>
public static class OverviewLimits
{
    /// <summary>Per-round-trip page for cursors/streams.</summary>
    public const int PageDefault = 256;

    /// <summary>Hard ceiling on any single page / batch round-trip (clamps caller-supplied page sizes).</summary>
    public const int PageMax = 4096;

    /// <summary>Ceiling on an explicit materialize (Take / finite slice / Materialize). Exceeding it throws.</summary>
    public const int HardCap = 100_000;

    /// <summary>Default recursion depth for a search cursor (finite on purpose -- NOT the whole subtree).</summary>
    public const int DefaultSearchDepth = 8;

    /// <summary>How many of the base's direct children a search window covers per round-trip.</summary>
    public const int DefaultSearchFanout = 16;

    /// <summary>Default ceiling on total search matches before a search throws.</summary>
    public const int DefaultResultCap = 100_000;

    /// <summary>Default poll interval for <c>follow</c> traversals while the overview is still growing.</summary>
    public static readonly TimeSpan FollowPoll = TimeSpan.FromMilliseconds(250);

    /// <summary>
    /// <c>SearchOverviewItems</c> maxDepth for "whole subtree" (the server saturates at the
    /// tree's real depth). The live analyzer treats maxDepth=0 as "direct children" and -1 as
    /// "nothing", so we never pass -1.
    /// </summary>
    internal const int UnboundedDepth = int.MaxValue;
}

/// <summary>Selects which batch operation a reader issues. One member == one plural Ice op.</summary>
public enum ItemField
{
    /// <summary>Text of the Item column (-&gt; GetOverviewItemsDescription).</summary>
    Description = 0,

    /// <summary>Timestamp in picoseconds (-&gt; GetOverviewItemsTimeInPicoseconds).</summary>
    Time = 1,

    /// <summary>Bytes shown in the Raw data view (-&gt; GetOverviewItemsData).</summary>
    Data = 2,

    /// <summary>Details view as XML (-&gt; GetOverviewItemsXmlReport).</summary>
    Xml = 3,
}

/// <summary>A request for the filtered Details XML of the given field names (-&gt; ...XmlReportFiltered).</summary>
public sealed class XmlFilter
{
    /// <summary>Build a filtered-XML field selector for <paramref name="fieldNames"/>.</summary>
    public XmlFilter(params string[] fieldNames)
    {
        FieldNames = (string[])fieldNames.Clone();
    }

    /// <summary>The Details field names to include in the filtered XML report.</summary>
    public IReadOnlyList<string> FieldNames { get; }

    internal string[] FieldNamesArray => (string[])FieldNames.ToArray();
}

/// <summary>
/// A pure-data, handle-FREE snapshot of one item -- safe to keep after the scope closes.
/// </summary>
/// <remarks>
/// Only the fields you requested are populated; the rest stay <c>null</c>.
/// <see cref="Position"/> is the item's index within its parent / result set (for
/// traceability) -- it is <b>not</b> a handle.
/// </remarks>
public sealed class ItemRecord
{
    /// <summary>Create a handle-free snapshot. Unset fields stay <c>null</c>.</summary>
    public ItemRecord(int position, string? description = null, long? timePs = null,
        byte[]? data = null, string? xml = null)
    {
        Position = position;
        Description = description;
        TimePs = timePs;
        Data = data;
        Xml = xml;
    }

    /// <summary>Index of this item within its parent / result set (traceability only; not a handle).</summary>
    public int Position { get; }

    /// <summary>The Item-column text, or <c>null</c> if not requested.</summary>
    public string? Description { get; }

    /// <summary>The timestamp in picoseconds, or <c>null</c> if not requested.</summary>
    public long? TimePs { get; }

    /// <summary>The raw-data-view bytes, or <c>null</c> if not requested.</summary>
    public byte[]? Data { get; }

    /// <summary>The Details XML report, or <c>null</c> if not requested.</summary>
    public string? Xml { get; }

    /// <summary><see cref="TimePs"/> as a <see cref="TimeSpan"/> (100-nanosecond resolution), or <c>null</c>.</summary>
    public TimeSpan? Time => TimePs is null ? null : OverviewTime.ToTimeSpan(TimePs.Value);

    /// <summary><see cref="TimePs"/> in seconds as a double, or <c>null</c>.</summary>
    public double? TimeSeconds => TimePs is null ? null : TimePs.Value / 1e12;
}

/// <summary>Picosecond/TimeSpan conversion helpers shared across the overview types.</summary>
internal static class OverviewTime
{
    public static TimeSpan ToTimeSpan(long picoseconds) =>
        TimeSpan.FromTicks(picoseconds / 100_000); // 1 tick == 100 ns == 100_000 ps
}

/// <summary>Whether a page-streaming cursor releases each page's handles at the page boundary.</summary>
public enum ReleaseMode
{
    /// <summary>
    /// Free each page's handles at the page boundary (default) -- a full scan keeps server
    /// memory at O(pageSize), at the cost that a live item must not be held across a page
    /// boundary (touching it throws <see cref="ScopeClosedException"/>).
    /// </summary>
    Page,

    /// <summary>Retain handles (e.g. while holding live items or running concurrent cursors).</summary>
    Defer,
}

/// <summary>
/// A lazy, scope-bound wrapper around one opaque handle.
/// </summary>
/// <remarks>
/// Constructing one is free. Each single-item field property does one Ice call on first
/// access then caches it. For many items, navigate with <see cref="Cursor"/> (bounded) or
/// stream with <see cref="IterateChildren"/> / <see cref="Walk"/>. The internal index path
/// lets a page-releasing cursor re-acquire the item after a global release; items whose path
/// is unknown (search results, the selected item) cannot be re-seated.
/// </remarks>
public sealed class OverviewItem
{
    private readonly OverviewScope _scope;
    private readonly int _gen;
    private readonly int[]? _path;
    private int _handle;

    private bool _hasDesc;
    private string? _desc;
    private bool _hasTime;
    private long _timePs;
    private bool _hasData;
    private byte[]? _data;
    private bool _hasXml;
    private string? _xml;
    private bool _hasChildCount;
    private int _childCount;

    internal OverviewItem(OverviewScope scope, int handle, int position = 0, int[]? path = null)
    {
        _scope = scope;
        _handle = handle;
        Position = position;
        _path = path;
        _gen = scope.Generation;
        Depth = 0;
    }

    internal int RawHandle => _handle;
    internal int[]? Path => _path;
    internal int Generation => _gen;
    internal OverviewScope Scope => _scope;

    internal void Check()
    {
        _scope.EnsureLive();
        if (_gen != _scope.Generation)
        {
            throw new ScopeClosedException(
                "this overview item's handles were released; re-navigate from scope.Root.");
        }
    }

    /// <summary>The raw server handle -- an escape hatch for ops the SDK doesn't wrap yet.</summary>
    public int Handle
    {
        get
        {
            Check();
            return _handle;
        }
    }

    /// <summary>Index of this item within its parent / result set.</summary>
    public int Position { get; }

    /// <summary>Depth relative to where a <see cref="Walk"/> started (0 for that level's children).</summary>
    public int Depth { get; internal set; }

    // -- single-item field accessors (one round-trip each, cached) -------------------

    /// <summary>Text of the Item column (-&gt; GetOverviewItemDescription).</summary>
    public string Description
    {
        get
        {
            Check(); // always: a cached value must not outlive its scope (use ItemRecord for that)
            if (!_hasDesc)
            {
                _desc = _scope.Call(p => p.GetOverviewItemDescription(_handle));
                _hasDesc = true;
            }
            return _desc!;
        }
    }

    /// <summary>Timestamp in picoseconds, lossless 64-bit (-&gt; GetOverviewItemTimeInPicoseconds).</summary>
    public long TimePs
    {
        get
        {
            Check();
            if (!_hasTime)
            {
                _timePs = _scope.Call(p => p.GetOverviewItemTimeInPicoseconds(_handle));
                _hasTime = true;
            }
            return _timePs;
        }
    }

    /// <summary>Timestamp as a <see cref="TimeSpan"/> (100-nanosecond resolution).</summary>
    public TimeSpan Time => OverviewTime.ToTimeSpan(TimePs);

    /// <summary>Bytes shown in the Raw data view (-&gt; GetOverviewItemData).</summary>
    public byte[] Data
    {
        get
        {
            Check();
            if (!_hasData)
            {
                _data = _scope.Call(p => p.GetOverviewItemData(_handle));
                _hasData = true;
            }
            return _data!;
        }
    }

    /// <summary>Details view as XML (-&gt; GetOverviewItemXmlReport, cached).</summary>
    public string XmlReport()
    {
        Check();
        if (!_hasXml)
        {
            _xml = _scope.Call(p => p.GetOverviewItemXmlReport(_handle));
            _hasXml = true;
        }
        return _xml!;
    }

    /// <summary>Filtered Details view as XML for the given field names (-&gt; GetOverviewItemXmlReportFiltered).</summary>
    public string XmlReport(params string[] fields)
    {
        Check();
        var copy = (string[])fields.Clone();
        return _scope.Call(p => p.GetOverviewItemXmlReportFiltered(_handle, copy));
    }

    // -- traversal ------------------------------------------------------------------

    /// <summary>
    /// Number of direct children (-&gt; GetOverviewItemChildCount, cached). Cheap even at millions.
    /// </summary>
    public int ChildCount
    {
        get
        {
            Check();
            if (!_hasChildCount)
            {
                _childCount = _scope.Call(p => p.GetOverviewItemChildCount(_handle));
                _hasChildCount = true;
            }
            return _childCount;
        }
    }

    internal void InvalidateChildCount() => _hasChildCount = false;

    internal void SeedDescription(string value) { _desc = value; _hasDesc = true; }
    internal void SeedTime(long value) { _timePs = value; _hasTime = true; }
    internal void SeedData(byte[] value) { _data = value; _hasData = true; }
    internal void SeedXml(string value) { _xml = value; _hasXml = true; }

    /// <summary>
    /// A bounded cursor over this item's children (replaces an unbounded children list).
    /// </summary>
    /// <remarks>
    /// The cursor yields one <see cref="Page"/> at a time. <paramref name="pageSize"/> is
    /// clamped to <see cref="OverviewLimits.PageMax"/>. With <see cref="ReleaseMode.Page"/>
    /// (default) each page's handles are freed at the page boundary, so a full scan keeps
    /// server memory at O(pageSize) -- at the cost that a live item must not be held across a
    /// page boundary (it throws <see cref="ScopeClosedException"/>; use
    /// <see cref="ChildCursor.StreamRecords"/> to keep data). Use <see cref="ReleaseMode.Defer"/>
    /// to retain handles (e.g. while holding live items or running concurrent cursors).
    /// </remarks>
    public ChildCursor Cursor(int pageSize = OverviewLimits.PageDefault,
        IReadOnlyList<ItemField>? prefetch = null, ReleaseMode releaseMode = ReleaseMode.Page)
    {
        Check();
        return new ChildCursor(this, pageSize, prefetch ?? OverviewDefaults.Prefetch, releaseMode);
    }

    /// <summary>The single child at <paramref name="index"/> (-&gt; GetOverviewItemChild).</summary>
    public OverviewItem Child(int index)
    {
        Check();
        var handle = _scope.Call(p => p.GetOverviewItemChild(_handle, index));
        var path = _path is null ? null : OverviewScope.Extend(_path, index);
        return new OverviewItem(_scope, handle, index, path);
    }

    /// <summary>
    /// Lazily page through direct children (<c>ceil(N/batchSize)</c> calls, not N).
    /// </summary>
    /// <remarks>
    /// A true generator for <b>bounded</b> exploration: break early and only fetched pages cost
    /// round-trips. It does NOT release handles per page (it yields live items), so for a full
    /// multi-million-item scan prefer <see cref="ChildCursor.StreamRecords"/>, which is
    /// page-released. While the overview is growing (loading/recording) this throws
    /// <see cref="OverviewIncompleteException"/> unless you pass <paramref name="follow"/>
    /// (live-tail the children as they arrive) or <paramref name="snapshot"/> (only the children
    /// that exist now).
    /// </remarks>
    public IEnumerable<OverviewItem> IterateChildren(int batchSize = OverviewLimits.PageDefault,
        bool follow = false, bool snapshot = false, TimeSpan? pollInterval = null)
    {
        Check();
        _scope.GuardGrowing(follow, snapshot);
        var size = OverviewScope.ClampPage(batchSize);
        var poll = pollInterval ?? OverviewLimits.FollowPoll;
        return Iterate();

        IEnumerable<OverviewItem> Iterate()
        {
            var start = 0;
            while (true)
            {
                if (follow)
                {
                    InvalidateChildCount(); // force a fresh count each pass
                }
                var total = ChildCount;
                while (start < total)
                {
                    var take = Math.Min(size, total - start);
                    var localStart = start;
                    var handles = _scope.Call(p => p.GetOverviewItemChildren(_handle, localStart, take));
                    for (var offset = 0; offset < handles.Length; offset++)
                    {
                        var path = _path is null ? null : OverviewScope.Extend(_path, start + offset);
                        yield return new OverviewItem(_scope, handles[offset], start + offset, path);
                    }
                    start += take;
                }
                if (!follow || !_scope.IsGrowing())
                {
                    break;
                }
                Thread.Sleep(poll);
            }
        }
    }

    /// <summary>
    /// Lazy depth-first walk of descendants; sets each item's <see cref="Depth"/>.
    /// </summary>
    /// <remarks>
    /// Yields this item's children at depth 0, their children at depth 1, etc.
    /// <paramref name="maxDepth"/> limits the levels (<c>null</c> = unbounded). Built on
    /// <see cref="IterateChildren"/> (no per-page release, since it holds ancestors while
    /// descending) -- intended for bounded exploration with an early break, not for materializing
    /// a whole huge tree. On a growing overview this throws <see cref="OverviewIncompleteException"/>
    /// unless you pass <paramref name="snapshot"/> (walk what exists now) or <paramref name="follow"/>
    /// (wait until loading / recording stops, then walk the complete tree -- live-tailing a
    /// recursive walk is not well-defined, so <c>follow</c> here means "let it finish first").
    /// </remarks>
    public IEnumerable<OverviewItem> Walk(int? maxDepth = null,
        int batchSize = OverviewLimits.PageDefault, bool follow = false, bool snapshot = false,
        TimeSpan? pollInterval = null)
    {
        Check();
        _scope.GuardGrowing(follow, snapshot);
        var poll = pollInterval ?? OverviewLimits.FollowPoll;
        return Run();

        IEnumerable<OverviewItem> Run()
        {
            if (follow)
            {
                while (_scope.IsGrowing())
                {
                    Thread.Sleep(poll);
                }
            }
            foreach (var item in Recurse(this, 0))
            {
                yield return item;
            }
        }

        IEnumerable<OverviewItem> Recurse(OverviewItem item, int depth)
        {
            // the policy was resolved at the top; iterate children unguarded (snapshot:true)
            foreach (var child in item.IterateChildren(batchSize: batchSize, snapshot: true))
            {
                child.Depth = depth;
                yield return child;
                if (maxDepth is null || depth + 1 < maxDepth)
                {
                    foreach (var deeper in Recurse(child, depth + 1))
                    {
                        yield return deeper;
                    }
                }
            }
        }
    }

    // -- selection / snapshot -------------------------------------------------------

    /// <summary>Highlight this item in the analyzer GUI (-&gt; SelectOverviewItem).</summary>
    public void Select()
    {
        Check();
        _scope.Call(p => { p.SelectOverviewItem(_handle); return 0; });
    }

    /// <summary>
    /// Select this item and drop a marker on it
    /// (-&gt; SelectOverviewItem + AddMarkerOnSelectedOverviewItem).
    /// </summary>
    public void AddMarker(string text, MarkerColor color = MarkerColor.Yellow)
    {
        Select();
        _scope.Analyzer.AddMarkerOnSelectedOverviewItem(text, color);
    }

    /// <summary>Snapshot this item to a handle-free <see cref="ItemRecord"/> (single-item ops).</summary>
    public ItemRecord Record(params ItemField[] fields)
    {
        Check();
        return RecordWith(fields, null);
    }

    /// <summary>Snapshot this item including a filtered-XML column (single-item ops).</summary>
    public ItemRecord Record(XmlFilter xmlFilter, params ItemField[] fields)
    {
        Check();
        return RecordWith(fields, xmlFilter);
    }

    private ItemRecord RecordWith(ItemField[] fields, XmlFilter? xmlFilter)
    {
        var useDefault = fields.Length == 0 && xmlFilter is null;
        string? description = null;
        long? timePs = null;
        byte[]? data = null;
        string? xml = null;

        if (useDefault)
        {
            description = Description;
            timePs = TimePs;
        }
        else
        {
            foreach (var field in fields)
            {
                switch (field)
                {
                    case ItemField.Description: description = Description; break;
                    case ItemField.Time: timePs = TimePs; break;
                    case ItemField.Data: data = Data; break;
                    case ItemField.Xml: xml = XmlReport(); break;
                }
            }
            if (xmlFilter is not null)
            {
                xml = XmlReport(xmlFilter.FieldNamesArray);
            }
        }
        return new ItemRecord(Position, description, timePs, data, xml);
    }
}

/// <summary>Fields a page prefetches on construction (the two columns analysts read most).</summary>
public static class OverviewDefaults
{
    /// <summary>The default prefetch columns (Description + Time). Override per call.</summary>
    public static readonly IReadOnlyList<ItemField> Prefetch =
        new[] { ItemField.Description, ItemField.Time };
}

/// <summary>
/// An ordered, scope-bound, batch-backed sequence of <see cref="OverviewItem"/> (base of
/// <see cref="Page"/>).
/// </summary>
/// <remarks>
/// Not constructed directly by users -- a bounded <see cref="Page"/> is what cursors hand out.
/// Count / indexing / slicing / iteration are pure-local; each batch reader is one bounded
/// round-trip over the list's handles. Construction is capped at <see cref="OverviewLimits.HardCap"/>.
/// </remarks>
public class OverviewItemList : IReadOnlyList<OverviewItem>
{
    private protected readonly OverviewScope ScopeRef;
    private readonly int _gen;
    private protected readonly List<OverviewItem> Items;

    internal OverviewItemList(OverviewScope scope, int[] handles, int start = 0,
        IReadOnlyList<ItemField>? prefetch = null, int[]? basePath = null)
    {
        if (handles.Length > OverviewLimits.HardCap)
        {
            throw new BoundExceededException(
                $"{handles.Length:N0} items exceed HardCap={OverviewLimits.HardCap:N0}.");
        }
        ScopeRef = scope;
        _gen = scope.Generation;
        Items = new List<OverviewItem>(handles.Length);
        for (var i = 0; i < handles.Length; i++)
        {
            var path = basePath is null ? null : OverviewScope.Extend(basePath, start + i);
            Items.Add(new OverviewItem(scope, handles[i], start + i, path));
        }

        var fields = prefetch ?? OverviewDefaults.Prefetch;
        if (Items.Count > 0 && fields.Count > 0)
        {
            var hs = Handles();
            foreach (var field in fields)
            {
                Seed(field, OverviewBatch.Column(scope, hs, field));
            }
        }
    }

    private OverviewItemList(OverviewScope scope, List<OverviewItem> items)
    {
        ScopeRef = scope;
        _gen = scope.Generation;
        Items = items;
    }

    internal static OverviewItemList FromItems(OverviewScope scope, IEnumerable<OverviewItem> items) =>
        new(scope, items.ToList());

    private protected void Check()
    {
        ScopeRef.EnsureLive();
        if (_gen != ScopeRef.Generation)
        {
            throw new ScopeClosedException(
                "this page's handles were released; fetch a fresh page from the cursor.");
        }
    }

    private int[] Handles()
    {
        var hs = new int[Items.Count];
        for (var i = 0; i < Items.Count; i++)
        {
            hs[i] = Items[i].RawHandle;
        }
        return hs;
    }

    private void Seed(ItemField field, Array column)
    {
        switch (field)
        {
            case ItemField.Description:
                var d = (string[])column;
                for (var i = 0; i < Items.Count; i++) { Items[i].SeedDescription(d[i]); }
                break;
            case ItemField.Time:
                var t = (long[])column;
                for (var i = 0; i < Items.Count; i++) { Items[i].SeedTime(t[i]); }
                break;
            case ItemField.Data:
                var b = (byte[][])column;
                for (var i = 0; i < Items.Count; i++) { Items[i].SeedData(b[i]); }
                break;
            case ItemField.Xml:
                var x = (string[])column;
                for (var i = 0; i < Items.Count; i++) { Items[i].SeedXml(x[i]); }
                break;
        }
    }

    // -- pure-local sequence protocol (zero round-trips) ----------------------------

    /// <summary>Number of items in this list (pure-local; no round-trip).</summary>
    public int Count => Items.Count;

    /// <summary>The item at <paramref name="index"/> (pure-local; no round-trip).</summary>
    public OverviewItem this[int index] => Items[index];

    /// <summary>A finite sub-window of this list reusing the same item objects (no round-trip).</summary>
    public OverviewItemList this[Range range] => FromItems(ScopeRef, ExtractRange(range));

    private IEnumerable<OverviewItem> ExtractRange(Range range)
    {
        var (offset, length) = range.GetOffsetAndLength(Items.Count);
        for (var i = 0; i < length; i++)
        {
            yield return Items[offset + i];
        }
    }

    /// <inheritdoc/>
    public IEnumerator<OverviewItem> GetEnumerator() => Items.GetEnumerator();

    System.Collections.IEnumerator System.Collections.IEnumerable.GetEnumerator() => GetEnumerator();

    /// <summary>The raw handles, in order (escape hatch).</summary>
    public IReadOnlyList<int> HandleValues
    {
        get
        {
            Check();
            return Handles();
        }
    }

    // -- batch readers (one bounded round-trip each; also seed item caches) ----------

    /// <summary>Item-column text for every item (-&gt; GetOverviewItemsDescription).</summary>
    public IReadOnlyList<string> Descriptions() => ReadStrings(ItemField.Description);

    /// <summary>Timestamps in picoseconds (-&gt; GetOverviewItemsTimeInPicoseconds).</summary>
    public IReadOnlyList<long> TimesPs()
    {
        Check();
        var column = (long[])OverviewBatch.Column(ScopeRef, Handles(), ItemField.Time);
        Seed(ItemField.Time, column);
        return column;
    }

    /// <summary>Timestamps as <see cref="TimeSpan"/>s (100-nanosecond resolution).</summary>
    public IReadOnlyList<TimeSpan> Times()
    {
        var ps = TimesPs();
        var result = new TimeSpan[ps.Count];
        for (var i = 0; i < ps.Count; i++)
        {
            result[i] = OverviewTime.ToTimeSpan(ps[i]);
        }
        return result;
    }

    /// <summary>Raw-data-view bytes for every item (-&gt; GetOverviewItemsData).</summary>
    public IReadOnlyList<byte[]> Data()
    {
        Check();
        var column = (byte[][])OverviewBatch.Column(ScopeRef, Handles(), ItemField.Data);
        Seed(ItemField.Data, column);
        return column;
    }

    /// <summary>Details XML for every item (-&gt; GetOverviewItemsXmlReport).</summary>
    public IReadOnlyList<string> XmlReports() => ReadStrings(ItemField.Xml);

    /// <summary>Filtered Details XML for every item (-&gt; GetOverviewItemsXmlReportFiltered).</summary>
    public IReadOnlyList<string> XmlReports(params string[] fields)
    {
        Check();
        var filter = new XmlFilter(fields);
        var column = (string[])OverviewBatch.Column(ScopeRef, Handles(), filter);
        return column; // filtered XML is not cached on items (the filter varies)
    }

    private IReadOnlyList<string> ReadStrings(ItemField field)
    {
        Check();
        var column = (string[])OverviewBatch.Column(ScopeRef, Handles(), field);
        Seed(field, column);
        return column;
    }

    // -- snapshots / convenience ----------------------------------------------------

    /// <summary>Snapshot the whole list to handle-free records (one batch per requested field).</summary>
    public IReadOnlyList<ItemRecord> Records(params ItemField[] fields)
    {
        Check();
        return OverviewBatch.Records(ScopeRef, Handles(), PositionsFrom(), fields, null);
    }

    /// <summary>Snapshot the whole list including a filtered-XML column (one batch per field).</summary>
    public IReadOnlyList<ItemRecord> Records(XmlFilter xmlFilter, params ItemField[] fields)
    {
        Check();
        return OverviewBatch.Records(ScopeRef, Handles(), PositionsFrom(), fields, xmlFilter);
    }

    /// <summary>Filtered Details fields parsed into dictionaries (for tabular export).</summary>
    public IReadOnlyList<IReadOnlyDictionary<string, string>> ToRows(params string[] fieldNames)
    {
        var records = Records(new XmlFilter(fieldNames));
        return OverviewBatch.ToRows(records, fieldNames);
    }

    /// <summary>A new list of the items matching <paramref name="predicate"/> (reuses the items).</summary>
    public OverviewItemList Filter(Func<OverviewItem, bool> predicate)
    {
        Check();
        return FromItems(ScopeRef, Items.Where(predicate));
    }

    private int[] PositionsFrom()
    {
        var positions = new int[Items.Count];
        for (var i = 0; i < Items.Count; i++)
        {
            positions[i] = Items[i].Position;
        }
        return positions;
    }
}

/// <summary>
/// One bounded window of children/matches -- the only object carrying whole-set readers.
/// </summary>
/// <remarks>
/// A <see cref="Page"/> is an <see cref="OverviewItemList"/> (so it has the batch readers /
/// slicing / filter) whose length is capped by construction (&lt;= <see cref="OverviewLimits.PageMax"/>
/// for a streamed page, &lt;= <see cref="OverviewLimits.HardCap"/> for a Take/slice result). It
/// also knows its <see cref="Position"/> in the parent and whether more follow
/// (<see cref="HasMore"/>).
/// </remarks>
public sealed class Page : OverviewItemList
{
    private readonly ChildCursor? _cursor;

    internal Page(OverviewScope scope, int[] handles, int position, int pageSize, int total,
        IReadOnlyList<ItemField>? prefetch = null, ChildCursor? cursor = null, int[]? basePath = null)
        : base(scope, handles, position, prefetch, basePath)
    {
        Position = position;
        PageSize = pageSize;
        Total = total;
        HasMore = position + Count < total;
        _cursor = cursor;
    }

    /// <summary>Index of this page's first item within the parent / result set.</summary>
    public int Position { get; }

    /// <summary>The page size used to fetch this window.</summary>
    public int PageSize { get; }

    /// <summary>Total number of children/matches in the parent / search space.</summary>
    public int Total { get; }

    /// <summary>Whether more items follow this page.</summary>
    public bool HasMore { get; }

    /// <summary>Advance the owning cursor and return the next page (<c>null</c> at the end).</summary>
    public Page? NextPage() => _cursor?.NextPage();
}

/// <summary>
/// A bounded, page-at-a-time cursor over one item's children. Built by
/// <see cref="OverviewItem.Cursor"/>.
/// </summary>
/// <remarks>
/// Streaming (<see cref="Stream"/>, <see cref="StreamRecords"/>) and manual paging
/// (<see cref="Page"/>, <see cref="NextPage"/>, <see cref="Seek"/>, <see cref="Reset"/>) page
/// in windows of <c>pageSize</c> (clamped to <see cref="OverviewLimits.PageMax"/>). Materializing
/// (<see cref="Take"/>, <c>cursor[a..b]</c>, <see cref="Materialize"/>) is bounded and throws
/// <see cref="BoundExceededException"/> past <see cref="OverviewLimits.HardCap"/>. It is NOT
/// iterable directly; <see cref="Total"/> is the cheap count, not a fetch of items.
/// </remarks>
public sealed class ChildCursor
{
    private readonly OverviewScope _scope;
    private readonly int[]? _parentPath;
    private readonly int _pageSize;
    private readonly IReadOnlyList<ItemField>? _prefetch;
    private readonly ReleaseMode _releaseMode;
    private int _parentHandle;
    private int _parentGen;
    private int _position;
    private int _lastLen;
    private int? _total;

    internal ChildCursor(OverviewItem parent, int pageSize, IReadOnlyList<ItemField>? prefetch,
        ReleaseMode releaseMode)
    {
        _scope = parent.Scope;
        _parentPath = parent.Path;
        _parentHandle = parent.RawHandle;
        _parentGen = parent.Generation;
        _pageSize = OverviewScope.ClampPage(pageSize);
        _prefetch = prefetch;
        // page-release needs a path to re-seat the parent after a global release; fall back to
        // Defer when the parent is not addressable (e.g. a search result).
        _releaseMode = releaseMode == ReleaseMode.Page && _parentPath is not null
            ? ReleaseMode.Page
            : ReleaseMode.Defer;
    }

    // -- re-seating after a global release ------------------------------------------
    private int ParentHandle()
    {
        _scope.EnsureLive();
        if (_parentGen == _scope.Generation)
        {
            return _parentHandle;
        }
        if (_parentPath is null)
        {
            throw new ScopeClosedException("cursor parent handle was released and cannot be re-seated.");
        }
        var handle = _scope.RootHandle();
        foreach (var index in _parentPath)
        {
            var h = handle;
            handle = _scope.Call(p => p.GetOverviewItemChild(h, index));
        }
        _parentHandle = handle;
        _parentGen = _scope.Generation;
        return handle;
    }

    private void ReleasePrior()
    {
        if (_releaseMode == ReleaseMode.Page)
        {
            _scope.ReleaseHandles(); // global ReleaseAll + generation bump
        }
    }

    /// <summary>Number of children (-&gt; GetOverviewItemChildCount). Cheap; not a fetch of items.</summary>
    public int Total
    {
        get
        {
            if (_total is null)
            {
                var h = ParentHandle();
                _total = _scope.Call(p => p.GetOverviewItemChildCount(h));
            }
            return _total.Value;
        }
    }

    /// <summary>Index of the next unread child.</summary>
    public int Position => _position;

    // -- internal fetch -------------------------------------------------------------
    private Page Window(int start, int size, IReadOnlyList<ItemField>? prefetch)
    {
        size = OverviewScope.ClampPage(size);
        var total = Total;
        start = Math.Max(0, Math.Min(start, total));
        var count = Math.Min(size, total - start);
        var handles = Array.Empty<int>();
        if (count > 0)
        {
            var h = ParentHandle();
            var s = start;
            handles = _scope.Call(p => p.GetOverviewItemChildren(h, s, count));
        }
        _lastLen = handles.Length;
        return new Page(_scope, handles, start, size, total, prefetch, this, _parentPath);
    }

    private int[] Collect(int start, int want)
    {
        var handles = new List<int>();
        var total = Total;
        var pos = start;
        while (handles.Count < want && pos < total)
        {
            var h = ParentHandle();
            var p2 = pos;
            var take = Math.Min(OverviewLimits.PageMax, want - handles.Count);
            var chunk = _scope.Call(p => p.GetOverviewItemChildren(h, p2, take));
            if (chunk.Length == 0)
            {
                break;
            }
            handles.AddRange(chunk);
            pos += chunk.Length;
        }
        if (handles.Count > want)
        {
            handles.RemoveRange(want, handles.Count - want);
        }
        return handles.ToArray();
    }

    // -- manual paging --------------------------------------------------------------

    /// <summary>The page at the current position (peek; does not advance). <paramref name="size"/> clamped to PageMax.</summary>
    public Page Page(int? size = null) =>
        Window(_position, size ?? _pageSize, _prefetch);

    /// <summary>Advance past the current page (releasing it if release mode is Page); <c>null</c> at end.</summary>
    public Page? NextPage()
    {
        _position += _lastLen;
        ReleasePrior();
        if (_position >= Total)
        {
            _lastLen = 0;
            return null;
        }
        return Window(_position, _pageSize, _prefetch);
    }

    /// <summary>Release any live page and seek back to the start.</summary>
    public void Reset()
    {
        ReleasePrior();
        _position = 0;
        _lastLen = 0;
    }

    /// <summary>Release any live page and jump the position to <paramref name="index"/>.</summary>
    public void Seek(int index)
    {
        ReleasePrior();
        _position = Math.Max(0, index);
        _lastLen = 0;
    }

    // -- streaming ------------------------------------------------------------------

    /// <summary>
    /// Yield children one at a time, paging under the hood (batched, bounded, page-released).
    /// </summary>
    /// <remarks>
    /// The obvious loop on a 10M-child node: O(pageSize) handles in flight, ~3 ops/page, an
    /// early break stops fetching. With <see cref="ReleaseMode.Page"/> an item must be consumed
    /// within its page -- don't stash live items across iterations (use <see cref="StreamRecords"/>).
    /// While the overview is still growing this throws <see cref="OverviewIncompleteException"/>
    /// unless you pass <paramref name="follow"/> (re-read the count at the end and keep yielding
    /// new items as they arrive) or <paramref name="snapshot"/> (traverse only what exists now).
    /// </remarks>
    public IEnumerable<OverviewItem> Stream(IReadOnlyList<ItemField>? prefetch = null,
        bool follow = false, bool snapshot = false, TimeSpan? pollInterval = null)
    {
        var pf = prefetch ?? _prefetch;
        _scope.GuardGrowing(follow, snapshot);
        var poll = pollInterval ?? OverviewLimits.FollowPoll;
        return Run();

        IEnumerable<OverviewItem> Run()
        {
            var pos = _position;
            var first = true;
            while (true)
            {
                if (follow)
                {
                    _total = null; // force a fresh count each pass
                }
                var total = Total;
                while (pos < total)
                {
                    if (!first)
                    {
                        ReleasePrior(); // release the PREVIOUS page before the next
                    }
                    first = false;
                    var page = Window(pos, _pageSize, pf);
                    if (page.Count == 0)
                    {
                        break;
                    }
                    foreach (var item in page)
                    {
                        yield return item;
                    }
                    pos += page.Count;
                    _position = pos;
                }
                if (!follow || !_scope.IsGrowing())
                {
                    break;
                }
                Thread.Sleep(poll);
            }
        }
    }

    /// <summary>
    /// Yield handle-free <see cref="ItemRecord"/>s, page by page, releasing each page.
    /// </summary>
    /// <remarks>
    /// The safe full-scan extractor: constant client memory, O(pageSize) server handles, batched
    /// (one round-trip per field per page). Records survive the per-page release. Defaults to
    /// description + time. <paramref name="follow"/> / <paramref name="snapshot"/> behave as in
    /// <see cref="Stream"/> (a growing overview otherwise throws <see cref="OverviewIncompleteException"/>).
    /// </remarks>
    public IEnumerable<ItemRecord> StreamRecords(IReadOnlyList<ItemField>? fields = null,
        int? pageSize = null, bool follow = false, bool snapshot = false,
        TimeSpan? pollInterval = null, XmlFilter? xmlFilter = null)
    {
        var size = OverviewScope.ClampPage(pageSize ?? _pageSize);
        _scope.GuardGrowing(follow, snapshot);
        var poll = pollInterval ?? OverviewLimits.FollowPoll;
        return Run();

        IEnumerable<ItemRecord> Run()
        {
            var pos = _position;
            var first = true;
            while (true)
            {
                if (follow)
                {
                    _total = null; // force a fresh count each pass
                }
                var total = Total;
                while (pos < total)
                {
                    if (!first)
                    {
                        ReleasePrior();
                    }
                    first = false;
                    var h = ParentHandle();
                    var p2 = pos;
                    var take = Math.Min(size, total - pos);
                    var handles = _scope.Call(p => p.GetOverviewItemChildren(h, p2, take));
                    if (handles.Length == 0)
                    {
                        break;
                    }
                    var records = OverviewBatch.Records(_scope, handles, Sequence(pos, handles.Length),
                        fields ?? Array.Empty<ItemField>(), xmlFilter);
                    foreach (var record in records)
                    {
                        yield return record;
                    }
                    pos += handles.Length;
                    _position = pos;
                }
                if (!follow || !_scope.IsGrowing())
                {
                    break;
                }
                Thread.Sleep(poll);
            }
            ReleasePrior(); // records are handle-free, so releasing the last page is safe
        }
    }

    private static int[] Sequence(int start, int count)
    {
        var result = new int[count];
        for (var i = 0; i < count; i++)
        {
            result[i] = start + i;
        }
        return result;
    }

    // -- bounded materialize (all THROW past the cap) -------------------------------

    /// <summary>A <see cref="Page"/> of the first <c>min(n, total)</c> children. Throws if <c>n &gt; HardCap</c>.</summary>
    public Page Take(int n)
    {
        if (n > OverviewLimits.HardCap)
        {
            throw new BoundExceededException(
                $"Take(n={n:N0}) exceeds HardCap={OverviewLimits.HardCap:N0}; stream or raise the cap deliberately.");
        }
        var want = Math.Min(Math.Max(0, n), Total);
        var handles = Collect(0, want);
        return new Page(_scope, handles, 0, handles.Length, Total, _prefetch, this, _parentPath);
    }

    /// <summary><c>cursor[a..b]</c> -&gt; a <see cref="Page"/> of that finite window. Over-cap slices throw.</summary>
    public Page this[Range range]
    {
        get
        {
            if (range.Start.IsFromEnd || range.End.IsFromEnd)
            {
                throw new ArgumentException(
                    "from-end (^) slice bounds are not allowed; give both absolute bounds, e.g. cursor[a..b].",
                    nameof(range));
            }
            var start = range.Start.Value;
            var stop = range.End.Value;
            if (start < 0 || stop < 0)
            {
                throw new ArgumentException("negative slice bounds are not supported.", nameof(range));
            }
            var span = stop - start;
            if (span > OverviewLimits.HardCap)
            {
                throw new BoundExceededException(
                    $"slice span {span:N0} exceeds HardCap={OverviewLimits.HardCap:N0}.");
            }
            var handles = Collect(start, Math.Max(0, span));
            return new Page(_scope, handles, start, handles.Length, Total, _prefetch, this, _parentPath);
        }
    }

    /// <summary>
    /// All children as handle-free records (page-released). Throws if <c>total &gt; cap</c>.
    /// </summary>
    /// <remarks>
    /// On a growing overview this throws <see cref="OverviewIncompleteException"/> unless you pass
    /// <paramref name="snapshot"/> (materialize what exists now) or <paramref name="follow"/>
    /// (wait until loading / recording stops, then materialize the complete set -- so do not
    /// follow an open-ended live recording here; use <see cref="Stream"/> and break for that).
    /// </remarks>
    public IReadOnlyList<ItemRecord> Materialize(int cap = OverviewLimits.HardCap,
        IReadOnlyList<ItemField>? fields = null, bool follow = false, bool snapshot = false,
        TimeSpan? pollInterval = null, XmlFilter? xmlFilter = null)
    {
        _scope.GuardGrowing(follow, snapshot);
        var poll = pollInterval ?? OverviewLimits.FollowPoll;
        if (follow)
        {
            while (_scope.IsGrowing())
            {
                Thread.Sleep(poll);
            }
            _total = null; // fresh count now that growth has stopped
        }
        var total = Total;
        if (total > cap)
        {
            throw new BoundExceededException(
                $"{total:N0} items exceed cap={cap:N0}; raise cap or use StreamRecords().");
        }
        var selected = fields ?? OverviewDefaults.Prefetch;
        var output = new List<ItemRecord>();
        var pos = 0;
        var first = true;
        while (pos < total)
        {
            if (!first)
            {
                ReleasePrior();
            }
            first = false;
            var h = ParentHandle();
            var p2 = pos;
            var take = Math.Min(OverviewLimits.PageMax, total - pos);
            var handles = _scope.Call(p => p.GetOverviewItemChildren(h, p2, take));
            if (handles.Length == 0)
            {
                break;
            }
            output.AddRange(OverviewBatch.Records(_scope, handles, Sequence(pos, handles.Length),
                selected, xmlFilter));
            pos += handles.Length;
        }
        ReleasePrior();
        return output;
    }

    /// <summary>
    /// All children's filtered Details fields as dictionaries (for tabular export). Throws if over <paramref name="cap"/>.
    /// </summary>
    public IReadOnlyList<IReadOnlyDictionary<string, string>> ToTable(string[] fieldNames,
        int cap = OverviewLimits.HardCap, bool follow = false, bool snapshot = false)
    {
        var records = Materialize(cap, Array.Empty<ItemField>(), follow, snapshot,
            xmlFilter: new XmlFilter(fieldNames));
        return OverviewBatch.ToRows(records, fieldNames);
    }
}

/// <summary>
/// A bounded cursor over search matches. Built by <see cref="OverviewScope.SearchCursor"/>.
/// </summary>
/// <remarks>
/// <c>SearchOverviewItems</c> has no result paging, so this bounds the search SPACE: it windows
/// the base's DIRECT children in steps of <c>searchFanout</c>, issuing one search per window and
/// (by default) releasing each window's match handles before the next. <c>maxDepth</c> is finite
/// by default; <c>resultCap</c> throws <see cref="BoundExceededException"/> if total matches
/// exceed it. <see cref="Scanned"/> / <see cref="Found"/> expose progress.
/// <para>
/// Residual risk (inherent to the server): a single windowed child whose subtree alone holds
/// millions of matches still returns them in one array; <c>maxDepth</c> and <c>resultCap</c> cap
/// the damage to a loud throw rather than an OOM, but cannot subdivide one subtree.
/// </para>
/// </remarks>
public sealed class SearchCursor
{
    private readonly OverviewScope _scope;
    private readonly int[]? _basePath;
    private readonly string[] _desc;
    private readonly string[] _name;
    private readonly string[] _val;
    private readonly int _fanout;
    private readonly int _maxDepth;
    private readonly int _resultCap;
    private readonly IReadOnlyList<ItemField>? _prefetch;
    private int _baseHandle;
    private int _baseGen;
    private int _windowIndex;
    private int _scanned;
    private int _found;
    private int? _baseTotal;

    internal SearchCursor(OverviewScope scope, OverviewItem baseItem,
        IReadOnlyList<string> description, IReadOnlyList<string> fieldName,
        IReadOnlyList<string> fieldValue, int searchFanout, int? maxDepth, int resultCap,
        IReadOnlyList<ItemField>? prefetch)
    {
        _scope = scope;
        _basePath = baseItem.Path;
        _baseHandle = baseItem.RawHandle;
        _baseGen = baseItem.Generation;
        _desc = description.ToArray();
        _name = fieldName.ToArray();
        _val = fieldValue.ToArray();
        _fanout = Math.Max(1, searchFanout);
        _maxDepth = maxDepth ?? OverviewLimits.UnboundedDepth;
        _resultCap = resultCap;
        _prefetch = prefetch;
    }

    /// <summary>Direct children of the base searched so far.</summary>
    public int Scanned => _scanned;

    /// <summary>Matches yielded so far.</summary>
    public int Found => _found;

    private int BaseHandle()
    {
        _scope.EnsureLive();
        if (_baseGen == _scope.Generation)
        {
            return _baseHandle;
        }
        if (_basePath is null)
        {
            throw new ScopeClosedException("search base handle was released and cannot be re-seated.");
        }
        var handle = _scope.RootHandle();
        foreach (var index in _basePath)
        {
            var h = handle;
            handle = _scope.Call(p => p.GetOverviewItemChild(h, index));
        }
        _baseHandle = handle;
        _baseGen = _scope.Generation;
        return handle;
    }

    private int BaseChildren()
    {
        if (_baseTotal is null)
        {
            var h = BaseHandle();
            _baseTotal = _scope.Call(p => p.GetOverviewItemChildCount(h));
        }
        return _baseTotal.Value;
    }

    private int[] SearchWindow(int start, int count)
    {
        var h = BaseHandle();
        return _scope.Call(p => p.SearchOverviewItems(h, start, count, _maxDepth, _desc, _name, _val));
    }

    /// <summary>The next window's matches as a <see cref="Page"/> (<c>null</c> when the search space is exhausted).</summary>
    public Page? NextWindow()
    {
        var total = BaseChildren();
        if (_windowIndex >= total)
        {
            return null;
        }
        if (_windowIndex > 0)
        {
            _scope.ReleaseHandles(); // release prior window before the next
        }
        var fanout = Math.Min(_fanout, total - _windowIndex);
        var handles = SearchWindow(_windowIndex, fanout);
        var windowStart = _windowIndex;
        _windowIndex += fanout;
        _scanned += fanout;
        var remaining = _resultCap - _found;
        if (handles.Length > remaining)
        {
            throw new BoundExceededException(
                $"search exceeded resultCap={_resultCap:N0} (>= {_found + handles.Length:N0} matches); " +
                "narrow the filter, lower maxDepth, or raise resultCap.");
        }
        if (handles.Length > OverviewLimits.HardCap)
        {
            throw new BoundExceededException(
                $"a single search window returned {handles.Length:N0} matches (> HardCap={OverviewLimits.HardCap:N0}); " +
                "narrow the filter or reduce maxDepth / searchFanout.");
        }
        _found += handles.Length;
        return new Page(_scope, handles, windowStart, handles.Length, total, _prefetch);
    }

    /// <summary>
    /// Yield matches one at a time, windowing the search space (consume within each window). Throws
    /// <see cref="OverviewIncompleteException"/> while the overview is loading or recording (the
    /// searched child count is captured once, so a live search would silently miss late arrivals);
    /// pass <paramref name="snapshot"/> = <c>true</c> to search just what exists now.
    /// </summary>
    public IEnumerable<OverviewItem> Stream(bool snapshot = false)
    {
        _scope.GuardGrowing(false, snapshot);
        while (true)
        {
            var page = NextWindow();
            if (page is null)
            {
                break;
            }
            foreach (var item in page)
            {
                yield return item;
            }
        }
    }

    /// <summary>Release matches and restart the search from the first window.</summary>
    public void Reset()
    {
        _scope.ReleaseHandles();
        _windowIndex = 0;
        _scanned = 0;
        _found = 0;
    }

    /// <summary>A <see cref="Page"/> of the first <c>min(n, matches)</c> matches. Throws if <c>n &gt; HardCap</c>.</summary>
    public Page Take(int n)
    {
        if (n > OverviewLimits.HardCap)
        {
            throw new BoundExceededException(
                $"Take(n={n:N0}) exceeds HardCap={OverviewLimits.HardCap:N0}; stream or raise the cap deliberately.");
        }
        var total = BaseChildren();
        var collected = new List<int>();
        var wi = 0;
        while (wi < total && collected.Count < n)
        {
            var fanout = Math.Min(_fanout, total - wi);
            collected.AddRange(SearchWindow(wi, fanout));
            wi += fanout;
            if (collected.Count > OverviewLimits.HardCap)
            {
                throw new BoundExceededException(
                    $"search accumulated > HardCap={OverviewLimits.HardCap:N0} matches; narrow the filter.");
            }
        }
        var kept = collected.Take(n).ToArray();
        _scanned = wi;
        _found = kept.Length;
        return new Page(_scope, kept, 0, kept.Length, kept.Length, _prefetch);
    }

    /// <summary>
    /// All matches as handle-free records (window-released). Throws if matches exceed
    /// <paramref name="cap"/>, or <see cref="OverviewIncompleteException"/> while loading/recording
    /// (pass <paramref name="snapshot"/> = <c>true</c> to materialize just what exists now).
    /// </summary>
    public IReadOnlyList<ItemRecord> Materialize(int cap = OverviewLimits.HardCap,
        IReadOnlyList<ItemField>? fields = null, XmlFilter? xmlFilter = null, bool snapshot = false)
    {
        _scope.GuardGrowing(false, snapshot);
        var selected = fields ?? OverviewDefaults.Prefetch;
        var total = BaseChildren();
        var output = new List<ItemRecord>();
        var wi = 0;
        var first = true;
        while (wi < total)
        {
            if (!first)
            {
                _scope.ReleaseHandles();
            }
            first = false;
            var fanout = Math.Min(_fanout, total - wi);
            var handles = SearchWindow(wi, fanout);
            wi += fanout;
            _scanned = wi;
            if (output.Count + handles.Length > cap)
            {
                throw new BoundExceededException(
                    $"search results exceed cap={cap:N0}; narrow the filter or raise cap.");
            }
            if (handles.Length > 0)
            {
                var positions = new int[handles.Length];
                var baseIndex = output.Count;
                for (var i = 0; i < handles.Length; i++)
                {
                    positions[i] = baseIndex + i;
                }
                output.AddRange(OverviewBatch.Records(_scope, handles, positions, selected, xmlFilter));
            }
            _found = output.Count;
        }
        _scope.ReleaseHandles();
        return output;
    }
}

/// <summary>
/// Owns one server-side handle session for one active overview.
/// </summary>
/// <remarks>
/// Constructed only by <see cref="Analyzer.Overview"/> -- never directly. It is the single place
/// that calls <c>ReleaseAllOverviewItemHandles</c> (on dispose, via <see cref="ReleaseHandles"/>,
/// or at a page-streaming cursor's page boundaries). Every item / page / cursor it mints checks
/// the scope is live before any network call. Dispose it (a <c>using</c> block) to release its
/// handles and, unless requested otherwise, re-select the previously active overview.
/// </remarks>
public sealed class OverviewScope : IDisposable
{
    private readonly Analyzer _analyzer;
    private readonly string? _name;
    private readonly string? _prior;
    private readonly bool _restoreActive;
    private bool _live;
    private int _generation;
    private OverviewItem? _root;

    internal OverviewScope(Analyzer analyzer, string? name, string? prior, bool restoreActive)
    {
        _analyzer = analyzer;
        _name = name;
        _prior = prior;
        _restoreActive = restoreActive;
        _live = true;
        _generation = 0;
    }

    internal Analyzer Analyzer => _analyzer;
    internal int Generation => _generation;

    // -- internal plumbing ----------------------------------------------------------
    internal void EnsureLive()
    {
        if (!_live)
        {
            throw new ScopeClosedException("the overview scope has closed; its item handles were released.");
        }
    }

    /// <summary>Invoke an Ice op through the analyzer's error-translating chokepoint.</summary>
    internal T Call<T>(Func<IceAnalyzer.AnalyzerRemoteControlPrx, T> operation)
    {
        EnsureLive();
        return _analyzer.Call(() => operation(_analyzer.Proxy));
    }

    internal int RootHandle()
    {
        EnsureLive();
        return Call(p => p.OverviewRootItem());
    }

    private void Invalidate()
    {
        _generation++;
        _root = null;
    }

    internal static int[] Extend(int[] path, int index)
    {
        var result = new int[path.Length + 1];
        Array.Copy(path, result, path.Length);
        result[path.Length] = index;
        return result;
    }

    internal static int ClampPage(int? size)
    {
        if (size is null)
        {
            return OverviewLimits.PageDefault;
        }
        return Math.Max(1, Math.Min(size.Value, OverviewLimits.PageMax));
    }

    // -- growth guard (loading / recording) -----------------------------------------

    /// <summary>True while the overview may still be growing -- a trace is loading or recording.</summary>
    internal bool IsGrowing() =>
        _analyzer.Call(() => _analyzer.Proxy.IsLoading()) ||
        _analyzer.Call(() => _analyzer.Proxy.IsRecording());

    /// <summary>
    /// Gate a full traversal when the overview is still being populated. Throws
    /// <see cref="OverviewIncompleteException"/> if a trace is loading / recording and the caller
    /// did not opt in via <paramref name="follow"/> or <paramref name="snapshot"/>. A no-op once
    /// growth has stopped.
    /// </summary>
    internal void GuardGrowing(bool follow, bool snapshot)
    {
        if (follow && snapshot)
        {
            throw new ArgumentException("pass at most one of follow / snapshot.");
        }
        if (!(follow || snapshot) && IsGrowing())
        {
            throw new OverviewIncompleteException(
                "the overview is still being populated (a trace is loading or the analyzer is " +
                "recording), so a full traversal would stop short and silently drop the rest. " +
                "Wait until it is complete (analyzer.WaitUntilLoaded()), or pass follow:true to " +
                "traverse as items arrive, or snapshot:true to traverse only what exists now.");
        }
    }

    // -- identity / context ---------------------------------------------------------

    /// <summary>The overview this scope is bound to (<c>null</c> for the already-active one).</summary>
    public string? Name => _name;

    /// <summary><c>true</c> once the scope has been disposed.</summary>
    public bool Closed => !_live;

    /// <summary>The active overview's root item (-&gt; OverviewRootItem; re-fetched if released).</summary>
    public OverviewItem Root
    {
        get
        {
            EnsureLive();
            if (_root is null)
            {
                _root = new OverviewItem(this, RootHandle(), 0, Array.Empty<int>());
            }
            return _root;
        }
    }

    // -- stateful settings (mutate the tree; invalidate existing handles) -----------

    /// <summary>The active overview's filter query (-&gt; GetOverviewQuery).</summary>
    public string Query => Call(p => p.GetOverviewQuery());

    /// <summary>Apply a filter query (-&gt; SetOverviewQuery). Invalidates existing handles.</summary>
    /// <remarks>
    /// Queries filter the overview, inside the analyzer, on any overview column or Details field
    /// -- e.g. <c>Item = "AVDTP*" &amp;&amp; Status != "OK"</c>. Comparators <c>= != &lt; &gt; &lt;= &gt;=</c>;
    /// comma-separated alternative values; <c>!</c> before a value for NOT; <c>&amp;&amp;</c>/<c>||</c> and
    /// parentheses; numbers (<c>123</c>, <c>0xABCD</c>, <c>0b0101</c>, inclusive ranges <c>7..10</c>);
    /// data patterns <c>0x[A1 ## *]</c> (<c>##</c> = any byte, trailing <c>*</c> = any rest);
    /// <c>RegEx("...")</c>; <c>ByteAt(Field, n)</c>. The analyzer re-filters in the background (a
    /// "Filtering data" running task; <see cref="Analyzer.IsLoading"/> stays <c>false</c>): by default
    /// this call BLOCKS until that finishes (<c>wait: false</c> returns immediately; settle later via
    /// <see cref="Analyzer.WaitUntilIdle"/>). A malformed query throws <see cref="OperationException"/>
    /// ("Invalid query"); an unknown field name silently matches nothing. <c>""</c> clears the filter.
    /// See the SDK guide's "Overview queries" section for the full syntax.
    /// </remarks>
    public void SetQuery(string query, bool wait = true, TimeSpan? timeout = null)
    {
        Call(p => { p.SetOverviewQuery(query); return 0; });
        Invalidate();
        if (wait)
        {
            _analyzer.WaitUntilIdle(timeout);
        }
    }

    /// <summary>The active overview's protocol layer (-&gt; GetSelectedProtocolLayer).</summary>
    public string ProtocolLayer => Call(p => p.GetSelectedProtocolLayer());

    /// <summary>Switch the protocol layer (-&gt; SelectProtocolLayer). Invalidates existing handles.</summary>
    /// <remarks>
    /// Protocol layers are per-protocol views of the overview; switching is instant (no background
    /// re-processing, unlike queries/device filters). Iterating <see cref="AvailableProtocolLayers"/>
    /// and reading <c>Root.ChildCount</c> per layer is the quickest way to fingerprint what traffic
    /// a trace contains.
    /// </remarks>
    public void SetProtocolLayer(string layer)
    {
        Call(p => { p.SelectProtocolLayer(layer); return 0; });
        Invalidate();
    }

    /// <summary>Protocol layers selectable on the active overview (-&gt; GetAvailableProtocolLayers).</summary>
    public IReadOnlyList<string> AvailableProtocolLayers() => Call(p => p.GetAvailableProtocolLayers());

    // -- search ---------------------------------------------------------------------

    /// <summary>
    /// A bounded cursor over matches under <paramref name="within"/> (default: the scope root).
    /// </summary>
    /// <remarks>
    /// Filters are <b>glob patterns</b> (<c>*</c> / <c>?</c>) or a .NET regex prefixed
    /// <c>regex:</c>; a bare literal must match the <i>whole</i> value. <paramref name="fieldName"/>
    /// / <paramref name="fieldValue"/> filter the Details fields, pairing by index when both are
    /// given. <paramref name="maxDepth"/> defaults to a finite
    /// <see cref="OverviewLimits.DefaultSearchDepth"/> (pass <c>null</c> for the whole subtree);
    /// <paramref name="resultCap"/> bounds the total matches before <see cref="BoundExceededException"/>.
    /// </remarks>
    public SearchCursor SearchCursor(
        IReadOnlyList<string>? description = null,
        IReadOnlyList<string>? fieldName = null,
        IReadOnlyList<string>? fieldValue = null,
        OverviewItem? within = null,
        int searchFanout = OverviewLimits.DefaultSearchFanout,
        int? maxDepth = OverviewLimits.DefaultSearchDepth,
        int resultCap = OverviewLimits.DefaultResultCap,
        IReadOnlyList<ItemField>? prefetch = null)
    {
        EnsureLive();
        var baseItem = within ?? Root;
        baseItem.Check();
        return new SearchCursor(this, baseItem,
            description ?? Array.Empty<string>(),
            fieldName ?? Array.Empty<string>(),
            fieldValue ?? Array.Empty<string>(),
            searchFanout, maxDepth, resultCap, prefetch ?? OverviewDefaults.Prefetch);
    }

    // -- selection ------------------------------------------------------------------

    /// <summary>The item highlighted in the GUI, or <c>null</c> (-&gt; GetSelectedOverviewItem).</summary>
    public OverviewItem? Selected
    {
        get
        {
            EnsureLive();
            var handle = Call(p => p.GetSelectedOverviewItem());
            if (handle <= 0) // returns 0/invalid when nothing is selected
            {
                return null;
            }
            return new OverviewItem(this, handle, 0, null);
        }
    }

    /// <summary>Highlight <paramref name="item"/> in the GUI (-&gt; SelectOverviewItem).</summary>
    public void Select(OverviewItem item)
    {
        item.Check();
        var handle = item.RawHandle;
        Call(p => { p.SelectOverviewItem(handle); return 0; });
    }

    // -- mid-scope reclamation ------------------------------------------------------

    /// <summary>
    /// Free <b>all</b> item handles now without closing the scope (-&gt; ReleaseAllOverviewItemHandles).
    /// </summary>
    /// <remarks>
    /// Global by nature -- there is no per-handle release. Every live item/page minted in this
    /// scope throws <see cref="ScopeClosedException"/> on next use; already-extracted
    /// <see cref="ItemRecord"/>s stay valid. This is also the primitive a page-streaming cursor
    /// uses at page boundaries.
    /// </remarks>
    public void ReleaseHandles()
    {
        Call(p => { p.ReleaseAllOverviewItemHandles(); return 0; });
        Invalidate();
    }

    /// <summary>
    /// Close the scope: release all item handles once and (unless requested otherwise) re-select
    /// the previously active overview (restored on <see cref="Dispose"/>).
    /// </summary>
    public void Dispose()
    {
        if (!_live)
        {
            return;
        }
        _live = false; // dead BEFORE release: stale use throws locally
        _analyzer.ClearActiveScope(this);
        try
        {
            _analyzer.Call(() => { _analyzer.Proxy.ReleaseAllOverviewItemHandles(); return 0; });
        }
        catch
        {
            // cleanup never masks the caller's error
        }
        if (_restoreActive && _prior is not null && _prior != _name)
        {
            try
            {
                _analyzer.Call(() => { _analyzer.Proxy.SelectOverview(_prior); return 0; });
            }
            catch
            {
                // best effort
            }
        }
    }
}

/// <summary>Internal one-round-trip batch helpers shared by lists, pages, and cursors.</summary>
internal static class OverviewBatch
{
    /// <summary>One bounded batch round-trip for a plain field across <paramref name="handles"/>.</summary>
    public static Array Column(OverviewScope scope, int[] handles, ItemField field)
    {
        if (handles.Length == 0)
        {
            return field switch
            {
                ItemField.Time => Array.Empty<long>(),
                ItemField.Data => Array.Empty<byte[]>(),
                _ => Array.Empty<string>(),
            };
        }
        GuardBatch(handles.Length);
        return field switch
        {
            ItemField.Description => scope.Call(p => p.GetOverviewItemsDescription(handles)),
            ItemField.Time => scope.Call(p => p.GetOverviewItemsTimeInPicoseconds(handles)),
            ItemField.Data => scope.Call(p => p.GetOverviewItemsData(handles)),
            ItemField.Xml => scope.Call(p => p.GetOverviewItemsXmlReport(handles)),
            _ => throw new ArgumentOutOfRangeException(nameof(field)),
        };
    }

    /// <summary>One bounded batch round-trip for the filtered Details XML across <paramref name="handles"/>.</summary>
    public static string[] Column(OverviewScope scope, int[] handles, XmlFilter filter)
    {
        if (handles.Length == 0)
        {
            return Array.Empty<string>();
        }
        GuardBatch(handles.Length);
        var names = filter.FieldNamesArray;
        return scope.Call(p => p.GetOverviewItemsXmlReportFiltered(handles, names));
    }

    private static void GuardBatch(int count)
    {
        if (count > OverviewLimits.HardCap)
        {
            throw new BoundExceededException(
                $"batch of {count:N0} handles exceeds HardCap={OverviewLimits.HardCap:N0}.");
        }
    }

    /// <summary>Snapshot <paramref name="handles"/> to handle-free records (one batch per requested field).</summary>
    public static List<ItemRecord> Records(OverviewScope scope, int[] handles, int[] positions,
        IReadOnlyList<ItemField> fields, XmlFilter? xmlFilter)
    {
        var useDefault = fields.Count == 0 && xmlFilter is null;
        var selected = useDefault ? OverviewDefaults.Prefetch : fields;

        string[]? descriptions = null;
        long[]? times = null;
        byte[][]? data = null;
        string[]? xml = null;

        foreach (var field in selected)
        {
            switch (field)
            {
                case ItemField.Description: descriptions = (string[])Column(scope, handles, ItemField.Description); break;
                case ItemField.Time: times = (long[])Column(scope, handles, ItemField.Time); break;
                case ItemField.Data: data = (byte[][])Column(scope, handles, ItemField.Data); break;
                case ItemField.Xml: xml = (string[])Column(scope, handles, ItemField.Xml); break;
            }
        }
        if (xmlFilter is not null)
        {
            xml = Column(scope, handles, xmlFilter);
        }

        var records = new List<ItemRecord>(handles.Length);
        for (var i = 0; i < handles.Length; i++)
        {
            records.Add(new ItemRecord(
                positions[i],
                descriptions?[i],
                times?[i],
                data?[i],
                xml?[i]));
        }
        return records;
    }

    /// <summary>Parse each record's filtered Details XML into a name-&gt;value dictionary.</summary>
    public static IReadOnlyList<IReadOnlyDictionary<string, string>> ToRows(
        IReadOnlyList<ItemRecord> records, string[] fieldNames)
    {
        var rows = new List<IReadOnlyDictionary<string, string>>(records.Count);
        foreach (var record in records)
        {
            var parsed = ParseDetailFields(record.Xml ?? string.Empty);
            var row = new Dictionary<string, string>(fieldNames.Length);
            foreach (var name in fieldNames)
            {
                row[name] = parsed.TryGetValue(name, out var value) ? value : string.Empty;
            }
            rows.Add(row);
        }
        return rows;
    }

    /// <summary>
    /// Best-effort name-&gt;value map from a Details XML report. Real Details XML nests
    /// <c>&lt;Item name="..." value="..."/&gt;</c> elements; we map each element carrying a name
    /// (name/Name) to its value (value/Value or element text).
    /// </summary>
    private static Dictionary<string, string> ParseDetailFields(string xmlText)
    {
        var fields = new Dictionary<string, string>();
        if (string.IsNullOrEmpty(xmlText))
        {
            return fields;
        }
        try
        {
            var doc = new XmlDocument();
            doc.LoadXml(xmlText);
            Visit(doc.DocumentElement, fields);
        }
        catch (XmlException)
        {
            // best effort: a malformed report yields no fields rather than throwing
        }
        return fields;
    }

    private static void Visit(XmlNode? node, Dictionary<string, string> fields)
    {
        if (node is null)
        {
            return;
        }
        if (node is XmlElement element)
        {
            var name = element.GetAttribute("name");
            if (string.IsNullOrEmpty(name))
            {
                name = element.GetAttribute("Name");
            }
            if (!string.IsNullOrEmpty(name))
            {
                var value = element.GetAttribute("value");
                if (string.IsNullOrEmpty(value))
                {
                    value = element.GetAttribute("Value");
                }
                if (string.IsNullOrEmpty(value))
                {
                    value = (element.InnerText ?? string.Empty).Trim();
                }
                fields[name] = value;
            }
        }
        foreach (XmlNode child in node.ChildNodes)
        {
            Visit(child, fields);
        }
    }
}

/// <summary>Analyzer-level overview entry points (reopens the foundation class).</summary>
public sealed partial class Analyzer
{
    private OverviewScope? _activeScope;

    /// <summary>Names of the available overviews (-&gt; GetAvailableOverviews). No scope needed.</summary>
    public IReadOnlyList<string> Overviews() => Call(() => Proxy.GetAvailableOverviews());

    /// <summary>Name of the currently selected overview, or <c>null</c> (-&gt; GetSelectedOverview).</summary>
    public string? ActiveOverview()
    {
        var name = Call(() => Proxy.GetSelectedOverview());
        return string.IsNullOrEmpty(name) ? null : name;
    }

    /// <summary>
    /// Open a navigation scope on <paramref name="name"/> (or the already-active overview if <c>null</c>).
    /// </summary>
    /// <remarks>
    /// Mirrors <c>Recording</c>: on entry it snapshots the active overview, selects
    /// <paramref name="name"/>, and optionally applies <paramref name="query"/> /
    /// <paramref name="protocolLayer"/>; it returns an <see cref="OverviewScope"/> (dispose it,
    /// e.g. with a <c>using</c> block, to close it). On disposal it frees all item handles once
    /// (<c>ReleaseAllOverviewItemHandles</c>) and, unless <paramref name="restoreActive"/> is
    /// <c>false</c>, re-selects the previously active overview.
    /// <para>
    /// Only one scope may be open at a time -- handle release is global, so a nested scope would
    /// free this one's handles. Opening a second throws <see cref="OperationException"/>.
    /// </para>
    /// </remarks>
    public OverviewScope Overview(string? name = null, string? query = null,
        string? protocolLayer = null, bool restoreActive = true)
    {
        if (_activeScope is not null && !_activeScope.Closed)
        {
            throw new OperationException(
                "an overview scope is already open; close it first -- " +
                "ReleaseAllOverviewItemHandles is global and would free its handles.");
        }

        var prior = Call(() => Proxy.GetSelectedOverview());
        prior = string.IsNullOrEmpty(prior) ? null : prior;
        var target = name ?? prior;
        if (name is not null)
        {
            Call(() => { Proxy.SelectOverview(name); return 0; });
        }
        if (query is not null)
        {
            Call(() => { Proxy.SetOverviewQuery(query); return 0; });
        }
        if (protocolLayer is not null)
        {
            Call(() => { Proxy.SelectProtocolLayer(protocolLayer); return 0; });
        }

        var scope = new OverviewScope(this, target, prior, restoreActive);
        _activeScope = scope;
        return scope;
    }

    internal void ClearActiveScope(OverviewScope scope)
    {
        if (ReferenceEquals(_activeScope, scope))
        {
            _activeScope = null;
        }
    }
}
