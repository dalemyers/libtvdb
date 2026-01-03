"""Test async episode retrieval."""

import pytest


@pytest.mark.asyncio
async def test_episodes_from_show_id_valid(async_tvdb_client):
    """Test retrieving episodes using a valid show ID."""
    episodes = await async_tvdb_client.episodes_from_show_id(78804)

    assert isinstance(episodes, list)
    assert len(episodes) > 0


@pytest.mark.asyncio
async def test_episodes_from_show(async_tvdb_client):
    """Test retrieving episodes from a Show object."""
    shows = await async_tvdb_client.search_show("Doctor Who")
    assert len(shows) > 0, "Failed to find any matching shows"

    # Use first show from results
    show = shows[0]
    episodes = await async_tvdb_client.episodes_from_show(show)

    assert len(episodes) > 0, "Show should have episodes"


@pytest.mark.asyncio
async def test_episode_by_id_valid(async_tvdb_client):
    """Test retrieving a specific episode by ID."""
    episode = await async_tvdb_client.episode_by_id(127396)

    assert episode.identifier == 127396
    assert episode.name is not None
