"""All the types that are used in the API."""

import datetime
from typing import Final

from libtvdb.utilities import parse_date, parse_datetime

# Constants for invalid date/datetime placeholders
INVALID_DATE_PLACEHOLDER: Final[str] = "0000-00-00"
INVALID_DATETIME_PLACEHOLDER: Final[str] = "0000-00-00 00:00:00"


def date_parser(value: str | None) -> datetime.date | None:
    """Parse a date string from the API into a date object.

    Args:
        value: Date string in YYYY-MM-DD format or None

    Returns:
        Parsed date object or None if value is None/empty/invalid
    """
    if value is None:
        return None

    if value in ["", INVALID_DATE_PLACEHOLDER]:
        return None

    return parse_date(value)


def datetime_parser(value: str | None) -> datetime.datetime | None:
    """Parse a datetime string from the API into a datetime object.

    Args:
        value: Datetime string in 'YYYY-MM-DD HH:MM:SS' format or None

    Returns:
        Parsed datetime object or None if value is None/empty/invalid
    """
    if value is None:
        return None

    if value in ["", INVALID_DATETIME_PLACEHOLDER]:
        return None

    return parse_datetime(value)


def timestamp_parser(value: int | None) -> datetime.datetime | None:
    """Parse a Unix timestamp into a datetime object.

    Args:
        value: Unix timestamp (seconds since epoch) or None

    Returns:
        Parsed datetime object in UTC or None if value is None
    """
    if value is None:
        return None

    return datetime.datetime.fromtimestamp(value, tz=datetime.UTC)


def optional_float(value: int | None) -> float | None:
    """Convert an optional integer to a float.

    Args:
        value: Integer value or None

    Returns:
        Float conversion of the value or None if value is None
    """
    if value is None:
        return None

    return float(value)


def optional_empty_str(value: str | None) -> str | None:
    """Convert empty strings to None for optional string fields.

    Args:
        value: String value or None

    Returns:
        The string value or None if value is None or empty string
    """
    if value is None:
        return None

    if value == "":
        return None

    return value
