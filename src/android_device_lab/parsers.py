from android_device_lab.models import BatteryInfo, StorageInfo, DeviceState, ConnectedDevice


def parse_percentage(value: str | None) -> int | None:
    if value is None:
        return None

    return parse_int(value.rstrip("%"))


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
        values[key] = value
        
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
            use_percentage=parse_percentage(parts[4]),
        )
    return StorageInfo()


def parse_sdk_version(raw: str | None)  -> int | None:
    if raw is None:
        return None
    try:
        return int(raw)
    except ValueError:
        return None


def parse_devices_output(raw: str) -> list[ConnectedDevice]:
    
    devices: list[ConnectedDevice] = []

    for line in raw.splitlines():
        line = line.strip()

        if not line:
            continue

        if line == "List of devices attached":
            continue

        parts = line.split()

        if len(parts) < 2:
            continue
        serial = parts[0]
        raw_state = parts[1]
        if raw_state not in {
        "device",
        "offline",
        "unauthorized"
        }:
            state = DeviceState.UNKNOWN
        else:
            state = parse_device_state(raw_state)
        details: dict[str, str] = {}
        for item in parts[2:]:
            if ":" not in item:
                continue

            key, value = item.split(":", 1)
            details[key] = value
        devices.append(
            ConnectedDevice(
                serial=serial,
                state=state,
                product=details.get("product"),
                model=details.get("model"),
                transport_id=details.get("transport_id"),
            )
        )
    return devices


def parse_device_state(raw: str) -> DeviceState:
    try:
        return DeviceState(raw)
    except ValueError:
        return DeviceState.UNKNOWN

