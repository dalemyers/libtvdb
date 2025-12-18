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

    def __str__(self) -> str:
        return f"SeasonBase<{self.identifier} - {self.name}>"

    def __repr__(self) -> str:
        return f"SeasonBase<{self.identifier} - S{self.number:02d} - {self.name}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SeasonBase):
            return NotImplemented
        return self.identifier == other.identifier

    def __hash__(self) -> int:
        return hash(self.identifier)
