"""Test searching for shows."""

import datetime

from libtvdb.model import StatusName


def test_show_parse_1(tvdb_client):
    """Test that a show is parsed as we'd expect."""
    show = tvdb_client.show_info(73739)  # Lost

    assert (
        show.airs_time == "21:00"
    ), f"'{show.airs_time}' was not equal to expected air time '21:00'"
    # API data changes over time, so just check aliases exist
    assert show.aliases is not None
    assert len(show.aliases) > 0
    assert (
        show.image == "https://artworks.thetvdb.com/banners/posters/73739-11.jpg"
    ), f"'{show.image}' was not equal to expected banner 'https://artworks.thetvdb.com/banners/posters/73739-11.jpg'"
    assert show.first_aired == datetime.date(
        2004, 9, 22
    ), f"'{show.first_aired}' was not equal to expected first_aired '{datetime.date(2004, 9, 22)}'"
    # API now returns more genres, just check key ones are present
    genre_names = sorted([g.name for g in show.genres])
    for expected_genre in ["Action", "Adventure", "Drama"]:
        assert expected_genre in genre_names
    assert (
        show.identifier == "73739"
    ), f"'{show.identifier}' was not equal to expected identifier '73739'"
    imdb_id = [
        remote_id.identifier for remote_id in show.remote_ids if remote_id.source_name == "IMDB"
    ][0]
    assert imdb_id == "tt0411008", f"'{imdb_id}' was not equal to expected imdb_id 'tt0411008'"
    assert show.name == "Lost", f"'{show.name}' was not equal to expected name Lost'"
    assert (
        show.companies[0].name == "ABC (US)"
    ), f"'{show.companies[0].name}' was not equal to expected network 'ABC (US)'"
    assert (
        show.average_runtime == 45
    ), f"'{show.average_runtime}' was not equal to expected runtime '45'"
    # Score system has changed in TVDB, just check it exists
    assert show.score is not None
    assert show.slug == "lost", f"'{show.slug}' was not equal to expected slug 'lost'"
    assert (
        show.status.name == StatusName.ENDED
    ), f"'{show.status.name}' was not equal to expected status '{StatusName.ENDED}'"
    assert show.last_updated >= datetime.datetime(2018, 11, 23, 0, 28, 59)

    # API now returns overview data
    assert show.overview is not None


def test_show_parse_2(tvdb_client):
    """Test that a show is parsed as we'd expect."""
    show = tvdb_client.show_info(73739)

    assert (
        show.airs_time == "21:00"
    ), f"'{show.airs_time}' was not equal to expected air time '21:00'"
    # API data changes over time, so just check aliases exist
    assert show.aliases is not None
    assert len(show.aliases) > 0
    assert (
        show.image == "https://artworks.thetvdb.com/banners/posters/73739-11.jpg"
    ), f"'{show.image}' was not equal to expected banner 'https://artworks.thetvdb.com/banners/posters/73739-11.jpg'"
    assert show.first_aired == datetime.date(
        2004, 9, 22
    ), f"'{show.first_aired}' was not equal to expected first_aired '{datetime.date(2004, 9, 22)}'"
    # API now returns more genres, just check key ones are present
    genre_names = sorted([g.name for g in show.genres])
    for expected_genre in ["Action", "Adventure", "Drama"]:
        assert expected_genre in genre_names
    assert (
        show.identifier == "73739"
    ), f"'{show.identifier}' was not equal to expected identifier '73739'"
    imdb_id = [
        remote_id.identifier for remote_id in show.remote_ids if remote_id.source_name == "IMDB"
    ][0]
    assert imdb_id == "tt0411008", f"'{imdb_id}' was not equal to expected imdb_id 'tt0411008'"
    assert show.name == "Lost", f"'{show.name}' was not equal to expected name Lost'"
    assert (
        show.companies[0].name == "ABC (US)"
    ), f"'{show.companies[0].name}' was not equal to expected network 'ABC (US)'"
    assert (
        show.average_runtime == 45
    ), f"'{show.average_runtime}' was not equal to expected runtime '45'"
    # Score system has changed in TVDB, just check it exists
    assert show.score is not None
    assert show.slug == "lost", f"'{show.slug}' was not equal to expected slug 'lost'"
    assert (
        show.status.name == StatusName.ENDED
    ), f"'{show.status.name}' was not equal to expected status '{StatusName.ENDED}'"
    assert show.last_updated >= datetime.datetime(2018, 11, 23, 0, 28, 59)

    # API now returns overview data
    assert show.overview is not None
