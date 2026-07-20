
from android_device_lab.parsers import parse_battery_info, parse_storage_info,parse_sdk_version


def test_parse_battery_info_empty_output_returns_empty_model() -> None:
    battery = parse_battery_info("")

    assert battery.temperature_c is None
    assert battery.ac_powered is None
    assert battery.voltage_mv is None
    assert battery.level_percent is None


def test_parse_storage_info_data_partition() -> None:
    raw = """
Filesystem        Size  Used Avail Use% Mounted on
/dev/block/dm-6   110G   40G   70G  37% /data
"""

    storage = parse_storage_info(raw)

    assert storage.total == "110G"
    assert storage.used == "40G"
    assert storage.available == "70G"
    assert storage.use_percentage == 37


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


def test_parse_battery_info_missing_temperature() -> None:
    raw = """
  AC powered: true
  level: 50
  voltage: 4000
"""

    battery = parse_battery_info(raw)

    assert battery.temperature_c is None
    assert battery.ac_powered is True
    assert battery.level_percent == 50
    assert battery.voltage_mv == 4000


def test_parse_battery_info_invalid_temperature() -> None:
    raw = """
  temperature: hot
  level: 50
"""

    battery = parse_battery_info(raw)

    assert battery.temperature_c is None
    assert battery.level_percent == 50


def test_parse_battery_info_line_with_multiple_colons() -> None:
    raw = """
  level: 80
  health: status: good
  temperature: 300
"""

    battery = parse_battery_info(raw)

    assert battery.level_percent == 80
    assert battery.temperature_c == 30.0


def test_parse_battery_info_empty_level() -> None:
    raw = """
  level:
  voltage: 4100
  temperature: 300
"""

    battery = parse_battery_info(raw)

    assert battery.level_percent is None
    assert battery.voltage_mv == 4100
    assert battery.temperature_c == 30.0


def test_parse_storage_info_without_data_partition_returns_empty_model() -> None:
    raw = """
Filesystem        Size  Used Avail Use% Mounted on
/dev/block/dm-1   2G    1G   1G    50% /system
"""

    storage = parse_storage_info(raw)

    assert storage.total is None
    assert storage.used is None
    assert storage.available is None
    assert storage.use_percentage is None


def test_parse_storage_info_selects_data_partition_from_multiple_mounts() -> None:
    raw = """
Filesystem        Size  Used Avail Use% Mounted on
/dev/block/dm-1   2G    1G   1G    50% /system
/dev/block/dm-6   110G  40G  70G   37% /data
/dev/block/dm-7   5G    1G   4G    20% /vendor
"""

    storage = parse_storage_info(raw)

    assert storage.total == "110G"
    assert storage.used == "40G"
    assert storage.available == "70G"
    assert storage.use_percentage == 37


def test_parse_storage_info_ignores_short_lines() -> None:
    raw = """
Filesystem Size Used
broken line
/dev/block/dm-6   110G   40G   70G  37% /data
"""

    storage = parse_storage_info(raw)

    assert storage.total == "110G"
    assert storage.used == "40G"
    assert storage.available == "70G"
    assert storage.use_percentage == 37


def test_parse_sdk_version_returns_int() -> None:
    assert parse_sdk_version("35") == 35


def test_parse_sdk_version_invalid_value_returns_none() -> None:
    assert parse_sdk_version("") is None
    assert parse_sdk_version("abc") is None
    assert parse_sdk_version(None) is None


def test_parse_devices_output_without_devices() -> None:
    raw = "List of devices attached\n\n"

    devices = parse_devices_output(raw)

    assert devices == []