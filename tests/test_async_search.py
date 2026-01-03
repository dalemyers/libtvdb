"""Test async searching for shows."""

import datetime

import pytest

from libtvdb.model import StatusName

EXPECTED_SHOWS = [
    "The Flash",
    "Doctor Who",
    "Mythbusters",
    "Only Connect",
]

UNEXPECTED_SHOWS = [
    "149FAB6D-94C1-4E93-9722-85D02272191B",
    "kj-98hpiu3bpiub-983bi",
]


@pytest.mark.asyncio
async def test_search_expected(async_tvdb_client):
    """Test that shows we expect to be there are found and parsed as expected."""
    for show_name in EXPECTED_SHOWS:
        shows = await async_tvdb_client.search_show(show_name)
        assert isinstance(shows, list)
        assert len(shows) > 0, f"Failed to find any shows matching: {show_name}"


@pytest.mark.asyncio
async def test_search_unexpected(async_tvdb_client):
    """Test that shows we expect to not be there are not in fact there."""
    for show_name in UNEXPECTED_SHOWS:
        assert await async_tvdb_client.search_show(show_name) == []


@pytest.mark.asyncio
async def test_show_parse_result(async_tvdb_client):
    """Test that the show values are what we'd expect."""
    shows = await async_tvdb_client.search_show("Better Off Ted")
    assert len(shows) > 0, "Failed to find any matching shows"

    filtered_shows = [show for show in shows if show.tvdb_id == "84021"]
    assert len(filtered_shows) == 1, "There should only be a single matching show for an ID"

    show = filtered_shows[0]

    assert (
        show.tvdb_id == "84021"
    ), f"'{show.tvdb_id}'' was not equal to expected identifier '84021'"
    assert (
        show.name == "Better Off Ted"
    ), f"'{show.name}' was not equal to expected name 'Better Off Ted'"
    assert (
        show.slug == "better-off-ted"
    ), f"'{show.slug}' was not equal to expected sluh 'Better Off Ted'"
    assert (
        show.status == StatusName.ENDED
    ), f"'{show.status}' was not equal to expected status '{StatusName.ENDED}'"
    assert show.first_air_time == datetime.date(2009, 3, 18)
    # API now returns additional Russian alias
    expected_aliases = [
        "Better off Ted - Die Chaos AG",
        "Везунчик Тэд",
        "Mejor Ted",
    ]
    assert show.aliases == expected_aliases
    assert show.network == "ABC (US)"
    assert show.overview[:30] == "As the head of research and de"
    assert (
        show.image_url == "https://artworks.thetvdb.com/banners/posters/84021-2.jpg"
    ), f"'{show.image_url}' was not equal to expected 'https://artworks.thetvdb.com/banners/posters/84021-2.jpg'"


@pytest.mark.asyncio
async def test_search_show_empty_string(async_tvdb_client):
    """Test that searching with empty string returns empty list."""
    assert await async_tvdb_client.search_show("") == []


@pytest.mark.asyncio
async def test_search_show_none(async_tvdb_client):
    """Test that searching with None returns empty list."""
    assert await async_tvdb_client.search_show(None) == []
