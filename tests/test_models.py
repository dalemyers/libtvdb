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
    Show,
    TagOption,
    Trailer,
)
from libtvdb.model.award import AwardBase
from libtvdb.model.company import CompanyType
from libtvdb.model.season import SeasonType
from libtvdb.model.show import Genre
from libtvdb.model.status import Status, StatusName


def test_actor_str():
    """Test Actor __str__ method."""
    actor = Actor()
    actor.identifier = 1
    actor.name = "Test Actor"
    actor.role = "Main Character"
    assert "Test Actor" in str(actor)


def test_actor_repr():
    """Test Actor __repr__ method."""
    actor = Actor()
    actor.identifier = 1
    actor.name = "Test Actor"
    actor.role = "Main Character"
    result = repr(actor)
    assert "Actor<" in result
    assert "Test Actor" in result


def test_actor_eq():
    """Test Actor __eq__ method."""
    actor1 = Actor()
    actor1.identifier = 1
    actor1.name = "Test Actor"

    actor2 = Actor()
    actor2.identifier = 1
    actor2.name = "Other Name"

    actor3 = Actor()
    actor3.identifier = 2
    actor3.name = "Test Actor"

    assert actor1 == actor2
    assert actor1 != actor3
    assert actor1 != "not an actor"


def test_actor_hash():
    """Test Actor __hash__ method."""
    actor1 = Actor()
    actor1.identifier = 1
    actor1.name = "Test Actor"

    actor2 = Actor()
    actor2.identifier = 1
    actor2.name = "Other Name"

    assert hash(actor1) == hash(actor2)


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


def test_artwork_repr():
    """Test Artwork __repr__ method."""
    artwork = Artwork()
    artwork.identifier = "1"
    artwork.image = "test.jpg"
    artwork.width = 1920
    artwork.height = 1080
    artwork.artwork_type = 1
    result = repr(artwork)
    assert "Artwork<" in result
    assert "1920x1080" in result


def test_artwork_eq():
    """Test Artwork __eq__ method."""
    artwork1 = Artwork()
    artwork1.identifier = "1"

    artwork2 = Artwork()
    artwork2.identifier = "1"

    artwork3 = Artwork()
    artwork3.identifier = "2"

    assert artwork1 == artwork2
    assert artwork1 != artwork3
    assert artwork1 != "not artwork"


def test_artwork_hash():
    """Test Artwork __hash__ method."""
    artwork1 = Artwork()
    artwork1.identifier = "1"

    artwork2 = Artwork()
    artwork2.identifier = "1"

    assert hash(artwork1) == hash(artwork2)


def test_character_str():
    """Test Character __str__ method."""
    character = Character()
    character.identifier = 1
    character.name = "Test Character"
    assert "Test Character" in str(character)


def test_character_repr():
    """Test Character __repr__ method."""
    character = Character()
    character.identifier = 1
    character.name = "Test Character"
    character.people_id = 123
    result = repr(character)
    assert "Character<" in result
    assert "people_id=123" in result


def test_character_eq():
    """Test Character __eq__ method."""
    char1 = Character()
    char1.identifier = 1

    char2 = Character()
    char2.identifier = 1

    char3 = Character()
    char3.identifier = 2

    assert char1 == char2
    assert char1 != char3
    assert char1 != "not a character"


def test_character_hash():
    """Test Character __hash__ method."""
    char1 = Character()
    char1.identifier = 1

    char2 = Character()
    char2.identifier = 1

    assert hash(char1) == hash(char2)


def test_company_type_str():
    """Test CompanyType __str__ method."""
    company_type = CompanyType()
    company_type.company_type_id = 1
    company_type.company_type_name = "Network"
    assert "Network" in str(company_type)


def test_company_type_repr():
    """Test CompanyType __repr__ method."""
    company_type = CompanyType()
    company_type.company_type_id = 1
    company_type.company_type_name = "Network"
    result = repr(company_type)
    assert "CompanyType<" in result
    assert "Network" in result


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


def test_company_repr():
    """Test Company __repr__ method."""
    company_type = CompanyType()
    company_type.company_type_id = 1
    company_type.company_type_name = "Network"

    company = Company()
    company.identifier = 1
    company.name = "Test Company"
    company.slug = "test-company"
    company.company_type = company_type
    result = repr(company)
    assert "Company<" in result
    assert "test-company" in result


def test_company_eq():
    """Test Company __eq__ method."""
    company1 = Company()
    company1.identifier = 1

    company2 = Company()
    company2.identifier = 1

    company3 = Company()
    company3.identifier = 2

    assert company1 == company2
    assert company1 != company3
    assert company1 != "not a company"


def test_company_hash():
    """Test Company __hash__ method."""
    company1 = Company()
    company1.identifier = 1

    company2 = Company()
    company2.identifier = 1

    assert hash(company1) == hash(company2)


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


def test_season_repr():
    """Test SeasonBase __repr__ method."""
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
    result = repr(season)
    assert "SeasonBase<" in result
    assert "S01" in result


def test_season_eq():
    """Test SeasonBase __eq__ method."""
    season1 = SeasonBase()
    season1.identifier = 1

    season2 = SeasonBase()
    season2.identifier = 1

    season3 = SeasonBase()
    season3.identifier = 2

    assert season1 == season2
    assert season1 != season3
    assert season1 != "not a season"


def test_season_hash():
    """Test SeasonBase __hash__ method."""
    season1 = SeasonBase()
    season1.identifier = 1

    season2 = SeasonBase()
    season2.identifier = 1

    assert hash(season1) == hash(season2)


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


def test_status_repr():
    """Test Status __repr__ method."""
    status = Status()
    status.identifier = 1
    status.name = StatusName.CONTINUING
    status.keep_updated = True
    result = repr(status)
    assert "Status<" in result
    assert "keep_updated=True" in result


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


def test_episode_repr():
    """Test Episode __repr__ method."""
    episode = Episode()
    episode.identifier = 1
    episode.name = "Test Episode"
    episode.number = 1
    episode.season_number = 1
    episode.series_id = 123
    episode.is_movie = 0
    episode.last_updated = datetime.datetime.now()

    result = repr(episode)
    assert "Episode<" in result
    assert "S01E01" in result


def test_episode_eq():
    """Test Episode __eq__ method."""
    episode1 = Episode()
    episode1.identifier = 1

    episode2 = Episode()
    episode2.identifier = 1

    episode3 = Episode()
    episode3.identifier = 2

    assert episode1 == episode2
    assert episode1 != episode3
    assert episode1 != "not an episode"


def test_episode_hash():
    """Test Episode __hash__ method."""
    episode1 = Episode()
    episode1.identifier = 1

    episode2 = Episode()
    episode2.identifier = 1

    assert hash(episode1) == hash(episode2)


def test_genre_str():
    """Test Genre __str__ method."""
    genre = Genre()
    genre.identifier = 1
    genre.name = "Drama"
    genre.slug = "drama"
    assert "Drama" in str(genre)


def test_genre_repr():
    """Test Genre __repr__ method."""
    genre = Genre()
    genre.identifier = 1
    genre.name = "Drama"
    genre.slug = "drama"
    result = repr(genre)
    assert "Genre<" in result
    assert "drama" in result


def test_genre_eq():
    """Test Genre __eq__ method."""
    genre1 = Genre()
    genre1.identifier = 1

    genre2 = Genre()
    genre2.identifier = 1

    genre3 = Genre()
    genre3.identifier = 2

    assert genre1 == genre2
    assert genre1 != genre3
    assert genre1 != "not a genre"


def test_genre_hash():
    """Test Genre __hash__ method."""
    genre1 = Genre()
    genre1.identifier = 1

    genre2 = Genre()
    genre2.identifier = 1

    assert hash(genre1) == hash(genre2)


def test_show_str():
    """Test Show __str__ method."""
    show = Show()
    show.identifier = 1
    show.name = "Test Show"
    assert "Test Show" in str(show)


def test_show_repr():
    """Test Show __repr__ method."""
    status = Status()
    status.identifier = 1
    status.name = StatusName.CONTINUING
    status.keep_updated = True

    show = Show()
    show.identifier = 1
    show.name = "Test Show"
    show.year = "2020"
    show.status = status
    result = repr(show)
    assert "Show<" in result
    assert "(2020)" in result


def test_show_eq():
    """Test Show __eq__ method."""
    show1 = Show()
    show1.identifier = 1

    show2 = Show()
    show2.identifier = 1

    show3 = Show()
    show3.identifier = 2

    assert show1 == show2
    assert show1 != show3
    assert show1 != "not a show"


def test_show_hash():
    """Test Show __hash__ method."""
    show1 = Show()
    show1.identifier = 1

    show2 = Show()
    show2.identifier = 1

    assert hash(show1) == hash(show2)
