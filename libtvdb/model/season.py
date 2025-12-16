"""All the types that are used in the API."""

from typing import Any

import deserialize


@deserialize.auto_snake()
@deserialize.key("identifier", "id")
@deserialize.key("season_type", "type")
class SeasonType:
    """Represents the type of a season."""

    identifier: int
    name: str
    season_type: str
    alternate_name: str | None


@deserialize.key("identifier", "id")
@deserialize.key("season_type", "type")
@deserialize.auto_snake()
class SeasonBase:
    """Represents a Season of a show."""

    abbreviation: str | None
    companies: dict[str, Any] | None
    country: str | None
    identifier: int
    image: str | None
    image_type: int | None
    last_updated: str | None
    name: str | None
    name_translations: list[str] | None
    number: int
    overview_translations: list[str] | None
    series_id: int
    slug: str | None
    season_type: SeasonType

    def __str__(self):
        return f"SeasonBase<{self.identifier} - {self.name}>"
