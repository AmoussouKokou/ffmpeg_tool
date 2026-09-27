from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FFmpegConfig:
    """
    Global configuration for FFmpeg operations.
    """

    ffmpeg_path: str = "ffmpeg"
    ffprobe_path: str = "ffprobe"

    overwrite: bool = True

    loglevel: str = "error"

    threads: int | None = None

    create_output_directories: bool = True

    @property
    def ffmpeg(self) -> str:
        return self.ffmpeg_path

    @property
    def ffprobe(self) -> str:
        return self.ffprobe_path