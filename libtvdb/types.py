"""All the types that are used in the API."""

import datetime
import enum
from typing import Any, Dict, List, Optional

from libtvdb.utilities import parse_date, parse_datetime, require, try_pop

class ShowStatus(enum.Enum):
    """Represents the status of a show."""
    continuing = 'Continuing'
    ended = 'Ended'
    unknown = 'Unknown'

class AirDay(enum.Enum):
    """Represents when a show airs."""
    monday = 'Monday'
    tuesday = 'Tuesday'
    wednesday = 'Wednesday'
    thursday = 'Thursday'
    friday = 'Friday'
    saturday = 'Saturday'
    sunday = 'Sunday'


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

    # These properties are only populated on a specific query (i.e. not a search)
    series_identifier: Optional[str]
    network_identifier: Optional[str]
    runtime: Optional[str]
    genres: Optional[List[str]]
    last_updated: Optional[datetime.datetime]
    air_day: Optional[AirDay]
    air_time: Optional[str]
    rating: Optional[str]
    imdb_id: Optional[str]
    zap2it_id: Optional[str]
    added: Optional[datetime.datetime]
    added_by: Optional[int]
    site_rating: Optional[float]
    site_rating_count: Optional[int]


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
            banner: Optional[str] = None,
            series_identifier: Optional[str] = None,
            network_identifier: Optional[str] = None,
            runtime: Optional[str] = None,
            genres: Optional[List[str]] = None,
            last_updated: Optional[datetime.datetime] = None,
            air_day: Optional[AirDay] = None,
            air_time: Optional[str] = None,
            rating: Optional[str] = None,
            imdb_id: Optional[str] = None,
            zap2it_id: Optional[str] = None,
            added: Optional[datetime.datetime] = None,
            added_by: Optional[int] = None,
            site_rating: Optional[float] = None,
            site_rating_count: Optional[int] = None
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

        self.series_identifier = series_identifier
        self.network_identifier = network_identifier
        self.runtime = runtime
        self.genres = genres
        self.last_updated = last_updated
        self.air_day = air_day
        self.air_time = air_time
        self.rating = rating
        self.imdb_id = imdb_id
        self.zap2it_id = zap2it_id
        self.added = added
        self.added_by = added_by
        self.site_rating = site_rating
        self.site_rating_count = site_rating_count

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

        print(data)

        # Get the fields which are always there
        aliases = require(try_pop(data, 'aliases'))
        first_aired_string = try_pop(data, 'firstAired')
        identifier = require(try_pop(data, 'id'))
        network = require(try_pop(data, 'network'))
        overview = try_pop(data, 'overview')
        series_name = require(try_pop(data, 'seriesName'))
        slug = require(try_pop(data, 'slug'))
        status_string = try_pop(data, 'status')
        banner = try_pop(data, 'banner')

        # These fields are only there on a specific show load (i.e. not a search)
        series_identifier = try_pop(data, 'seriesId')
        network_identifier = try_pop(data, 'networkId')
        runtime = try_pop(data, 'runtime')
        genres = try_pop(data, 'genre')
        last_updated_stamp = try_pop(data, 'lastUpdated')
        air_day_string = try_pop(data, 'airsDayOfWeek')
        air_time = try_pop(data, 'airsTime')
        rating = try_pop(data, 'rating')
        imdb_id = try_pop(data, 'imdbId')
        zap2it_id = try_pop(data, 'zap2itId')
        added_date_string = try_pop(data, 'added')
        added_by = try_pop(data, 'addedBy')
        site_rating = try_pop(data, 'siteRating')
        site_rating_count = try_pop(data, 'siteRatingCount')

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

        last_updated: Optional[datetime.datetime] = None
        if last_updated_stamp is not None:
            last_updated = datetime.datetime.fromtimestamp(last_updated_stamp)

        added: Optional[datetime.datetime] = None
        if added_date_string is not None and added_date_string != "":
            added = parse_datetime(added_date_string)

        air_day: Optional[AirDay] = None
        if air_day_string is not None:
            air_day = AirDay(air_day_string)

        return Show(
            identifier=identifier,
            name=series_name,
            aliases=aliases,
            first_aired=first_aired,
            network=network,
            overview=overview,
            slug=slug,
            status=status,
            banner=banner,
            series_identifier=series_identifier,
            network_identifier=network_identifier,
            runtime=runtime,
            genres=genres,
            last_updated=last_updated,
            air_day=air_day,
            air_time=air_time,
            rating=rating,
            imdb_id=imdb_id,
            zap2it_id=zap2it_id,
            added=added,
            added_by=added_by,
            site_rating=site_rating,
            site_rating_count=site_rating_count
        )
