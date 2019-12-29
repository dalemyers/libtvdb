"""All the types that are used in the API."""

import datetime
from typing import List, Optional

import deserialize

from libtvdb.utilities import parse_date


def date_parser(value: Optional[str]) -> Optional[datetime.date]:
    """Parser method for parsing dates to pass to deserialize."""
    if value is None:
        return None

    if value in ["", "0000-00-00"]:
        return None

    return parse_date(value)


def timestamp_parser(value: Optional[int]) -> Optional[datetime.datetime]:
    """Parser method for parsing datetimes to pass to deserialize."""
    if value is None:
        return None

    return datetime.datetime.fromtimestamp(value)


def optional_float(value: Optional[int]) -> Optional[float]:
    """Parser for optional ints to floats."""
    if value is None:
        return None

    return float(value)


def optional_empty_str(value: Optional[str]) -> Optional[str]:
    """Parser for empty strs to None."""
    if value is None:
        return None

    if value == "":
        return None

    return value


@deserialize.key("absolute_number", "absoluteNumber")
@deserialize.key("aired_episode_number", "airedEpisodeNumber")
@deserialize.key("aired_season", "airedSeason")
@deserialize.key("aired_season_id", "airedSeasonID")
@deserialize.key("airs_after_season", "airsAfterSeason")
@deserialize.key("airs_before_season", "airsBeforeSeason")
@deserialize.key("airs_before_episode", "airsBeforeEpisode")
@deserialize.key("dvd_chapter", "dvdChapter")
@deserialize.key("dvd_disc_id", "dvdDiscid")
@deserialize.key("dvd_episode_number", "dvdEpisodeNumber")
@deserialize.key("dvd_season", "dvdSeason")
@deserialize.key("episode_name", "episodeName")
@deserialize.key("file_name", "filename")
@deserialize.key("first_aired", "firstAired")
@deserialize.key("guest_stars", "guestStars")
@deserialize.key("identifier", "id")
@deserialize.key("imdb_id", "imdbId")
@deserialize.key("last_updated", "lastUpdated")
@deserialize.key("last_updated_by", "lastUpdatedBy")
@deserialize.key("production_code", "productionCode")
@deserialize.key("series_id", "seriesId")
@deserialize.key("show_url", "showUrl")
@deserialize.key("site_rating", "siteRating")
@deserialize.key("site_rating_count", "siteRatingCount")
@deserialize.key("thumb_added", "thumbAdded")
@deserialize.key("thumb_author", "thumbAuthor")
@deserialize.key("thumb_height", "thumbHeight")
@deserialize.key("thumb_width", "thumbWidth")
@deserialize.parser("director", optional_empty_str)
@deserialize.parser("dvdDiscid", optional_empty_str)
@deserialize.parser("dvdEpisodeNumber", optional_float)
@deserialize.parser("filename", optional_empty_str)
@deserialize.parser("firstAired", date_parser)
@deserialize.parser("imdbId", optional_empty_str)
@deserialize.parser("lastUpdated", timestamp_parser)
@deserialize.parser("productionCode", optional_empty_str)
@deserialize.parser("showUrl", optional_empty_str)
@deserialize.parser("siteRating", float)
@deserialize.parser("thumbAdded", optional_empty_str)
class Episode:
    """Represents an episode of a show."""

    @deserialize.key("episode_name", "episodeName")
    class LanguageCode:
        """Represents the language that an episode is in."""

        episode_name: str
        overview: str

    absolute_number: Optional[int]
    aired_episode_number: int
    aired_season: int
    aired_season_id: Optional[int]
    airs_after_season: Optional[int]
    airs_before_episode: Optional[int]
    airs_before_season: Optional[int]
    director: Optional[str]
    directors: List[str]
    dvd_chapter: Optional[int]
    dvd_disc_id: Optional[str]
    dvd_episode_number: Optional[float]
    dvd_season: Optional[int]
    episode_name: str
    file_name: Optional[str]
    first_aired: Optional[datetime.date]
    guest_stars: List[str]
    identifier: int
    imdb_id: Optional[str]
    language: Optional[LanguageCode]
    last_updated: datetime.datetime
    last_updated_by: int
    overview: Optional[str]
    production_code: Optional[str]
    series_id: int
    show_url: Optional[str]
    site_rating: float
    site_rating_count: int
    thumb_added: Optional[str]
    thumb_author: int
    thumb_height: Optional[str]
    thumb_width: Optional[str]
    writers: List[str]

    def __str__(self):
        return f"{self.identifier})"
