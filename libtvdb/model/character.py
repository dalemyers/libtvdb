"""All the types that are used in the API."""

from typing import List, Optional

import deserialize

from libtvdb.model.alias import Alias
from libtvdb.model.parsers import (
    optional_empty_str,
)


@deserialize.key("identifier", "id")
@deserialize.key("character_type", "type")
@deserialize.parser("url", optional_empty_str)
@deserialize.auto_snake()
class Character:
    """Represents a character of a show."""

    aliases: Optional[List[Alias]]
    character_type: Optional[int]
    episode_id: Optional[int]
    identifier: int
    image: Optional[str]
    is_featured: bool
    movie_id: Optional[int]
    name: Optional[str]
    name_translations: Optional[List[str]]
    overview_translations: Optional[List[str]]
    people_id: int
    people_type: Optional[str]
    series_id: int
    sort: int
    url: Optional[str]
    person_name: str

    def __str__(self):
        return f"Character<{self.identifier} - {self.name}>"
