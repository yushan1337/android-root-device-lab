# Design Notes — Android Device Info Collection

## 字段说明

| 字段 | ADB 属性 | 含义 | 示例值 |
|------|----------|------|--------|
| `product` | `ro.product.name` | 产品代号 | `socrates` |
| `model` | `ro.product.model` | 设备型号 | `22127RK46C` |
| `manufacturer` | `ro.product.manufacturer` | 制造商 | `Xiaomi` |
| `android_version` | `ro.build.version.release` | Android 系统版本 | `15` |
| `sdk_version` | `ro.build.version.sdk` | SDK API 级别 | `35` |
| `build_fingerprint` | `ro.build.fingerprint` | 完整构建指纹 | `Redmi/socrates/socrates:15/...` |
| `brand` | `ro.product.brand` | 品牌名称 | `Redmi` |
| `security_patch` | `ro.build.version.security_patch` | 安全补丁日期 | `2025-12-01` |

## 注意事项

- 所有设备基础字段通过 `adb shell getprop <属性名>` 获取。
- `security_patch` 在不同 ROM 上路径可能不同，备选：`ro.vendor.build.security_patch`。
- `getprop` 返回值为空时不报错，当前 v0.1 调用方仍需要自行处理空值。
- 当前 CLI 支持在只有一个可用设备时自动选择 serial；多设备时仍要求显式传入 `--serial`。所有设备相关采集命令都通过 `adb -s SERIAL ...` 执行。

## 实现位置

- 数据模型：`models.py` — `DeviceInfo`, `BatteryInfo`, `StorageInfo`, `ConnectedDevice`, `DeviceState`
- 采集函数：`adb.py` — `get_device_info()`, `get_battery_info()`, `get_storage_info()`, `list_devices()`, `resolve_device_serial()`
- 解析函数：`parsers.py` — `parse_battery_info()`, `parse_storage_info()`, `parse_devices_output()`
- 命令封装：`command.py` — `run_command()`, `CommandResult`
- 报告导出：`exporters.py` — `export_json_report()`, `export_markdown_report()`
- CLI 入口：`cli.py` — `parse_args()`, `main()`

## CLI 设计决策

v0.1 已从早期菜单式交互改为 argparse 参数式 CLI。

当前支持：

```text
--serial SERIAL  # 可选；多设备时需要
--format json|markdown|both
--output OUTPUT
--device-info
--battery-info
--storage-info
--verbose
```

设计取舍：

- `--serial` 当前可选；如果恰好一个状态为 `device` 的设备在线，则自动选择；如果多个可用设备在线，则要求用户显式指定。
- `--format` 默认 `both`，方便一次运行同时生成机器可读 JSON 和人类可读 Markdown。
- `--output` 默认 `reports`，并在其下创建时间戳目录。
- `--device-info`、`--battery-info`、`--storage-info` 只控制终端显示，不影响报告采集和导出。
- `--verbose` 用于控制 logging 输出。

## 报告导出设计

报告输出目录：

```text
reports/YYYY-MM-DD_HHMMSS/
├── report.json
└── report.md
```

`DiagnosticReport` 由三个 dataclass 组成：

- `DeviceInfo`
- `BatteryInfo`
- `StorageInfo`

JSON 和 Markdown 均从同一个 `DiagnosticReport` 生成，避免两套数据源不一致。

当前 Markdown 报告仍直接使用 dataclass 字段名，例如：

```text
model
android_version
temperature_c
ac_powered
available
use_percentage
```

这有利于当前阶段保持实现简单，但展示效果仍比较原始。后续可以增加字段名映射层，并在 Markdown / CLI 展示时补充 `°C`、`mV`、`%` 等单位。

## 测试策略

v0.1 的测试重点是不依赖真实 Android 设备的纯逻辑：

- `adb_command()`：验证 `adb -s SERIAL ...` 命令构造。
- `parse_storage_info()`：验证 `df -h` 输出中 `/data` 行的解析。
- `parse_args()`：验证 CLI 参数解析。
- 电池温度格式化：验证 Android 原始温度值和异常值的展示结果。
- JSON / Markdown 导出：使用 `tmp_path` 验证报告文件内容。

暂不测试真实 ADB 设备采集流程，因为这会引入设备连接状态、USB 授权、ROM 差异等不稳定因素。

## 边界情况记录

### 1. `voltage` 关键字误匹配

`dumpsys battery` 输出中可能有两行包含 `voltage`：

```text
voltage: 3932
Max charging voltage: 5000000
```

使用 `in` 做子串匹配时，`"voltage" in line` 对两行都返回 `True`，可能导致 `voltage` 变量被覆盖。

**解决：** 当前解析逻辑使用拆分后的精确 key 判断：

```python
key, value = line.split(":", 1)
key = key.strip()

if key == "voltage":
    ...
```

---

### 2. `security_patch` 属性路径错误

`getprop ro.system.security_patch` 在部分设备上可能返回空字符串，因为该属性路径不一定存在。

实际设备上常见路径：

```text
ro.build.version.security_patch
ro.vendor.build.security_patch
```

**解决：** v0.1 使用 `ro.build.version.security_patch`。后续可考虑增加 fallback。

---

### 3. 电池温度展示崩溃风险

Android `dumpsys battery` 中的 `temperature` 通常是十倍摄氏度，例如：

```text
temperature: 312
```

展示层会显示为：

```text
31.2°C
```

早期实现直接调用：

```python
int(battery_info.temperature)
```

当值为 `N/A`、空字符串或其他非数字文本时会触发 `ValueError`。

**解决：** v0.1 将温度格式化拆为 `format_battery_temperature()`，无法转换时显示 `N/A`，避免 CLI 展示阶段崩溃。

---

### 4. `StorageInfo.available` 拼写修复

早期实现曾将可用容量字段写成错误拼写。

Week 02 Day 1 已统一修复为：

```python
available
```

该修改已同步到：

- `StorageInfo`
- `parse_storage_info()`
- CLI 显示函数
- JSON / Markdown 报告字段
- 测试
- README / design notes

后续如果对报告 schema 做兼容性管理，需要在 changelog 或 schema version 中说明字段名变化。

## 当前限制

- 不支持多设备批量采集。
- 命令执行层已建立显式错误模型，包括非零退出码、命令不存在、超时和 `stderr` 保留。
- CLI 普通模式会捕获项目异常并给出错误信息；`--verbose` 模式保留 traceback 以便调试。
- 设备发现层已支持基础状态解析和自动选择；`unauthorized`、`offline` 等恢复建议仍可继续细化。
- Markdown 报告目前使用原始字段名，尚未做中文字段名映射和单位美化。
- 电池数据已在解析层规范化，但展示层仍需要统一的格式化函数处理 `None`、单位和布尔值。
- 存储信息目前只关注 `/data` 分区。
- 不支持 logcat 分析、root 专项检测、GUI、多设备工作流或后台长期运行。
