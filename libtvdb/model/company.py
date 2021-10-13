"""All the types that are used in the API."""

import datetime
from typing import List, Optional

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

    def __str__(self):
        return f"CompanyType<{self.company_type_id} - {self.company_type_name}>"


@deserialize.key("identifier", "id")
@deserialize.parser("active_date", date_parser)
@deserialize.parser("inactive_date", date_parser)
@deserialize.auto_snake()
class Company:
    """Represents a company."""

    active_date: Optional[datetime.date]
    inactive_date: Optional[datetime.date]
    aliases: Optional[List[Alias]]
    country: Optional[str]
    identifier: int
    name: str
    name_translations: Optional[List[str]]
    overview_translations: Optional[List[str]]
    primary_company_type: Optional[int]
    company_type: CompanyType
    slug: str

    def __str__(self):
        return f"Company<{self.identifier} - {self.name}>"
