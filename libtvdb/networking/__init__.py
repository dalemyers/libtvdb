"""Networking utilities."""

from typing import List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from libtvdb.utilities import Log

MAX_RETRIES = 2
BACKOFF_FACTOR = 0
RETRY_STATUS_CODES = [500, 502, 504]

_SHARED_SESSION: Optional[requests.Session] = None


class HTTPTimeoutAdapter(requests.adapters.HTTPAdapter):
    """An override to HTTPAdapter which allows setting the default timeout for requests."""

    def __init__(self, *args, timeout: float = 5.0, **kwargs) -> None:
        self.timeout = timeout
        super().__init__(*args, **kwargs)

    #pylint: disable=arguments-differ
    def send(self, *args, **kwargs) -> requests.Response:
        """Send a request."""
        if 'timeout' not in kwargs.keys():
            kwargs['timeout'] = self.timeout
        Log.info("Sending request")
        return super().send(*args, **kwargs)
    #pylint: enable=arguments-differ

def requests_retry_session():
    """Create a session with retry functionality built in."""

    #pylint: disable=global-statement
    global _SHARED_SESSION
    #pylint: enable=global-statement

    if _SHARED_SESSION is not None:
        return _SHARED_SESSION

    session = requests.Session()

    retry = Retry(
        total=MAX_RETRIES,
        read=MAX_RETRIES,
        connect=MAX_RETRIES,
        backoff_factor=BACKOFF_FACTOR,
        status_forcelist=tuple(RETRY_STATUS_CODES),
    )

    adapter = HTTPTimeoutAdapter(max_retries=retry)

    session.mount('http://', adapter)
    session.mount('https://', adapter)

    _SHARED_SESSION = session

    return session
