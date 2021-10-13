"""All the types that are used in the API."""

import deserialize


@deserialize.key("identifier", "id")
class AwardBase:
    """Represents an award of a show."""

    identifier: int
    name: str

    def __str__(self):
        return f"Award<{self.identifier} - {self.name}>"
