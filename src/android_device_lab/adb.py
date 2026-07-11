# src/android_device_lab/adb.py
# adb.py
import logging
from dataclasses import dataclass
@dataclass
class DeviceInfo:
    product: str
    model: str
    manufacturer: str
    android_version: str
    sdk_version: str
    build_fingerprint: str
    brand: str
    security_patch: str
from android_device_lab.command import CommandResult, run_command
def list_devices() -> CommandResult:
    result = run_command(["adb", "devices"])
    print(result.stdout)
    return result
def get_device_info() -> DeviceInfo:
    logging.info("开始获取设备信息...")
    device_info = DeviceInfo(
        product=run_command(["adb", "shell", "getprop", "ro.product.name"]).stdout.strip(),
        model=run_command(["adb", "shell", "getprop", "ro.product.model"]).stdout.strip(),
        manufacturer=run_command(["adb", "shell", "getprop", "ro.product.manufacturer"]).stdout.strip(),
        android_version=run_command(["adb", "shell", "getprop", "ro.build.version.release"]).stdout.strip(),
        sdk_version=run_command(["adb", "shell", "getprop", "ro.build.version.sdk"]).stdout.strip(),
        build_fingerprint=run_command(["adb", "shell", "getprop", "ro.build.fingerprint"]).stdout.strip(),
        brand=run_command(["adb", "shell", "getprop", "ro.product.brand"]).stdout.strip(),
        security_patch=run_command(["adb", "shell", "getprop", "ro.build.version.security_patch"]).stdout.strip()
    )
    logging.info(f"获取设备信息完成: {device_info}")
    return device_info