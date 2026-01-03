"""Test async authentication."""

import pytest

import libtvdb
from libtvdb.exceptions import TVDBAuthenticationException, TVDBException


@pytest.mark.asyncio
async def test_authenticate_valid():
    """Test that authentication works with valid credentials."""
    from tests.context import _read_secret

    api_key = _read_secret("libtvdb_api_key")
    pin = _read_secret("libtvdb_pin")

    client = libtvdb.AsyncTVDBClient(api_key=api_key, pin=pin)
    await client.authenticate()

    assert client.auth_token is not None


@pytest.mark.asyncio
async def test_authenticate_invalid():
    """Test that authentication fails with invalid credentials."""
    client = libtvdb.AsyncTVDBClient(api_key="invalid_key", pin="invalid_pin")

    with pytest.raises(TVDBAuthenticationException):
        await client.authenticate()


def test_no_api_key():
    """Test that creating a client without an API key raises an exception."""
    with pytest.raises(TVDBException):
        libtvdb.AsyncTVDBClient(api_key="")


def test_no_api_key_none():
    """Test that creating a client with None API key raises an exception."""
    with pytest.raises(TVDBException):
        libtvdb.AsyncTVDBClient(api_key=None)
