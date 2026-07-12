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
@dataclass
class BetteryInfo:
    temperature: str = "N/A"  # 默认值为 "N/A"，表示未获取到温度信息
    ac_power_status: str = "N/A"  # 默认值为 "N/A"，表示未获取到交流电状态信息
    voltage: str = "N/A"  # 默认值为 "N/A"，表示未获取到电压信息
    level: str = "N/A"  # 默认值为 "N/A"，表示未获取到电量信息  
@dataclass
class StorageInfo:
    total: str
    used: str
    availiable: str
    use_percentage: str
from android_device_lab.command import CommandResult, run_command
def list_devices() -> CommandResult:
    result = run_command(["adb", "devices"])
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
        security_patch=run_command(["adb", "shell", "getprop", "ro.build.version.security_patch"]).stdout.strip(),
    )
    logging.info(f"获取设备信息完成: {device_info}")
    return device_info
def get_battery_info() -> BetteryInfo:
    logging.info("开始获取电池信息...")
    op = run_command(["adb", "shell", "dumpsys", "battery"]).stdout.strip()
    for line in op.splitlines():           # ← 先在外面解析
        if "temperature" in line:
            temperature = line.split(":")[1].strip()
        elif "AC powered" in line:
            ac_power_status = line.split(":")[1].strip()
        elif line.strip().startswith("voltage"):
            voltage = line.split(":")[1].strip()
        elif "level" in line:
            level = line.split(":")[1].strip()

    battery_info = BetteryInfo(            # ← 解析完再构造
        temperature=temperature,
        ac_power_status=ac_power_status,
        voltage=voltage,
        level=level
    )
    logging.info(f"获取电池信息完成: {battery_info}")
    return battery_info
def get_storage_info() -> StorageInfo:
    logging.info("开始获取存储信息...")
    result = run_command(["adb", "shell", "df", "-h","|","grep", "/data$"]).stdout.strip()
    result=result.split()
    storage_info = StorageInfo(
        total=result[1],
        used=result[2],
        availiable=result[3],
        use_percentage=result[4]
    )
    logging.info(f"获取存储信息完成: {storage_info}")
    return storage_info