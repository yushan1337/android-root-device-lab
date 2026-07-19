import subprocess
from dataclasses import dataclass
import logging
from android_device_lab.exceptions import CommandExecutionError, CommandNotFoundError, CommandTimeoutError


@dataclass(slots=True)
class CommandResult:
    arg: list[str]
    exit_code: int
    stdout: str
    stderr: str
    @property
    def succeeded(self) -> bool:
        if self.exit_code == 0:
            return True
        return False
    def ensure_success(self) -> None:
        if self.succeeded:
            return
        raise CommandExecutionError(
        args=self.arg,
        exit_code=self.exit_code,
        stderr=self.stderr,
        )
    
def run_command(
    args: list[str],
    check: bool = False,
    timeout: float | None = 10,
    ) -> CommandResult:
    logging.info(f"执行命令: {' '.join(args)}")
    try:
        result = subprocess.run(args, capture_output=True, text=True, check=False, timeout=timeout,)
        logging.info(f"命令执行完成，退出码: {result.returncode}")
        command_result = CommandResult(
            arg=args,
            exit_code=result.returncode,
            stdout=result.stdout.strip(),
            stderr=result.stderr.strip(),
        )
        if check:
            command_result.ensure_success()
        return command_result
    except FileNotFoundError as error:
        executable = args[0] if args else ""
        raise CommandNotFoundError(executable) from error
    except subprocess.TimeoutExpired as error:
        raise CommandTimeoutError(
            args=args,
            timeout=timeout if timeout is not None else 0,
        ) from error