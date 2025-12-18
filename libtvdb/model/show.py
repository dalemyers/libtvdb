"""All the types that are used in the API."""

import datetime
import json
from typing import Any

import deserialize

from libtvdb.model.artwork import Artwork
from libtvdb.model.character import Character
from libtvdb.model.company import Company
from libtvdb.model.parsers import date_parser, datetime_parser, optional_float
from libtvdb.model.remote_id import RemoteID
from libtvdb.model.season import SeasonBase
from libtvdb.model.status import Status, StatusName
from libtvdb.model.trailer import Trailer


def translated_name_parser(value: str | None) -> dict[str, str]:
    """Parser method for cleaning up statuses to pass to deserialize."""
    if value is None or value == "":
        return {}

    try:
        result = json.loads(value)
        return result if isinstance(result, dict) else {}
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

    def __str__(self) -> str:
        return f"Genre<{self.identifier} - {self.name}>"

    def __repr__(self) -> str:
        return f"Genre<{self.identifier} - {self.name} ({self.slug})>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Genre):
            return NotImplemented
        return self.identifier == other.identifier

    def __hash__(self) -> int:
        return hash(self.identifier)


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
@deserialize.parser("score", optional_float)
@deserialize.auto_snake()
class Show:
    """Represents a single show."""

    abbreviation: str | None
    airs_days: SeriesAirsDays | None
    airs_time_utc: str | None
    airs_time: str | None
    aliases: list[str | dict[str, str]] | None
    artworks: list[Artwork] | None
    average_runtime: int | None
    characters: list[Character] | None
    companies: list[Company] | None
    content_ratings: list[Any] | None
    country: str | None
    default_season_type: int | None
    episodes: list[Any] | None
    first_air_time: datetime.date | None
    first_aired: datetime.date | None
    genres: list[Genre] | None
    identifier: str
    image: str | None
    image_url: str | None
    is_order_randomized: bool | None
    last_aired: datetime.date | None
    last_updated: datetime.datetime | None
    latest_network: Company | None
    lists: list[dict[str, Any]] | None
    name_translated: dict[str, str] | None
    name_translations: list[str] | None  # Confirmed
    name: str
    network: str | None
    next_aired: datetime.date | None
    object_id: str | None
    original_country: str | None
    original_language: str | None
    original_network: Company | None
    overview_translated: list[str] | None
    overview_translations: list[str] | None
    overview: str | None
    overviews: dict[str, str] | None
    primary_language: str | None
    primary_type: str | None
    remote_ids: list[RemoteID] | None
    score: float | None
    season_types: list[Any] | None
    seasons: list[SeasonBase] | None
    show_type: str | None
    slug: str
    status: Status | StatusName
    tags: list[Any] | None
    thumbnail: str | None
    trailers: list[Trailer] | None
    translations: dict[str, str] | None
    tvdb_id: str | None
    year: str | None

    def __str__(self) -> str:
        return f"Show<{self.identifier} - {self.name}>"

    def __repr__(self) -> str:
        return f"Show<{self.identifier} - {self.name} ({self.year}) - {self.status}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Show):
            return NotImplemented
        return self.identifier == other.identifier

    def __hash__(self) -> int:
        return hash(self.identifier)
