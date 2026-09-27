from dataclasses import dataclass

from ..base import Operation
from ...utils.time import parse_time


@dataclass
class FadeAudio(Operation):

    input: str
    output_path: str

    fade_in: float | str | None = None
    fade_out_start: float | str | None = None
    fade_out_duration: float | str | None = None

    codec: str | None = None

    @property
    def output(self) -> str:
        return self.output_path

    def build_args(self) -> list[str]:

        self.check_input(self.input)

        filters = []

        if self.fade_in is not None:
            duration = parse_time(self.fade_in)

            filters.append(
                f"afade=t=in:st=0:d={duration}"
            )

        if (
            self.fade_out_start is not None
            and self.fade_out_duration is not None
        ):
            start = parse_time(self.fade_out_start)
            duration = parse_time(self.fade_out_duration)

            filters.append(
                f"afade=t=out:st={start}:d={duration}"
            )

        if not filters:
            raise ValueError(
                "At least one fade must be specified."
            )

        args = [
            "-i",
            self.input,
            "-af",
            ",".join(filters),
        ]

        if self.codec:
            args.extend([
                "-c:a",
                self.codec,
            ])

        args.append(self.output_path)

        return args