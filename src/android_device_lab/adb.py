# src/android_device_lab/adb.py
# adb.py
import logging
from android_device_lab.command import run_command,CommandResult
from android_device_lab.models import DeviceInfo, BatteryInfo, DeviceState, StorageInfo, ConnectedDevice
from android_device_lab.parsers import parse_battery_info,parse_storage_info,parse_sdk_version,parse_devices_output
from android_device_lab.exceptions import AdbDeviceError

logger = logging.getLogger(__name__)

def adb_command(serial: str, *args: str) -> list[str]:
    return ["adb", "-s", serial, *args]


def get_device_info(serial: str) -> DeviceInfo:
    logger.info("开始获取设备信息...")
    device_info = DeviceInfo(
        product=run_command(adb_command(serial, "shell", "getprop", "ro.product.name"),timeout=5,
        check=True,).stdout.strip(),
        model=run_command(adb_command(serial, "shell", "getprop", "ro.product.model"),timeout=5, check=True).stdout.strip(),
        manufacturer=run_command(adb_command(serial, "shell", "getprop", "ro.product.manufacturer"),timeout=5, check=True).stdout.strip(),
        android_version=run_command(adb_command(serial, "shell", "getprop", "ro.build.version.release"),timeout=5, check=True).stdout.strip(),
        sdk_version=parse_sdk_version(run_command(adb_command(serial, "shell", "getprop", "ro.build.version.sdk"),timeout=5, check=True).stdout.strip()),
        build_fingerprint=run_command(adb_command(serial, "shell", "getprop", "ro.build.fingerprint"),timeout=5, check=True).stdout.strip(),
        brand=run_command(adb_command(serial, "shell", "getprop", "ro.product.brand"),timeout=5, check=True).stdout.strip(),
        security_patch=run_command(adb_command(serial, "shell", "getprop", "ro.build.version.security_patch"),timeout=5, check=True).stdout.strip(),
    )
    logger.info(f"获取设备信息完成: {device_info}")
    return device_info

def get_battery_info(serial: str) -> BatteryInfo:
    result = run_command(adb_command(serial, "shell", "dumpsys", "battery"),timeout=10,
    check=True,)
    logger.info(f"获取电池信息完成: ")
    return parse_battery_info(result.stdout)


def get_storage_info(serial: str) -> StorageInfo:
    result = run_command(adb_command(serial, "shell", "df", "-h"),timeout=10,
    check=True,)
    return parse_storage_info(result.stdout)


def select_device(
    devices: list[ConnectedDevice],
    requested_serial: str | None,
    ) -> ConnectedDevice:
    if requested_serial is not None:
        for device in devices:
            if device.serial == requested_serial and device.state == DeviceState.DEVICE:
                return device
    if requested_serial is None:
        available_devices = [
        device for device in devices
        if device.state == DeviceState.DEVICE
        ]
        if len(available_devices) == 1:
            return available_devices[0]
        if len(available_devices) == 0:
            raise AdbDeviceError("No available devices")
    raise AdbDeviceError("Device not found")


def list_devices() -> CommandResult:
    return run_command(["adb","devices","-l"], timeout=5, check=True)


def resolve_device_serial(requested_serial: str | None) -> str:
    result = list_devices()
    devices = parse_devices_output(result.stdout)
    selected = select_device(devices, requested_serial)
    return selected.serial
    