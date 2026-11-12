// Polyfills that let the SDK's modern C# compile for the net48 target. On net10 these types
// already live in the BCL, so under `#if NETFRAMEWORK` the whole file compiles to nothing there.
//
//   * IsExternalInit  -- records and `init`-only setters (C# 9).
//   * Index / Range   -- the Range-based slice indexers on OverviewItemList / Page
//                        (added to the BCL in netstandard2.1; faithful port of the runtime impl).
//
// Index/Range are public to match the BCL surface, because the indexers that take a Range are
// public (an internal Range parameter would be less accessible than its method).
#if NETFRAMEWORK
namespace System.Runtime.CompilerServices
{
    /// <summary>Marker the compiler requires for <c>init</c>-only setters and records on .NET Framework.</summary>
    internal static class IsExternalInit { }
}

namespace System
{
    /// <summary>Represents a type that can index a collection from the start or the end.</summary>
    public readonly struct Index : IEquatable<Index>
    {
        private readonly int _value;

        public Index(int value, bool fromEnd = false)
        {
            if (value < 0) throw new ArgumentOutOfRangeException(nameof(value), "Non-negative number required.");
            _value = fromEnd ? ~value : value;
        }

        private Index(int value) => _value = value;

        public static Index Start => new Index(0);
        public static Index End => new Index(~0);

        public static Index FromStart(int value)
        {
            if (value < 0) throw new ArgumentOutOfRangeException(nameof(value), "Non-negative number required.");
            return new Index(value);
        }

        public static Index FromEnd(int value)
        {
            if (value < 0) throw new ArgumentOutOfRangeException(nameof(value), "Non-negative number required.");
            return new Index(~value);
        }

        public int Value => _value < 0 ? ~_value : _value;
        public bool IsFromEnd => _value < 0;

        public int GetOffset(int length)
        {
            var offset = _value;
            if (IsFromEnd) offset += length + 1;
            return offset;
        }

        public static implicit operator Index(int value) => FromStart(value);

        public override bool Equals(object? value) => value is Index index && _value == index._value;
        public bool Equals(Index other) => _value == other._value;
        public override int GetHashCode() => _value;
        public override string ToString() => IsFromEnd ? "^" + ((uint)Value) : ((uint)Value).ToString();
    }

    /// <summary>Represents a range with a start and an end <see cref="Index"/>.</summary>
    public readonly struct Range : IEquatable<Range>
    {
        public Index Start { get; }
        public Index End { get; }

        public Range(Index start, Index end)
        {
            Start = start;
            End = end;
        }

        public override bool Equals(object? value) => value is Range r && r.Start.Equals(Start) && r.End.Equals(End);
        public bool Equals(Range other) => other.Start.Equals(Start) && other.End.Equals(End);
        public override int GetHashCode() => Start.GetHashCode() * 31 + End.GetHashCode();
        public override string ToString() => Start + ".." + End;

        public static Range StartAt(Index start) => new Range(start, Index.End);
        public static Range EndAt(Index end) => new Range(Index.Start, end);
        public static Range All => new Range(Index.Start, Index.End);

        public (int Offset, int Length) GetOffsetAndLength(int length)
        {
            var startIndex = Start;
            var start = startIndex.IsFromEnd ? length - startIndex.Value : startIndex.Value;

            var endIndex = End;
            var end = endIndex.IsFromEnd ? length - endIndex.Value : endIndex.Value;

            if ((uint)end > (uint)length || (uint)start > (uint)end)
                throw new ArgumentOutOfRangeException(nameof(length));

            return (start, end - start);
        }
    }
}

namespace System.Collections.Generic
{
    /// <summary>Enables <c>foreach (var (key, value) in dictionary)</c> on .NET Framework
    /// (<see cref="KeyValuePair{TKey,TValue}"/> gained an instance <c>Deconstruct</c> in netstandard2.1).</summary>
    internal static class KeyValuePairDeconstructExtensions
    {
        public static void Deconstruct<TKey, TValue>(this KeyValuePair<TKey, TValue> pair, out TKey key, out TValue value)
        {
            key = pair.Key;
            value = pair.Value;
        }
    }
}
#endif
