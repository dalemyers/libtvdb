"""Tests for async client error handling and edge cases."""

import json
from unittest.mock import AsyncMock, Mock, patch

import httpx
import pytest

from libtvdb import AsyncTVDBClient
from libtvdb.exceptions import NotFoundException, TVDBAuthenticationException, TVDBException
from libtvdb.model import Show


def test_async_client_missing_api_key():
    """Test that async client raises exception when API key is missing."""
    with pytest.raises(TVDBException, match="No API key"):
        AsyncTVDBClient(api_key=None, pin="test_pin")


def test_async_client_missing_pin():
    """Test that async client raises exception when PIN is missing."""
    # PIN is optional, so this should not raise an exception
    client = AsyncTVDBClient(api_key="test_key", pin=None)
    assert client.pin is None


def test_async_construct_headers_with_additional():
    """Test async header construction with additional headers."""
    client = AsyncTVDBClient(api_key="test_key", pin="test_pin")
    client.auth_token = "test_token"

    # pylint: disable=protected-access
    headers = client._construct_headers(additional_headers={"X-Custom": "value"})
    # pylint: enable=protected-access

    assert headers["Accept"] == "application/json"
    assert headers["Authorization"] == "Bearer test_token"
    assert headers["X-Custom"] == "value"


@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_async_authentication_timeout_retry(mock_client_class):
    """Test async authentication timeout with retry."""
    client = AsyncTVDBClient(api_key="test_key", pin="test_pin")

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"token": "test_token"}}

    mock_client = AsyncMock()
    mock_client.post = AsyncMock(side_effect=[httpx.TimeoutException("Timeout"), mock_response])

    mock_client_class.return_value.__aenter__.return_value = mock_client

    await client.authenticate()

    assert client.auth_token == "test_token"
    assert mock_client.post.call_count == 2


@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_async_authentication_timeout_max_retries(mock_client_class):
    """Test async authentication fails after max retries."""
    client = AsyncTVDBClient(api_key="test_key", pin="test_pin")

    mock_client = AsyncMock()
    mock_client.post = AsyncMock(side_effect=httpx.TimeoutException("Timeout"))

    mock_client_class.return_value.__aenter__.return_value = mock_client

    with pytest.raises(TVDBAuthenticationException, match="timed out maximum number of times"):
        await client.authenticate()


@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_async_authentication_bad_status_code(mock_client_class):
    """Test async authentication with bad status code."""
    client = AsyncTVDBClient(api_key="test_key", pin="test_pin")

    mock_response = Mock()
    mock_response.status_code = 401

    mock_client = AsyncMock()
    mock_client.post = AsyncMock(return_value=mock_response)

    mock_client_class.return_value.__aenter__.return_value = mock_client

    with pytest.raises(TVDBAuthenticationException, match="401"):
        await client.authenticate()


@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_async_authentication_no_token_in_response(mock_client_class):
    """Test async authentication when token is missing from response."""
    client = AsyncTVDBClient(api_key="test_key", pin="test_pin")

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {}}

    mock_client = AsyncMock()
    mock_client.post = AsyncMock(return_value=mock_response)

    mock_client_class.return_value.__aenter__.return_value = mock_client

    with pytest.raises(TVDBAuthenticationException, match="Failed to get token"):
        await client.authenticate()


@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_async_get_no_data(mock_client_class):
    """Test async get method when data is None."""
    client = AsyncTVDBClient(api_key="test_key", pin="test_pin")
    client.auth_token = "test_token"

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": None}

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)

    mock_client_class.return_value.__aenter__.return_value = mock_client

    with pytest.raises(NotFoundException, match="Could not get data"):
        await client.get("/test", timeout=10)


@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_async_get_paged_no_data(mock_client_class):
    """Test async get_paged method when data is None."""
    client = AsyncTVDBClient(api_key="test_key", pin="test_pin")
    client.auth_token = "test_token"

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": None}

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)

    mock_client_class.return_value.__aenter__.return_value = mock_client

    with pytest.raises(NotFoundException, match="Could not get data"):
        await client.get_paged("/test", timeout=10)


@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_async_get_paged_no_links(mock_client_class):
    """Test async get_paged method with no pagination links."""
    client = AsyncTVDBClient(api_key="test_key", pin="test_pin")
    client.auth_token = "test_token"

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"id": 1}], "links": None}

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)

    mock_client_class.return_value.__aenter__.return_value = mock_client

    result = await client.get_paged("/test", timeout=10)
    assert len(result) == 1
    assert result[0]["id"] == 1


@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_async_get_paged_with_next(mock_client_class):
    """Test async get_paged method with pagination."""
    client = AsyncTVDBClient(api_key="test_key", pin="test_pin")
    client.auth_token = "test_token"

    mock_response1 = Mock()
    mock_response1.status_code = 200
    mock_response1.json.return_value = {
        "data": [{"id": 1}],
        "links": {"next": "https://api.thetvdb.com/test?page=2"},
    }

    mock_response2 = Mock()
    mock_response2.status_code = 200
    mock_response2.json.return_value = {"data": [{"id": 2}], "links": {"next": None}}

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(side_effect=[mock_response1, mock_response2])

    mock_client_class.return_value.__aenter__.return_value = mock_client

    result = await client.get_paged("/test", timeout=10)
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 2


@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_async_get_paged_with_key(mock_client_class):
    """Test async get_paged method with key parameter."""
    client = AsyncTVDBClient(api_key="test_key", pin="test_pin")
    client.auth_token = "test_token"

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": {"episodes": [{"id": 1}, {"id": 2}]},
        "links": None,
    }

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)

    mock_client_class.return_value.__aenter__.return_value = mock_client

    result = await client.get_paged("/test", timeout=10, key="episodes")
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 2


def test_async_check_errors_bad_status_code():
    """Test async _check_errors with bad status code and JSON error."""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.json.return_value = {"Error": "Server error"}
    mock_response.text = "Server error"

    with pytest.raises(TVDBException, match="Unknown error"):
        AsyncTVDBClient._check_errors(mock_response)  # pylint: disable=protected-access


def test_async_check_errors_not_found():
    """Test async _check_errors with Resource not found error."""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.json.return_value = {"Error": "Resource not found"}
    mock_response.url = "https://api.thetvdb.com/test"

    with pytest.raises(NotFoundException, match="Could not find resource"):
        AsyncTVDBClient._check_errors(mock_response)  # pylint: disable=protected-access


def test_async_check_errors_json_decode_error():
    """Test async _check_errors when JSON decoding fails."""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.json.side_effect = json.JSONDecodeError("error", "doc", 0)
    mock_response.text = "Invalid JSON"

    with pytest.raises(TVDBException, match="Could not decode error response"):
        AsyncTVDBClient._check_errors(mock_response)  # pylint: disable=protected-access


def test_async_check_errors_no_error_field():
    """Test async _check_errors when Error field is missing."""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.json.return_value = {"status": "error"}
    mock_response.text = "No error field"

    with pytest.raises(TVDBException, match="Could not get error information"):
        AsyncTVDBClient._check_errors(mock_response)  # pylint: disable=protected-access


@pytest.mark.asyncio
async def test_async_get_invalid_url_path_none():
    """Test async get method with None URL path."""
    client = AsyncTVDBClient(api_key="test_key", pin="test_pin")
    client.auth_token = "test_token"

    with pytest.raises(ValueError, match="invalid URL path"):
        await client.get(None, timeout=10)


@pytest.mark.asyncio
async def test_async_get_invalid_url_path_empty():
    """Test async get method with empty URL path."""
    client = AsyncTVDBClient(api_key="test_key", pin="test_pin")
    client.auth_token = "test_token"

    with pytest.raises(ValueError, match="invalid URL path"):
        await client.get("", timeout=10)


@pytest.mark.asyncio
async def test_async_get_paged_invalid_url_path_none():
    """Test async get_paged method with None URL path."""
    client = AsyncTVDBClient(api_key="test_key", pin="test_pin")
    client.auth_token = "test_token"

    with pytest.raises(ValueError, match="invalid URL path"):
        await client.get_paged(None, timeout=10)


@pytest.mark.asyncio
async def test_async_get_paged_invalid_url_path_empty():
    """Test async get_paged method with empty URL path."""
    client = AsyncTVDBClient(api_key="test_key", pin="test_pin")
    client.auth_token = "test_token"

    with pytest.raises(ValueError, match="invalid URL path"):
        await client.get_paged("", timeout=10)


@pytest.mark.asyncio
async def test_async_episodes_from_show_no_tvdb_id():
    """Test async episodes_from_show with None tvdb_id."""
    client = AsyncTVDBClient(api_key="test_key", pin="test_pin")
    client.auth_token = "test_token"
    show = Show()
    show.tvdb_id = None

    with pytest.raises(ValueError, match="must have a tvdb_id"):
        await client.episodes_from_show(show)
