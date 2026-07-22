from dataclasses import dataclass
from dataclasses import asdict
from pathlib import Path
import json
from datetime import datetime
import android_device_lab.adb
from android_device_lab.models import BatteryInfo, DeviceInfo, StorageInfo
from android_device_lab.presentation import (
    BATTERY_FIELD_LABELS,
    DEVICE_FIELD_LABELS,
    STORAGE_FIELD_LABELS,
    format_report_value,
)




@dataclass(slots=True)
class DiagnosticReport:
    schema_version: str
    generated_at: str
    device_serial: str
    device: DeviceInfo
    battery: BatteryInfo
    storage: StorageInfo
    warnings: list[str]


def export_json_report(report: DiagnosticReport, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    report_dict = asdict(report)

    with output.open("w", encoding="utf-8") as file:
        json.dump(
            report_dict,
            file,
            ensure_ascii=False,
            indent=2,
        )

def get_all_info(serial: str) -> DiagnosticReport:
    device_info = android_device_lab.adb.get_device_info(serial)
    battery_info = android_device_lab.adb.get_battery_info(serial)
    storage_info = android_device_lab.adb.get_storage_info(serial)
    warnings = build_report_warnings(
    device=device_info,
    battery=battery_info,
    storage=storage_info,
    )

    report = DiagnosticReport(
        schema_version="1.0",
        generated_at=datetime.now().strftime("%Y-%m-%d_%H%M%S"),
        device_serial=serial,
        device=device_info,
        battery=battery_info,
        storage=storage_info,
        warnings=warnings,
    )
    return report

def export_markdown_report(report: DiagnosticReport, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    report_dict = asdict(report)

    with output.open("w", encoding="utf-8") as file:
        file.write("# Android 设备诊断报告\n\n")
        file.write("## 报告信息\n\n")
        file.write("| 字段 | 值 |\n")
        file.write("|---|---|\n")
        file.write(f"| Schema | {report.schema_version} |\n")
        file.write(f"| 生成时间 | {report.generated_at} |\n")
        file.write(f"| 设备序列号 | {report.device_serial} |\n") 

        if report.warnings:
            file.write("\n## Warnings\n\n")

        for warning in report.warnings:
            file.write(f"- {warning}\n")

        write_markdown_section(
        file=file,
        title="设备信息",
        values=report_dict["device"],
        labels=DEVICE_FIELD_LABELS,
        section="device",
        )

        write_markdown_section(
        file=file,
        title="电池信息",
        values=report_dict["battery"],
        labels=BATTERY_FIELD_LABELS,
        section="battery",
        )

        write_markdown_section(
            file=file,
            title="存储信息",
            values=report_dict["storage"],
            labels=STORAGE_FIELD_LABELS,
            section="storage"
        )

def write_markdown_section(
    file,
    title: str,
    values: dict[str, object | None],
    labels: dict[str, str],
    section: str,
) -> None:
    file.write(f"\n## {title}\n\n")
    file.write("| 字段 | 值 |\n")
    file.write("|---|---|\n")

    for key, value in values.items():
        label = labels.get(key, key)
        formatted_value = format_report_value(section, key, value)
        file.write(f"| {label} | {formatted_value} |\n")


def build_report_warnings(
    device: DeviceInfo,
    battery: BatteryInfo,
    storage: StorageInfo,
) -> list[str]:
    warnings: list[str] = []

    if battery.temperature_c is None:
        warnings.append("Battery temperature unavailable")

    if battery.level_percent is None:
        warnings.append("Battery level unavailable")

    if storage.available is None:
        warnings.append("Storage available space unavailable")

    if storage.use_percentage is None:
        warnings.append("Storage usage percentage unavailable")

    if device.security_patch is None:
        warnings.append("Security patch value is empty")

    return warnings