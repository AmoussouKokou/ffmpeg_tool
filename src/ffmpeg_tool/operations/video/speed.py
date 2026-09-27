from dataclasses import dataclass

from ..base import Operation
from ..audio.speed import _atempo_filters


@dataclass
class SpeedVideo(Operation):

    input: str
    output_path: str

    speed: float

    video_codec: str = "libx264"
    audio_codec: str = "aac"

    @property
    def output(self) -> str:
        return self.output_path

    def build_args(self) -> list[str]:

        self.check_input(self.input)

        if self.speed <= 0:
            raise ValueError(
                "Speed must be greater than zero."
            )

        video_filter = (
            f"setpts={1 / self.speed}*PTS"
        )

        audio_filter = _atempo_filters(
            self.speed
        )

        args = [
            "-i",
            self.input,
            "-vf",
            video_filter,
            "-af",
            audio_filter,
            "-c:v",
            self.video_codec,
            "-c:a",
            self.audio_codec,
            self.output_path,
        ]

        return args