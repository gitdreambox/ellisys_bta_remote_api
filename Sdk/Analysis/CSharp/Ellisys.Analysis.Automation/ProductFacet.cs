namespace Ellisys.Analysis.Automation;

/// <summary>Shared plumbing for the product facets: lazily attaches the product proxy and maps a
/// missing/wrong-product interface to <see cref="NotAvailableException"/>.</summary>
public abstract class ProductFacet
{
    private protected readonly Analyzer Owner;

    private protected ProductFacet(Analyzer owner) => Owner = owner;

    private protected static TPrx Attach<TPrx>(Analyzer owner, string identityValue,
        Func<global::Ice.ObjectPrx, TPrx?> checkedCast, string product) where TPrx : class
    {
        try
        {
            var prx = owner.Proxy.ice_identity(global::Ice.Util.stringToIdentity(identityValue));
            var typed = checkedCast(prx);
            if (typed is null)
            {
                throw new NotAvailableException($"This analyzer does not provide the {product} interface.");
            }
            return typed;
        }
        catch (global::Ice.ObjectNotExistException e)
        {
            throw new NotAvailableException($"This analyzer does not provide the {product} interface.", e);
        }
        catch (global::Ice.FacetNotExistException e)
        {
            throw new NotAvailableException($"This analyzer does not provide the {product} interface.", e);
        }
        catch (global::Ice.LocalException e)
        {
            throw new ConnectionFailedException(e.Message, e);
        }
    }

    private protected static long CheckAddr48(long address)
    {
        if (address < 0 || address > 0xFFFF_FFFF_FFFFL)
        {
            throw new ArgumentException($"address must be a 48-bit value, got 0x{address:X}");
        }
        return address;
    }

    /// <summary>
    /// Parse a 48-bit address from the forms the analyzer displays (e.g. in the Overview's
    /// Communication column): "AA:BB:CC:DD:EE:FF", "AA-BB-CC-DD-EE-FF", 12 hex digits, or "0x...".
    /// Exactly 12 hex digits always parse as hex (it's an address, even when all the digits are
    /// 0-9); any other plain-digit string is decimal.
    /// </summary>
    internal static long ParseAddr48(string address)
    {
        var s = address.Trim().Replace(":", "").Replace("-", "").Replace(" ", "");
        try
        {
            var value = s.StartsWith("0x", StringComparison.OrdinalIgnoreCase)
                ? Convert.ToInt64(s.Substring(2), 16)
                : s.Length == 12
                    ? Convert.ToInt64(s, 16)
                    : long.Parse(s, System.Globalization.CultureInfo.InvariantCulture);
            return CheckAddr48(value);
        }
        catch (Exception e) when (e is FormatException or OverflowException or ArgumentOutOfRangeException)
        {
            throw new ArgumentException(
                $"not a 48-bit address: \"{address}\" (expected \"AA:BB:CC:DD:EE:FF\", 12 hex digits, 0x..., or a number)", e);
        }
    }

    private protected static int CheckPanId(int panId)
    {
        if (panId < 0 || panId > 0xFFFF)
        {
            throw new ArgumentException($"PAN id must be a 16-bit value, got 0x{panId:X}");
        }
        return panId;
    }

    private protected static byte[] CheckKey(byte[] key, int length)
    {
        if (key is null || key.Length != length)
        {
            throw new ArgumentException($"key must be exactly {length} bytes, got {key?.Length ?? 0}");
        }
        return key;
    }
}
