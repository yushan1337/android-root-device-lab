import android_device_lab.adb as adb
from datetime import datetime
from android_device_lab.exporters import DiagnosticReport, export_json_report,export_markdown_report, get_all_info
from pathlib import Path
import argparse
import logging

logger = logging.getLogger(__name__)

def configure_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

def export_report_by_format(
    report,
    output_root: Path,
    report_format: str,
) -> None:
    report_dir = output_root / report.generated_at

    if report_format in ("json", "both"):
        json_file = report_dir / "report.json"
        export_json_report(report, json_file)
        logger.info("JSON report exported to %s", json_file.resolve())

    if report_format in ("markdown", "both"):
        markdown_file = report_dir / "report.md"
        export_markdown_report(report, markdown_file)
        logger.info("Markdown report exported to %s", markdown_file.resolve())

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="android-device-lab",
        description="ADB-based Android device diagnostics toolkit",
    )

    parser.add_argument(
        "--serial",
        required=True,
        help="Android device serial number",
    )

    parser.add_argument(
        "--format",
        choices=["json", "markdown", "both"],
        default="both",
        help="Report format to export",
    )

    parser.add_argument(
        "--output",
        default="reports",
        help="Output directory for diagnostic reports",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    return parser.parse_args(argv)

def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    configure_logging(args.verbose)

    output_root = Path(args.output)

    report = get_all_info()

    report_dir = output_root / report.generated_at

        if choice == 1:
            print(adb.list_devices(args.serial).stdout)

        elif choice == 2:
            device_info = adb.get_device_info(args.serial)
            line =[f"型号: {device_info.model}",
                f"制造商: {device_info.manufacturer}",
                f"Android版本: {device_info.android_version}",
            f"SDK版本: {device_info.sdk_version}",
            f"Build指纹: {device_info.build_fingerprint}",
            f"品牌: {device_info.brand}",
            f"安全补丁: {device_info.security_patch}"]
            for l in line:
                print(l)

        elif choice == 3:
            battery_info = adb.get_battery_info()
            line = [f"温度: {int(battery_info.temperature)/10}°C",
                    f"交流电状态: {battery_info.ac_power_status}",
                    f"电压: {battery_info.voltage}mv",
                    f"电量: {battery_info.level}%"]
            for l in line:
                print(l)    

        elif choice == 4:
            storage_info = adb.get_storage_info()
            line = [f"总容量: {storage_info.total}",
                    f"已用容量: {storage_info.used}",
                    f"可用容量: {storage_info.availiable}",
                    f"使用百分比: {storage_info.use_percentage}"]
            for l in line:
                print(l)   

        elif choice == 5:
            report = get_all_info()
            report_dir = Path("reports") / report.generated_at
            json_file = report_dir / "report.json"
            export_json_report(report, json_file)
            print(f"诊断报告已导出到: {json_file.resolve()}")
        
        elif choice == 6:
            report = get_all_info()
            report_dir = Path("reports") / report.generated_at
            markdown_file = report_dir / "report.md"
            export_markdown_report(report, markdown_file)
            print(f"诊断报告已导出到: {markdown_file.resolve()}")
        
        else:
            print("无效的选择，请输入有效的数字.")
            continue
if __name__ == "__main__":
    main()

