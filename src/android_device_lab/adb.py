# src/android_device_lab/adb.py
# adb.py
import logging
from android_device_lab.command import CommandResult, run_command
from android_device_lab.models import DeviceInfo, BatteryInfo, StorageInfo
from android_device_lab.parsers import parse_battery_info,parse_storage_info,parse_sdk_version

logger = logging.getLogger(__name__)

def adb_command(serial: str, *args: str) -> list[str]:
    return ["adb", "-s", serial, *args]

def list_devices() -> CommandResult:
    return run_command(["adb", "devices"])

def get_device_info(serial: str) -> DeviceInfo:
    logger.info("开始获取设备信息...")
    device_info = DeviceInfo(
        product=run_command(adb_command(serial, "shell", "getprop", "ro.product.name"),timeout=5,
        check=True,).stdout.strip(),
        model=run_command(adb_command(serial, "shell", "getprop", "ro.product.model")).stdout.strip(),
        manufacturer=run_command(adb_command(serial, "shell", "getprop", "ro.product.manufacturer")).stdout.strip(),
        android_version=run_command(adb_command(serial, "shell", "getprop", "ro.build.version.release")).stdout.strip(),
        sdk_version=parse_sdk_version(run_command(adb_command(serial, "shell", "getprop", "ro.build.version.sdk")).stdout.strip()),
        build_fingerprint=run_command(adb_command(serial, "shell", "getprop", "ro.build.fingerprint")).stdout.strip(),
        brand=run_command(adb_command(serial, "shell", "getprop", "ro.product.brand")).stdout.strip(),
        security_patch=run_command(adb_command(serial, "shell", "getprop", "ro.build.version.security_patch")).stdout.strip(),
    )
    logger.info(f"获取设备信息完成: {device_info}")
    return device_info

def get_battery_info(serial: str) -> BatteryInfo:
    result = run_command(adb_command(serial, "shell", "dumpsys", "battery"),timeout=5,
    check=True,)
    logger.info(f"获取电池信息完成: ")
    return parse_battery_info(result.stdout)


def get_storage_info(serial: str) -> StorageInfo:
    result = run_command(adb_command(serial, "shell", "df", "-h"),timeout=5,
    check=True,)
    return parse_storage_info(result.stdout)