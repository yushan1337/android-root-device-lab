from android_device_lab.adb import adb_command


def test_adb_command_with_serial() -> None:
    command = adb_command("ABC123", "shell", "id")

    assert command == ["adb", "-s", "ABC123", "shell", "id"]


