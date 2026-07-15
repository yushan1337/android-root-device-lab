# Python and C++ Responsibility Boundary

## Purpose

This document records the v0.1 decision about how the current Python prototype relates to a possible future C++ / Qt implementation.

The Python prototype is not disposable code. It remains useful as an automation, testing, and verification layer even if the main user-facing application is later implemented in C++.

## Current Python Prototype

The current v0.1 project is a Python + ADB diagnostic prototype.

It already handles:

- command-line execution
- ADB command construction
- basic device information collection
- battery information collection
- storage information collection
- JSON report export
- Markdown report export
- pytest tests for pure logic and report export

Its main value is rapid iteration and easy automation.

## Python Keeps

Python should continue to own tasks that benefit from fast scripting and flexible text processing:

- ADB automation scripts
- command-line diagnostic workflows
- logcat collection and quick analysis
- pytest-based parser and exporter tests
- JSON / Markdown report verification
- CI scripts and smoke tests
- sample data generation
- rapid experiments against real Android devices
- compatibility checks for different ROM outputs

Python is also a good place to keep small pure parsers, such as:

- `df -h` storage output parsing
- `dumpsys battery` parsing
- future `logcat` parsing experiments

## C++ Future Implementation

C++ can be considered later for parts that benefit from a long-running, packaged desktop application:

- Qt GUI
- persistent device model
- richer state management
- cross-platform packaged executable
- reusable ADB client abstraction
- long-running background monitoring
- formal error handling and state transitions
- report browsing UI
- device history visualization

C++ should not replace Python merely for the sake of rewriting. It should solve a concrete product or architecture need.

## Boundary Decision

Current decision:

```text
Python remains the automation and testing layer.
C++ may become the future desktop application layer.
```

The two layers can coexist:

```text
Python
├── ADB experiments
├── parser tests
├── report generation tests
├── logcat analysis
└── CI / validation scripts

C++ / Qt
├── desktop GUI
├── device state model
├── long-running sessions
├── packaged app experience
└── user-facing workflows
```

## Data Contract Between Layers

If a C++ application is added later, JSON reports can become the boundary format.

Python can continue to produce and validate reports such as:

```text
report.json
```

C++ can later consume or produce compatible structures.

This keeps the boundary simple:

- Python validates device collection behavior.
- C++ focuses on user interface and application state.
- JSON acts as a shared contract.

## What Should Not Move to C++ Yet

The following should remain in Python during early learning and prototyping:

- quick ADB experiments
- parser exploration
- report format experiments
- one-off diagnostic scripts
- pytest-based regression tests

Moving these too early to C++ would increase build complexity without improving the v0.1 learning goal.

## Possible Future C++ Milestones

Only after the Python prototype stabilizes, consider:

1. Define a C++ `DeviceInfo` / `BatteryInfo` / `StorageInfo` model.
2. Build a minimal Qt window that displays a loaded `report.json`.
3. Add a device list view.
4. Add a report history view.
5. Decide whether C++ should call ADB directly or consume Python-generated reports.

Each step should have clear acceptance criteria before implementation.

## Current Decision

The v0.1 Python prototype is complete enough to serve as the foundation for future work.

It should remain in the repository as:

- the reference ADB automation implementation
- the report generation prototype
- the regression-test layer for parsers and exporters
- the fastest place to validate new Android diagnostic ideas

A future C++ / Qt application should be added only when the project needs a durable graphical desktop experience.
