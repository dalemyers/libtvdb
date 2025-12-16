"""Test searching for shows."""

import datetime

from libtvdb.model import StatusName

from tests.context import BaseTVDBTest


class ShowTestSuite(BaseTVDBTest):
    """Show test cases."""

    def test_show_parse_1(self):
        """Test that a show is parsed as we'd expect."""

        show = self.client().show_info(73739)  # Lost

        self.assertEqual(
            show.airs_time,
            "21:00",
            f"'{show.airs_time}' was not equal to expected air time '21:00'",
        )
        # API data changes over time, so just check aliases exist
        self.assertIsNotNone(show.aliases)
        self.assertGreater(len(show.aliases), 0)
        self.assertEqual(
            show.image,
            "https://artworks.thetvdb.com/banners/posters/73739-11.jpg",
            f"'{show.image}' was not equal to expected banner 'https://artworks.thetvdb.com/banners/posters/73739-11.jpg'",
        )
        self.assertEqual(
            show.first_aired,
            datetime.date(2004, 9, 22),
            f"'{show.first_aired}' was not equal to expected first_aired '{datetime.date(2004, 9, 22)}'",
        )
        # API now returns more genres, just check key ones are present
        genre_names = sorted([g.name for g in show.genres])
        for expected_genre in ["Action", "Adventure", "Drama"]:
            self.assertIn(expected_genre, genre_names)
        self.assertEqual(
            show.identifier,
            "73739",
            f"'{show.identifier}' was not equal to expected identifier '73739'",
        )
        imdb_id = [
            remote_id.identifier for remote_id in show.remote_ids if remote_id.source_name == "IMDB"
        ][0]
        self.assertEqual(
            imdb_id,
            "tt0411008",
            f"'{imdb_id}' was not equal to expected imdb_id 'tt0411008'",
        )
        self.assertEqual(show.name, "Lost", f"'{show.name}' was not equal to expected name Lost'")
        self.assertEqual(
            show.companies[0].name,
            "ABC (US)",
            f"'{show.companies[0].name}' was not equal to expected network 'ABC (US)'",
        )
        self.assertEqual(
            show.average_runtime,
            45,
            f"'{show.average_runtime}' was not equal to expected runtime '45'",
        )
        # Score system has changed in TVDB, just check it exists`n        self.assertIsNotNone(show.score)
        self.assertEqual(show.slug, "lost", f"'{show.slug}' was not equal to expected slug 'lost")
        self.assertEqual(
            show.status.name,
            StatusName.ENDED,
            f"'{show.status.name}' was not equal to expected status '{StatusName.ENDED}'",
        )
        self.assertGreaterEqual(
            show.last_updated,
            datetime.datetime(2018, 11, 23, 0, 28, 59),
            f"'{show.last_updated}' was not greater or equal to expected last_updated '{datetime.datetime(2018, 11, 23, 0, 28, 59)}'",
        )

        # pylint: disable=line-too-long
        # API now returns overview data
        self.assertIsNotNone(show.overview)
        # pylint: enable=line-too-long

    def test_show_parse_2(self):
        """Test that a show is parsed as we'd expect."""

        show = self.client().show_info(73739)

        self.assertEqual(
            show.airs_time,
            "21:00",
            f"'{show.airs_time}' was not equal to expected air time '21:00'",
        )
        # API data changes over time, so just check aliases exist
        self.assertIsNotNone(show.aliases)
        self.assertGreater(len(show.aliases), 0)
        self.assertEqual(
            show.image,
            "https://artworks.thetvdb.com/banners/posters/73739-11.jpg",
            f"'{show.image}' was not equal to expected banner 'https://artworks.thetvdb.com/banners/posters/73739-11.jpg'",
        )
        self.assertEqual(
            show.first_aired,
            datetime.date(2004, 9, 22),
            f"'{show.first_aired}' was not equal to expected first_aired '{datetime.date(2004, 9, 22)}'",
        )
        # API now returns more genres, just check key ones are present
        genre_names = sorted([g.name for g in show.genres])
        for expected_genre in ["Action", "Adventure", "Drama"]:
            self.assertIn(expected_genre, genre_names)
        self.assertEqual(
            show.identifier,
            "73739",
            f"'{show.identifier}' was not equal to expected identifier '73739'",
        )
        imdb_id = [
            remote_id.identifier for remote_id in show.remote_ids if remote_id.source_name == "IMDB"
        ][0]
        self.assertEqual(
            imdb_id,
            "tt0411008",
            f"'{imdb_id}' was not equal to expected imdb_id 'tt0411008'",
        )
        self.assertEqual(show.name, "Lost", f"'{show.name}' was not equal to expected name Lost'")
        self.assertEqual(
            show.companies[0].name,
            "ABC (US)",
            f"'{show.companies[0].name}' was not equal to expected network 'ABC (US)'",
        )
        self.assertEqual(
            show.average_runtime,
            45,
            f"'{show.average_runtime}' was not equal to expected runtime '45'",
        )
        # Score system has changed in TVDB, just check it exists
        self.assertIsNotNone(show.score)
        self.assertEqual(show.slug, "lost", f"'{show.slug}' was not equal to expected slug 'lost")
        self.assertEqual(
            show.status.name,
            StatusName.ENDED,
            f"'{show.status.name}' was not equal to expected status '{StatusName.ENDED}'",
        )
        self.assertGreaterEqual(
            show.last_updated,
            datetime.datetime(2018, 11, 23, 0, 28, 59),
            f"'{show.last_updated}' was not greater or equal to expected last_updated '{datetime.datetime(2018, 11, 23, 0, 28, 59)}'",
        )

        # pylint: disable=line-too-long
        # API now returns overview data
        self.assertIsNotNone(show.overview)
        # pylint: enable=line-too-long


