# src/android_device_lab/adb.py
# adb.py
from android_device_lab.command import CommandResult, run_command
def list_devices() -> CommandResult:
    result = run_command(["adb", "devices"])
    print(result.stdout)
    return result
def get_device_info(device_id: str) -> CommandResult:
    result = run_command(["adb", "-s", device_id, "shell", "getprop"])
    print(result.stdout)
    return result