from android_device_lab.models import BatteryInfo,StorageInfo






def parse_int(value: str | None) -> int | None:
    if value is None:
        return None

    try:
        return int(value)
    except ValueError:
        return None


def parse_android_bool(value: str | None) -> bool | None:
    if value == "true":
        return True
    if value == "false":
        return False
    return None


def parse_battery_info(raw: str) -> BatteryInfo:
    values: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        values[key.strip()] = value.strip()
        
    raw_temperature = parse_int(values.get("temperature"))
    return BatteryInfo(
        temperature_c=(
            raw_temperature / 10
            if raw_temperature is not None
            else None
        ),
        ac_powered=parse_android_bool(values.get("AC powered")),
        voltage_mv=parse_int(values.get("voltage")),
        level_percent=parse_int(values.get("level")),
        )



def parse_storage_info(raw: str) -> StorageInfo:
    for line in raw.strip().splitlines():
        parts = line.split()

        if len(parts) < 6:
            continue

        if parts[-1] != "/data":
            continue

        return StorageInfo(
            total=parts[1],
            used=parts[2],
            available=parts[3],
            use_percentage=parts[4],
        )
    return StorageInfo()