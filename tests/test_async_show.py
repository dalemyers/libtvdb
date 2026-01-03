"""Test async show retrieval."""

import pytest

from libtvdb.model import StatusName


@pytest.mark.asyncio
async def test_show_info_valid(async_tvdb_client):
    """Test that we can get information about a valid show."""
    show = await async_tvdb_client.show_info(78804)

    assert show.identifier == "78804"
    assert show.name == "Doctor Who (2005)"
    assert show.status.name == StatusName.ENDED
    assert show.companies[0].name == "BBC One"
