"""Test episodes."""

import datetime

from tests.context import BaseTVDBTest


class EpisodeTestSuite(BaseTVDBTest):
    """Episode test cases."""

    def test_episode_parse(self):
        """Test that a shows episodes are parsed as we'd expect."""

        show_ids = [
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

        # pylint: disable=line-too-long
        self.assertEqual(
            episode.identifier,
            6814868,
            f"'{episode.identifier}' was not equal to expected '6814868'",
        )
        self.assertEqual(
            episode.aired_season,
            5,
            f"'{episode.aired_season}' was not equal to expected '5'",
        )
        self.assertEqual(
            episode.aired_season_id,
            777511,
            f"'{episode.aired_season_id}' was not equal to expected '777511'",
        )
        self.assertEqual(
            episode.aired_episode_number,
            3,
            f"'{episode.aired_episode_number}' was not equal to expected '3'",
        )
        self.assertEqual(
            episode.episode_name,
            "Five, Six, Seven, Ate!",
            f"'{episode.episode_name}' was not equal to expected 'Five, Six, Seven, Ate!'",
        )
        self.assertIsNone(
            episode.first_aired, "Episode was not expected to have firsted aired data"
        )
        self.assertEqual(
            episode.guest_stars,
            [],
            f"'{episode.guest_stars}' was not equal to expected '[]'",
        )
        self.assertEqual(
            episode.director,
            "||",
            f"'{episode.director}' was not equal to expected '||'",
        )
        self.assertEqual(
            episode.directors,
            [],
            f"'{episode.directors}' was not equal to expected '[]'",
        )
        self.assertEqual(episode.writers, [], f"'{episode.writers}' was not equal to expected '[]'")
        self.assertIsNone(episode.overview, "Episode was not expected to have overview")
        self.assertEqual(
            episode.language.episode_name,
            "en",
            f"'{episode.language.episode_name}' was not equal to expected 'en'",
        )
        self.assertEqual(
            episode.language.overview,
            "en",
            f"'{episode.language.overview}' was not equal to expected 'en'",
        )
        self.assertIsNone(
            episode.production_code, "Episode was not expected to have production code"
        )
        self.assertIsNone(episode.show_url, "Episode was not expected to have show url")
        self.assertGreater(
            episode.last_updated,
            datetime.datetime(2018, 9, 3, 17, 17, 36),
            f"'{episode.last_updated}' was not greater than expected last updated '{datetime.datetime(2018, 9, 3, 17, 17, 36)}'",
        )
        self.assertIsNone(episode.dvd_disc_id, "Episode was not expected to have DVD disc ID")
        self.assertIsNone(episode.dvd_season, "Episode was not expected to have DVD season")
        self.assertIsNone(
            episode.dvd_episode_number,
            "Episode was not expected to have DVD episode number",
        )
        self.assertIsNone(episode.dvd_chapter, "Episode was not expected to have DVD chapter")
        self.assertIsNone(
            episode.absolute_number, "Episode was not expected to have absolute number"
        )
        self.assertIsNone(episode.file_name, "Episode was not expected to have file name")
        self.assertEqual(
            episode.series_id,
            281470,
            f"'{episode.series_id}' was not equal to expected '281470'",
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
        self.assertIsNone(episode.thumb_added, "Episode was not expected to have thumb added")
        self.assertIsNone(episode.thumb_width, "Episode was not expected to have thumb width")
        self.assertIsNone(episode.thumb_height, "Episode was not expected to have thumb height")
        self.assertIsNone(episode.imdb_id, "Episode was not expected to have imdb ID")
        self.assertEqual(
            episode.site_rating,
            0,
            f"'{episode.site_rating}' was not equal to expected '0'",
        )
        self.assertEqual(
            episode.site_rating_count,
            0,
            f"'{episode.site_rating_count}' was not equal to expected '0'",
        )
        # pylint: enable=line-too-long

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
            episode.aired_season,
            3,
            f"'{episode.aired_season}' was not equal to expected '3'",
        )
        self.assertEqual(
            episode.aired_season_id,
            16270,
            f"'{episode.aired_season_id}' was not equal to expected '16270'",
        )
        self.assertEqual(
            episode.aired_episode_number,
            12,
            f"'{episode.aired_episode_number}' was not equal to expected '12'",
        )
        self.assertEqual(
            episode.episode_name,
            "Par Avion",
            f"'{episode.episode_name}' was not equal to expected 'Par Avion'",
        )
        self.assertEqual(
            episode.first_aired,
            datetime.date(2007, 3, 14),
            f"'{episode.first_aired}' was not equal to expected '{datetime.date(2007, 3, 14)}'",
        )
        self.assertEqual(
            sorted(episode.guest_stars),
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
            f"'{episode.guest_stars}' was not equal to expected '['Andrew Divoff', 'Anne Elizabeth Logan', 'Arlene Newman-Van Asperan', 'Danan Pere', 'Gabrielle Fitzpatrick', 'John Medlen', 'Julian Barnes', 'Rhett Giles']'",
        )
        self.assertEqual(
            episode.director,
            "|Paul Edwards|",
            f"'{episode.director}' was not equal to expected '|Paul Edwards|'",
        )
        self.assertEqual(
            episode.directors,
            ["Paul Edwards"],
            f"'{episode.directors}' was not equal to expected '['Paul Edwards']'",
        )
        self.assertEqual(
            sorted(episode.writers),
            ["Christina M. Kim", "Jordan Rosenberg"],
            f"'{episode.writers}' was not equal to expected '['Christina M. Kim', 'Jordan Rosenberg']'",
        )
        self.assertEqual(
            episode.overview,
            "Claire has an idea to send a message to the outside world. Charlie, however, is resistant to the idea, and Desmond tries to sabotage the plan. As Claire tries to get the truth behind their actions out of the pair, she remembers traumatic events from her past. Meanwhile, the rescue party encounters a dangerous obstacle.\r\n",
            f"'{episode.overview}' was not equal to expected 'Claire has an idea to send a message to the outside world. Charlie, however, is resistant to the idea, and Desmond tries to sabotage the plan. As Claire tries to get the truth behind their actions out of the pair, she remembers traumatic events from her past. Meanwhile, the rescue party encounters a dangerous obstacle.\r\n'",
        )
        self.assertEqual(
            episode.language.episode_name,
            "en",
            f"'{episode.language.episode_name}' was not equal to expected 'en'",
        )
        self.assertEqual(
            episode.language.overview,
            "en",
            f"'{episode.language.overview}' was not equal to expected 'en'",
        )
        self.assertIsNone(
            episode.production_code, "Episode was not expected to have production code"
        )
        self.assertEqual(
            episode.show_url,
            "http://www.tv.com/episode/934480/summary.html",
            f"'{episode.show_url}' was not equal to expected 'http://www.tv.com/episode/934480/summary.html'",
        )
        self.assertGreater(
            episode.last_updated,
            datetime.datetime(2018, 12, 28, 20, 16, 0),
            f"'{episode.last_updated}' was not greater than expected last updated '{datetime.datetime(2018, 12, 28, 20, 16, 0)}'",
        )
        self.assertIsNone(episode.dvd_disc_id, "Episode was not expected to have DVD disc ID")
        self.assertEqual(
            episode.dvd_season,
            3,
            f"'{episode.dvd_season}' was not equal to expected '3'",
        )
        self.assertEqual(
            episode.dvd_episode_number,
            12,
            f"'{episode.dvd_episode_number}' was not equal to expected '12'",
        )
        self.assertIsNone(episode.dvd_chapter, "Episode was not expected to have DVD chapter")
        self.assertEqual(
            episode.absolute_number,
            0,
            f"'{episode.absolute_number}' was not equal to expected '0'",
        )
        self.assertEqual(
            episode.file_name,
            "episodes/73739/314260.jpg",
            f"'{episode.file_name}' was not equal to expected 'episodes/73739/314260.jpg'",
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
        self.assertIsNone(episode.thumb_added, "Episode was not expected to have thumb added")
        self.assertEqual(
            episode.imdb_id,
            "tt0959403",
            f"'{episode.imdb_id}' was not equal to expected 'tt0959403'",
        )
        self.assertGreater(
            episode.site_rating_count,
            77,
            f"'{episode.site_rating_count}' was not greater than expected '77'",
        )
        # pylint: enable=line-too-long
