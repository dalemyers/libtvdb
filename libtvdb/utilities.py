"""Utility classes and methods for working with the TVDB API."""

import datetime
import logging
from typing import Final

logger = logging.getLogger(__name__)

# Constants for date format validation
EXPECTED_DATE_FORMAT: Final[str] = "YYYY-MM-DD"
EXPECTED_DATETIME_FORMAT: Final[str] = "YYYY-MM-DD HH:MM:SS"
INVALID_DATETIME_PLACEHOLDER: Final[str] = "0000-00-00 00:00:00"
DATE_COMPONENTS_COUNT: Final[int] = 3
DATETIME_FORMAT_STRING: Final[str] = "%Y-%m-%d %H:%M:%S"


def parse_date(input_string: str) -> datetime.date:
    """Parse a date string from the API in YYYY-MM-DD format into a date object.

    Args:
        input_string: Date string in YYYY-MM-DD format

    Returns:
        Parsed date object

    Raises:
        ValueError: If input is None, empty, or not in expected format
    """

    if not input_string:
        raise ValueError("The input string should not be None or empty.")

    components = input_string.split("-")

    if len(components) != DATE_COMPONENTS_COUNT:
        raise ValueError(f"The input string should be of the format {EXPECTED_DATE_FORMAT}.")

    for component in components:
        try:
            _ = int(component)
        except ValueError as ex:
            raise ValueError(
                f"The input string should be of the format {EXPECTED_DATE_FORMAT}, "
                "where each date component is an integer."
            ) from ex

    year = int(components[0])
    month = int(components[1])
    day = int(components[2])

    return datetime.date(year=year, month=month, day=day)


def parse_datetime(input_string: str) -> datetime.datetime:
    """Parse a datetime string from the API in 'YYYY-MM-DD HH:MM:SS' format.

    Args:
        input_string: Datetime string in 'YYYY-MM-DD HH:MM:SS' format

    Returns:
        Parsed datetime object

    Raises:
        ValueError: If input is None, empty, or invalid placeholder
    """

    if not input_string:
        raise ValueError("The input string should not be None or empty.")

    if input_string == INVALID_DATETIME_PLACEHOLDER:
        raise ValueError(f"Invalid date time: {INVALID_DATETIME_PLACEHOLDER}")

    return datetime.datetime.strptime(input_string, DATETIME_FORMAT_STRING)


class Log:
    """Logging wrapper class for backward compatibility."""

    @staticmethod
    def info(message: str) -> None:
        """Log an info level log message."""
        logger.info(message)

    @staticmethod
    def debug(message: str) -> None:
        """Log a debug level log message."""
        logger.debug(message)

    @staticmethod
    def warning(message: str) -> None:
        """Log a warning level log message."""
        logger.warning(message)

    @staticmethod
    def error(message: str) -> None:
        """Log an error level log message."""
        logger.error(message)
