import subprocess
from dataclasses import dataclass


@dataclass
class CommandResult:
    exit_code: int
    stdout: str
    stderr: str


def run_command(args: list[str]) -> CommandResult:
    try:
        result = subprocess.run(args, capture_output=True, text=True, check=False)
        return CommandResult(
            exit_code=result.returncode,
            stdout=result.stdout.strip(),
            stderr=result.stderr.strip(),
        )
    except FileNotFoundError:
        return CommandResult(
            exit_code=-1,
            stdout="",
            stderr=f"命令不存在：{args[0]}",
        )
