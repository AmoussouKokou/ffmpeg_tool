import pytest

from ffmpeg_tool.core.exceptions import InvalidTimeError
from ffmpeg_tool.utils.time import (
    format_time,
    parse_time,
    validate_range,
)


def test_parse_seconds():
    assert parse_time(90) == 90


def test_parse_decimal_seconds():
    assert parse_time(90.5) == 90.5


def test_parse_mm_ss():
    assert parse_time("01:30") == 90


def test_parse_hh_mm_ss():
    assert parse_time("01:02:03") == 3723


def test_parse_string_seconds():
    assert parse_time("90") == 90


def test_invalid_time():
    with pytest.raises(InvalidTimeError):
        parse_time("abc")


def test_invalid_range():
    with pytest.raises(InvalidTimeError):
        validate_range(
            "00:10",
            "00:05",
        )


def test_format_time():
    assert format_time(90) == "00:01:30.000"