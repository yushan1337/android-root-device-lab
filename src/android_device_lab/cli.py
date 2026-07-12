import android_device_lab.adb as adb
def main() -> None:
    print("Welcome to Android Root Device Lab CLI!")
    print("请输入功能数字:")
    print("1. 列出已连接的设备")
    print("2. 获取设备信息")
    choice = input("选择功能: ")
    if choice == "1":
        adb.list_devices()
        return 0
    elif choice == "2":
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
    elif choice == "3":
        battery_info = adb.get_battery_info()
        line = [f"温度: {battery_info.temperature}",
                f"交流电状态: {battery_info.ac_power_status}",
                f"电压: {battery_info.voltage}",
                f"电量: {battery_info.level}"]
        for l in line:
            print(l)        
if __name__ == "__main__":
    main()

