





DEVICE_FIELD_LABELS = {
    "product": "产品",
    "model": "型号",
    "manufacturer": "制造商",
    "android_version": "Android 版本",
    "sdk_version": "SDK 版本",
    "build_fingerprint": "Build 指纹",
    "brand": "品牌",
    "security_patch": "安全补丁",
}

BATTERY_FIELD_LABELS = {
    "temperature_c": "温度",
    "ac_powered": "交流电供电",
    "voltage_mv": "电压",
    "level_percent": "电量",
}

STORAGE_FIELD_LABELS = {
    "total": "总容量",
    "used": "已用容量",
    "available": "可用容量",
    "use_percentage": "使用率",
}


def format_optional(value: object | None, suffix: str = "") -> str:
    if value is None:
        return "N/A"

    return f"{value}{suffix}"


def format_bool(value: bool | None) -> str:
    if value is None:
        return "N/A"

    return "是" if value else "否"


def format_report_value(section: str, key: str, value: object | None) -> str:
    if section == "battery":
        if key == "temperature_c":
            return format_optional(value, " °C")

        if key == "voltage_mv":
            return format_optional(value, " mV")

        if key == "level_percent":
            return format_optional(value, "%")

        if key == "ac_powered":
            if isinstance(value, bool) or value is None:
                return format_bool(value)
            return "N/A"

    if section == "storage":
        if key == "use_percentage":
            return format_optional(value, "%")

    return format_optional(value)