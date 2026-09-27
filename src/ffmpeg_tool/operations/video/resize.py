from dataclasses import dataclass

from ..base import Operation


@dataclass
class ResizeVideo(Operation):

    input: str
    output_path: str

    width: int
    height: int

    keep_aspect_ratio: bool = False

    video_codec: str = "libx264"

    audio_codec: str | None = "aac"

    @property
    def output(self) -> str:
        return self.output_path

    def build_args(self) -> list[str]:

        self.check_input(self.input)

        if self.keep_aspect_ratio:
            scale = (
                f"scale={self.width}:"
                f"{self.height}:"
                "force_original_aspect_ratio=decrease"
            )
        else:
            scale = (
                f"scale={self.width}:"
                f"{self.height}"
            )

        args = [
            "-i",
            self.input,
            "-vf",
            scale,
            "-c:v",
            self.video_codec,
        ]

        if self.audio_codec:
            args.extend([
                "-c:a",
                self.audio_codec,
            ])

        args.append(self.output_path)

        return args