"""All the types that are used in the API."""

import datetime
from typing import List, Optional

import deserialize

from libtvdb.model.parsers import date_parser
from libtvdb.model.company import CompanyType


@deserialize.key("identifier", "id")
@deserialize.parser("active_date", date_parser)
@deserialize.parser("inactive_date", date_parser)
@deserialize.auto_snake()
class NetworkBase:
    """Represents a network."""

    abbreviation: Optional[str]
    active_date: Optional[datetime.date]
    aliases: Optional[List[str]]
    company_type: CompanyType
    country: str
    identifier: int
    inactive_date: Optional[datetime.date]
    name: str
    name_translations: Optional[List[str]]
    overview: Optional[str]
    overview_translations: Optional[List[str]]
    primary_company_type: int
    slug: str

    def __str__(self):
        return f"NetworkBase<{self.identifier} - {self.name}>"
