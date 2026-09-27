from dataclasses import dataclass

from ..base import Operation
from ...utils.time import (
    validate_range,
    format_time,
)


@dataclass
class CutAudio(Operation):

    input: str
    output_path: str

    start: int | float | str
    end: int | float | str

    copy: bool = False

    codec: str | None = None

    @property
    def output(self) -> str:
        return self.output_path

    def build_args(self) -> list[str]:

        self.check_input(self.input)

        start, end = validate_range(
            self.start,
            self.end,
        )

        duration = end - start

        if self.copy:
            args = [
                "-ss",
                format_time(start),
                "-i",
                self.input,
                "-t",
                format_time(duration),
                "-c",
                "copy",
            ]

        else:
            args = [
                "-i",
                self.input,
                "-ss",
                format_time(start),
                "-t",
                format_time(duration),
            ]

            if self.codec:
                args.extend([
                    "-c:a",
                    self.codec,
                ])

        args.append(self.output_path)

        return args