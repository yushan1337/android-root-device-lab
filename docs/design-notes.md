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

## 当前限制

- 不支持指定设备序列号（仅操作默认设备）
- 不支持多设备
