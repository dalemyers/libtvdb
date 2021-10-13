"""All the types that are used in the API."""

from typing import Any, Dict, Optional
import deserialize

from libtvdb.model.tags import TagOption


@deserialize.key("identifier", "id")
@deserialize.key("artwork_type", "type")
@deserialize.parser("id", str)
@deserialize.parser("score", float)
@deserialize.auto_snake()
class Artwork:
    """Represents an artwork."""

    identifier: str
    image: str
    thumbnail: str
    language: Optional[str]
    artwork_type: int
    score: Optional[float]
    width: int
    height: int
    thumbnail_width: int
    thumbnail_height: int
    updated_at: int
    series_id: Optional[int]
    people_id: Optional[int]
    season_id: Optional[int]
    episode_id: Optional[int]
    series_people_id: Optional[int]
    network_id: Optional[int]
    movie_id: Optional[int]
    tag_options: TagOption
    status: Dict[str, Any]

    def __str__(self):
        return f"Artwork<{self.identifier} - {self.image}>"
