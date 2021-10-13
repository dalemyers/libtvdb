"""All the types that are used in the API."""

import datetime
from typing import Optional

import deserialize

from libtvdb.model.parsers import datetime_parser


@deserialize.key("identifier", "id")
@deserialize.key("series_identifier", "seriesId")
@deserialize.key("sort_order", "sortOrder")
@deserialize.key("image_author", "imageAuthor")
@deserialize.key("image_added", "imageAdded")
@deserialize.key("last_updated", "lastUpdated")
@deserialize.parser("imageAdded", datetime_parser)
@deserialize.parser("lastUpdated", datetime_parser)
class Actor:
    """Represents an actor on a show."""

    identifier: int
    series_identifier: int
    name: str
    role: str
    sort_order: int
    image: str
    image_author: int
    image_added: Optional[datetime.datetime]
    last_updated: Optional[datetime.datetime]

    def __str__(self):
        return f"{self.name} ({self.role}, {self.identifier})"
