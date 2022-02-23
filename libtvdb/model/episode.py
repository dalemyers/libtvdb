"""All the types that are used in the API."""

from collections import defaultdict
import datetime
from typing import Any, Dict, List, Optional

import deserialize

from libtvdb.model.parsers import date_parser, datetime_parser
from libtvdb.model.award import AwardBase
from libtvdb.model.character import Character
from libtvdb.model.content_rating import ContentRating
from libtvdb.model.network import NetworkBase
from libtvdb.model.remote_id import RemoteID
from libtvdb.model.season import SeasonBase
from libtvdb.model.tags import TagOption
from libtvdb.model.trailer import Trailer


@deserialize.auto_snake()
@deserialize.key("identifier", "id")
@deserialize.parser("aired", date_parser)
@deserialize.parser("last_updated", datetime_parser)
class Episode:
    """Represents an episode of a show."""

    @deserialize.key("episode_name", "episodeName")
    class LanguageCode:
        """Represents the language that an episode is in."""

        episode_name: str
        overview: str

    aired: Optional[datetime.date]
    airs_after_season: Optional[int]
    airs_before_episode: Optional[int]
    airs_before_season: Optional[int]
    awards: Optional[List[AwardBase]]
    characters: Optional[List[Character]]
    content_ratings: Optional[List[ContentRating]]
    finale_type: Optional[Any]
    identifier: int
    image: Optional[str]
    image_type: Optional[int]
    is_movie: int  # ?
    last_updated: datetime.datetime
    name: str
    name_translations: Optional[List[str]]
    networks: Optional[List[NetworkBase]]
    nominations: Optional[Any]
    number: int
    overview: Optional[str]
    overview_translations: Optional[List[str]]
    production_code: Optional[str]
    remote_ids: Optional[List[RemoteID]]
    runtime: Optional[int]
    season_name: Optional[str]
    season_number: int
    seasons: Optional[List[SeasonBase]]
    series_id: int
    studios: Optional[List[Any]]
    tag_options: Optional[List[TagOption]]
    trailers: Optional[List[Trailer]]

    @property
    def characters_by_role(self) -> Dict[str, List[Character]]:
        """Get all characters keyed by their role.

        :returns: A dict mapping roles to characters
        """
        output: Dict[str, List[Character]] = defaultdict(list)

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
