from dataclasses import dataclass

from ..base import Operation
from ...utils.time import format_time, parse_time


@dataclass
class ExtractFrame(Operation):

    input: str
    output_path: str

    timestamp: int | float | str

    quality: int | None = None

    @property
    def output(self) -> str:
        return self.output_path

    def build_args(self) -> list[str]:

        self.check_input(self.input)

        timestamp = parse_time(self.timestamp)

        args = [
            "-ss",
            format_time(timestamp),
            "-i",
            self.input,
            "-frames:v",
            "1",
        ]

        if self.quality is not None:
            args.extend([
                "-q:v",
                str(self.quality),
            ])

        args.append(self.output_path)

        return args