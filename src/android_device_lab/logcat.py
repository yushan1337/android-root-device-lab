VALID_LOG_LEVELS = {"V", "D", "I", "W", "E", "F", "S"}

import subprocess
from android_device_lab.exceptions import CommandNotFoundError, LogcatStreamError

def stop_process(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return

    process.terminate()

    try:
        process.wait(timeout=3)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()


def normalize_log_level(level: str | None) -> str | None:
    if level is None:
        return None

    normalized = level.upper()

    if normalized not in VALID_LOG_LEVELS:
        raise ValueError(f"Invalid logcat level: {level}")

    return normalized


def build_logcat_command(
    serial: str,
    level: str | None = None,
    tag: str | None = None,
    ) -> list[str]:
    normalized_level = normalize_log_level(level)

    command = ["adb", "-s", serial, "logcat"]

    if tag is not None:
        command.append(f"{tag}:{normalized_level or 'V'}")
        command.append("*:S")
        return command

    if normalized_level is not None:
        command.append(f"*:{normalized_level}")

    return command


def stream_logcat(
    serial: str,
    level: str | None = None,
    tag: str | None = None,
    ) -> None:
    command = build_logcat_command(
        serial=serial,
        level=level,
        tag=tag,
    )

    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except FileNotFoundError as error:
        raise CommandNotFoundError(command[0]) from error

    try:
        if process.stdout is None:
            raise LogcatStreamError("Logcat stdout was not captured")

        try:
            exit_code = process.wait(timeout=1)
        except subprocess.TimeoutExpired:
            exit_code = None

        if exit_code is not None:
            raise_logcat_exit_error(process, exit_code)

        for line in process.stdout:
            print(line, end="")

        exit_code = process.wait()

        if exit_code != 0:
            raise_logcat_exit_error(process, exit_code)

    except KeyboardInterrupt:
        print("\nLogcat stream interrupted by user.")

    finally:
        stop_process(process)

def read_process_stderr(process: subprocess.Popen[str]) -> str:
    if process.stderr is None:
        return ""

    return process.stderr.read().strip()


def raise_logcat_exit_error(
    process: subprocess.Popen[str],
    exit_code: int,
) -> None:
    stderr = read_process_stderr(process)
    message = f"Logcat exited with code {exit_code}"

    if stderr:
        message = f"{message}: {stderr}"

    raise LogcatStreamError(message)


