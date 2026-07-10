# src/android_device_lab/adb.py
# adb.py
from android_device_lab.command import CommandResult, run_command
def list_devices() -> None:
    result = run_command(["adb", "devices"])
    print(result.stdout)
