"""All the types that are used in the API."""

import deserialize


@deserialize.key("identifier", "id")
@deserialize.key("remoteid_type", "type")
@deserialize.auto_snake()
class RemoteID:
    """Represents a remote ID."""

    identifier: str
    remoteid_type: int
    source_name: str

    def __str__(self):
        return f"RemoteID<{self.identifier} - {self.source_name}>"
