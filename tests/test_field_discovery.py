"""Test for discovering missing fields in API responses.

This test suite attempts to deserialize data from various shows to discover
any fields that exist in the API but are missing from our models.
"""

# pylint: disable=duplicate-code

import pytest

from libtvdb.exceptions import NotFoundException, TVDBException


def test_discover_missing_show_fields(tvdb_client):
    """Test various shows to discover any missing fields in Show model."""
    # A diverse set of shows with different properties
    test_shows = [
        73739,  # Lost - Classic drama
        121361,  # Game of Thrones - Fantasy epic
        78804,  # Doctor Who - Long-running sci-fi
        81189,  # Breaking Bad - Crime drama
        295759,  # Supergirl - Superhero
        393187,  # Ahsoka - Recent Disney+ series
        328487,  # The Orville - Sci-fi comedy
        279121,  # The 100 - Post-apocalyptic
        371572,  # The Last of Us - Video game adaptation
        425451,  # House of the Dragon - Fantasy prequel
        392256,  # The Rings of Power - Fantasy epic
        419048,  # Yellowstone - Western drama
        360068,  # Wednesday - Horror comedy
    ]

    missing_fields_found = False
    shows_with_issues = []

    for show_id in test_shows:
        try:
            show = tvdb_client.show_info(show_id)
            assert show is not None, f"Show {show_id} should not be None"
        except (NotFoundException, TVDBException) as e:
            # Skip shows that don't exist or have API issues
            if "not found" in str(e).lower():
                continue
            # But report other deserialization errors
            missing_fields_found = True
            shows_with_issues.append((show_id, str(e)))
        except Exception as e:  # pylint: disable=broad-except
            missing_fields_found = True
            shows_with_issues.append((show_id, str(e)))

    if missing_fields_found:
        error_msg = "Missing fields discovered in Show model:\n"
        for show_id, error in shows_with_issues:
            error_msg += f"  - Show ID {show_id}: {error}\n"
        pytest.fail(error_msg)


def test_discover_missing_episode_fields(tvdb_client):
    """Test episodes from various shows to discover any missing fields in Episode model."""
    # Shows with diverse episode structures
    test_shows = [
        73739,  # Lost - Standard episodes
        121361,  # Game of Thrones - Fantasy episodes
        78804,  # Doctor Who - Long-running series
        393187,  # Ahsoka - Recent series with linked_movie
        371572,  # The Last of Us - Limited series
        425451,  # House of the Dragon - Recent HBO
        392256,  # The Rings of Power - Amazon series
        360068,  # Wednesday - Netflix series
    ]

    missing_fields_found = False
    shows_with_issues = []

    for show_id in test_shows:
        try:
            episodes = tvdb_client.episodes_from_show_id(show_id)
            assert len(episodes) > 0, f"Show {show_id} should have episodes"

            # Try to access various properties to ensure they deserialize
            for episode in episodes:
                _ = episode.identifier
                _ = episode.name
                _ = episode.season_number
                _ = episode.number
        except (NotFoundException, TVDBException) as e:
            # Skip shows that don't exist or have API issues
            if "not found" in str(e).lower():
                continue
            # But report other deserialization errors
            missing_fields_found = True
            shows_with_issues.append((show_id, str(e)))
        except Exception as e:  # pylint: disable=broad-except
            missing_fields_found = True
            shows_with_issues.append((show_id, str(e)))

    if missing_fields_found:
        error_msg = "Missing fields discovered in Episode model:\n"
        for show_id, error in shows_with_issues:
            error_msg += f"  - Show ID {show_id}: {error}\n"
        pytest.fail(error_msg)


def test_discover_missing_episode_extended_fields(tvdb_client):
    """Test extended episode data to discover missing fields."""
    # Specific episodes with potentially unique fields
    test_episodes = [
        314260,  # Lost S03E12 - Standard episode
        6814868,  # Modern Family episode
        8657076,  # Ahsoka episode - has linked_movie
    ]

    missing_fields_found = False
    episodes_with_issues = []

    for episode_id in test_episodes:
        try:
            episode = tvdb_client.episode_by_id(episode_id)
            assert episode is not None, f"Episode {episode_id} should not be None"

            # Access various properties
            _ = episode.identifier
            _ = episode.name
            _ = episode.characters
            _ = episode.linked_movie
        except (NotFoundException, TVDBException) as e:
            # Skip episodes that don't exist
            if "not found" in str(e).lower():
                continue
            # But report other deserialization errors
            missing_fields_found = True
            episodes_with_issues.append((episode_id, str(e)))
        except Exception as e:  # pylint: disable=broad-except
            missing_fields_found = True
            episodes_with_issues.append((episode_id, str(e)))

    if missing_fields_found:
        error_msg = "Missing fields discovered in Episode extended model:\n"
        for episode_id, error in episodes_with_issues:
            error_msg += f"  - Episode ID {episode_id}: {error}\n"
        pytest.fail(error_msg)


def test_discover_missing_fields_in_recent_shows(tvdb_client):
    """Test very recent shows that might have new API fields."""
    # Recent shows from 2023-2024
    recent_shows = [
        425451,  # House of the Dragon (2022)
        437239,  # The Last of Us (2023)
        434355,  # The Witcher S3 (2023)
        360068,  # Wednesday (2022)
    ]

    missing_fields_found = False
    shows_with_issues = []

    for show_id in recent_shows:
        try:
            # Test show info
            show = tvdb_client.show_info(show_id)
            assert show is not None

            # Test episodes
            episodes = tvdb_client.episodes_from_show_id(show_id)
            if len(episodes) > 0:
                # Test first episode extended data
                first_ep = tvdb_client.episode_by_id(episodes[0].identifier)
                assert first_ep is not None
        except (NotFoundException, TVDBException) as e:
            # Skip shows that don't exist with this ID
            if "not found" in str(e).lower():
                continue
            # But report other deserialization errors
            missing_fields_found = True
            shows_with_issues.append((show_id, str(e)))
        except Exception as e:  # pylint: disable=broad-except
            missing_fields_found = True
            shows_with_issues.append((show_id, str(e)))

    if missing_fields_found:
        error_msg = "Missing fields discovered in recent shows:\n"
        for show_id, error in shows_with_issues:
            error_msg += f"  - Show ID {show_id}: {error}\n"
        pytest.fail(error_msg)


def test_discover_missing_fields_in_anime(tvdb_client):
    """Test anime shows which might have different field structures."""
    anime_shows = [
        79604,  # Attack on Titan
        81797,  # One Piece
        81834,  # Naruto
        296762,  # My Hero Academia
        355567,  # Demon Slayer
        366524,  # Jujutsu Kaisen
    ]

    missing_fields_found = False
    shows_with_issues = []

    for show_id in anime_shows:
        try:
            show = tvdb_client.show_info(show_id)
            assert show is not None

            # Try to get episodes
            episodes = tvdb_client.episodes_from_show_id(show_id)
            assert len(episodes) > 0
        except (NotFoundException, TVDBException) as e:
            # Skip shows that don't exist
            if "not found" in str(e).lower():
                continue
            # But report other deserialization errors
            missing_fields_found = True
            shows_with_issues.append((show_id, str(e)))
        except Exception as e:  # pylint: disable=broad-except
            missing_fields_found = True
            shows_with_issues.append((show_id, str(e)))

    if missing_fields_found:
        error_msg = "Missing fields discovered in anime shows:\n"
        for show_id, error in shows_with_issues:
            error_msg += f"  - Show ID {show_id}: {error}\n"
        pytest.fail(error_msg)
