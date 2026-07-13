import android_device_lab.adb as adb
from datetime import datetime
from android_device_lab.exporters import DiagnosticReport, export_json_report,export_markdown_report, get_all_info
from pathlib import Path

def main() -> None:
    while True:
        print("Welcome to Android Root Device Lab CLI!")
        print("请输入功能数字:")
        print("1. 列出已连接的设备")
        print("2. 获取设备信息")
        print("3. 获取电池信息")
        print("4. 获取存储信息")
        print("5. 导出诊断报告为JSON文件")
        print("6. 导出诊断报告为Markdown文件")
        choice = input("选择功能: ")
        try:
            choice = int(choice)
        except ValueError:
            print("输入错误，请输入有效的数字.")
            continue

        if choice == 1:
            print(adb.list_devices().stdout)

        elif choice == 2:
            device_info = adb.get_device_info()
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

