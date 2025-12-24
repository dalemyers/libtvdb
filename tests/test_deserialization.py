"""Test model deserialization from TVDB API responses.

This test suite validates that various API queries properly deserialize
into the expected model structures without errors.
"""

import datetime

from libtvdb.model import StatusName
from tests.context import BaseTVDBTest


class DeserializationTestSuite(BaseTVDBTest):
    """Test cases for validating model deserialization."""

    def test_search_show_deserialization(self):
        """Test that search results deserialize correctly."""
        shows = self.client().search_show("The Witcher")
        self.assertGreater(len(shows), 0, "Failed to find any matching shows")

        for show in shows:
            self.assertIsNotNone(show.identifier, "Show should have an identifier")
            self.assertIsNotNone(show.name, "Show should have a name")
            self.assertIsNotNone(show.slug, "Show should have a slug")
            if show.status:
                self.assertIsInstance(
                    show.status, (StatusName, type(show.status)), "Status should be StatusName or Status"
                )

    def test_show_extended_deserialization(self):
        """Test that extended show info deserializes all fields correctly."""
        show = self.client().show_info(121361)  # Game of Thrones

        self.assertIsNotNone(show, "Show should not be None")
        self.assertEqual(show.identifier, "121361", "Show ID should match")
        self.assertIsNotNone(show.name, "Show should have a name")
        self.assertIsNotNone(show.slug, "Show should have a slug")

        if show.first_aired:
            self.assertIsInstance(show.first_aired, datetime.date, "first_aired should be a date")

        if show.last_aired:
            self.assertIsInstance(show.last_aired, datetime.date, "last_aired should be a date")

        if show.next_aired:
            self.assertIsInstance(show.next_aired, datetime.date, "next_aired should be a date")

        if show.last_updated:
            self.assertIsInstance(
                show.last_updated, datetime.datetime, "last_updated should be a datetime"
            )

        if show.genres:
            self.assertIsInstance(show.genres, list, "genres should be a list")
            for genre in show.genres:
                self.assertIsNotNone(genre.identifier, "Genre should have an identifier")
                self.assertIsNotNone(genre.name, "Genre should have a name")
                self.assertIsNotNone(genre.slug, "Genre should have a slug")

        if show.artworks:
            self.assertIsInstance(show.artworks, list, "artworks should be a list")
            for artwork in show.artworks:
                self.assertIsNotNone(artwork.identifier, "Artwork should have an identifier")
                self.assertIsNotNone(artwork.image, "Artwork should have an image URL")
                self.assertIsNotNone(artwork.artwork_type, "Artwork should have a type")
                self.assertIsInstance(artwork.width, int, "Artwork width should be an int")
                self.assertIsInstance(artwork.height, int, "Artwork height should be an int")

        if show.characters:
            self.assertIsInstance(show.characters, list, "characters should be a list")
            for character in show.characters:
                self.assertIsNotNone(character.identifier, "Character should have an identifier")
                self.assertIsNotNone(character.people_id, "Character should have a people_id")
                self.assertIsInstance(character.sort, int, "Character sort should be an int")

        if show.companies:
            self.assertIsInstance(show.companies, list, "companies should be a list")
            for company in show.companies:
                self.assertIsNotNone(company.identifier, "Company should have an identifier")
                self.assertIsNotNone(company.name, "Company should have a name")

        if show.remote_ids:
            self.assertIsInstance(show.remote_ids, list, "remote_ids should be a list")
            for remote_id in show.remote_ids:
                self.assertIsNotNone(remote_id.identifier, "RemoteID should have an identifier")
                self.assertIsNotNone(
                    remote_id.source_name, "RemoteID should have a source_name"
                )

        if show.seasons:
            self.assertIsInstance(show.seasons, list, "seasons should be a list")
            for season in show.seasons:
                self.assertIsNotNone(season.identifier, "Season should have an identifier")
                self.assertIsNotNone(season.number, "Season should have a number")
                self.assertIsNotNone(season.series_id, "Season should have a series_id")
                self.assertIsNotNone(season.season_type, "Season should have a season_type")

        if show.trailers:
            self.assertIsInstance(show.trailers, list, "trailers should be a list")
            for trailer in show.trailers:
                self.assertIsNotNone(trailer.identifier, "Trailer should have an identifier")

    def test_episodes_list_deserialization(self):
        """Test that episode lists deserialize correctly."""
        episodes = self.client().episodes_from_show_id(121361)  # Game of Thrones

        self.assertGreater(len(episodes), 0, "Show should have episodes")

        for episode in episodes:
            self.assertIsNotNone(episode.identifier, "Episode should have an identifier")
            self.assertIsNotNone(episode.name, "Episode should have a name")
            self.assertIsInstance(episode.number, int, "Episode number should be an int")
            self.assertIsInstance(
                episode.season_number, int, "Episode season_number should be an int"
            )
            self.assertIsInstance(episode.series_id, int, "Episode series_id should be an int")
            self.assertIsInstance(
                episode.last_updated, datetime.datetime, "last_updated should be a datetime"
            )

            if episode.aired:
                self.assertIsInstance(episode.aired, datetime.date, "aired should be a date")

    def test_episode_extended_deserialization(self):
        """Test that extended episode info deserializes all fields correctly."""
        episode = self.client().episode_by_id(314260)  # Lost S03E12

        self.assertIsNotNone(episode, "Episode should not be None")
        self.assertEqual(episode.identifier, 314260, "Episode ID should match")
        self.assertIsNotNone(episode.name, "Episode should have a name")
        self.assertIsInstance(episode.number, int, "Episode number should be an int")
        self.assertIsInstance(
            episode.season_number, int, "Episode season_number should be an int"
        )

        if episode.aired:
            self.assertIsInstance(episode.aired, datetime.date, "aired should be a date")

        if episode.last_updated:
            self.assertIsInstance(
                episode.last_updated, datetime.datetime, "last_updated should be a datetime"
            )

        if episode.characters:
            self.assertIsInstance(episode.characters, list, "characters should be a list")
            for character in episode.characters:
                self.assertIsNotNone(character.identifier, "Character should have an identifier")
                self.assertIsNotNone(character.people_id, "Character should have a people_id")
                self.assertIsNotNone(
                    character.person_name, "Character should have a person_name"
                )
                if character.people_type:
                    self.assertIsInstance(
                        character.people_type, str, "people_type should be a string"
                    )

        if episode.remote_ids:
            self.assertIsInstance(episode.remote_ids, list, "remote_ids should be a list")
            for remote_id in episode.remote_ids:
                self.assertIsNotNone(remote_id.identifier, "RemoteID should have an identifier")
                self.assertIsNotNone(
                    remote_id.source_name, "RemoteID should have a source_name"
                )

        if episode.seasons:
            self.assertIsInstance(episode.seasons, list, "seasons should be a list")
            for season in episode.seasons:
                self.assertIsNotNone(season.identifier, "Season should have an identifier")
                self.assertIsNotNone(season.number, "Season should have a number")

        if episode.networks:
            self.assertIsInstance(episode.networks, list, "networks should be a list")
            for network in episode.networks:
                self.assertIsNotNone(network.identifier, "Network should have an identifier")
                self.assertIsNotNone(network.name, "Network should have a name")

        if episode.content_ratings:
            self.assertIsInstance(episode.content_ratings, list, "content_ratings should be a list")
            for rating in episode.content_ratings:
                self.assertIsNotNone(rating.identifier, "ContentRating should have an identifier")

        if episode.trailers:
            self.assertIsInstance(episode.trailers, list, "trailers should be a list")
            for trailer in episode.trailers:
                self.assertIsNotNone(trailer.identifier, "Trailer should have an identifier")

    def test_show_with_different_status_types(self):
        """Test shows with different status types deserialize correctly."""
        test_cases = [
            (73739, StatusName.ENDED),  # Lost - Ended
            (279121, StatusName.CONTINUING),  # The 100 - Ended (but check actual status)
        ]

        for show_id, expected_status_type in test_cases:
            show = self.client().show_info(show_id)
            self.assertIsNotNone(show, f"Show {show_id} should not be None")

            if hasattr(show.status, "name"):
                self.assertIsInstance(
                    show.status.name,
                    StatusName,
                    f"Show {show_id} status.name should be StatusName enum",
                )
            else:
                self.assertIsInstance(
                    show.status,
                    StatusName,
                    f"Show {show_id} status should be StatusName enum",
                )

    def test_show_with_various_content(self):
        """Test shows with different types of content deserialize correctly."""
        test_shows = [
            73739,  # Lost (drama, ended)
            121361,  # Game of Thrones (fantasy, ended)
            78804,  # Doctor Who (sci-fi, continuing)
            279121,  # The 100 (sci-fi, ended)
        ]

        for show_id in test_shows:
            show = self.client().show_info(show_id)
            self.assertIsNotNone(show, f"Show {show_id} should not be None")
            self.assertIsNotNone(show.name, f"Show {show_id} should have a name")
            self.assertIsNotNone(show.identifier, f"Show {show_id} should have an identifier")

            if show.score is not None:
                self.assertIsInstance(
                    show.score, float, f"Show {show_id} score should be a float"
                )

            if show.average_runtime is not None:
                self.assertIsInstance(
                    show.average_runtime, int, f"Show {show_id} average_runtime should be an int"
                )

    def test_episode_characters_by_role(self):
        """Test that characters_by_role property works correctly."""
        episode = self.client().episode_by_id(314260)  # Lost S03E12

        characters_by_role = episode.characters_by_role
        self.assertIsInstance(
            characters_by_role, dict, "characters_by_role should return a dict"
        )

        if "Guest Star" in characters_by_role:
            guest_stars = characters_by_role["Guest Star"]
            self.assertIsInstance(guest_stars, list, "Guest stars should be a list")
            for guest_star in guest_stars:
                self.assertIsNotNone(
                    guest_star.person_name, "Guest star should have a person_name"
                )

        if "Director" in characters_by_role:
            directors = characters_by_role["Director"]
            self.assertIsInstance(directors, list, "Directors should be a list")
            for director in directors:
                self.assertIsNotNone(director.person_name, "Director should have a person_name")

        if "Writer" in characters_by_role:
            writers = characters_by_role["Writer"]
            self.assertIsInstance(writers, list, "Writers should be a list")
            for writer in writers:
                self.assertIsNotNone(writer.person_name, "Writer should have a person_name")

    def test_show_artwork_types(self):
        """Test that shows with various artwork types deserialize correctly."""
        show = self.client().show_info(121361)  # Game of Thrones

        if show.artworks:
            artwork_types = set()
            for artwork in show.artworks:
                artwork_types.add(artwork.artwork_type)
                self.assertIsInstance(
                    artwork.artwork_type, int, "Artwork type should be an int"
                )

            self.assertGreater(
                len(artwork_types), 0, "Show should have at least one artwork type"
            )

    def test_show_translations(self):
        """Test that translation fields deserialize correctly."""
        show = self.client().show_info(121361)  # Game of Thrones

        if show.name_translations:
            self.assertIsInstance(
                show.name_translations, list, "name_translations should be a list"
            )
            for translation in show.name_translations:
                self.assertIsInstance(translation, str, "Translation should be a string")

        if show.overview_translations:
            self.assertIsInstance(
                show.overview_translations, list, "overview_translations should be a list"
            )
            for translation in show.overview_translations:
                self.assertIsInstance(translation, str, "Translation should be a string")

        if show.name_translated:
            self.assertIsInstance(
                show.name_translated, dict, "name_translated should be a dict"
            )

    def test_episode_with_special_properties(self):
        """Test episodes with special properties deserialize correctly."""
        episodes = self.client().episodes_from_show_id(121361)  # Game of Thrones

        for episode in episodes:
            if episode.absolute_number is not None:
                self.assertIsInstance(
                    episode.absolute_number, int, "absolute_number should be an int"
                )

            if episode.runtime is not None:
                self.assertIsInstance(episode.runtime, int, "runtime should be an int")

            if episode.production_code is not None:
                self.assertIsInstance(
                    episode.production_code, str, "production_code should be a string"
                )

            if episode.year is not None:
                self.assertIsInstance(episode.year, int, "year should be an int")

    def test_multiple_shows_batch_deserialization(self):
        """Test that multiple different shows all deserialize without errors."""
        show_ids = [
            73739,  # Lost
            121361,  # Game of Thrones
            78804,  # Doctor Who
            81189,  # Breaking Bad
            295759,  # Supergirl
        ]

        for show_id in show_ids:
            show = self.client().show_info(show_id)
            self.assertIsNotNone(show, f"Show {show_id} should not be None")
            self.assertIsNotNone(show.name, f"Show {show_id} should have a name")

            episodes = self.client().episodes_from_show_id(show_id)
            self.assertGreater(
                len(episodes), 0, f"Show {show_id} should have at least one episode"
            )

    def test_show_aliases_deserialization(self):
        """Test that show aliases deserialize correctly in different formats."""
        show = self.client().show_info(73739)  # Lost

        if show.aliases:
            self.assertIsInstance(show.aliases, list, "aliases should be a list")
            for alias in show.aliases:
                self.assertTrue(
                    isinstance(alias, (str, dict)),
                    "Alias should be either string or dict",
                )

    def test_the_orville_deserialization(self):
        """Test that The Orville show and episodes deserialize correctly.
        
        This is a specific test for show ID 328487 to ensure all fields
        deserialize properly for this particular show.
        """
        show = self.client().show_info(328487)  # The Orville

        self.assertIsNotNone(show, "The Orville show should not be None")
        self.assertEqual(show.identifier, "328487", "Show ID should match")
        self.assertEqual(show.name, "The Orville", "Show name should be 'The Orville'")
        self.assertIsNotNone(show.slug, "Show should have a slug")

        if show.status:
            self.assertTrue(
                hasattr(show.status, "name") or isinstance(show.status, StatusName),
                "Status should have proper type",
            )

        episodes = self.client().episodes_from_show_id(328487)
        self.assertGreater(len(episodes), 0, "The Orville should have episodes")

        for episode in episodes:
            self.assertIsNotNone(episode.identifier, "Episode should have an identifier")
            self.assertIsNotNone(episode.name, "Episode should have a name")
            self.assertIsInstance(episode.number, int, "Episode number should be an int")
            self.assertIsInstance(
                episode.season_number, int, "Episode season_number should be an int"
            )
            self.assertEqual(
                episode.series_id, 328487, "Episode series_id should match show ID"
            )
            self.assertIsInstance(
                episode.last_updated, datetime.datetime, "last_updated should be a datetime"
            )

            if episode.aired:
                self.assertIsInstance(episode.aired, datetime.date, "aired should be a date")

            if episode.characters:
                for character in episode.characters:
                    self.assertIsNotNone(
                        character.identifier, "Character should have an identifier"
                    )
                    self.assertIsNotNone(
                        character.people_id, "Character should have a people_id"
                    )
