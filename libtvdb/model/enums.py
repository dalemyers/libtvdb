"""All the enums that are used in the API."""

import enum


class ShowStatus(enum.Enum):
    """Represents the status of a show."""

    continuing = "Continuing"
    ended = "Ended"
    unknown = "Unknown"


class AirDay(enum.Enum):
    """Represents when a show airs."""

    monday = "Monday"
    tuesday = "Tuesday"
    wednesday = "Wednesday"
    thursday = "Thursday"
    friday = "Friday"
    saturday = "Saturday"
    sunday = "Sunday"
