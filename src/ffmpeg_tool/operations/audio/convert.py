from dataclasses import dataclass
from pathlib import Path

from ..base import Operation


@dataclass
class ConvertAudio(Operation):

    input: str
    output_path: str

    codec: str | None = None

    bitrate: str | None = None

    quality: int | None = None

    sample_rate: int | None = None

    channels: int | None = None

    @property
    def output(self) -> str:
        return self.output_path

    def build_args(self) -> list[str]:

        self.check_input(self.input)

        args = [
            "-i",
            self.input,
            "-vn",
        ]

        if self.codec:
            args.extend([
                "-c:a",
                self.codec,
            ])

        if self.bitrate:
            args.extend([
                "-b:a",
                self.bitrate,
            ])

        if self.quality is not None:
            args.extend([
                "-q:a",
                str(self.quality),
            ])

        if self.sample_rate:
            args.extend([
                "-ar",
                str(self.sample_rate),
            ])

        if self.channels:
            args.extend([
                "-ac",
                str(self.channels),
            ])

        args.append(self.output_path)

        return args