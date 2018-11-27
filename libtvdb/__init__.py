"""libtvdb is a wrapper around the TVDB API (https://api.thetvdb.com/swagger).
"""

import json
from typing import Any, ClassVar, Dict, List, Optional
import urllib.parse

import keyper
import requests

from libtvdb.exceptions import TVDBException, ShowNotFoundException
from libtvdb import types
from libtvdb.utilities import Log


class TVDBClient:
    """The main client wrapper around the TVDB API.

    Instantiate a new one of these to use a new authentication session.
    """

    class Constants:
        """Constants that are used elsewhere in the TVDBClient class."""
        AUTH_TIMEOUT: ClassVar[float] = 3
        MAX_AUTH_RETRY_COUNT: ClassVar[int] = 3

    _BASE_API: ClassVar[str] = "https://api.thetvdb.com"

    def __init__(self, *, api_key: Optional[str] = None, user_key: Optional[str] = None, user_name: Optional[str] = None) -> None:
        """Create a new client wrapper.

        If any of the supplied parameters are None, they will be loaded from the
        keychain if possible. If not possible, an exception will be thrown.
        """

        if api_key is None:
            api_key = keyper.get_password(label="libtvdb_api_key")

        if api_key is None:
            raise Exception("No API key was supplied or could be found in the keychain")

        if user_key is None:
            user_key = keyper.get_password(label="libtvdb_user_key")

        if user_key is None:
            raise Exception("No user key was supplied or could be found in the keychain")

        if user_name is None:
            user_name = keyper.get_password(label="libtvdb_user_name")

        if user_name is None:
            raise Exception("No user name was supplied or could be found in the keychain")

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

        if self.auth_token is not None:
            headers["Authorization"] = f"Bearer {self.auth_token}"

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

    def search_show(self, show_name: str) -> List[types.Show]:
        """Search for shows matching the name supplied.

        If no matching show is found, a ShowNotFoundException will be thrown.
        """

        if show_name is None or show_name == "":
            return []

        self.authenticate()

        Log.info(f"Searching for show: {show_name}")

        encoded_name = urllib.parse.quote(show_name)

        response = requests.get(
            self._expand_url(f"search/series?name={encoded_name}"),
            headers=self._construct_headers()
        )

        if response.status_code < 200 or response.status_code >= 300:
            # Try and read the JSON. If we don't have it, we return the generic
            # exception type
            try:
                data = response.json()
            except json.JSONDecodeError:
                raise TVDBException(f"Could not find show: {response.text}")

            # Try and get the error message so we can use it
            error = data.get('Error')

            # If we don't have it, just return the generic exception type
            if error is None:
                raise TVDBException(f"Could not find show: {response.text}")

            if error == "Resource not found":
                raise ShowNotFoundException(f"Could not find show: {show_name}")
            else:
                raise TVDBException(f"Could not find show: {response.text}")

        content = response.json()

        shows_data = content.get('data')

        if shows_data is None:
            raise ShowNotFoundException(f"Could not find show: {show_name}")

        shows = []

        for show_data in shows_data:
            show = types.Show.from_json(show_data)
            shows.append(show)

        return shows


    def show_info(self, show_identifier: int) -> Optional[types.Show]:
        """Get the full information for the show with the given identifier.
        """

        self.authenticate()

        Log.info(f"Fetching data for show: {show_identifier}")

        response = requests.get(
            self._expand_url(f"series/{show_identifier}"),
            headers=self._construct_headers()
        )

        if response.status_code < 200 or response.status_code >= 300:
            # Try and read the JSON. If we don't have it, we return the generic
            # exception type
            try:
                data = response.json()
            except json.JSONDecodeError:
                raise TVDBException(f"Could not find show: {response.text}")

            # Try and get the error message so we can use it
            error = data.get('Error')

            # If we don't have it, just return the generic exception type
            if error is None:
                raise TVDBException(f"Could not find show: {response.text}")

            if error == "Resource not found":
                raise ShowNotFoundException(f"Could not find show with ID: {show_identifier}")
            else:
                raise TVDBException(f"Could not find show: {response.text}")

        content = response.json()

        show_data = content.get('data')

        if show_data is None:
            raise ShowNotFoundException(f"Could not find show with ID: {show_identifier}")

        return types.Show.from_json(show_data)
