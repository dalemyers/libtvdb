"""All the types that are used in the API."""

import datetime
from collections import defaultdict
from typing import Any

import deserialize

from libtvdb.model.award import AwardBase
from libtvdb.model.character import Character
from libtvdb.model.content_rating import ContentRating
from libtvdb.model.network import NetworkBase
from libtvdb.model.parsers import date_parser, datetime_parser
from libtvdb.model.remote_id import RemoteID
from libtvdb.model.season import SeasonBase
from libtvdb.model.tags import TagOption
from libtvdb.model.trailer import Trailer


@deserialize.auto_snake()
@deserialize.key("identifier", "id")
@deserialize.parser("aired", date_parser)
@deserialize.parser("last_updated", datetime_parser)
@deserialize.parser("year", lambda x: int(x) if x else None)
class Episode:
    """Represents an episode of a show."""

    @deserialize.key("episode_name", "episodeName")
    class LanguageCode:
        """Represents the language that an episode is in."""

        episode_name: str
        overview: str

    absolute_number: int | None
    aired: datetime.date | None
    airs_after_season: int | None
    airs_before_episode: int | None
    airs_before_season: int | None
    awards: list[AwardBase] | None
    characters: list[Character] | None
    companies: list[Any] | None
    content_ratings: list[ContentRating] | None
    finale_type: Any | None
    identifier: int
    image: str | None
    image_type: int | None
    is_movie: int  # ?
    last_updated: datetime.datetime
    name: str
    name_translations: list[str] | None
    networks: list[NetworkBase] | None
    nominations: Any | None
    number: int
    overview: str | None
    overview_translations: list[str] | None
    production_code: str | None
    remote_ids: list[RemoteID] | None
    runtime: int | None
    season_name: str | None
    season_number: int
    seasons: list[SeasonBase] | None
    series_id: int
    studios: list[Any] | None
    tag_options: list[TagOption] | None
    trailers: list[Trailer] | None
    year: int | None

    @property
    def characters_by_role(self) -> dict[str, list[Character]]:
        """Get all characters keyed by their role.

        :returns: A dict mapping roles to characters
        """
        output: dict[str, list[Character]] = defaultdict(list)

        if self.characters is None:
            return output

        for character in self.characters:
            if character.people_type is None:
                output["Unknown"].append(character)
            else:
                output[character.people_type].append(character)

        return output

    def __str__(self):
        return f"Episode<{self.identifier} - {self.name}"
