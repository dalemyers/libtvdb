"""Tests for model properties and string representations."""

import datetime

from libtvdb.model import (
    Actor,
    Alias,
    Artwork,
    Character,
    Company,
    ContentRating,
    Episode,
    NetworkBase,
    RemoteID,
    SeasonBase,
    TagOption,
    Trailer,
)
from libtvdb.model.award import AwardBase
from libtvdb.model.company import CompanyType
from libtvdb.model.season import SeasonType
from libtvdb.model.status import Status, StatusName


def test_actor_str():
    """Test Actor __str__ method."""
    actor = Actor()
    actor.identifier = 1
    actor.name = "Test Actor"
    actor.role = "Main Character"
    assert "Test Actor" in str(actor)


def test_alias_str():
    """Test Alias __str__ method."""
    alias = Alias()
    alias.language = "eng"
    alias.name = "Test Alias"
    assert "Test Alias" in str(alias)


def test_artwork_str():
    """Test Artwork __str__ method."""
    artwork = Artwork()
    artwork.identifier = "1"
    artwork.image = "test.jpg"
    assert "1" in str(artwork)


def test_character_str():
    """Test Character __str__ method."""
    character = Character()
    character.identifier = 1
    character.name = "Test Character"
    assert "Test Character" in str(character)


def test_company_type_str():
    """Test CompanyType __str__ method."""
    company_type = CompanyType()
    company_type.company_type_id = 1
    company_type.company_type_name = "Network"
    assert "Network" in str(company_type)


def test_company_str():
    """Test Company __str__ method."""
    company_type = CompanyType()
    company_type.company_type_id = 1
    company_type.company_type_name = "Network"

    company = Company()
    company.identifier = 1
    company.name = "Test Company"
    company.slug = "test-company"
    company.company_type = company_type
    assert "Test Company" in str(company)


def test_content_rating_str():
    """Test ContentRating __str__ method."""
    rating = ContentRating()
    rating.identifier = 1
    rating.name = "PG"
    assert "PG" in str(rating)


def test_network_str():
    """Test NetworkBase __str__ method."""
    network = NetworkBase()
    network.identifier = 1
    network.name = "Test Network"
    assert "Test Network" in str(network)


def test_remote_id_str():
    """Test RemoteID __str__ method."""
    remote_id = RemoteID()
    remote_id.identifier = "tt123456"
    remote_id.source_name = "IMDB"
    assert "tt123456" in str(remote_id)


def test_season_str():
    """Test SeasonBase __str__ method."""
    season_type = SeasonType()
    season_type.identifier = 1
    season_type.name = "Regular"
    season_type.season_type = "official"

    season = SeasonBase()
    season.identifier = 1
    season.name = "Season 1"
    season.number = 1
    season.series_id = 123
    season.slug = "season-1"
    season.season_type = season_type
    assert "Season 1" in str(season)


def test_tag_option_str():
    """Test TagOption __str__ method."""
    tag = TagOption()
    tag.identifier = 1
    tag.name = "Test Tag"
    assert "Test Tag" in str(tag)


def test_trailer_str():
    """Test Trailer __str__ method."""
    trailer = Trailer()
    trailer.identifier = 1
    trailer.name = "Test Trailer"
    trailer.url = "http://test.com"
    trailer.language = "eng"
    assert "Test Trailer" in str(trailer)


def test_award_str():
    """Test AwardBase __str__ method."""
    award = AwardBase()
    award.identifier = 1
    award.name = "Test Award"
    assert "Test Award" in str(award)


def test_status_str():
    """Test Status __str__ method."""
    status = Status()
    status.identifier = 1
    status.name = StatusName.CONTINUING
    assert "CONTINUING" in str(status)


def test_episode_characters_by_role_none():
    """Test Episode.characters_by_role when characters is None."""
    episode = Episode()
    episode.identifier = 1
    episode.name = "Test"
    episode.number = 1
    episode.season_number = 1
    episode.series_id = 123
    episode.is_movie = 0
    episode.last_updated = datetime.datetime.now()
    episode.characters = None

    result = episode.characters_by_role
    assert len(result) == 0


def test_episode_characters_by_role_with_unknown():
    """Test Episode.characters_by_role with character missing people_type."""
    episode = Episode()
    episode.identifier = 1
    episode.name = "Test"
    episode.number = 1
    episode.season_number = 1
    episode.series_id = 123
    episode.is_movie = 0
    episode.last_updated = datetime.datetime.now()

    char = Character()
    char.identifier = 1
    char.name = "Test Character"
    char.people_type = None
    char.people_id = 1
    char.series_id = 123
    char.sort = 1
    char.is_featured = True

    episode.characters = [char]

    result = episode.characters_by_role
    assert "Unknown" in result
    assert len(result["Unknown"]) == 1


def test_episode_str():
    """Test Episode __str__ method."""
    episode = Episode()
    episode.identifier = 1
    episode.name = "Test Episode"
    episode.number = 1
    episode.season_number = 1
    episode.series_id = 123
    episode.is_movie = 0
    episode.last_updated = datetime.datetime.now()

    result = str(episode)
    assert "Test Episode" in result
