import json

from android_device_lab.models import BatteryInfo, DeviceInfo, StorageInfo
from android_device_lab.exporters import DiagnosticReport, export_json_report, export_markdown_report, build_report_warnings


def test_export_json_report_writes_expected_fields(tmp_path) -> None:
    report = DiagnosticReport(
    schema_version="1.0",
    generated_at="2026-07-15_140000",
    device_serial="ABC123",
    device=DeviceInfo(model="Pixel 7", manufacturer="Google"),
    battery=BatteryInfo(level_percent=76, temperature_c=31.2),
    storage=StorageInfo(total="110G", used="40G", available="70G", use_percentage=37),
    warnings=[],
    )
    output = tmp_path / "report.json"

    export_json_report(report, output)

    assert output.exists()

    data = json.loads(output.read_text(encoding="utf-8"))

    assert data["generated_at"] == "2026-07-15_140000"
    assert data["device"]["model"] == "Pixel 7"
    assert data["device"]["manufacturer"] == "Google"
    assert data["battery"]["level_percent"] == 76
    assert data["storage"]["total"] == "110G"
    assert data["battery"]["temperature_c"] == 31.2
    assert data["schema_version"] == "1.0"
    assert data["device_serial"] == "ABC123"
    assert data["warnings"] == []


def test_export_markdown_report_writes_expected_sections(tmp_path) -> None:
    report = DiagnosticReport(
    schema_version="1.0",
    generated_at="2026-07-15_140000",
    device_serial="ABC123",
    device=DeviceInfo(model="Pixel 7", manufacturer="Google"),
    battery=BatteryInfo(level_percent=76, temperature_c=31.2),
    storage=StorageInfo(total="110G", used="40G", available="70G", use_percentage=37),
    warnings=[],
    )
    output = tmp_path / "report.md"

    export_markdown_report(report, output)

    assert output.exists()

    content = output.read_text(encoding="utf-8")

    assert "# Android 设备诊断报告" in content
    assert "## 报告信息" in content
    assert "| Schema | 1.0 |" in content

    assert "## 电池信息" in content
    assert "| 电量 | 76% |" in content
    assert "| 温度 | 31.2 °C |" in content

    assert "## 存储信息" in content
    assert "| 总容量 | 110G |" in content
    assert "| 使用率 | 37% |" in content


def test_export_markdown_report_formats_none_as_na(tmp_path) -> None:
    report = DiagnosticReport(
        schema_version="1.0",
        generated_at="2026-07-15_140000",
        device_serial="ABC123",
        device=DeviceInfo(model=None),
        battery=BatteryInfo(level_percent=None, temperature_c=None),
        storage=StorageInfo(total=None, use_percentage=None),
        warnings=[],
    )

    output = tmp_path / "report.md"

    export_markdown_report(report, output)

    content = output.read_text(encoding="utf-8")

    assert "| 型号 | N/A |" in content
    assert "| 电量 | N/A |" in content
    assert "| 温度 | N/A |" in content
    assert "| 总容量 | N/A |" in content
    assert "| 使用率 | N/A |" in content


def test_build_report_warnings_for_missing_fields() -> None:
    warnings = build_report_warnings(
        device=DeviceInfo(security_patch=None),
        battery=BatteryInfo(temperature_c=None, level_percent=None),
        storage=StorageInfo(available=None, use_percentage=None),
    )

    assert "Battery temperature unavailable" in warnings
    assert "Battery level unavailable" in warnings
    assert "Storage available space unavailable" in warnings
    assert "Storage usage percentage unavailable" in warnings
    assert "Security patch value is empty" in warnings


def test_build_report_warnings_returns_empty_list_for_complete_report() -> None:
    warnings = build_report_warnings(
        device=DeviceInfo(security_patch="2026-07-01"),
        battery=BatteryInfo(temperature_c=31.2, level_percent=76),
        storage=StorageInfo(available="70G", use_percentage=37),
    )

    assert warnings == []
