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


def test_parse_args_logcat_options() -> None:
    args = parse_args([
        "--logcat",
        "--logcat-level",
        "E",
        "--logcat-tag",
        "ActivityManager",
    ])

    assert args.logcat is True
    assert args.logcat_level == "E"
    assert args.logcat_tag == "ActivityManager"


def test_parse_args_logcat_level_accepts_lowercase() -> None:
    args = parse_args(["--logcat", "--logcat-level", "e"])

    assert args.logcat_level == "e"