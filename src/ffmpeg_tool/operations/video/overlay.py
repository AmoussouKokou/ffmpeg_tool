from dataclasses import dataclass

from ..base import Operation


@dataclass
class OverlayImage(Operation):

    input: str
    image: str
    output_path: str

    x: int | str = 0
    y: int | str = 0

    video_codec: str = "libx264"
    audio_codec: str = "aac"

    @property
    def output(self) -> str:
        return self.output_path

    def build_args(self) -> list[str]:

        self.check_input(self.input)
        self.check_input(self.image)

        filter_expression = (
            f"[0:v][1:v]overlay={self.x}:{self.y}"
        )

        args = [
            "-i",
            self.input,
            "-i",
            self.image,
            "-filter_complex",
            filter_expression,
            "-c:v",
            self.video_codec,
            "-c:a",
            self.audio_codec,
            "-map",
            "0:a?",
            "-map",
            "0:v",
            self.output_path,
        ]

        return args