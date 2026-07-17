# Android Root Device Lab

A Python + ADB based Android device diagnostics toolkit.

## Goals

- Collect Android device information
- Collect battery and storage diagnostics
- Export diagnostic reports as Markdown / JSON
- Support command-line usage for automation
- Analyze logcat output in later versions
- Support rooted Android devices in later versions

## Current Version

v0.1 Python prototype.

This version focuses on Python engineering basics and a working ADB diagnostic workflow:

- virtual environment based development
- `src/` project layout
- safe `subprocess.run()` usage without `shell=True`
- dataclass-based diagnostic models
- JSON / Markdown report export
- argparse-based CLI
- logging
- pytest tests for pure parsing, CLI, and report export logic

The Python prototype is not intended to be the final desktop product. It is the automation and validation layer for future iterations.

## Tech Stack

- Python 3.11+
- ADB (Android Debug Bridge)
- Android shell commands
- Markdown / JSON reports
- pytest

## Project Structure

```text
android-root-device-lab/
├── src/
│   └── android_device_lab/
│       ├── cli.py        # CLI entry point
│       ├── adb.py        # ADB data collection and parsers
│       ├── command.py    # Safe command execution wrapper
│       └── exporters.py  # JSON / Markdown report export
├── tests/                # pytest tests
├── reports/              # Generated diagnostic reports, ignored by Git
├── samples/              # Sample outputs
├── docs/                 # Design notes
└── .gitignore
```

## Requirements

- Python 3.11 or newer
- ADB installed and available in `PATH`
- Android device with USB debugging enabled
- A known device serial number

Check connected devices:

```bash
adb devices
```

Example output:

```text
List of devices attached
SERIAL_NUMBER    device
```

Use the `SERIAL_NUMBER` value with `--serial`.

## Development Setup

Create and activate a virtual environment from the project root:

```bash
cd /path/to/android-root-device-lab
python3 -m venv .venv
source .venv/bin/activate
```

Install test dependencies as needed:

```bash
python -m pip install pytest
```

This project currently uses a `src/` layout. During development, commands can be run from the project root with `PYTHONPATH=src`:

```bash
PYTHONPATH=src ./.venv/bin/python -m android_device_lab.cli --help
```

The pytest configuration in `pyproject.toml` already sets:

```toml
[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
```

So tests can be run with:

```bash
.venv/bin/python -m pytest
```

## Running the CLI

Show help:

```bash
PYTHONPATH=src ./.venv/bin/python -m android_device_lab.cli --help
```

The CLI requires `--serial`:

```bash
PYTHONPATH=src ./.venv/bin/python -m android_device_lab.cli --serial SERIAL_NUMBER
```

By default, this exports both JSON and Markdown reports.

## CLI Options

```text
--serial SERIAL       Android device serial number. Required.
--format FORMAT       Report format: json, markdown, or both. Default: both.
--output OUTPUT       Output directory for diagnostic reports. Default: reports.
--device-info         Also print device information to the terminal.
--battery-info        Also print battery information to the terminal.
--storage-info        Also print storage information to the terminal.
--verbose             Enable verbose logging.
```

## Examples

Export both JSON and Markdown reports:

```bash
PYTHONPATH=src ./.venv/bin/python -m android_device_lab.cli \
  --serial SERIAL_NUMBER
```

Export only JSON:

```bash
PYTHONPATH=src ./.venv/bin/python -m android_device_lab.cli \
  --serial SERIAL_NUMBER \
  --format json
```

Export only Markdown:

```bash
PYTHONPATH=src ./.venv/bin/python -m android_device_lab.cli \
  --serial SERIAL_NUMBER \
  --format markdown
```

Use a custom output directory:

```bash
PYTHONPATH=src ./.venv/bin/python -m android_device_lab.cli \
  --serial SERIAL_NUMBER \
  --output reports
```

Enable verbose logging:

```bash
PYTHONPATH=src ./.venv/bin/python -m android_device_lab.cli \
  --serial SERIAL_NUMBER \
  --verbose
```

Export a report and also print selected sections:

```bash
PYTHONPATH=src ./.venv/bin/python -m android_device_lab.cli \
  --serial SERIAL_NUMBER \
  --device-info \
  --battery-info \
  --storage-info
```

## Report Export

The tool can export Android diagnostic reports to:

- JSON
- Markdown

Reports are saved under timestamped directories:

```text
reports/
└── YYYY-MM-DD_HHMMSS/
    ├── report.json
    └── report.md
```

Current report sections:

- Device information
- Battery information
- Storage information

Example Markdown fields currently use raw dataclass field names:

```markdown
## 设备信息
- product: socrates
- model: 22127RK46C
- manufacturer: Xiaomi

## 电池信息
- temperature_c: 31.2
- ac_powered: false
- voltage_mv: 4210
- level_percent: 76

## 存储信息
- total: 110G
- used: 40G
- available: 70G
- use_percentage: 37
```

The diagnostic data model now uses normalized internal fields. Display units such as `°C`, `mV`, and `%` should be added by presentation code instead of being stored in JSON data.

## Current Implementation Notes

- Commands are executed through `subprocess.run()` without `shell=True`.
- ADB commands use argument lists instead of string concatenation.
- Device-specific commands use `adb -s SERIAL ...`.
- Storage parsing currently reads `adb shell df -h` and selects the row whose mount point is `/data`.
- Battery information is normalized in the data model: temperature uses Celsius, voltage uses millivolts, level uses an integer percentage, and AC power state uses a boolean value.
- JSON and Markdown reports are generated from dataclass-based diagnostic data.
- Tests focus on pure parsing, CLI argument parsing, display formatting, and report export behavior.

## Current Limitations

- `--serial` is required; automatic single-device selection is not implemented yet.
- Multi-device batch collection is not implemented yet.
- Device connection and ADB error handling are still basic.
- Markdown reports currently use raw field names; presentation-friendly labels and units are still planned.
- Storage reporting currently focuses on the `/data` partition.
- Battery and storage parsing are implemented as standalone pure parser functions.
- JSON / Markdown report field names are not yet localized or presentation-friendly.
- Logcat analysis, root-specific checks, GUI, and multi-device workflows are out of scope for v0.1.

## Development Checks

Show CLI help:

```bash
PYTHONPATH=src ./.venv/bin/python -m android_device_lab.cli --help
```

Check required `--serial` validation:

```bash
PYTHONPATH=src ./.venv/bin/python -m android_device_lab.cli --format both
```

Expected result: argparse reports that `--serial` is required.

Run tests:

```bash
.venv/bin/python -m pytest
```

Current v0.1 test coverage includes:

- `adb_command()` command construction
- `parse_storage_info()` storage parser
- `parse_args()` CLI argument parser
- battery temperature display formatting
- JSON report export
- Markdown report export
