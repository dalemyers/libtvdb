"""All the types that are used in the API."""

from typing import Optional

import deserialize


@deserialize.key("identifier", "id")
@deserialize.auto_snake()
class ContentRating:
    """Represents a content rating of an episode of a show."""

    identifier: int
    description: Optional[str]
    name: str
    country: str
    content_type: str
    order: int
    fullname: Optional[str]

    def __str__(self):
        return f"ContentRating<{self.identifier} - {self.name}>"
