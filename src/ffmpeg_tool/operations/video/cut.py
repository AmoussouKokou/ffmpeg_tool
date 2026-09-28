from __future__ import annotations

from ffmpeg_tool.operations.base import Operation
from ffmpeg_tool.utils.time import parse_time, validate_range


class CutVideo(Operation):
    """
    Coupe une vidéo entre deux positions temporelles.

    Les temps peuvent être fournis sous forme :

        30
        30.5
        "01:30"
        "00:01:30"
    """

    def __init__(
        self,
        input: str,
        output_path: str,
        start: int | float | str,
        end: int | float | str,
        copy: bool = False,
        video_codec: str | None = None,
        audio_codec: str | None = None,
    ) -> None:

        super().__init__(output_path)

        self.input = input

        self.start = parse_time(start)
        self.end = parse_time(end)

        validate_range(
            self.start,
            self.end,
        )

        self.copy = copy
        self.video_codec = video_codec
        self.audio_codec = audio_codec

    # ==================================================================
    # Durée de la portion à produire
    # ==================================================================

    def get_progress_duration(
        self,
        runner,
    ) -> float:

        return self.end - self.start

    # ==================================================================
    # Construction FFmpeg
    # ==================================================================

    def build_args(self) -> list[str]:

        duration = self.end - self.start

        args: list[str] = []

        # --------------------------------------------------------------
        # Copie directe
        # --------------------------------------------------------------

        if self.copy:

            args.extend(
                [
                    "-ss",
                    str(self.start),
                    "-i",
                    self.input,
                    "-t",
                    str(duration),
                    "-c",
                    "copy",
                ]
            )

        # --------------------------------------------------------------
        # Réencodage
        # --------------------------------------------------------------

        else:

            args.extend(
                [
                    "-i",
                    self.input,
                    "-ss",
                    str(self.start),
                    "-t",
                    str(duration),
                ]
            )

            if self.video_codec is not None:

                args.extend(
                    [
                        "-c:v",
                        self.video_codec,
                    ]
                )

            if self.audio_codec is not None:

                args.extend(
                    [
                        "-c:a",
                        self.audio_codec,
                    ]
                )

        args.append(self.output)

        return args