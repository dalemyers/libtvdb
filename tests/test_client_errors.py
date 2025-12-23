"""Tests for client error handling and edge cases."""

import json
from unittest.mock import Mock, patch

import pytest
import requests

from libtvdb import TVDBClient
from libtvdb.exceptions import NotFoundException, TVDBAuthenticationException, TVDBException
from libtvdb.model import Show
from libtvdb.utilities import Log


def test_client_missing_api_key():
    """Test that client raises exception when API key is missing."""
    with pytest.raises(TVDBException, match="No API key"):
        TVDBClient(api_key=None, pin="test_pin")


def test_client_missing_pin():
    """Test that client raises exception when PIN is missing."""
    with pytest.raises(TVDBException, match="No PIN"):
        TVDBClient(api_key="test_key", pin=None)


def test_construct_headers_with_additional():
    """Test header construction with additional headers."""
    client = TVDBClient(api_key="test_key", pin="test_pin")
    client.auth_token = "test_token"

    # pylint: disable=protected-access
    headers = client._construct_headers(additional_headers={"X-Custom": "value"})
    # pylint: enable=protected-access

    assert headers["Accept"] == "application/json"
    assert headers["Authorization"] == "Bearer test_token"
    assert headers["X-Custom"] == "value"


@patch("requests.post")
def test_authentication_timeout_retry(mock_post):
    """Test authentication timeout with retry."""
    client = TVDBClient(api_key="test_key", pin="test_pin")

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"token": "test_token"}}

    mock_post.side_effect = [requests.exceptions.Timeout("Timeout"), mock_response]

    client.authenticate()

    assert client.auth_token == "test_token"
    assert mock_post.call_count == 2


@patch("requests.post")
def test_authentication_timeout_max_retries(mock_post):
    """Test authentication fails after max retries."""
    client = TVDBClient(api_key="test_key", pin="test_pin")
    mock_post.side_effect = requests.exceptions.Timeout("Timeout")

    with pytest.raises(TVDBAuthenticationException, match="timed out maximum number of times"):
        client.authenticate()


@patch("requests.post")
def test_authentication_bad_status_code(mock_post):
    """Test authentication with bad status code."""
    client = TVDBClient(api_key="test_key", pin="test_pin")
    mock_response = Mock()
    mock_response.status_code = 401
    mock_post.return_value = mock_response

    with pytest.raises(TVDBAuthenticationException, match="401"):
        client.authenticate()


@patch("requests.post")
def test_authentication_no_token_in_response(mock_post):
    """Test authentication when token is missing from response."""
    client = TVDBClient(api_key="test_key", pin="test_pin")
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {}}
    mock_post.return_value = mock_response

    with pytest.raises(TVDBAuthenticationException, match="Failed to get token"):
        client.authenticate()


@patch("requests.get")
def test_get_paginated_no_data(mock_get):
    """Test get method when data is None."""
    client = TVDBClient(api_key="test_key", pin="test_pin")
    client.auth_token = "test_token"
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": None}
    mock_get.return_value = mock_response

    with pytest.raises(NotFoundException, match="Could not get data"):
        client.get("/test", timeout=10)


@patch("requests.get")
def test_get_paginated_no_links(mock_get):
    """Test get method with no pagination links."""
    client = TVDBClient(api_key="test_key", pin="test_pin")
    client.auth_token = "test_token"
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"id": 1}], "links": None}
    mock_get.return_value = mock_response

    result = client.get("/test", timeout=10)
    assert result == [{"id": 1}]


@patch("requests.get")
def test_get_paginated_with_next(mock_get):
    """Test get_paged method with pagination."""
    client = TVDBClient(api_key="test_key", pin="test_pin")
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

    mock_get.side_effect = [mock_response1, mock_response2]

    result = client.get_paged("/test", timeout=10)
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 2


def test_check_errors_bad_status_code():
    """Test _check_errors with bad status code and JSON error."""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.json.return_value = {"Error": "Server error"}
    mock_response.text = "Server error"

    with pytest.raises(TVDBException, match="Unknown error"):
        TVDBClient._check_errors(mock_response)  # pylint: disable=protected-access


def test_check_errors_not_found():
    """Test _check_errors with Resource not found error."""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.json.return_value = {"Error": "Resource not found"}
    mock_response.url = "https://api.thetvdb.com/test"

    with pytest.raises(NotFoundException, match="Could not find resource"):
        TVDBClient._check_errors(mock_response)  # pylint: disable=protected-access


def test_check_errors_json_decode_error():
    """Test _check_errors when JSON decoding fails."""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.json.side_effect = json.JSONDecodeError("error", "doc", 0)
    mock_response.text = "Invalid JSON"

    with pytest.raises(TVDBException, match="Could not decode error response"):
        TVDBClient._check_errors(mock_response)  # pylint: disable=protected-access


def test_check_errors_no_error_field():
    """Test _check_errors when Error field is missing."""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.json.return_value = {"status": "error"}
    mock_response.text = "No error field"

    with pytest.raises(TVDBException, match="Could not get error information"):
        TVDBClient._check_errors(mock_response)  # pylint: disable=protected-access


def test_log_methods():
    """Test all log methods."""
    with patch("libtvdb.utilities.logger") as mock_logger:
        Log.info("info message")
        Log.debug("debug message")
        Log.warning("warning message")
        Log.error("error message")

        mock_logger.info.assert_called_once_with("info message")
        mock_logger.debug.assert_called_once_with("debug message")
        mock_logger.warning.assert_called_once_with("warning message")
        mock_logger.error.assert_called_once_with("error message")


def test_get_invalid_url_path_none():
    """Test get method with None URL path."""
    client = TVDBClient(api_key="test_key", pin="test_pin")
    client.auth_token = "test_token"

    with pytest.raises(AttributeError, match="invalid URL path"):
        client.get(None, timeout=10)


def test_get_invalid_url_path_empty():
    """Test get method with empty URL path."""
    client = TVDBClient(api_key="test_key", pin="test_pin")
    client.auth_token = "test_token"

    with pytest.raises(AttributeError, match="invalid URL path"):
        client.get("", timeout=10)


def test_get_paged_invalid_url_path_none():
    """Test get_paged method with None URL path."""
    client = TVDBClient(api_key="test_key", pin="test_pin")
    client.auth_token = "test_token"

    with pytest.raises(AttributeError, match="invalid URL path"):
        client.get_paged(None, timeout=10)


def test_get_paged_invalid_url_path_empty():
    """Test get_paged method with empty URL path."""
    client = TVDBClient(api_key="test_key", pin="test_pin")
    client.auth_token = "test_token"

    with pytest.raises(AttributeError, match="invalid URL path"):
        client.get_paged("", timeout=10)


@patch("requests.get")
def test_get_paged_no_data(mock_get):
    """Test get_paged method when data is None."""
    client = TVDBClient(api_key="test_key", pin="test_pin")
    client.auth_token = "test_token"
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": None}
    mock_get.return_value = mock_response

    with pytest.raises(NotFoundException, match="Could not get data"):
        client.get_paged("/test", timeout=10)


def test_episodes_from_show_no_tvdb_id():
    """Test episodes_from_show with None tvdb_id."""
    client = TVDBClient(api_key="test_key", pin="test_pin")
    client.auth_token = "test_token"
    show = Show()
    show.tvdb_id = None

    with pytest.raises(ValueError, match="must have a tvdb_id"):
        client.episodes_from_show(show)


@patch("requests.get")
def test_get_paged_no_links(mock_get):
    """Test get_paged method with no pagination links."""
    client = TVDBClient(api_key="test_key", pin="test_pin")
    client.auth_token = "test_token"
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"id": 1}], "links": None}
    mock_get.return_value = mock_response

    result = client.get_paged("/test", timeout=10)
    assert len(result) == 1
    assert result[0]["id"] == 1
