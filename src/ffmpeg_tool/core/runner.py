from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

from .config import FFmpegConfig
from .exceptions import (
    FFmpegExecutionError,
    FFmpegNotFoundError,
)


ProgressCallback = Callable[[str], None]


@dataclass
class CommandResult:
    command: list[str]
    return_code: int
    stdout: str
    stderr: str
    duration: float


class FFmpegRunner:
    """
    Low-level wrapper around FFmpeg and FFprobe.

    This class is deliberately independent from audio/video operations.
    """

    def __init__(
        self,
        config: FFmpegConfig | None = None,
    ):
        self.config = config or FFmpegConfig()

    def run(
        self,
        command: Sequence[str],
        *,
        progress_callback: ProgressCallback | None = None,
        check: bool = True,
    ) -> CommandResult:

        command = [str(arg) for arg in command]

        start_time = time.perf_counter()

        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                shell=False,
            )

        except FileNotFoundError as exc:
            raise FFmpegNotFoundError(
                f"Executable not found: {command[0]}"
            ) from exc

        stdout, stderr = process.communicate()

        elapsed = time.perf_counter() - start_time

        if progress_callback:
            for line in stderr.splitlines():
                progress_callback(line)

        result = CommandResult(
            command=command,
            return_code=process.returncode,
            stdout=stdout,
            stderr=stderr,
            duration=elapsed,
        )

        if check and process.returncode != 0:
            raise FFmpegExecutionError(
                message=(
                    f"FFmpeg command failed with return code "
                    f"{process.returncode}."
                ),
                command=command,
                return_code=process.returncode,
                stderr=stderr,
            )

        return result

    def ffmpeg(
        self,
        args: Sequence[str],
        *,
        progress_callback: ProgressCallback | None = None,
    ) -> CommandResult:

        command = [
            self.config.ffmpeg,
            "-hide_banner",
            "-loglevel",
            self.config.loglevel,
        ]

        if self.config.overwrite:
            command.append("-y")
        else:
            command.append("-n")

        command.extend(args)

        return self.run(
            command,
            progress_callback=progress_callback,
        )

    def ffprobe(
        self,
        args: Sequence[str],
    ) -> CommandResult:

        command = [
            self.config.ffprobe,
            "-hide_banner",
            "-loglevel",
            self.config.loglevel,
        ]

        command.extend(args)

        return self.run(command)

    def ensure_output_directory(self, output: str | Path) -> None:
        if not self.config.create_output_directories:
            return

        output_path = Path(output)

        if output_path.parent != Path("."):
            output_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )