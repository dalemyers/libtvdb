"""All the types that are used in the API."""

import datetime
from typing import Any, Dict, Optional

from libtvdb.utilities import parse_datetime, require, try_pop

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

    def __init__(
            self,
            *,
            identifier: int,
            series_identifier: int,
            name: str,
            role: str,
            sort_order: int,
            image: str,
            image_author: int,
            image_added: Optional[datetime.datetime],
            last_updated: Optional[datetime.datetime]
        ) -> None:

        self.identifier = identifier
        self.series_identifier = series_identifier
        self.name = name
        self.role = role
        self.sort_order = sort_order
        self.image = image
        self.image_author = image_author
        self.image_added = image_added
        self.last_updated = last_updated

        if self.identifier is None:
            raise ValueError("Identifier should not be None")

        if self.series_identifier is None:
            raise ValueError("Series identifier should not be None")

        if self.name is None:
            raise ValueError("Name should not be None")

        if self.role is None:
            raise ValueError("Role should not be None")

        if self.sort_order is None:
            raise ValueError("Sort order should not be None")

        if self.image is None:
            raise ValueError("Image should not be None")

        if self.image_author is None:
            raise ValueError("Image author should not be None")

    def __str__(self):
        return f"{self.name} ({self.role}, {self.identifier})"

    @staticmethod
    def from_json(data: Dict[str, Any]) -> 'Actor':
        """Convert actor data from the API to an Actor object."""

        # Get the fields which are always there
        identifier = require(try_pop(data, 'id'))
        series_identifier = require(try_pop(data, 'seriesId'))
        name = require(try_pop(data, 'name'))
        role = require(try_pop(data, 'role'))
        sort_order = require(try_pop(data, 'sortOrder'))
        image = require(try_pop(data, 'image'))
        image_author = require(try_pop(data, 'imageAuthor'))
        image_added_string = require(try_pop(data, 'imageAdded'))
        last_updated_string = require(try_pop(data, 'lastUpdated'))

        if len(data.keys()) > 0:
            raise Exception(f"Extra keys remain in Actor data: {data.keys()}")

        image_added: Optional[datetime.datetime]
        try:
            image_added = parse_datetime(image_added_string)
        except ValueError:
            image_added = None

        last_updated: Optional[datetime.datetime]
        try:
            last_updated = parse_datetime(last_updated_string)
        except ValueError:
            last_updated = None

        return Actor(
            identifier=identifier,
            series_identifier=series_identifier,
            name=name,
            role=role,
            sort_order=sort_order,
            image=image,
            image_author=image_author,
            image_added=image_added,
            last_updated=last_updated
        )
