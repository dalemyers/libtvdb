"""All the types that are used in the API."""

import datetime
from typing import List, Optional

import deserialize

from libtvdb.model.enums import AirDay, ShowStatus
from libtvdb.utilities import parse_date, parse_datetime


def date_parser(value: Optional[str]) -> Optional[datetime.date]:
    """Parser method for parsing dates to pass to deserialize."""
    if value is None:
        return None

    if value in ["", "0000-00-00"]:
        return None

    return parse_date(value)


def datetime_parser(value: Optional[str]) -> Optional[datetime.datetime]:
    """Parser method for parsing datetimes to pass to deserialize."""
    if value is None:
        return None

    if value in ["", "0000-00-00 00:00:00"]:
        return None

    return parse_datetime(value)


def timestamp_parser(value: Optional[int]) -> Optional[datetime.datetime]:
    """Parser method for parsing datetimes to pass to deserialize."""
    if value is None:
        return None

    return datetime.datetime.fromtimestamp(value)


def status_parser(value: Optional[str]) -> str:
    """Parser method for cleaning up statuses to pass to deserialize."""
    if value is None or value == "":
        return ShowStatus.unknown.value

    return value


@deserialize.key("identifier", "id")
@deserialize.key("name", "seriesName")
@deserialize.key("first_aired", "firstAired")
@deserialize.key("series_identifier", "seriesId")
@deserialize.key("network_identifier", "networkId")
@deserialize.key("genres", "genre")
@deserialize.key("last_updated", "lastUpdated")
@deserialize.key("air_day", "airsDayOfWeek")
@deserialize.key("air_time", "airsTime")
@deserialize.key("imdb_id", "imdbId")
@deserialize.key("zap2it_id", "zap2itId")
@deserialize.key("added_by", "addedBy")
@deserialize.key("site_rating", "siteRating")
@deserialize.key("site_rating_count", "siteRatingCount")
@deserialize.parser("status", status_parser)
@deserialize.parser("firstAired", date_parser)
@deserialize.parser("lastUpdated", timestamp_parser)
@deserialize.parser("added", datetime_parser)
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
