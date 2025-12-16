"""All the types that are used in the API."""

import datetime

from libtvdb.utilities import parse_date, parse_datetime


def date_parser(value: str | None) -> datetime.date | None:
    """Parser method for parsing dates to pass to deserialize."""
    if value is None:
        return None

    if value in ["", "0000-00-00"]:
        return None

    return parse_date(value)


def datetime_parser(value: str | None) -> datetime.datetime | None:
    """Parser method for parsing datetimes to pass to deserialize."""
    if value is None:
        return None

    if value in ["", "0000-00-00 00:00:00"]:
        return None

    return parse_datetime(value)


def timestamp_parser(value: int | None) -> datetime.datetime | None:
    """Parser method for parsing datetimes to pass to deserialize."""
    if value is None:
        return None

    return datetime.datetime.fromtimestamp(value)


def optional_float(value: int | None) -> float | None:
    """Parser for optional ints to floats."""
    if value is None:
        return None

    return float(value)


def optional_empty_str(value: str | None) -> str | None:
    """Parser for empty strs to None."""
    if value is None:
        return None

    if value == "":
        return None

    return value
