from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class StreamInfo:
    index: int | None
    codec_type: str | None
    codec_name: str | None
    codec_long_name: str | None


@dataclass
class VideoStreamInfo(StreamInfo):
    width: int | None = None
    height: int | None = None
    fps: float | None = None
    pixel_format: str | None = None

    def __init__(
        self,
        index: int | None,
        codec_name: str | None,
        codec_long_name: str | None,
        width: int | None,
        height: int | None,
        fps: float | None,
        pixel_format: str | None,
    ):
        super().__init__(
            index=index,
            codec_type="video",
            codec_name=codec_name,
            codec_long_name=codec_long_name,
        )

        self.width = width
        self.height = height
        self.fps = fps
        self.pixel_format = pixel_format


@dataclass
class AudioStreamInfo(StreamInfo):
    sample_rate: int | None = None
    channels: int | None = None
    channel_layout: str | None = None

    def __init__(
        self,
        index: int | None,
        codec_name: str | None,
        codec_long_name: str | None,
        sample_rate: int | None,
        channels: int | None,
        channel_layout: str | None,
    ):
        super().__init__(
            index=index,
            codec_type="audio",
            codec_name=codec_name,
            codec_long_name=codec_long_name,
        )

        self.sample_rate = sample_rate
        self.channels = channels
        self.channel_layout = channel_layout


@dataclass
class MediaInfo:
    path: Path
    format_name: str | None
    duration: float | None
    size: int | None
    bit_rate: int | None
    streams: list[StreamInfo]

    @property
    def video_streams(self) -> list[VideoStreamInfo]:
        return [
            stream
            for stream in self.streams
            if isinstance(stream, VideoStreamInfo)
        ]

    @property
    def audio_streams(self) -> list[AudioStreamInfo]:
        return [
            stream
            for stream in self.streams
            if isinstance(stream, AudioStreamInfo)
        ]

    @property
    def has_video(self) -> bool:
        return bool(self.video_streams)

    @property
    def has_audio(self) -> bool:
        return bool(self.audio_streams)

    @property
    def video(self) -> VideoStreamInfo | None:
        return self.video_streams[0] if self.video_streams else None

    @property
    def audio(self) -> AudioStreamInfo | None:
        return self.audio_streams[0] if self.audio_streams else None