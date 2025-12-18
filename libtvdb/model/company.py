"""All the types that are used in the API."""

import datetime
from typing import Any

import deserialize

from libtvdb.model.alias import Alias
from libtvdb.model.parsers import date_parser


@deserialize.key("identifier", "id")
@deserialize.parser("active_date", date_parser)
@deserialize.auto_snake()
class CompanyType:
    """Represents a company type."""

    company_type_id: int
    company_type_name: str

    def __str__(self) -> str:
        return f"CompanyType<{self.company_type_id} - {self.company_type_name}>"

    def __repr__(self) -> str:
        return f"CompanyType<{self.company_type_id} - {self.company_type_name}>"


@deserialize.key("identifier", "id")
@deserialize.parser("active_date", date_parser)
@deserialize.parser("inactive_date", date_parser)
@deserialize.auto_snake()
class Company:
    """Represents a company."""

    aliases: list[Alias] | None
    active_date: datetime.date | None
    inactive_date: datetime.date | None
    country: str | None
    identifier: int
    name: str
    name_translations: list[str] | None
    overview_translations: list[str] | None
    parent_company: dict[str, Any] | None
    primary_company_type: int | None
    company_type: CompanyType
    slug: str
    tag_options: Any | None

    def __str__(self) -> str:
        return f"Company<{self.identifier} - {self.name}>"

    def __repr__(self) -> str:
        return f"Company<{self.identifier} - {self.name} ({self.slug})>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Company):
            return NotImplemented
        return self.identifier == other.identifier

    def __hash__(self) -> int:
        return hash(self.identifier)
