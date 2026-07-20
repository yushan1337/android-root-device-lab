class AndroidDeviceLabError(Exception):
    """Base exception for android-device-lab."""


class CommandExecutionError(AndroidDeviceLabError):
    def __init__(
        self,
        args: list[str],
        exit_code: int,
        stderr: str,
    ) -> None:
        self.arg = args
        self.exit_code = exit_code
        self.stderr = stderr

        message = f"Command failed with exit code {exit_code}: {' '.join(args)}"
        if stderr:
            message = f"{message}\n{stderr}"

        super().__init__(message)


class CommandNotFoundError(AndroidDeviceLabError):
    def __init__(self, executable: str) -> None:
        self.executable = executable
        super().__init__(f"Command not found: {executable}")


class CommandTimeoutError(AndroidDeviceLabError):
    def __init__(self, args: list[str], timeout: float) -> None:
        self.arg = args
        self.timeout = timeout

        super().__init__(
            f"Command timed out after {timeout} seconds: {' '.join(args)}"
        )


class AdbDeviceError(AndroidDeviceLabError):
    pass