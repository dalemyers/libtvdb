"""libtvdb is a wrapper around the TVDB API (https://api.thetvdb.com/swagger).
"""

from typing import Any, Dict, ClassVar, Optional

import requests

class Log:
    """Fake log class that will be used until we implement logging."""

    @staticmethod
    def info(message):
        """Log an info level log message."""
        print("INFO: " + message)

    @staticmethod
    def debug(message):
        """Log a debug level log message."""
        print("DEBUG: " + message)

    @staticmethod
    def warning(message):
        """Log a warning level log message."""
        print("WARNING: " + message)

    @staticmethod
    def error(message):
        """Log an error level log message."""
        print("ERROR: " + message)


class TVDBClient:
    """The main client wrapper around the TVDB API.

    Instantiate a new one of these to use a new authentication session.
    """

    class Constants:
        """Constants that are used elsewhere in the TVDBClient class."""
        AUTH_TIMEOUT: ClassVar[float] = 3
        MAX_AUTH_RETRY_COUNT: ClassVar[int] = 3

    _BASE_API: ClassVar[str] = "https://api.thetvdb.com"

    def __init__(self, *, api_key: str, user_key: str, user_name: str) -> None:
        self.api_key = api_key
        self.user_key = user_key
        self.user_name = user_name
        self.auth_token = None

    #pylint: disable=no-self-use
    def _expand_url(self, path: str) -> str:
        """Take the path from a URL and expand it to the full API path."""
        return f"{TVDBClient._BASE_API}/{path}"
    #pylint: enable=no-self-use

    #pylint: disable=no-self-use
    def _construct_headers(self, *, additional_headers: Optional[Any] = None) -> Dict[str, str]:
        """Construct the headers used for all requests, inserting any additional headers as required."""

        headers = {
            "Accept": "application/json"
        }

        if additional_headers is None:
            return headers

        for header_name, header_value in additional_headers.items():
            headers[header_name] = header_value

        return headers
    #pylint: enable=no-self-use

    def authenticate(self) -> bool:
        """Authenticate the client with the API.

        This will exit early if we are already authenticated. It does not need
        to be called. All calls requiring that the client is authenticated will
        call this.
        """

        if self.auth_token is not None:
            Log.debug("Already authenticated, skipping")
            return True

        Log.info("Authenticating...")

        login_body = {
            "apikey": self.api_key,
            "userkey": self.user_key,
            "username": self.user_name,
        }

        for i in range(0, TVDBClient.Constants.MAX_AUTH_RETRY_COUNT):
            try:
                response = requests.post(
                    self._expand_url("login"),
                    json=login_body,
                    headers=self._construct_headers(),
                    timeout=TVDBClient.Constants.AUTH_TIMEOUT
                )

                # Since we authenticated successfully, we can break out of the
                # retry loop
                break
            except requests.exceptions.Timeout:
                will_retry = i < (TVDBClient.Constants.MAX_AUTH_RETRY_COUNT - 1)
                if will_retry:
                    Log.warning(f"Authentication timed out, but will retry.")
                else:
                    Log.error(f"Authentication timed out maximum number of times.")
                    return False

        if response.status_code < 200 or response.status_code >= 300:
            Log.error(f"Authentication failed withs status code: {response.status_code}")
            return False

        content = response.json()

        token = content.get("token")

        if token is None:
            Log.error("Failed to get token from login request")
            return False

        self.auth_token = token

        Log.info("Authenticated successfully")

        return True
