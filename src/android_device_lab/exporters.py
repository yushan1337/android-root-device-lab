from dataclasses import dataclass
from android_device_lab.adb import DeviceInfo, BetteryInfo, StorageInfo
from dataclasses import asdict
from pathlib import Path
import json

@dataclass
class DiagnosticReport:
    generated_at: str
    device: DeviceInfo
    battery: BetteryInfo
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