from android_device_lab.cli import parse_args
from android_device_lab.cli import parse_args, format_battery_temperature

def test_parse_args_json_verbose() -> None:
    args = parse_args([
        "--serial",
        "ABC123",
        "--format",
        "json",
        "--output",
        "reports",
        "--verbose",
    ])

    assert args.serial == "ABC123"
    assert args.format == "json"
    assert args.output == "reports"
    assert args.verbose is True

def test_format_battery_temperature_numeric_android_raw_value() -> None:
    assert format_battery_temperature("312") == "31.2°C"


def test_format_battery_temperature_na() -> None:
    assert format_battery_temperature("N/A") == "N/A"


def test_format_battery_temperature_invalid_value() -> None:
    assert format_battery_temperature("unknown") == "N/A"