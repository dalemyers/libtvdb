"""Custom exception types."""

class TVDBException(Exception):
    """Thrown when we can't get a more specific exception type."""


class ShowNotFoundException(TVDBException):
    """Thrown when a show is not found after a search."""
    pass
