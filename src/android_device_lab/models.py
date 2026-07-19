from dataclasses import dataclass



@dataclass(slots=True)
class DeviceInfo:
    product: str | None = None  
    model: str | None = None
    manufacturer: str | None = None
    android_version: str | None = None
    sdk_version: int | None = None
    build_fingerprint: str | None = None
    brand: str | None = None
    security_patch: str | None = None

@dataclass(slots=True)
class BatteryInfo:
    temperature_c: float | None = None
    ac_powered: bool | None = None
    voltage_mv: int | None = None
    level_percent: int | None = None  

@dataclass(slots=True)
class StorageInfo:
    total: str | None = None
    used: str | None = None
    available: str | None = None
    use_percentage: int | None = None
