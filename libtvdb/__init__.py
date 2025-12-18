"""libtvdb is a wrapper around the TVDB API (https://api.thetvdb.com/swagger)."""

import json
import urllib.parse
from typing import Any, ClassVar

import deserialize
import requests

from libtvdb.exceptions import (
    NotFoundException,
    TVDBAuthenticationException,
    TVDBException,
)
from libtvdb.model import Episode, Show
from libtvdb.utilities import Log


class TVDBClient:
    """The main client wrapper around the TVDB API.

    Instantiate a new one of these to use a new authentication session.
    """

    class Constants:
        """Constants that are used elsewhere in the TVDBClient class."""

        AUTH_TIMEOUT: ClassVar[float] = 3
        MAX_AUTH_RETRY_COUNT: ClassVar[int] = 3
        DEFAULT_TIMEOUT: ClassVar[float] = 10.0
        SUCCESS_STATUS_MIN: ClassVar[int] = 200
        SUCCESS_STATUS_MAX: ClassVar[int] = 300

    _BASE_API: ClassVar[str] = "https://api4.thetvdb.com/v4"

    def __init__(self, *, api_key: str, pin: str) -> None:
        """Create a new client wrapper.

        Args:
            api_key: The TVDB API key for authentication
            pin: The TVDB PIN for authentication

        Raises:
            TVDBException: If api_key or pin is None or empty
        """

        if not api_key:
            raise TVDBException("No API key was supplied")

        if not pin:
            raise TVDBException("No PIN was supplied")

        self.api_key = api_key
        self.pin = pin
        self.auth_token = None

    def _expand_url(self, path: str) -> str:
        """Take the path from a URL and expand it to the full API path.

        Args:
            path: API endpoint path (e.g., "login", "series/123")

        Returns:
            Full API URL with base path prepended
        """
        return f"{TVDBClient._BASE_API}/{path}"

    def _construct_headers(self, *, additional_headers: Any | None = None) -> dict[str, str]:
        """Construct the headers used for all requests.

        Args:
            additional_headers: Optional dict of additional headers to include

        Returns:
            Dictionary of HTTP headers for the request
        """

        headers = {"Accept": "application/json"}

        if self.auth_token is not None:
            headers["Authorization"] = f"Bearer {self.auth_token}"

        if additional_headers is None:
            return headers

        for header_name, header_value in additional_headers.items():
            headers[header_name] = header_value

        return headers

    def authenticate(self) -> None:
        """Authenticate the client with the API.

        This will exit early if already authenticated. All API calls requiring
        authentication will call this method automatically.

        Raises:
            TVDBAuthenticationException: If authentication fails or times out
        """

        if self.auth_token is not None:
            Log.debug("Already authenticated, skipping")
            return

        Log.info("Authenticating...")

        login_body = {
            "apikey": self.api_key,
            "pin": self.pin,
        }

        for i in range(TVDBClient.Constants.MAX_AUTH_RETRY_COUNT):
            try:
                response = requests.post(
                    self._expand_url("login"),
                    json=login_body,
                    headers=self._construct_headers(),
                    timeout=TVDBClient.Constants.AUTH_TIMEOUT,
                )

                # Since we authenticated successfully, we can break out of the
                # retry loop
                break
            except requests.exceptions.Timeout as ex:
                will_retry = i < (TVDBClient.Constants.MAX_AUTH_RETRY_COUNT - 1)
                if will_retry:
                    Log.warning("Authentication timed out, but will retry.")
                else:
                    Log.error("Authentication timed out maximum number of times.")
                    raise TVDBAuthenticationException(
                        "Authentication timed out maximum number of times."
                    ) from ex

        if not (
            TVDBClient.Constants.SUCCESS_STATUS_MIN
            <= response.status_code
            < TVDBClient.Constants.SUCCESS_STATUS_MAX
        ):
            Log.error(f"Authentication failed with status code: {response.status_code}")
            raise TVDBAuthenticationException(
                f"Authentication failed with status code: {response.status_code}"
            )

        content = response.json()
        token = content.get("data", {}).get("token")

        if token is None:
            Log.error("Failed to get token from login request")
            raise TVDBAuthenticationException("Failed to get token from login request")

        self.auth_token = token

        Log.info("Authenticated successfully")

    def get(self, url_path: str, *, timeout: float) -> Any:
        """Execute a GET request to the TVDB API.

        Args:
            url_path: The API endpoint path
            timeout: Request timeout in seconds

        Returns:
            The data from the API response

        Raises:
            ValueError: If url_path is invalid
            NotFoundException: If the resource is not found
            TVDBException: For other API errors
        """

        if not url_path:
            raise ValueError("An invalid URL path was supplied")

        self.authenticate()

        Log.info(f"GET: {url_path}")

        response = requests.get(
            self._expand_url(url_path),
            headers=self._construct_headers(),
            timeout=timeout,
        )

        TVDBClient._check_errors(response)

        content = response.json()

        data = content.get("data")

        if data is None:
            raise NotFoundException(f"Could not get data for path: {url_path}")

        return data

    def get_paged(self, url_path: str, *, timeout: float, key: str | None = None) -> list[Any]:
        """Execute a GET request for paginated data.

        Args:
            url_path: The API endpoint path
            timeout: Request timeout in seconds
            key: Optional key to extract from each page's data

        Returns:
            Combined list of all paginated results

        Raises:
            ValueError: If url_path is invalid
            NotFoundException: If the resource is not found
            TVDBException: For other API errors
        """

        if not url_path:
            raise ValueError("An invalid URL path was supplied")

        self.authenticate()

        url_path = self._expand_url(url_path)

        all_results: list[Any] = []

        while True:

            Log.info(f"GET: {url_path}")

            response = requests.get(
                url_path,
                headers=self._construct_headers(),
                timeout=timeout,
            )

            TVDBClient._check_errors(response)

            content = response.json()

            data = content.get("data")

            if data is None:
                raise NotFoundException(f"Could not get data for path: {url_path}")

            if key is None:
                all_results += data
            else:
                all_results += data[key]

            links = content.get("links")

            if links is None:
                break

            if links.get("next"):
                Log.debug("Fetching next page")
                url_path = links["next"]
            else:
                break

        return all_results

    def search_show(
        self, show_name: str, *, timeout: float | None = None
    ) -> list[Show]:
        """Search for shows matching the name supplied.

        Args:
            show_name: The name of the show to search for
            timeout: Request timeout in seconds (default: 10.0)

        Returns:
            List of matching shows, empty list if no matches or invalid input
        """
        if timeout is None:
            timeout = TVDBClient.Constants.DEFAULT_TIMEOUT

        if not show_name:
            return []

        encoded_name = urllib.parse.quote(show_name)

        Log.info(f"Searching for show: {show_name}")

        shows_data = self.get(f"search?type=series&query={encoded_name}", timeout=timeout)

        shows = []

        for show_data in shows_data:
            show = deserialize.deserialize(Show, show_data, throw_on_unhandled=True)
            shows.append(show)

        return shows

    def show_info(self, show_identifier: int, *, timeout: float | None = None) -> Show | None:
        """Get the full information for the show with the given identifier.

        Args:
            show_identifier: The TVDB ID of the show
            timeout: Request timeout in seconds (default: 10.0)

        Returns:
            Show object with detailed information

        Raises:
            NotFoundException: If the show is not found
            TVDBException: For other API errors
        """
        if timeout is None:
            timeout = TVDBClient.Constants.DEFAULT_TIMEOUT

        Log.info(f"Fetching data for show: {show_identifier}")

        show_data = self.get(f"series/{show_identifier}/extended", timeout=timeout)

        return deserialize.deserialize(Show, show_data, throw_on_unhandled=True)

    def episodes_from_show_id(
        self, show_identifier: int | str, timeout: float | None = None
    ) -> list[Episode]:
        """Get the episodes in the given show.

        Args:
            show_identifier: The TVDB ID of the show
            timeout: Request timeout in seconds (default: 10.0)

        Returns:
            List of episodes for the show

        Raises:
            NotFoundException: If the show is not found
            TVDBException: For other API errors
        """
        if timeout is None:
            timeout = TVDBClient.Constants.DEFAULT_TIMEOUT

        Log.info(f"Fetching episodes for show id: {show_identifier}")

        episode_data = self.get_paged(
            f"series/{show_identifier}/episodes/default",
            timeout=timeout,
            key="episodes",
        )

        episodes: list[Episode] = []

        for episode_data_item in episode_data:
            episodes.append(
                deserialize.deserialize(Episode, episode_data_item, throw_on_unhandled=True)
            )

        return episodes

    def episodes_from_show(self, show: Show, timeout: float | None = None) -> list[Episode]:
        """Get the episodes in the given show.

        Args:
            show: The Show object
            timeout: Request timeout in seconds (default: 10.0)

        Returns:
            List of episodes for the show

        Raises:
            ValueError: If the show does not have a tvdb_id
            NotFoundException: If the show is not found
            TVDBException: For other API errors
        """
        if show.tvdb_id is None:
            raise ValueError("Show must have a tvdb_id")
        return self.episodes_from_show_id(show.tvdb_id, timeout=timeout)

    def episode_by_id(self, episode_identifier: int, timeout: float | None = None) -> Episode:
        """Get the episode information from its ID.

        Args:
            episode_identifier: The TVDB ID of the episode
            timeout: Request timeout in seconds (default: 10.0)

        Returns:
            Episode object with detailed information

        Raises:
            NotFoundException: If the episode is not found
            TVDBException: For other API errors
        """
        if timeout is None:
            timeout = TVDBClient.Constants.DEFAULT_TIMEOUT

        Log.info(f"Fetching info for episode id: {episode_identifier}")

        episode_data = self.get(f"episodes/{episode_identifier}/extended", timeout=timeout)

        return deserialize.deserialize(Episode, episode_data, throw_on_unhandled=True)

    @staticmethod
    def _check_errors(response: requests.Response) -> None:
        """Check an API response for errors.

        Args:
            response: The requests Response object

        Raises:
            NotFoundException: If the resource is not found
            TVDBException: For other API errors
        """

        if (
            TVDBClient.Constants.SUCCESS_STATUS_MIN
            <= response.status_code
            < TVDBClient.Constants.SUCCESS_STATUS_MAX
        ):
            return

        Log.error(f"Bad response code from API: {response.status_code}")

        # Try and read the JSON. If we don't have it, we return the generic
        # exception type
        try:
            data = response.json()
        except json.JSONDecodeError as ex:
            raise TVDBException(f"Could not decode error response: {response.text}") from ex

        # Try and get the error message so we can use it
        error = data.get("Error")

        # If we don't have it, just return the generic exception type
        if error is None:
            raise TVDBException(f"Could not get error information: {response.text}")

        if error == "Resource not found":
            raise NotFoundException(f"Could not find resource: {response.url}")

        raise TVDBException(f"Unknown error: {response.text}")
