"""All the types that are used in the API."""

from typing import Any

import deserialize

from libtvdb.model.alias import Alias
from libtvdb.model.parsers import (
    optional_empty_str,
)


@deserialize.key("identifier", "id")
@deserialize.key("character_type", "type")
@deserialize.key("person_img_url", "personImgURL")
@deserialize.parser("url", optional_empty_str)
@deserialize.auto_snake()
class Character:
    """Represents a character of a show."""

    aliases: list[Alias] | None
    character_type: int | None
    episode_id: int | None
    identifier: int
    image: str | None
    is_featured: bool
    movie: int | None
    movie_id: int | None
    name: str | None
    name_translations: list[str] | None
    overview_translations: list[str] | None
    people_id: int
    people_type: str | None
    series: int | None
    series_id: int
    sort: int
    url: str | None
    person_name: str
    person_img_url: str | None
    tag_options: Any | None

    def __str__(self) -> str:
        return f"Character<{self.identifier} - {self.name}>"

    def __repr__(self) -> str:
        return f"Character<{self.identifier} - {self.name} (people_id={self.people_id})>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Character):
            return NotImplemented
        return self.identifier == other.identifier

    def __hash__(self) -> int:
        return hash(self.identifier)
