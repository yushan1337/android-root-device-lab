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
- 报告导出：`exporters.py` — `DiagnosticReport`, `export_json_report()`, `export_markdown_report()`, `build_report_warnings()`
- 展示格式：`presentation.py` — 字段中文标签、单位格式化、布尔值与 `N/A` 展示
- 实时日志：`logcat.py` — `build_logcat_command()`, `stream_logcat()`, `stop_process()`
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
--logcat
--logcat-level LEVEL
--logcat-tag TAG
--verbose
```

设计取舍：

- `--serial` 当前可选；如果恰好一个状态为 `device` 的设备在线，则自动选择；如果多个可用设备在线，则要求用户显式指定。
- `--format` 默认 `both`，方便一次运行同时生成机器可读 JSON 和人类可读 Markdown。
- `--output` 默认 `reports`，并在其下创建时间戳目录。
- `--device-info`、`--battery-info`、`--storage-info` 只控制终端显示，不影响报告采集和导出。
- `--verbose` 用于控制 logging 输出。
- `--logcat` 是独立实时日志模式：启用后只读取 logcat，不生成 JSON / Markdown 报告。
- `--logcat-level` 和 `--logcat-tag` 会被转换为 ADB logcat filter spec，例如 `*:E` 或 `ActivityManager:W *:S`。

## 报告导出设计

报告输出目录：

```text
reports/YYYY-MM-DD_HHMMSS/
├── report.json
└── report.md
```

`DiagnosticReport` 是报告层的数据契约，包含：

- `schema_version`：当前为 `1.0`，用于后续报告格式演进。
- `generated_at`：报告生成时间。
- `device_serial`：实际采集目标设备 serial。
- `device`：`DeviceInfo`。
- `battery`：`BatteryInfo`。
- `storage`：`StorageInfo`。
- `warnings`：命令成功但部分可选字段缺失时的非致命提示。

JSON 和 Markdown 均从同一个 `DiagnosticReport` 生成，避免两套数据源不一致。

JSON 输出保持结构化数据：

- `temperature_c` 保持数字，例如 `31.2`。
- `voltage_mv` 保持整数，例如 `4210`。
- `level_percent` / `use_percentage` 保持整数，例如 `76`、`37`。
- `ac_powered` 保持布尔值。
- 缺失字段使用 JSON `null`。
- 不保存 `°C`、`mV`、`%`、`N/A` 等展示字符串。

Markdown 和终端输出通过 `presentation.py` 统一转换为面向人的展示：

```text
level_percent -> 电量 -> 76%
temperature_c -> 温度 -> 31.2 °C
ac_powered -> 交流电供电 -> 是 / 否
None -> N/A
```

`warnings` 只表示“核心命令成功，但报告中某些字段不可用”。核心命令失败、ADB 超时、设备不可用等情况仍由命令层和设备发现层抛出显式异常，不降级为 warning。

## 实时 Logcat 设计

Day 6 的实际实现从原计划的“有限行数 Logcat 摘要”调整为“实时 Logcat stream”。当前目标是提供一个可手动观察设备日志的最小工具，而不是把日志统计写入诊断报告。

CLI 参数：

```text
--logcat              启用实时 logcat 模式
--logcat-level LEVEL  最低日志级别：V, D, I, W, E, F, S
--logcat-tag TAG      只显示指定 tag 的日志
```

ADB filter spec 规则：

```text
无过滤                  -> adb -s SERIAL logcat
仅 level=E              -> adb -s SERIAL logcat *:E
tag=ActivityManager     -> adb -s SERIAL logcat ActivityManager:V *:S
tag + level=W           -> adb -s SERIAL logcat ActivityManager:W *:S
```

实现取舍：

- `adb logcat` 是长期运行命令，不能复用基于 `subprocess.run()` 的一次性命令封装。
- `stream_logcat()` 使用 `subprocess.Popen()` 启动进程，并实时读取 `stdout`。
- 用户按 Ctrl+C 时捕获 `KeyboardInterrupt`，视为正常停止，而不是程序错误。
- `finally` 中调用 `stop_process()`，先 `terminate()`，等待超时后再 `kill()`，避免残留 `adb logcat` 子进程。
- 不追求跨设备、跨 ROM、跨 ADB 版本的一致错误文本。实际验证中设备突然断开可能只有退出码而没有稳定 stderr。当前只保证不静默、不长期卡死、不残留子进程，并抛出基础 `LogcatStreamError`。

当前未实现：

- 不把 logcat 摘要写入 `DiagnosticReport`。
- 不保存完整原始日志。
- 不做 ANR / tombstone / native crash 深度分析。
- 不做多设备并行实时监听。

## 测试策略

v0.1 的测试重点是不依赖真实 Android 设备的纯逻辑：

- `adb_command()`：验证 `adb -s SERIAL ...` 命令构造。
- `parse_storage_info()`：验证 `df -h` 输出中 `/data` 行的解析。
- `parse_args()`：验证 CLI 参数解析。
- 电池温度格式化：验证 Android 原始温度值和异常值的展示结果。
- JSON / Markdown 导出：使用 `tmp_path` 验证报告文件内容。
- 展示层格式化：验证 Markdown 单位、中文标签、`None` 到 `N/A` 的转换。
- warning 生成：验证缺失字段会进入 `DiagnosticReport.warnings`。
- logcat 命令构造：验证 level / tag filter spec。
- logcat CLI 参数：验证 `--logcat`、`--logcat-level`、`--logcat-tag` 的解析。

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
- Markdown 报告已使用中文字段名和单位展示。
- 展示层格式化已集中到 `presentation.py`，供 Markdown 和 CLI 复用。
- 存储信息目前只关注 `/data` 分区。
- 已支持单设备实时 logcat stream，但不支持结构化 logcat 摘要、原始日志归档、GUI、多设备并行监听或后台长期运行。
