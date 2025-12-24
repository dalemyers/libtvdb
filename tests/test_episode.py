"""Test episodes."""

import datetime


def test_episode_parse(tvdb_client):
    """Test that a shows episodes are parsed as we'd expect."""
    show_ids = [
        71565,
        95011,  # Modern Family
        121361,  # Game of thrones
        295759,  # Supergirl
        73739,  # Lost
        281470,  # iZombie
    ]

    for show_id in show_ids:
        _ = tvdb_client.episodes_from_show_id(show_id)


def test_episode_properties_1(tvdb_client):
    """Test that specific episodes parse as expected."""
    episode_id = 6814868  # Game of thrones S05E03

    episode = tvdb_client.episode_by_id(episode_id)

    assert episode is not None, "Failed to find episode"
    assert (
        episode.identifier == 6814868
    ), f"'{episode.identifier}' was not equal to expected '6814868'"
    assert episode.season_number == 5, f"'{episode.season_number}' was not equal to expected '5'"
    assert (
        episode.seasons[0].identifier == 777511
    ), f"'{episode.seasons[0].identifier}' was not equal to expected '777511'"
    assert episode.number == 3, f"'{episode.number}' was not equal to expected '3'"
    assert (
        episode.name == "Five, Six, Seven, Ate!"
    ), f"'{episode.name}' was not equal to expected 'Five, Six, Seven, Ate!'"
    assert episode.aired == datetime.date(
        2019, 5, 16
    ), f"'{episode.aired}' was not equal to expected '{datetime.date(2019, 5, 16)}'"
    assert episode.airs_after_season is None
    assert episode.airs_before_episode is None
    assert episode.airs_before_season is None
    assert episode.awards == []
    assert episode.is_movie == 0
    if episode.networks and len(episode.networks) > 0:
        assert episode.networks[0].name == "The CW"
    assert episode.runtime == 45


def test_episode_properties_2(tvdb_client):
    """Test that specific episodes parse as expected."""
    episode_id = 314260  # Lost S03E12

    episode = tvdb_client.episode_by_id(episode_id)

    assert episode is not None, "Failed to find episode"
    assert (
        episode.identifier == 314260
    ), f"'{episode.identifier}' was not equal to expected '314260'"
    assert episode.season_number == 3, f"'{episode.season_number}' was not equal to expected '3'"
    assert (
        episode.seasons[0].identifier == 16270
    ), f"'{episode.seasons[0].identifier}' was not equal to expected '16270'"
    assert episode.number == 12, f"'{episode.number}' was not equal to expected '12'"
    assert episode.name == "Par Avion", f"'{episode.name}' was not equal to expected 'Par Avion'"
    assert episode.aired == datetime.date(
        2007, 3, 14
    ), f"'{episode.aired}' was not equal to expected '{datetime.date(2007, 3, 14)}'"
    guest_stars = sorted(
        [person.person_name for person in episode.characters if person.people_type == "Guest Star"]
    )
    assert guest_stars == [
        "Andrew Divoff",
        "Anne Elizabeth Logan",
        "Arlene Newman-Van Asperan",
        "Danan Pere",
        "Gabrielle Fitzpatrick",
        "John Medlen",
        "Julian Barnes",
        "Rhett Giles",
    ]
    expected_guests = [
        "Andrew Divoff",
        "Anne Elizabeth Logan",
        "Arlene Newman-Van Asperan",
        "Danan Pere",
        "Gabrielle Fitzpatrick",
        "John Medlen",
        "Julian Barnes",
        "Rhett Giles",
    ]
    assert guest_stars == expected_guests, f"'{guest_stars}' was not equal to expected"
    directors = [director.person_name for director in episode.characters_by_role["Director"]]
    assert directors == ["Paul A. Edwards"]
    writers = sorted([writer.person_name for writer in episode.characters_by_role["Writer"]])
    assert writers == [
        "Christina M. Kim",
        "Jordan Rosenberg",
    ], f"'{writers}' was not equal to expected '['Christina M. Kim', 'Jordan Rosenberg']'"
    # API now returns overview data, so we just check it exists
    assert episode.overview is not None
    assert (
        episode.image == "https://artworks.thetvdb.com/banners/episodes/73739/60942d39c6dd6.jpg"
    ), f"'{episode.image}' was not equal to expected 'https://artworks.thetvdb.com/banners/episodes/73739/60942d39c6dd6.jpg'"
    assert episode.series_id == 73739, f"'{episode.series_id}' was not equal to expected '73739'"
    assert episode.airs_after_season is None, "Episode was not expected to have airs after season"
    assert episode.airs_before_season is None, "Episode was not expected to have airs before season"
    assert (
        episode.airs_before_episode is None
    ), "Episode was not expected to have airs before episode"
    assert (
        episode.remote_ids[0].identifier == "tt0959403"
    ), f"'{episode.remote_ids[0].identifier}' was not equal to expected 'tt0959403'"


def test_episodes_from_show(tvdb_client):
    """Test episodes_from_show wrapper method."""
    shows = tvdb_client.search_show("Doctor Who")
    assert len(shows) > 0, "Failed to find any matching shows"

    # Use first show from results
    show = shows[0]
    episodes = tvdb_client.episodes_from_show(show)

    assert len(episodes) > 0, "Show should have episodes"
