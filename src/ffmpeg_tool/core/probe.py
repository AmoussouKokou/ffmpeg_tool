from __future__ import annotations

import json
from pathlib import Path

from ..models.media import (
    AudioStreamInfo,
    MediaInfo,
    StreamInfo,
    VideoStreamInfo,
)
from .exceptions import InvalidMediaError
from .runner import FFmpegRunner


class FFprobe:
    """
    Analyze media files using FFprobe.
    """

    def __init__(self, runner: FFmpegRunner | None = None):
        self.runner = runner or FFmpegRunner()

    def probe(self, input_path: str | Path) -> MediaInfo:
        input_path = Path(input_path)

        if not input_path.exists():
            raise FileNotFoundError(
                f"Media file does not exist: {input_path}"
            )

        result = self.runner.ffprobe(
            [
                "-print_format",
                "json",
                "-show_format",
                "-show_streams",
                str(input_path),
            ]
        )

        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise InvalidMediaError(
                "FFprobe returned invalid JSON."
            ) from exc

        return self._parse_media_info(
            input_path,
            data,
        )

    def _parse_media_info(
        self,
        input_path: Path,
        data: dict,
    ) -> MediaInfo:

        format_data = data.get("format", {})
        streams_data = data.get("streams", [])

        streams: list[StreamInfo] = []

        for stream in streams_data:
            codec_type = stream.get("codec_type")

            if codec_type == "video":
                streams.append(
                    VideoStreamInfo(
                        index=stream.get("index"),
                        codec_name=stream.get("codec_name"),
                        codec_long_name=stream.get("codec_long_name"),
                        width=stream.get("width"),
                        height=stream.get("height"),
                        fps=self._parse_fps(stream.get("r_frame_rate")),
                        pixel_format=stream.get("pix_fmt"),
                    )
                )

            elif codec_type == "audio":
                streams.append(
                    AudioStreamInfo(
                        index=stream.get("index"),
                        codec_name=stream.get("codec_name"),
                        codec_long_name=stream.get("codec_long_name"),
                        sample_rate=self._to_int(
                            stream.get("sample_rate")
                        ),
                        channels=stream.get("channels"),
                        channel_layout=stream.get("channel_layout"),
                    )
                )

            else:
                streams.append(
                    StreamInfo(
                        index=stream.get("index"),
                        codec_type=codec_type,
                        codec_name=stream.get("codec_name"),
                        codec_long_name=stream.get(
                            "codec_long_name"
                        ),
                    )
                )

        return MediaInfo(
            path=input_path,
            format_name=format_data.get("format_name"),
            duration=self._to_float(
                format_data.get("duration")
            ),
            size=self._to_int(
                format_data.get("size")
            ),
            bit_rate=self._to_int(
                format_data.get("bit_rate")
            ),
            streams=streams,
        )

    @staticmethod
    def _to_float(value):
        if value is None:
            return None

        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _to_int(value):
        if value is None:
            return None

        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _parse_fps(value: str | None):
        if not value or value == "0/0":
            return None

        try:
            numerator, denominator = value.split("/")
            return float(numerator) / float(denominator)
        except (ValueError, ZeroDivisionError):
            return None