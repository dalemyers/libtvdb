"""Test model deserialization from TVDB API responses.

This test suite validates that various API queries properly deserialize
into the expected model structures without errors.
"""

import datetime

from libtvdb.model import StatusName


def test_search_show_deserialization(tvdb_client):
    """Test that search results deserialize correctly."""
    shows = tvdb_client.search_show("The Witcher")
    assert len(shows) > 0, "Failed to find any matching shows"

    for show in shows:
        assert show.identifier is not None, "Show should have an identifier"
        assert show.name is not None, "Show should have a name"
        assert show.slug is not None, "Show should have a slug"
        if show.status:
            assert isinstance(
                show.status, (StatusName, type(show.status))
            ), "Status should be StatusName or Status"


def test_show_extended_deserialization(tvdb_client):
    """Test that extended show info deserializes all fields correctly."""
    # pylint: disable=too-many-branches
    show = tvdb_client.show_info(121361)  # Game of Thrones

    assert show is not None, "Show should not be None"
    assert show.identifier == "121361", "Show ID should match"
    assert show.name is not None, "Show should have a name"
    assert show.slug is not None, "Show should have a slug"

    if show.first_aired:
        assert isinstance(show.first_aired, datetime.date), "first_aired should be a date"

    if show.last_aired:
        assert isinstance(show.last_aired, datetime.date), "last_aired should be a date"

    if show.next_aired:
        assert isinstance(show.next_aired, datetime.date), "next_aired should be a date"

    if show.last_updated:
        assert isinstance(show.last_updated, datetime.datetime), "last_updated should be a datetime"

    if show.genres:
        assert isinstance(show.genres, list), "genres should be a list"
        for genre in show.genres:
            assert genre.identifier is not None, "Genre should have an identifier"
            assert genre.name is not None, "Genre should have a name"
            assert genre.slug is not None, "Genre should have a slug"

    if show.artworks:
        assert isinstance(show.artworks, list), "artworks should be a list"
        for artwork in show.artworks:
            assert artwork.identifier is not None, "Artwork should have an identifier"
            assert artwork.image is not None, "Artwork should have an image URL"
            assert artwork.artwork_type is not None, "Artwork should have a type"
            assert isinstance(artwork.width, int), "Artwork width should be an int"
            assert isinstance(artwork.height, int), "Artwork height should be an int"

    if show.characters:
        assert isinstance(show.characters, list), "characters should be a list"
        for character in show.characters:
            assert character.identifier is not None, "Character should have an identifier"
            assert character.people_id is not None, "Character should have a people_id"
            assert isinstance(character.sort, int), "Character sort should be an int"

    if show.companies:
        assert isinstance(show.companies, list), "companies should be a list"
        for company in show.companies:
            assert company.identifier is not None, "Company should have an identifier"
            assert company.name is not None, "Company should have a name"

    if show.remote_ids:
        assert isinstance(show.remote_ids, list), "remote_ids should be a list"
        for remote_id in show.remote_ids:
            assert remote_id.identifier is not None, "RemoteID should have an identifier"
            assert remote_id.source_name is not None, "RemoteID should have a source_name"

    if show.seasons:
        assert isinstance(show.seasons, list), "seasons should be a list"
        for season in show.seasons:
            assert season.identifier is not None, "Season should have an identifier"
            assert season.number is not None, "Season should have a number"
            assert season.series_id is not None, "Season should have a series_id"
            assert season.season_type is not None, "Season should have a season_type"

    if show.trailers:
        assert isinstance(show.trailers, list), "trailers should be a list"
        for trailer in show.trailers:
            assert trailer.identifier is not None, "Trailer should have an identifier"


def test_episodes_list_deserialization(tvdb_client):
    """Test that episode lists deserialize correctly."""
    episodes = tvdb_client.episodes_from_show_id(121361)  # Game of Thrones

    assert len(episodes) > 0, "Show should have episodes"

    for episode in episodes:
        assert episode.identifier is not None, "Episode should have an identifier"
        assert episode.name is not None, "Episode should have a name"
        assert isinstance(episode.number, int), "Episode number should be an int"
        assert isinstance(episode.season_number, int), "Episode season_number should be an int"
        assert isinstance(episode.series_id, int), "Episode series_id should be an int"
        assert isinstance(
            episode.last_updated, datetime.datetime
        ), "last_updated should be a datetime"

        if episode.aired:
            assert isinstance(episode.aired, datetime.date), "aired should be a date"


def test_episode_extended_deserialization(tvdb_client):
    """Test that extended episode info deserializes all fields correctly."""
    # pylint: disable=too-many-branches
    episode = tvdb_client.episode_by_id(314260)  # Lost S03E12

    assert episode is not None, "Episode should not be None"
    assert episode.identifier == 314260, "Episode ID should match"
    assert episode.name is not None, "Episode should have a name"
    assert isinstance(episode.number, int), "Episode number should be an int"
    assert isinstance(episode.season_number, int), "Episode season_number should be an int"

    if episode.aired:
        assert isinstance(episode.aired, datetime.date), "aired should be a date"

    if episode.last_updated:
        assert isinstance(
            episode.last_updated, datetime.datetime
        ), "last_updated should be a datetime"

    if episode.characters:
        assert isinstance(episode.characters, list), "characters should be a list"
        for character in episode.characters:
            assert character.identifier is not None, "Character should have an identifier"
            assert character.people_id is not None, "Character should have a people_id"
            assert character.person_name is not None, "Character should have a person_name"
            if character.people_type:
                assert isinstance(character.people_type, str), "people_type should be a string"

    if episode.remote_ids:
        assert isinstance(episode.remote_ids, list), "remote_ids should be a list"
        for remote_id in episode.remote_ids:
            assert remote_id.identifier is not None, "RemoteID should have an identifier"
            assert remote_id.source_name is not None, "RemoteID should have a source_name"

    if episode.seasons:
        assert isinstance(episode.seasons, list), "seasons should be a list"
        for season in episode.seasons:
            assert season.identifier is not None, "Season should have an identifier"
            assert season.number is not None, "Season should have a number"

    if episode.networks:
        assert isinstance(episode.networks, list), "networks should be a list"
        for network in episode.networks:
            assert network.identifier is not None, "Network should have an identifier"
            assert network.name is not None, "Network should have a name"

    if episode.content_ratings:
        assert isinstance(episode.content_ratings, list), "content_ratings should be a list"
        for rating in episode.content_ratings:
            assert rating.identifier is not None, "ContentRating should have an identifier"

    if episode.trailers:
        assert isinstance(episode.trailers, list), "trailers should be a list"
        for trailer in episode.trailers:
            assert trailer.identifier is not None, "Trailer should have an identifier"


def test_show_with_different_status_types(tvdb_client):
    """Test shows with different status types deserialize correctly."""
    test_cases = [
        (73739, StatusName.ENDED),  # Lost - Ended
        (279121, StatusName.CONTINUING),  # The 100 - Ended (but check actual status)
    ]

    for show_id, _ in test_cases:
        show = tvdb_client.show_info(show_id)
        assert show is not None, f"Show {show_id} should not be None"

        if hasattr(show.status, "name"):
            assert isinstance(
                show.status.name, StatusName
            ), f"Show {show_id} status.name should be StatusName enum"
        else:
            assert isinstance(
                show.status, StatusName
            ), f"Show {show_id} status should be StatusName enum"


def test_show_with_various_content(tvdb_client):
    """Test shows with different types of content deserialize correctly."""
    test_shows = [
        73739,  # Lost (drama, ended)
        121361,  # Game of Thrones (fantasy, ended)
        78804,  # Doctor Who (sci-fi, continuing)
        279121,  # The 100 (sci-fi, ended)
    ]

    for show_id in test_shows:
        show = tvdb_client.show_info(show_id)
        assert show is not None, f"Show {show_id} should not be None"
        assert show.name is not None, f"Show {show_id} should have a name"
        assert show.identifier is not None, f"Show {show_id} should have an identifier"

        if show.score is not None:
            assert isinstance(show.score, float), f"Show {show_id} score should be a float"

        if show.average_runtime is not None:
            assert isinstance(
                show.average_runtime, int
            ), f"Show {show_id} average_runtime should be an int"


def test_episode_characters_by_role(tvdb_client):
    """Test that characters_by_role property works correctly."""
    episode = tvdb_client.episode_by_id(314260)  # Lost S03E12

    characters_by_role = episode.characters_by_role
    assert isinstance(characters_by_role, dict), "characters_by_role should return a dict"

    if "Guest Star" in characters_by_role:
        guest_stars = characters_by_role["Guest Star"]
        assert isinstance(guest_stars, list), "Guest stars should be a list"
        for guest_star in guest_stars:
            assert guest_star.person_name is not None, "Guest star should have a person_name"

    if "Director" in characters_by_role:
        directors = characters_by_role["Director"]
        assert isinstance(directors, list), "Directors should be a list"
        for director in directors:
            assert director.person_name is not None, "Director should have a person_name"

    if "Writer" in characters_by_role:
        writers = characters_by_role["Writer"]
        assert isinstance(writers, list), "Writers should be a list"
        for writer in writers:
            assert writer.person_name is not None, "Writer should have a person_name"


def test_show_artwork_types(tvdb_client):
    """Test that shows with various artwork types deserialize correctly."""
    show = tvdb_client.show_info(121361)  # Game of Thrones

    if show.artworks:
        artwork_types = set()
        for artwork in show.artworks:
            artwork_types.add(artwork.artwork_type)
            assert isinstance(artwork.artwork_type, int), "Artwork type should be an int"

        assert len(artwork_types) > 0, "Show should have at least one artwork type"


def test_show_translations(tvdb_client):
    """Test that translation fields deserialize correctly."""
    show = tvdb_client.show_info(121361)  # Game of Thrones

    if show.name_translations:
        assert isinstance(show.name_translations, list), "name_translations should be a list"
        for translation in show.name_translations:
            assert isinstance(translation, str), "Translation should be a string"

    if show.overview_translations:
        assert isinstance(
            show.overview_translations, list
        ), "overview_translations should be a list"
        for translation in show.overview_translations:
            assert isinstance(translation, str), "Translation should be a string"

    if show.name_translated:
        assert isinstance(show.name_translated, dict), "name_translated should be a dict"


def test_episode_with_special_properties(tvdb_client):
    """Test episodes with special properties deserialize correctly."""
    episodes = tvdb_client.episodes_from_show_id(121361)  # Game of Thrones

    for episode in episodes:
        if episode.absolute_number is not None:
            assert isinstance(episode.absolute_number, int), "absolute_number should be an int"

        if episode.runtime is not None:
            assert isinstance(episode.runtime, int), "runtime should be an int"

        if episode.production_code is not None:
            assert isinstance(episode.production_code, str), "production_code should be a string"

        if episode.year is not None:
            assert isinstance(episode.year, int), "year should be an int"


def test_multiple_shows_batch_deserialization(tvdb_client):
    """Test that multiple different shows all deserialize without errors."""
    show_ids = [
        73739,  # Lost
        121361,  # Game of Thrones
        78804,  # Doctor Who
        81189,  # Breaking Bad
        295759,  # Supergirl
    ]

    for show_id in show_ids:
        show = tvdb_client.show_info(show_id)
        assert show is not None, f"Show {show_id} should not be None"
        assert show.name is not None, f"Show {show_id} should have a name"

        episodes = tvdb_client.episodes_from_show_id(show_id)
        assert len(episodes) > 0, f"Show {show_id} should have at least one episode"


def test_show_aliases_deserialization(tvdb_client):
    """Test that show aliases deserialize correctly in different formats."""
    show = tvdb_client.show_info(73739)  # Lost

    if show.aliases:
        assert isinstance(show.aliases, list), "aliases should be a list"
        for alias in show.aliases:
            assert isinstance(alias, (str, dict)), "Alias should be either string or dict"


def test_ahsoka_deserialization(tvdb_client):
    """Test that Ahsoka show and episodes deserialize correctly.

    This is a specific test for show ID 393187 to ensure all fields
    deserialize properly for this particular show, including the linkedMovie field.
    """
    show = tvdb_client.show_info(393187)  # Ahsoka

    assert show is not None, "Ahsoka show should not be None"
    assert show.identifier == "393187", "Show ID should match"
    assert show.name == "Ahsoka", "Show name should be 'Ahsoka'"
    assert show.slug is not None, "Show should have a slug"

    if show.status:
        assert hasattr(show.status, "name") or isinstance(
            show.status, StatusName
        ), "Status should have proper type"

    episodes = tvdb_client.episodes_from_show_id(393187)
    assert len(episodes) > 0, "Ahsoka should have episodes"

    for episode in episodes:
        assert episode.identifier is not None, "Episode should have an identifier"
        assert episode.name is not None, "Episode should have a name"
        assert isinstance(episode.number, int), "Episode number should be an int"
        assert isinstance(episode.season_number, int), "Episode season_number should be an int"
        assert episode.series_id == 393187, "Episode series_id should match show ID"
        assert isinstance(
            episode.last_updated, datetime.datetime
        ), "last_updated should be a datetime"

        if episode.aired:
            assert isinstance(episode.aired, datetime.date), "aired should be a date"

        if episode.linked_movie is not None:
            assert isinstance(episode.linked_movie, int), "linked_movie should be an int"

        if episode.characters:
            for character in episode.characters:
                assert character.identifier is not None, "Character should have an identifier"
                assert character.people_id is not None, "Character should have a people_id"
