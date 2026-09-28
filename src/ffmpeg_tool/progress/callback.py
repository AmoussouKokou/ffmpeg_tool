from collections.abc import Callable
from typing import Protocol

from ffmpeg_tool.models.progress import ProgressEvent


class ProgressCallback(Protocol):
    """
    Interface utilisée pour recevoir les événements de progression.
    """

    def __call__(self, event: ProgressEvent) -> None:
        ...


ProgressCallbackType = Callable[[ProgressEvent], None]