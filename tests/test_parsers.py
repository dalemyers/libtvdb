"""Tests for parser functions and edge cases."""

import datetime

import pytest

from libtvdb.model.parsers import (
    date_parser,
    datetime_parser,
    optional_empty_str,
    optional_float,
    timestamp_parser,
)
from libtvdb.model.show import translated_name_parser
from libtvdb.utilities import parse_date, parse_datetime


def test_parse_datetime_none():
    """Test parse_datetime with None input."""
    with pytest.raises(ValueError, match="should not be None"):
        parse_datetime(None)


def test_parse_datetime_empty():
    """Test parse_datetime with empty string."""
    with pytest.raises(ValueError, match="should not be empty"):
        parse_datetime("")


def test_parse_datetime_invalid():
    """Test parse_datetime with invalid date."""
    with pytest.raises(ValueError, match="Invalid date time"):
        parse_datetime("0000-00-00 00:00:00")


def test_parse_date_valid():
    """Test parse_date with valid input."""
    result = parse_date("2020-01-15")
    assert result == datetime.date(2020, 1, 15)


def test_parse_datetime_valid():
    """Test parse_datetime with valid input."""
    result = parse_datetime("2020-01-15 10:30:45")
    assert result == datetime.datetime(2020, 1, 15, 10, 30, 45)


def test_parser_date_empty_string():
    """Test date_parser with empty string."""
    assert date_parser("") is None


def test_parser_date_invalid_format():
    """Test date_parser with invalid format."""
    assert date_parser("0000-00-00") is None


def test_parser_datetime_empty_string():
    """Test datetime_parser with empty string."""
    assert datetime_parser("") is None


def test_parser_datetime_invalid_format():
    """Test datetime_parser with invalid format."""
    assert datetime_parser("0000-00-00 00:00:00") is None


def test_parser_timestamp_none():
    """Test timestamp_parser with None."""
    assert timestamp_parser(None) is None


def test_parser_timestamp_valid():
    """Test timestamp_parser with valid timestamp."""
    result = timestamp_parser(1609459200)
    assert isinstance(result, datetime.datetime)


def test_parser_optional_float_none():
    """Test optional_float with None."""
    assert optional_float(None) is None


def test_parser_optional_float_valid():
    """Test optional_float with valid int."""
    assert optional_float(42) == 42.0


def test_parser_optional_empty_str_none():
    """Test optional_empty_str with None."""
    assert optional_empty_str(None) is None


def test_parser_optional_empty_str_empty():
    """Test optional_empty_str with empty string."""
    assert optional_empty_str("") is None


def test_parser_optional_empty_str_valid():
    """Test optional_empty_str with valid string."""
    assert optional_empty_str("test") == "test"


def test_translated_name_parser_none():
    """Test translated_name_parser with None."""
    assert translated_name_parser(None) == {}


def test_translated_name_parser_empty():
    """Test translated_name_parser with empty string."""
    assert translated_name_parser("") == {}


def test_translated_name_parser_valid_json():
    """Test translated_name_parser with valid JSON."""
    result = translated_name_parser('{"eng": "English Name"}')
    assert result == {"eng": "English Name"}


def test_translated_name_parser_invalid_json():
    """Test translated_name_parser with invalid JSON."""
    assert translated_name_parser("{invalid json") == {}


def test_translated_name_parser_non_dict():
    """Test translated_name_parser when JSON is not a dict."""
    assert translated_name_parser('["not", "a", "dict"]') == {}
