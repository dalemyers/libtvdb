"""All the types that are used in the API."""

from typing import Any

import deserialize

from libtvdb.model.parsers import optional_float
from libtvdb.model.tags import TagOption


@deserialize.key("identifier", "id")
@deserialize.key("artwork_type", "type")
@deserialize.parser("id", str)
@deserialize.parser("score", optional_float)
@deserialize.auto_snake()
class Artwork:
    """Represents an artwork."""

    identifier: str
    image: str
    thumbnail: str
    language: str | None
    artwork_type: int
    score: float | None
    width: int
    height: int
    includes_text: bool | None
    thumbnail_width: int
    thumbnail_height: int
    updated_at: int
    series_id: int | None
    people_id: int | None
    season_id: int | None
    episode_id: int | None
    series_people_id: int | None
    network_id: int | None
    movie_id: int | None
    tag_options: TagOption | None
    status: dict[str, Any]

    def __str__(self):
        return f"Artwork<{self.identifier} - {self.image}>"
