"""All the types that are used in the API."""

import datetime
import json
from typing import Any, Dict, List, Optional, Union

import deserialize

from libtvdb.model.artwork import Artwork
from libtvdb.model.character import Character
from libtvdb.model.company import Company
from libtvdb.model.status import Status, StatusName
from libtvdb.model.remote_id import RemoteID
from libtvdb.model.season import SeasonBase
from libtvdb.model.trailer import Trailer
from libtvdb.model.parsers import date_parser, datetime_parser


def translated_name_parser(value: Optional[str]) -> Dict[str, str]:
    """Parser method for cleaning up statuses to pass to deserialize."""
    if value is None or value == "":
        return {}

    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return {}


class SeriesAirsDays:
    """Represents the days a show airs."""

    monday: bool
    tuesday: bool
    wednesday: bool
    thursday: bool
    friday: bool
    saturday: bool
    sunday: bool


@deserialize.key("identifier", "id")
@deserialize.auto_snake()
class Genre:
    """Represents a genre."""

    identifier: int
    name: str
    slug: str


@deserialize.key("identifier", "id")
@deserialize.key("show_type", "type")
@deserialize.key("object_id", "objectID")
@deserialize.key("airs_time_utc", "airsTimeUTC")
@deserialize.parser("id", str)
@deserialize.parser("first_aired", date_parser)
@deserialize.parser("first_air_time", date_parser)
@deserialize.parser("last_aired", date_parser)
@deserialize.parser("last_updated", datetime_parser)
@deserialize.parser("next_aired", date_parser)
@deserialize.parser("name_translated", translated_name_parser)
@deserialize.parser("score", float)
@deserialize.auto_snake()
class Show:
    """Represents a single show."""

    abbreviation: Optional[str]
    airs_days: Optional[SeriesAirsDays]
    airs_time_utc: Optional[str]
    airs_time: Optional[str]
    aliases: Optional[List[Union[str, Dict[str, str]]]]
    artworks: Optional[List[Artwork]]
    average_runtime: Optional[int]
    characters: Optional[List[Character]]
    companies: Optional[List[Company]]
    country: Optional[str]
    default_season_type: Optional[int]
    first_air_time: Optional[datetime.date]
    first_aired: Optional[datetime.date]
    genres: Optional[List[Genre]]
    identifier: str
    image: Optional[str]
    image_url: Optional[str]
    is_order_randomized: Optional[bool]
    last_aired: Optional[datetime.date]
    last_updated: Optional[datetime.datetime]
    lists: Optional[List[Dict[str, Any]]]
    name_translated: Optional[Dict[str, str]]
    name_translations: Optional[List[str]]  # Confirmed
    name: str
    network: Optional[str]
    next_aired: Optional[datetime.date]
    object_id: Optional[str]
    original_country: Optional[str]
    original_language: Optional[str]
    overview_translated: Optional[List[str]]
    overview_translations: Optional[List[str]]
    overview: Optional[str]
    overviews: Optional[Dict[str, str]]
    primary_language: Optional[str]
    remote_ids: Optional[List[RemoteID]]
    score: Optional[float]
    seasons: Optional[List[SeasonBase]]
    show_type: Optional[str]
    slug: str
    status: Union[Status, StatusName]
    thumbnail: Optional[str]
    trailers: Optional[List[Trailer]]
    translations: Optional[Dict[str, str]]
    tvdb_id: Optional[str]
    year: Optional[str]
