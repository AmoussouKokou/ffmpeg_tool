from dataclasses import dataclass

from ..base import Operation


@dataclass
class ImageAudioToVideo(Operation):

    image: str
    audio: str
    output_path: str

    video_codec: str = "libx264"
    audio_codec: str = "aac"

    audio_bitrate: str = "320k"

    preset: str = "medium"

    pixel_format: str = "yuv420p"

    loop_image: bool = True

    @property
    def output(self) -> str:
        return self.output_path

    def build_args(self) -> list[str]:

        self.check_input(self.image)
        self.check_input(self.audio)

        args = []

        if self.loop_image:
            args.extend([
                "-loop",
                "1",
            ])

        args.extend([
            "-i",
            self.image,
            "-i",
            self.audio,
            "-c:v",
            self.video_codec,
            "-tune",
            "stillimage",
            "-c:a",
            self.audio_codec,
            "-b:a",
            self.audio_bitrate,
            "-pix_fmt",
            self.pixel_format,
            "-shortest",
            self.output_path,
        ])

        return args