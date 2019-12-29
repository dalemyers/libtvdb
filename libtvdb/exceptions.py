"""Custom exception types."""


class TVDBException(Exception):
    """Thrown when we can't get a more specific exception type."""


class NotFoundException(TVDBException):
    """Thrown when a show is not found after a search."""


class TVDBAuthenticationException(TVDBException):
    """Thrown on authentication error."""
