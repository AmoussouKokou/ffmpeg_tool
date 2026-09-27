from dataclasses import dataclass

from ..base import Operation


@dataclass
class Volume(Operation):

    input: str
    output_path: str

    volume: float

    codec: str | None = None

    @property
    def output(self) -> str:
        return self.output_path

    def build_args(self) -> list[str]:

        self.check_input(self.input)

        args = [
            "-i",
            self.input,
            "-af",
            f"volume={self.volume}",
        ]

        if self.codec:
            args.extend([
                "-c:a",
                self.codec,
            ])

        args.append(self.output_path)

        return args