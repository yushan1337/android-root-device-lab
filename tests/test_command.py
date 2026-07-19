from android_device_lab.command import CommandResult,run_command
import pytest
from android_device_lab.exceptions import CommandExecutionError, CommandNotFoundError, CommandTimeoutError


def test_command_result_succeeded_when_exit_code_zero() -> None:
    result = CommandResult(arg=["python3"],exit_code=0, stdout="", stderr="")

    assert result.succeeded is True


def test_command_result_not_succeeded_when_exit_code_non_zero() -> None:
    result = CommandResult(arg=["python3"],exit_code=7, stdout="", stderr="error")

    assert result.succeeded is False


def test_command_result_ensure_success_does_not_raise_for_success() -> None:
    result = CommandResult(arg=["python3"],exit_code=0, stdout="ok", stderr="")

    result.ensure_success()


def test_command_result_ensure_success_raises_for_failure() -> None:
    result = CommandResult(
        arg=["python3", "-c", "exit"],
        exit_code=7,
        stdout="",
        stderr="bad",
    )

    with pytest.raises(CommandExecutionError) as error:
        result.ensure_success()

    assert error.value.exit_code == 7
    assert error.value.stderr == "bad"
    assert error.value.arg == ["python3", "-c", "exit"]


def test_run_command_non_zero_without_check_returns_result() -> None:
    result = run_command(
        ["python3", "-c", "import sys; sys.exit(7)"],
        check=False,
    )

    assert result.succeeded is False
    assert result.exit_code == 7


def test_run_command_non_zero_with_check_raises() -> None:
    with pytest.raises(CommandExecutionError) as error:
        run_command(
            ["python3", "-c", "import sys; sys.exit(7)"],
            check=True,
        )

    assert error.value.exit_code == 7


def test_run_command_missing_executable_raises() -> None:
    with pytest.raises(CommandNotFoundError) as error:
        run_command(["definitely-not-a-real-command-xyz"])

    assert error.value.executable == "definitely-not-a-real-command-xyz"


def test_run_command_timeout_raises() -> None:
    with pytest.raises(CommandTimeoutError) as error:
        run_command(
            ["python3", "-c", "import time; time.sleep(2)"],
            timeout=0.1,
        )

    assert error.value.timeout == 0.1


def test_run_command_preserves_stderr() -> None:
    result = run_command(
        [
            "python3",
            "-c",
            "import sys; print('bad', file=sys.stderr); sys.exit(2)",
        ],
        check=False,
    )

    assert result.exit_code == 2
    assert result.stderr == "bad"