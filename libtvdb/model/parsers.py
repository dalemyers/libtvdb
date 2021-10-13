"""All the types that are used in the API."""

import datetime
from typing import Optional

from libtvdb.utilities import parse_date, parse_datetime


def date_parser(value: Optional[str]) -> Optional[datetime.date]:
    """Parser method for parsing dates to pass to deserialize."""
    if value is None:
        return None

    if value in ["", "0000-00-00"]:
        return None

    return parse_date(value)


def datetime_parser(value: Optional[str]) -> Optional[datetime.datetime]:
    """Parser method for parsing datetimes to pass to deserialize."""
    if value is None:
        return None

    if value in ["", "0000-00-00 00:00:00"]:
        return None

    return parse_datetime(value)


def timestamp_parser(value: Optional[int]) -> Optional[datetime.datetime]:
    """Parser method for parsing datetimes to pass to deserialize."""
    if value is None:
        return None

    return datetime.datetime.fromtimestamp(value)


def optional_float(value: Optional[int]) -> Optional[float]:
    """Parser for optional ints to floats."""
    if value is None:
        return None

    return float(value)


def optional_empty_str(value: Optional[str]) -> Optional[str]:
    """Parser for empty strs to None."""
    if value is None:
        return None

    if value == "":
        return None

    return value
