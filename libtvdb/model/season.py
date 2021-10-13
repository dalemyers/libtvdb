"""All the types that are used in the API."""

from typing import Any, Dict, List, Optional
import deserialize


@deserialize.auto_snake()
@deserialize.key("identifier", "id")
@deserialize.key("season_type", "type")
class SeasonType:
    """Represents the type of a season."""

    identifier: int
    name: str
    season_type: str


@deserialize.key("identifier", "id")
@deserialize.key("season_type", "type")
@deserialize.auto_snake()
class SeasonBase:
    """Represents a Season of a show."""

    abbreviation: Optional[str]
    companies: Optional[Dict[str, Any]]
    country: Optional[str]
    identifier: int
    image: Optional[str]
    image_type: Optional[int]
    name: Optional[str]
    name_translations: Optional[List[str]]
    number: int
    overview_translations: Optional[List[str]]
    series_id: int
    slug: Optional[str]
    season_type: SeasonType

    def __str__(self):
        return f"SeasonBase<{self.identifier} - {self.name}>"
