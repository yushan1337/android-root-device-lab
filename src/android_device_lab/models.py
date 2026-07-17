from dataclasses import dataclass



@dataclass
class DeviceInfo:
    product: str = "N/A"  
    model: str = "N/A"
    manufacturer: str = "N/A"
    android_version: str = "N/A"
    sdk_version: str = "N/A"
    build_fingerprint: str = "N/A"
    brand: str = "N/A"
    security_patch: str = "N/A"

@dataclass
class BatteryInfo:
    temperature: str = "N/A"  
    ac_power_status: str = "N/A" 
    voltage: str = "N/A"  
    level: str = "N/A"  

@dataclass
class StorageInfo:
    total: str = "N/A"
    used: str = "N/A"
    available: str = "N/A"
    use_percentage: str = "N/A"
