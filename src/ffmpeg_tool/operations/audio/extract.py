from dataclasses import dataclass

from ..base import Operation


@dataclass
class ExtractAudio(Operation):

    input: str
    output_path: str

    codec: str | None = None

    bitrate: str | None = None

    @property
    def output(self) -> str:
        return self.output_path

    def build_args(self) -> list[str]:

        self.check_input(self.input)

        args = [
            "-i",
            self.input,
            "-vn",
        ]

        if self.codec:
            args.extend([
                "-c:a",
                self.codec,
            ])

        if self.bitrate:
            args.extend([
                "-b:a",
                self.bitrate,
            ])

        args.append(self.output_path)

        return args