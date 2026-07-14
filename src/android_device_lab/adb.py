# src/android_device_lab/adb.py
# adb.py
import logging
from dataclasses import dataclass
from android_device_lab.command import CommandResult, run_command

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
    availiable: str = "N/A"
    use_percentage: str = "N/A"

def adb_command(serial: str, *args: str) -> list[str]:
    return ["adb", "-s", serial, *args]

def list_devices() -> CommandResult:
    return run_command(["adb", "devices"])

def get_device_info(serial: str) -> DeviceInfo:
    logging.info("开始获取设备信息...")
    device_info = DeviceInfo(
        product=run_command(adb_command(serial, "shell", "getprop", "ro.product.name")).stdout.strip(),
        model=run_command(adb_command(serial, "shell", "getprop", "ro.product.model")).stdout.strip(),
        manufacturer=run_command(adb_command(serial, "shell", "getprop", "ro.product.manufacturer")).stdout.strip(),
        android_version=run_command(adb_command(serial, "shell", "getprop", "ro.build.version.release")).stdout.strip(),
        sdk_version=run_command(adb_command(serial, "shell", "getprop", "ro.build.version.sdk")).stdout.strip(),
        build_fingerprint=run_command(adb_command(serial, "shell", "getprop", "ro.build.fingerprint")).stdout.strip(),
        brand=run_command(adb_command(serial, "shell", "getprop", "ro.product.brand")).stdout.strip(),
        security_patch=run_command(adb_command(serial, "shell", "getprop", "ro.build.version.security_patch")).stdout.strip(),
    )
    logging.info(f"获取设备信息完成: {device_info}")
    return device_info

def get_battery_info(serial: str) -> BatteryInfo:
    logging.info("开始获取电池信息...")
    op = run_command(adb_command(serial, "shell", "dumpsys", "battery")).stdout.strip()

    data = {}
    for line in op.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if key == "temperature":
            data["temperature"] = value
        elif key == "AC powered":
            data["ac_power_status"] = value
        elif key == "voltage":
            data["voltage"] = value
        elif key == "level":
            data["level"] = value

    battery_info = BatteryInfo(**data)  # 只传收集到的字段
    logging.info(f"获取电池信息完成: {battery_info}")
    return battery_info

def parse_storage_info(raw: str) -> StorageInfo:
    for line in raw.strip().splitlines():
        parts = line.split()

        if len(parts) < 6:
            continue

        if parts[-1] != "/data":
            continue

        return StorageInfo(
            total=parts[1],
            used=parts[2],
            availiable=parts[3],
            use_percentage=parts[4],
        )
    logging.info(f"获取存储信息完成")
    return StorageInfo()

def get_storage_info(serial: str) -> StorageInfo:
    result = run_command(adb_command(serial, "shell", "df", "-h"))
    logging.info("开始获取存储信息...")
    return parse_storage_info(result.stdout)