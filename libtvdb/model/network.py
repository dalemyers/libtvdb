"""All the types that are used in the API."""

import datetime

import deserialize

from libtvdb.model.company import CompanyType
from libtvdb.model.parsers import date_parser


@deserialize.key("identifier", "id")
@deserialize.parser("active_date", date_parser)
@deserialize.parser("inactive_date", date_parser)
@deserialize.auto_snake()
class NetworkBase:
    """Represents a network."""

    abbreviation: str | None
    active_date: datetime.date | None
    aliases: list[str] | None
    company_type: CompanyType
    country: str
    identifier: int
    inactive_date: datetime.date | None
    name: str
    name_translations: list[str] | None
    overview: str | None
    overview_translations: list[str] | None
    primary_company_type: int
    slug: str

    def __str__(self):
        return f"NetworkBase<{self.identifier} - {self.name}>"
