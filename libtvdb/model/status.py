"""All the types that are used in the API."""

import enum

import deserialize


class StatusName(enum.Enum):
    """Represents the status of a show."""

    CONTINUING = "Continuing"
    ENDED = "Ended"
    UPCOMING = "Upcoming"
    UNKNOWN = "Unknown"


@deserialize.key("identifier", "id")
@deserialize.auto_snake()
class Status:
    """Represents a Status."""

    identifier: int
    name: StatusName
    record_type: str
    keep_updated: bool

    def __str__(self):
        return f"Status<{self.identifier} - {self.name}>"
