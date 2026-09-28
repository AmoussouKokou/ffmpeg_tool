from __future__ import annotations

from ffmpeg_tool.operations.base import Operation
from ffmpeg_tool.utils.time import parse_time, validate_range


class CutAudio(Operation):
    """
    Coupe un fichier audio entre deux positions temporelles.
    """

    def __init__(
        self,
        input: str,
        output_path: str,
        start: int | float | str,
        end: int | float | str,
        copy: bool = False,
        codec: str | None = None,
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
        self.codec = codec

    # ==================================================================
    # Durée de sortie
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

            if self.codec is not None:

                args.extend(
                    [
                        "-c:a",
                        self.codec,
                    ]
                )

        args.append(self.output)

        return args