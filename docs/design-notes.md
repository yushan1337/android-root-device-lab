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

- 所有字段通过 `adb shell getprop <属性名>` 获取
- `security_patch` 在不同 ROM 上路径可能不同，备选：`ro.vendor.build.security_patch`
- `getprop` 返回值为空时不报错，需调用方自行处理空值

## 实现位置

- 数据模型：`adb.py` — `DeviceInfo` dataclass
- 采集函数：`adb.py` — `get_device_info()`
- 命令封装：`command.py` — `run_command()`

## 边界情况记录

### 1. `voltage` 关键字误匹配

`dumpsys battery` 输出中有两行包含 `voltage`：

```
voltage: 3932              ← 想要的实际电压
Max charging voltage: 5000000  ← 也会被 "voltage" in line 匹配到
```

使用 `in` 做子串匹配时，`"voltage" in line` 对两行都返回 `True`，导致 `voltage` 变量被覆盖为 `5000000`。

**解决：** 改用 `line.strip().startswith("voltage")` 只匹配以 `voltage` 开头的行。

---

### 2. `security_patch` 属性路径错误

`getprop ro.system.security_patch` 返回空字符串，因为该属性在此设备上不存在。

实际设备上存在的路径：

```
ro.build.version.security_patch → 2025-12-01
ro.vendor.build.security_patch  → 2025-12-01
```

**解决：** 改为 `ro.build.version.security_patch`。不同 ROM 上路径可能不同，备选 `ro.vendor.build.security_patch`。

## 当前限制

- 目前默认操作单台已连接设备。
- 不支持指定设备序列号。
- 不支持多设备选择。
- 设备连接状态检查仍较基础；未连接设备时部分采集流程可能无法继续。
- Markdown 报告目前使用原始字段名和原始字段值，尚未做中文字段名映射和单位美化。
- 电池温度在采集层保留原始值（例如 `348`），展示层再转换为 `34.8°C`。
- 存储信息目前只关注 `/data` 分区。
- 报告导出路径当前使用默认时间戳目录，暂不支持用户自定义输出路径。
