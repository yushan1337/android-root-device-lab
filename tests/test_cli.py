from android_device_lab.cli import parse_args

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


def test_parse_args_serial_is_optional() -> None:
    args = parse_args([])

    assert args.serial is None