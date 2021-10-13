"""All the types that are used in the API."""


class Alias:
    """Represents an alias of a character."""

    language: str
    name: str

    def __str__(self):
        return f"Alias<{self.language} - {self.name}>"
