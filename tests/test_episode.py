"""Test episodes."""

import datetime

from tests.context import BaseTVDBTest


class EpisodeTestSuite(BaseTVDBTest):
    """Episode test cases."""

    def test_episode_parse(self):
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
            _ = self.client().episodes_from_show_id(show_id)

    def test_episode_properties_1(self):
        """Test that specific episodes parse as expected."""

        episode_id = 6814868  # Game of thrones S05E03

        episode = self.client().episode_by_id(episode_id)

        self.assertIsNotNone(episode, "Failed to find episode")

        self.assertEqual(
            episode.identifier,
            6814868,
            f"'{episode.identifier}' was not equal to expected '6814868'",
        )
        self.assertEqual(
            episode.season_number,
            5,
            f"'{episode.season_number}' was not equal to expected '5'",
        )
        self.assertEqual(
            episode.seasons[0].identifier,
            777511,
            f"'{episode.seasons[0].identifier}' was not equal to expected '777511'",
        )
        self.assertEqual(
            episode.number,
            3,
            f"'{episode.number}' was not equal to expected '3'",
        )
        self.assertEqual(
            episode.name,
            "Five, Six, Seven, Ate!",
            f"'{episode.name}' was not equal to expected 'Five, Six, Seven, Ate!'",
        )
        self.assertEqual(
            episode.aired,
            datetime.date(2019, 5, 16),
            f"'{episode.aired}' was not equal to expected '{datetime.date(2019, 5, 16)}'",
        )
        self.assertIsNone(episode.airs_after_season)
        self.assertIsNone(episode.airs_before_episode)
        self.assertIsNone(episode.airs_before_season)
        self.assertEqual(episode.awards, [])
        self.assertEqual(episode.is_movie, 0)
        if episode.networks and len(episode.networks) > 0:
            self.assertEqual(episode.networks[0].name, "The CW")
        self.assertEqual(episode.runtime, 45)

    def test_episode_properties_2(self):
        """Test that specific episodes parse as expected."""

        episode_id = 314260  # Lost S03E12

        episode = self.client().episode_by_id(episode_id)

        self.assertIsNotNone(episode, "Failed to find episode")

        # pylint: disable=line-too-long
        self.assertEqual(
            episode.identifier,
            314260,
            f"'{episode.identifier}' was not equal to expected '314260'",
        )
        self.assertEqual(
            episode.season_number,
            3,
            f"'{episode.season_number}' was not equal to expected '3'",
        )
        self.assertEqual(
            episode.seasons[0].identifier,
            16270,
            f"'{episode.seasons[0].identifier}' was not equal to expected '16270'",
        )
        self.assertEqual(
            episode.number,
            12,
            f"'{episode.number}' was not equal to expected '12'",
        )
        self.assertEqual(
            episode.name,
            "Par Avion",
            f"'{episode.name}' was not equal to expected 'Par Avion'",
        )
        self.assertEqual(
            episode.aired,
            datetime.date(2007, 3, 14),
            f"'{episode.aired}' was not equal to expected '{datetime.date(2007, 3, 14)}'",
        )
        guest_stars = sorted(
            [
                person.person_name
                for person in episode.characters
                if person.people_type == "Guest Star"
            ]
        )
        self.assertEqual(
            guest_stars,
            [
                "Andrew Divoff",
                "Anne Elizabeth Logan",
                "Arlene Newman-Van Asperan",
                "Danan Pere",
                "Gabrielle Fitzpatrick",
                "John Medlen",
                "Julian Barnes",
                "Rhett Giles",
            ],
            f"'{guest_stars}' was not equal to expected '['Andrew Divoff', 'Anne Elizabeth Logan', 'Arlene Newman-Van Asperan', 'Danan Pere', 'Gabrielle Fitzpatrick', 'John Medlen', 'Julian Barnes', 'Rhett Giles']'",
        )
        directors = [director.person_name for director in episode.characters_by_role["Director"]]
        self.assertEqual(
            directors,
            ["Paul A. Edwards"],
        )
        writers = sorted([writer.person_name for writer in episode.characters_by_role["Writer"]])
        self.assertEqual(
            writers,
            ["Christina M. Kim", "Jordan Rosenberg"],
            f"'{writers}' was not equal to expected '['Christina M. Kim', 'Jordan Rosenberg']'",
        )
        # API now returns overview data, so we just check it exists
        self.assertIsNotNone(episode.overview)
        self.assertEqual(
            episode.image,
            "https://artworks.thetvdb.com/banners/episodes/73739/60942d39c6dd6.jpg",
            f"'{episode.image}' was not equal to expected 'https://artworks.thetvdb.com/banners/episodes/73739/60942d39c6dd6.jpg'",
        )
        self.assertEqual(
            episode.series_id,
            73739,
            f"'{episode.series_id}' was not equal to expected '73739'",
        )
        self.assertIsNone(
            episode.airs_after_season,
            "Episode was not expected to have airs after season",
        )
        self.assertIsNone(
            episode.airs_before_season,
            "Episode was not expected to have airs before season",
        )
        self.assertIsNone(
            episode.airs_before_episode,
            "Episode was not expected to have airs before episode",
        )
        self.assertEqual(
            episode.remote_ids[0].identifier,
            "tt0959403",
            f"'{episode.remote_ids[0].identifier}' was not equal to expected 'tt0959403'",
        )
        # pylint: enable=line-too-long

    def test_episodes_from_show(self):
        """Test episodes_from_show wrapper method."""
        shows = self.client().search_show("Doctor Who")
        self.assertGreater(len(shows), 0, "Failed to find any matching shows")

        # Use first show from results
        show = shows[0]
        episodes = self.client().episodes_from_show(show)

        self.assertGreater(len(episodes), 0, "Show should have episodes")
