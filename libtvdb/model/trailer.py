"""All the types that are used in the API."""

import deserialize


@deserialize.key("identifier", "id")
@deserialize.auto_snake()
class Trailer:
    """Represents a Trailer."""

    identifier: int
    language: str
    name: str
    url: str

    def __str__(self):
        return f"Trailer<{self.identifier} - {self.name}>"
