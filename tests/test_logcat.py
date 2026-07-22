import pytest

from android_device_lab.logcat import build_logcat_command


def test_build_logcat_command_without_filters() -> None:
    command = build_logcat_command("ABC123")

    assert command == ["adb", "-s", "ABC123", "logcat"]


def test_build_logcat_command_with_level_filter() -> None:
    command = build_logcat_command("ABC123", level="E")

    assert command == ["adb", "-s", "ABC123", "logcat", "*:E"]


def test_build_logcat_command_normalizes_level() -> None:
    command = build_logcat_command("ABC123", level="w")

    assert command == ["adb", "-s", "ABC123", "logcat", "*:W"]


def test_build_logcat_command_with_tag_and_level_filter() -> None:
    command = build_logcat_command(
        "ABC123",
        tag="ActivityManager",
        level="W",
    )

    assert command == [
        "adb",
        "-s",
        "ABC123",
        "logcat",
        "ActivityManager:W",
        "*:S",
    ]


def test_build_logcat_command_with_tag_defaults_to_verbose() -> None:
    command = build_logcat_command("ABC123", tag="ActivityManager")

    assert command == [
        "adb",
        "-s",
        "ABC123",
        "logcat",
        "ActivityManager:V",
        "*:S",
    ]


def test_build_logcat_command_rejects_invalid_level() -> None:
    with pytest.raises(ValueError, match="Invalid logcat level"):
        build_logcat_command("ABC123", level="ERROR")