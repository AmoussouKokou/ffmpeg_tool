from dataclasses import dataclass

from ..base import Operation


def _atempo_filters(speed: float) -> str:
    if speed <= 0:
        raise ValueError(
            "Speed must be greater than zero."
        )

    factors = []

    remaining = speed

    while remaining < 0.5:
        factors.append(0.5)
        remaining /= 0.5

    while remaining > 2.0:
        factors.append(2.0)
        remaining /= 2.0

    factors.append(remaining)

    return ",".join(
        f"atempo={factor}"
        for factor in factors
    )


@dataclass
class SpeedAudio(Operation):

    input: str
    output_path: str

    speed: float

    codec: str | None = None

    @property
    def output(self) -> str:
        return self.output_path

    def build_args(self) -> list[str]:

        self.check_input(self.input)

        filter_expression = _atempo_filters(
            self.speed
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