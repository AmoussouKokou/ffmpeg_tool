from __future__ import annotations

import re

from ..core.exceptions import InvalidTimeError


TimeValue = int | float | str


def parse_time(value: TimeValue) -> float:
    """
    Convert a timestamp into seconds.

    Accepted formats:

        90
        90.5
        "90"
        "90.5"
        "01:30"
        "00:01:30"
    """

    if isinstance(value, bool):
        raise InvalidTimeError(
            "Boolean values are not valid timestamps."
        )

    if isinstance(value, (int, float)):
        seconds = float(value)

        if seconds < 0:
            raise InvalidTimeError(
                "Time cannot be negative."
            )

        return seconds

    if not isinstance(value, str):
        raise InvalidTimeError(
            f"Unsupported time type: {type(value)}"
        )

    value = value.strip()

    if not value:
        raise InvalidTimeError(
            "Timestamp cannot be empty."
        )

    # Simple numeric string
    try:
        seconds = float(value)

        if seconds < 0:
            raise InvalidTimeError(
                "Time cannot be negative."
            )

        return seconds

    except ValueError:
        pass

    parts = value.split(":")

    if len(parts) not in (2, 3):
        raise InvalidTimeError(
            f"Invalid timestamp: {value}"
        )

    try:
        numbers = [float(part) for part in parts]
    except ValueError as exc:
        raise InvalidTimeError(
            f"Invalid timestamp: {value}"
        ) from exc

    if any(number < 0 for number in numbers):
        raise InvalidTimeError(
            "Time cannot be negative."
        )

    if len(numbers) == 2:
        minutes, seconds = numbers

        if seconds >= 60:
            raise InvalidTimeError(
                "Seconds must be lower than 60."
            )

        return minutes * 60 + seconds

    hours, minutes, seconds = numbers

    if minutes >= 60 or seconds >= 60:
        raise InvalidTimeError(
            "Minutes and seconds must be lower than 60."
        )

    return (
        hours * 3600
        + minutes * 60
        + seconds
    )


def validate_range(
    start: TimeValue,
    end: TimeValue,
) -> tuple[float, float]:

    start_seconds = parse_time(start)
    end_seconds = parse_time(end)

    if end_seconds <= start_seconds:
        raise InvalidTimeError(
            "End time must be greater than start time."
        )

    return start_seconds, end_seconds


def format_time(seconds: float) -> str:
    """
    Convert seconds into HH:MM:SS.mmm.
    """

    if seconds < 0:
        raise InvalidTimeError(
            "Time cannot be negative."
        )

    hours = int(seconds // 3600)

    remaining = seconds - hours * 3600

    minutes = int(remaining // 60)

    remaining -= minutes * 60

    return (
        f"{hours:02d}:"
        f"{minutes:02d}:"
        f"{remaining:06.3f}"
    )