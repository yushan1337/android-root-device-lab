from android_device_lab.adb import adb_command, parse_storage_info


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
    assert storage.availiable == "70G"
    assert storage.use_percentage == "37%"