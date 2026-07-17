from dataclasses import dataclass
from dataclasses import asdict
from pathlib import Path
import json
from datetime import datetime
import android_device_lab.adb
from android_device_lab.models import BatteryInfo, DeviceInfo, StorageInfo
@dataclass
class DiagnosticReport:
    generated_at: str
    device: DeviceInfo
    battery: BatteryInfo
    storage: StorageInfo


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
    report = DiagnosticReport(
        generated_at=datetime.now().strftime("%Y-%m-%d_%H%M%S"),
        device=device_info,
        battery=battery_info,
        storage=storage_info
    )
    return report

def export_markdown_report(report: DiagnosticReport, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    report_dict = asdict(report)

    with output.open("w", encoding="utf-8") as file:
        file.write(f"# 诊断报告\n")
        file.write(f"生成时间: {report.generated_at}\n\n")

        file.write(f"## 设备信息\n")
        for key, value in report_dict["device"].items():
            file.write(f"- {key}: {value}\n")

        file.write(f"\n## 电池信息\n")
        for key, value in report_dict["battery"].items():
            file.write(f"- {key}: {value}\n")

        file.write(f"\n## 存储信息\n")
        for key, value in report_dict["storage"].items():
            file.write(f"- {key}: {value}\n")