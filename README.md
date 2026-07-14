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

v0.1 Python prototype in progress.

Current focus: Python engineering basics, ADB automation, CLI arguments, logging, and pytest.

## Tech Stack

- Python
- ADB (Android Debug Bridge)
- Android shell
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
├── reports/              # Generated diagnostic reports
├── samples/              # Sample outputs
├── docs/                 # Design notes
└── .gitignore
```

## Requirements

- Python 3.11+
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

## Running the CLI

This project currently uses a `src/` layout. During development, run commands from the project root with `PYTHONPATH=src`:

```bash
cd /path/to/android-root-device-lab
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

## Current Implementation Notes

- Commands are executed through `subprocess.run()` without `shell=True`.
- ADB commands use argument lists instead of string concatenation.
- Device-specific commands use `adb -s SERIAL ...`.
- Storage parsing currently reads `adb shell df -h` and selects the row whose mount point is `/data`.
- JSON and Markdown reports are generated from dataclass-based diagnostic data.

## Current Limitations

- `--serial` is required; automatic single-device selection is not implemented yet.
- Multi-device batch collection is not implemented yet.
- Device connection and ADB error handling are still basic.
- Markdown reports currently use raw field names and raw values.
- Battery temperature is still stored as the raw Android value and converted during display.
- Storage reporting currently focuses on the `/data` partition.
- pytest coverage is still being added.

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

Run tests after adding pytest tests:

```bash
PYTHONPATH=src ./.venv/bin/python -m pytest
```
