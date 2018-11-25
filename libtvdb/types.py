"""All the types that are used in the API."""

import datetime
import enum
from typing import Any, Dict, List, Optional

from libtvdb.utilities import parse_date, require, try_pop

class ShowStatus(enum.Enum):
    """Represents the status of a show."""
    continuing = 'Continuing'
    ended = 'Ended'
    unknown = 'Unknown'


class Show:
    """Represents a single show."""

    identifier: int
    name: str
    slug: str
    status: ShowStatus
    first_aired: Optional[datetime.date]
    aliases: List[str]
    network: str
    overview: Optional[str]
    banner: Optional[str]

    def __init__(
            self,
            *,
            identifier: int,
            name: str,
            slug: str,
            status: ShowStatus,
            aliases: List[str],
            network: str,
            first_aired: Optional[datetime.date] = None,
            overview: Optional[str] = None,
            banner: Optional[str] = None
        ) -> None:

        self.identifier = identifier
        self.name = name
        self.slug = slug
        self.status = status
        self.first_aired = first_aired
        self.aliases = aliases
        self.network = network
        self.overview = overview
        self.banner = banner

        if self.identifier is None:
            raise ValueError("Identifier should not be None")

        if self.name is None:
            raise ValueError("Name should not be None")

        if self.slug is None:
            raise ValueError("Slug should not be None")

        if self.status is None:
            raise ValueError("Status should not be None")

        if self.aliases is None:
            raise ValueError("Aliases should not be None")

        if self.network is None:
            raise ValueError("Network should not be None")

    def __str__(self):
        return f"{self.name} ({self.identifier})"

    @staticmethod
    def from_json(data: Dict[str, Any]) -> 'Show':
        """Convert Show data from the API to a Show object."""

        aliases = require(try_pop(data, 'aliases'))
        first_aired_string = try_pop(data, 'firstAired')
        identifier = require(try_pop(data, 'id'))
        network = require(try_pop(data, 'network'))
        overview = try_pop(data, 'overview')
        series_name = require(try_pop(data, 'seriesName'))
        slug = require(try_pop(data, 'slug'))
        status_string = try_pop(data, 'status')
        banner = try_pop(data, 'banner')

        if len(data.keys()) > 0:
            raise Exception(f"Extra keys remain in Show data: {data.keys()}")

        if status_string is None or status_string == "":
            status = ShowStatus.unknown
        else:
            status = ShowStatus(status_string)

        if first_aired_string is None or first_aired_string == "":
            first_aired = None
        else:
            first_aired = parse_date(first_aired_string)

        return Show(
            identifier=identifier,
            name=series_name,
            aliases=aliases,
            first_aired=first_aired,
            network=network,
            overview=overview,
            slug=slug,
            status=status,
            banner=banner
        )
