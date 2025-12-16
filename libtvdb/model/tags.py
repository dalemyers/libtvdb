"""All the types that are used in the API."""

import deserialize


@deserialize.key("identifier", "id")
@deserialize.auto_snake()
class TagOption:
    """Represents a Tag Option."""

    help_text: str | None
    identifier: int
    name: str
    tag: int
    tag_name: str

    def __str__(self):
        return f"TagOption<{self.identifier} - {self.name}>"
