from dataclasses import dataclass



@dataclass(slots=True)
class DeviceInfo:
    product: str = "N/A"  
    model: str = "N/A"
    manufacturer: str = "N/A"
    android_version: str = "N/A"
    sdk_version: str = "N/A"
    build_fingerprint: str = "N/A"
    brand: str = "N/A"
    security_patch: str = "N/A"

@dataclass(slots=True)
class BatteryInfo:
    temperature_c: float | None = None
    ac_powered: bool | None = None
    voltage_mv: int | None = None
    level_percent: int | None = None  

@dataclass(slots=True)
class StorageInfo:
    total: str = "N/A"
    used: str = "N/A"
    available: str = "N/A"
    use_percentage: str = "N/A"
