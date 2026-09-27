from dataclasses import dataclass

from ..base import Operation


@dataclass
class NormalizeAudio(Operation):

    input: str
    output_path: str

    target_loudness: float = -16.0
    true_peak: float = -1.5
    loudness_range: float = 11.0

    codec: str | None = None

    @property
    def output(self) -> str:
        return self.output_path

    def build_args(self) -> list[str]:

        self.check_input(self.input)

        filter_expression = (
            "loudnorm="
            f"I={self.target_loudness}:"
            f"TP={self.true_peak}:"
            f"LRA={self.loudness_range}"
        )

        args = [
            "-i",
            self.input,
            "-af",
            filter_expression,
        ]

        if self.codec:
            args.extend([
                "-c:a",
                self.codec,
            ])

        args.append(self.output_path)

        return args