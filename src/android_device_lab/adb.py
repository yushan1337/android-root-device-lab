# src/android_device_lab/adb.py
# adb.py
import logging
from dataclasses import dataclass
from android_device_lab.command import CommandResult, run_command
from android_device_lab.models import DeviceInfo, BatteryInfo, StorageInfo

logger = logging.getLogger(__name__)

def adb_command(serial: str, *args: str) -> list[str]:
    return ["adb", "-s", serial, *args]

def list_devices() -> CommandResult:
    return run_command(["adb", "devices"])

def get_device_info(serial: str) -> DeviceInfo:
    logger.info("开始获取设备信息...")
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
    logger.info(f"获取设备信息完成: {device_info}")
    return device_info

def get_battery_info(serial: str) -> BatteryInfo:
    result = run_command(adb_command(serial, "shell", "dumpsys", "battery"))
    logger.info(f"获取电池信息完成: ")
    return parse_battery_info(result.stdout)

def parse_battery_info(raw: str) -> BatteryInfo:
    data = {}
    for line in raw.splitlines():
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

    return BatteryInfo(**data)  # 只传收集到的字段   

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
            available=parts[3],
            use_percentage=parts[4],
        )
    return StorageInfo()

def get_storage_info(serial: str) -> StorageInfo:
    result = run_command(adb_command(serial, "shell", "df", "-h"))
    return parse_storage_info(result.stdout)