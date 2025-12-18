"""Custom exception types for the libtvdb library."""


class TVDBException(Exception):
    """Base exception for all TVDB-related errors.
    
    All libtvdb exceptions inherit from this base class, allowing
    for easy catching of library-specific errors.
    """


class NotFoundException(TVDBException):
    """Raised when a requested resource is not found.
    
    This typically occurs when requesting a show, episode, or other
    resource that doesn't exist in the TVDB database.
    """


class TVDBAuthenticationException(TVDBException):
    """Raised when authentication with the TVDB API fails.
    
    This can occur due to invalid credentials, network timeouts,
    or server-side authentication issues.
    """
