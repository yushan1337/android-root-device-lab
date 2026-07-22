from android_device_lab.exporters import export_json_report,export_markdown_report, get_all_info
from android_device_lab.adb import resolve_device_serial
from pathlib import Path
import argparse
import logging
from android_device_lab.exceptions import AndroidDeviceLabError
logger = logging.getLogger(__name__)
from android_device_lab.presentation import format_report_value


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


def display_device_info(device_info) -> None:
    lines = [
        f"型号: {format_report_value('device', 'model', device_info.model)}",
        f"制造商: {format_report_value('device', 'manufacturer', device_info.manufacturer)}",
        f"Android版本: {format_report_value('device', 'android_version', device_info.android_version)}",
        f"SDK版本: {format_report_value('device', 'sdk_version', device_info.sdk_version)}",
        f"Build指纹: {format_report_value('device', 'build_fingerprint', device_info.build_fingerprint)}",
        f"品牌: {format_report_value('device', 'brand', device_info.brand)}",
        f"安全补丁: {format_report_value('device', 'security_patch', device_info.security_patch)}",
    ]

    for line in lines:
        print(line)


def display_storage_info(storage_info) -> None:
    lines = [
        f"总容量: {format_report_value('storage', 'total', storage_info.total)}",
        f"已用容量: {format_report_value('storage', 'used', storage_info.used)}",
        f"可用容量: {format_report_value('storage', 'available', storage_info.available)}",
        f"使用率: {format_report_value('storage', 'use_percentage', storage_info.use_percentage)}",
    ]

    for line in lines:
        print(line)


def display_battery_info(battery_info) -> None:
    lines = [
        f"温度: {format_report_value('battery', 'temperature_c', battery_info.temperature_c)}",
        f"交流电状态: {format_report_value('battery', 'ac_powered', battery_info.ac_powered)}",
        f"电压: {format_report_value('battery', 'voltage_mv', battery_info.voltage_mv)}",
        f"电量: {format_report_value('battery', 'level_percent', battery_info.level_percent)}",
    ]

    for line in lines:
        print(line)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="android-device-lab",
        description="ADB-based Android device diagnostics toolkit",
    )

    parser.add_argument(
        "--serial",
        help="Android device serial number",
    )

    parser.add_argument(
        "--format",
        choices=["json", "markdown", "both"],
        default="both",
        help="Report format to export",
    )

    parser.add_argument(
        "--device-info",
        action="store_true",
        help="Display device information",
    )

    parser.add_argument(
        "--battery-info",
        action="store_true",
        help="Display battery information",
    )

    parser.add_argument(
        "--storage-info",
        action="store_true",
        help="Display storage information",
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
    try:
        serial = resolve_device_serial(args.serial)
        report = get_all_info(serial)
        export_report_by_format(
            report=report,
            output_root=output_root,
            report_format=args.format,
        )
    except AndroidDeviceLabError as error:
        logger.error("Error: %s", error)

        if args.verbose:
            raise

        raise SystemExit(1)
    if args.device_info:
        display_device_info(report.device)

    if args.battery_info:
        display_battery_info(report.battery)

    if args.storage_info:
        display_storage_info(report.storage)
if __name__ == "__main__":
    main()

