from dataclasses import dataclass

from ..base import Operation


@dataclass
class ConvertVideo(Operation):

    input: str
    output_path: str

    video_codec: str | None = None
    audio_codec: str | None = None

    video_bitrate: str | None = None
    audio_bitrate: str | None = None

    preset: str | None = None

    crf: int | None = None

    @property
    def output(self) -> str:
        return self.output_path

    def build_args(self) -> list[str]:

        self.check_input(self.input)

        args = [
            "-i",
            self.input,
        ]

        if self.video_codec:
            args.extend([
                "-c:v",
                self.video_codec,
            ])

        if self.audio_codec:
            args.extend([
                "-c:a",
                self.audio_codec,
            ])

        if self.video_bitrate:
            args.extend([
                "-b:v",
                self.video_bitrate,
            ])

        if self.audio_bitrate:
            args.extend([
                "-b:a",
                self.audio_bitrate,
            ])

        if self.preset:
            args.extend([
                "-preset",
                self.preset,
            ])

        if self.crf is not None:
            args.extend([
                "-crf",
                str(self.crf),
            ])

        args.append(self.output_path)

        return args