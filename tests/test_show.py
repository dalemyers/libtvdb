"""Test searching for shows."""

import datetime

from tests.context import BaseTVDBTest

from libtvdb.model.enums import AirDay, ShowStatus

class ShowTestSuite(BaseTVDBTest):
    """Show test cases."""

    def test_show_parse(self):
        """Test that a show is parsed as we'd expect."""

        show = self.client().show_info(73739)

        self.assertIsNotNone(show.added, f"'{show.added}' was expected to not be None")
        self.assertEqual(
            show.added_by, 1, f"'{show.added_by}' was not equal to expected added by '1'"
        )
        self.assertEqual(
            show.air_day,
            AirDay.tuesday,
            f"'{show.air_day}' was not equal to expected air_day '{AirDay.tuesday}'",
        )
        self.assertEqual(
            show.air_time,
            "9:00 PM",
            f"'{show.air_time}' was not equal to expected air time '9:00 PM'",
        )
        self.assertEqual(
            show.aliases,
            ["Lost: Missing Pieces"],
            f"'{show.aliases}' was not equal to expected aliases '{['Lost: Missing Pieces']}'",
        )
        self.assertEqual(
            show.banner,
            "graphical/73739-g4.jpg",
            f"'{show.banner}' was not equal to expected banner 'graphical/73739-g4.jpg",
        )
        self.assertEqual(
            show.first_aired,
            datetime.date(2004, 9, 22),
            f"'{show.first_aired}' was not equal to expected first_aired '{datetime.date(2004, 9, 22)}'",
        )
        self.assertEqual(
            show.genres,
            ["Action", "Adventure", "Drama", "Science Fiction"],
            f"'{show.genres}' was not equal to expected genres '{['Action', 'Adventure', 'Drama', 'Science Fiction']}'",
        )
        self.assertEqual(
            show.identifier,
            73739,
            f"'{show.identifier}' was not equal to expected identifier '73739'",
        )
        self.assertEqual(
            show.imdb_id,
            "tt0411008",
            f"'{show.imdb_id}' was not equal to expected imdb_id 'tt0411008'",
        )
        self.assertEqual(show.name, "Lost", f"'{show.name}' was not equal to expected name Lost'")
        self.assertEqual(
            show.network,
            "ABC (US)",
            f"'{show.network}' was not equal to expected network 'ABC (US)'",
        )
        self.assertEqual(
            show.network_identifier,
            "5",
            f"'{show.network_identifier}' was not equal to expected network_identifier ''",
        )
        self.assertEqual(
            show.rating, "TV-14", f"'{show.rating}' was not equal to expected rating 'TV-14'"
        )
        self.assertEqual(
            show.runtime, "45", f"'{show.runtime}' was not equal to expected runtime '45'"
        )
        self.assertEqual(
            show.series_identifier,
            "24313",
            f"'{show.series_identifier}' was not equal to expected series_identifier '24313'",
        )
        self.assertEqual(
            show.site_rating,
            9.1,
            f"'{show.site_rating}' was not equal to expected site_rating '9.1'",
        )
        self.assertEqual(show.slug, "lost", f"'{show.slug}' was not equal to expected slug 'lost")
        self.assertEqual(
            show.status,
            ShowStatus.ended,
            f"'{show.status}' was not equal to expected status '{ShowStatus.ended}'",
        )
        self.assertEqual(
            show.zap2it_id,
            "SH672362",
            f"'{show.zap2it_id}' was not equal to expected zap2it_id 'SH672362'",
        )

        self.assertGreaterEqual(
            show.last_updated,
            datetime.datetime(2018, 11, 23, 0, 28, 59),
            f"'{show.last_updated}' was not greater or equal to expected last_updated '{datetime.datetime(2018, 11, 23, 0, 28, 59)}'",
        )

        # pylint: disable=line-too-long
        self.assertEqual(
            show.overview,
            "After their plane, Oceanic Air flight 815, tore apart whilst thousands of miles off course, the survivors find themselves on a mysterious deserted island where they soon find out they are not alone.",
            f"'{show.overview}' was not equal to expected overview 'After their plane, Oceanic Air flight 815, tore apart whilst thousands of miles off course, the survivors find themselves on a mysterious deserted island where they soon find out they are not alone.'",
        )
        # pylint: enable=line-too-long
