import subprocess
from dataclasses import dataclass
import logging

@dataclass
class CommandResult:
    exit_code: int
    stdout: str
    stderr: str
def run_command(args: list[str]) -> CommandResult:
    logging.info(f"执行命令: {' '.join(args)}")
    try:
        result = subprocess.run(args, capture_output=True, text=True, check=False)
        logging.info(f"命令执行完成，退出码: {result.returncode}")
        return CommandResult(
            exit_code=result.returncode,
            stdout=result.stdout.strip(),
            stderr=result.stderr.strip(),
        )
    except FileNotFoundError:
        logging.error(f"命令不存在：{args[0]}")
        return CommandResult(
            exit_code=-1,
            stdout="",
            stderr=f"命令不存在：{args[0]}",
        )
