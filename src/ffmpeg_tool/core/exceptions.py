class FFmpegError(Exception):
    """Base exception for the library."""


class FFmpegNotFoundError(FFmpegError):
    """Raised when FFmpeg or FFprobe cannot be found."""


class FFmpegExecutionError(FFmpegError):
    """Raised when an FFmpeg command fails."""

    def __init__(
        self,
        message: str,
        command: list[str] | None = None,
        return_code: int | None = None,
        stderr: str | None = None,
    ):
        super().__init__(message)
        self.command = command
        self.return_code = return_code
        self.stderr = stderr


class InvalidMediaError(FFmpegError):
    """Raised when a media file is invalid or cannot be analyzed."""


class InvalidTimeError(FFmpegError):
    """Raised when a timestamp is invalid."""


class OperationError(FFmpegError):
    """Raised when an operation cannot be created or executed."""


class PipelineError(FFmpegError):
    """Raised when a pipeline fails."""