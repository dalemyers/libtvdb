"""Shared context information for all tests."""

import os
import sys

import dotenv
import pytest

try:
    import keyper
except (ImportError, Exception):  # pylint: disable=broad-exception-caught
    keyper = None
    dotenv.load_dotenv()


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# pylint: disable=wrong-import-position
import libtvdb

# pylint: enable=wrong-import-position


def _read_secret(secret_name: str) -> str | None:
    """Read a secret from environment or keychain."""
    if secret := os.environ.get(secret_name):
        return secret

    if keyper is not None:
        try:
            keychain_value = keyper.get_password(label=secret_name.lower())
            if keychain_value is not None:
                return str(keychain_value)
        except Exception:  # pylint: disable=broad-exception-caught
            pass

    return os.environ.get(secret_name.upper())


@pytest.fixture(scope="session")
def tvdb_client() -> libtvdb.TVDBClient:
    """Fixture that provides a TVDB client for tests."""
    api_key = _read_secret("libtvdb_api_key")
    pin = _read_secret("libtvdb_pin")

    if api_key is None:
        raise Exception("Failed to get API Key")

    if pin is None:
        raise Exception("Failed to get PIN")

    return libtvdb.TVDBClient(api_key=api_key, pin=pin)
