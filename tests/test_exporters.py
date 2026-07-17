import json

from android_device_lab.models import BatteryInfo, DeviceInfo, StorageInfo
from android_device_lab.exporters import DiagnosticReport, export_json_report, export_markdown_report


def test_export_json_report_writes_expected_fields(tmp_path) -> None:
    report = DiagnosticReport(
        generated_at="2026-07-15_140000",
        device=DeviceInfo(model="Pixel 7", manufacturer="Google"),
        battery=BatteryInfo(level=76, temperature="312"),
        storage=StorageInfo(total="110G", used="40G", available="70G", use_percentage="37%"),
    )

    output = tmp_path / "report.json"

    export_json_report(report, output)

    assert output.exists()

    data = json.loads(output.read_text(encoding="utf-8"))

    assert data["generated_at"] == "2026-07-15_140000"
    assert data["device"]["model"] == "Pixel 7"
    assert data["device"]["manufacturer"] == "Google"
    assert data["battery"]["level"] == "76"
    assert data["storage"]["total"] == "110G"

def test_export_markdown_report_writes_expected_sections(tmp_path) -> None:
    report = DiagnosticReport(
        generated_at="2026-07-15_140000",
        device=DeviceInfo(model="Pixel 7", manufacturer="Google"),
        battery=BatteryInfo(level="76", temperature="312"),
        storage=StorageInfo(total="110G", used="40G", available="70G", use_percentage="37%"),
    )

    output = tmp_path / "report.md"

    export_markdown_report(report, output)

    assert output.exists()

    content = output.read_text(encoding="utf-8")

    assert "# 诊断报告" in content
    assert "## 设备信息" in content
    assert "- model: Pixel 7" in content
    assert "## 电池信息" in content
    assert "- level: 76" in content
    assert "## 存储信息" in content
    assert "- total: 110G" in content