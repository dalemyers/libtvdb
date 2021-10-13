"""All the types that are used in the API."""

from typing import Optional

import deserialize


@deserialize.key("identifier", "id")
@deserialize.auto_snake()
class TagOption:
    """Represents a Tag Option."""

    help_text: Optional[str]
    identifier: int
    name: str
    tag: int
    tag_name: str

    def __str__(self):
        return f"TagOption<{self.identifier} - {self.name}>"
