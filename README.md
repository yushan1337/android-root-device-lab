# Android Root Device Lab

A Python + ADB based Android device diagnostics toolkit.

## Goals

- Collect Android device information
- Export diagnostic reports (Markdown / JSON)
- Analyze logcat output
- Support rooted Android 15 devices

## Current Version

v0.1 planning stage

## Tech Stack

- Python
- ADB (Android Debug Bridge)
- Android shell
- Markdown / JSON reports

## Project Structure

```
android-root-device-lab/
├── src/
│   └── android_device_lab/
│       ├── cli.py        # CLI entry point
│       ├── adb.py        # ADB data collection
│       ├── command.py    # Safe command execution wrapper
│       └── exporters.py  # JSON / Markdown report export
├── reports/              # Generated diagnostic reports
├── samples/              # Sample outputs
├── docs/                 # Design notes
└── .gitignore
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

To export a report, run the CLI and choose the report export option:

```bash
python -m android_device_lab.cli
```
