from android_device_lab.adb import adb_command
from android_device_lab.parsers import parse_battery_info, parse_storage_info

def test_adb_command_with_serial() -> None:
    command = adb_command("ABC123", "shell", "id")

    assert command == ["adb", "-s", "ABC123", "shell", "id"]


def test_parse_storage_info_data_partition() -> None:
    raw = """
Filesystem        Size  Used Avail Use% Mounted on
/dev/block/dm-6   110G   40G   70G  37% /data
"""

    storage = parse_storage_info(raw)

    assert storage.total == "110G"
    assert storage.used == "40G"
    assert storage.available == "70G"
    assert storage.use_percentage == "37%"


def test_parse_battery_info_returns_typed_fields() -> None:
    raw = """
Current Battery Service state:
  AC powered: false
  USB powered: true
  level: 76
  voltage: 4210
  temperature: 312
"""

    battery = parse_battery_info(raw)

    assert battery.level_percent == 76
    assert battery.voltage_mv == 4210
    assert battery.temperature_c == 31.2
    assert battery.ac_powered is False