"""Utility classes and methods for working with the TVDB API."""

import datetime


def parse_date(input_string: str) -> datetime.date:
    """Parse a date string from the API in YYYY-MM-DD format into a date object."""

    if input_string is None:
        raise ValueError("The input string should not be none.")

    if input_string == "":
        raise ValueError("The input string should not be empty.")

    components = input_string.split("-")

    if len(components) != 3:
        raise ValueError("The input string should be of the format YYYY-MM-DD.")

    for component in components:
        try:
            _ = int(component)
        except ValueError as ex:
            raise ValueError(
                "The input string should be of the format YYYY-MM-DD, where each date component is an integer."
            ) from ex

    year = int(components[0])
    month = int(components[1])
    day = int(components[2])

    return datetime.date(year=year, month=month, day=day)


def parse_datetime(input_string: str) -> datetime.datetime:
    """Parse a datetime string from the API in 'YYYY-MM-DD HH:MM:SS' format into a datetime object."""

    if input_string is None:
        raise ValueError("The input string should not be none.")

    if input_string == "":
        raise ValueError("The input string should not be empty.")

    if input_string == "0000-00-00 00:00:00":
        raise ValueError("Invalid date time")

    return datetime.datetime.strptime(input_string, "%Y-%m-%d %H:%M:%S")


class Log:
    """Fake log class that will be used until we implement logging."""

    @staticmethod
    def info(message):
        """Log an info level log message."""
        print("INFO: " + message)

    @staticmethod
    def debug(message):
        """Log a debug level log message."""
        print("DEBUG: " + message)

    @staticmethod
    def warning(message):
        """Log a warning level log message."""
        print("WARNING: " + message)

    @staticmethod
    def error(message):
        """Log an error level log message."""
        print("ERROR: " + message)
