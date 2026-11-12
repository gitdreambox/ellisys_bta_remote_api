namespace Ellisys.Analysis.Automation;

/// <summary>
/// Which devices a capture keeps or excludes (-> ConfigureDeviceFilter). Shared by the Bluetooth
/// and Wi-Fi device filters.
/// </summary>
public enum DeviceFilterMode
{
    /// <summary>Keep traffic from every device.</summary>
    KeepAll = 0,

    /// <summary>Exclude background/uninvolved devices.</summary>
    ExcludeBackground = 1,

    /// <summary>Keep only the listed devices.</summary>
    KeepOnly = 2,

    /// <summary>Keep traffic involving the listed devices.</summary>
    KeepInvolving = 3,
}
