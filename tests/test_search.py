"""Test searching for shows."""

import datetime

from tests.context import BaseTVDBTest

from libtvdb.model import StatusName


class SearchTestSuite(BaseTVDBTest):
    """Show search test cases."""

    expected_shows = [
        "The Flash",
        "Doctor Who",
        "Mythbusters",
        "Only Connect",
    ]

    unexpected_shows = [
        "149FAB6D-94C1-4E93-9722-85D02272191B",
        "kj-98hpiu3bpiub-983bi",
    ]

    def test_search_expected(self):
        """Test that shows we expect to be there are found and parsed as expected."""

        for show_name in SearchTestSuite.expected_shows:
            shows = self.client().search_show(show_name)
            self.assertTrue(isinstance(shows, list))
            self.assertGreater(len(shows), 0, f"Failed to find any shows matching: {show_name}")

    def test_search_unexpected(self):
        """Test that shows we expect to not be there are not in fact there."""

        for show_name in SearchTestSuite.unexpected_shows:
            self.assertEqual(self.client().search_show(show_name), [])

    def test_show_parse_result(self):
        """Test that the show values are what we'd expect."""
        shows = self.client().search_show("Better Off Ted")
        self.assertGreater(len(shows), 0, "Failed to find any matching shows")

        filtered_shows = [show for show in shows if show.tvdb_id == "84021"]
        self.assertEqual(
            1,
            len(filtered_shows),
            "There should only be a single matching show for an ID",
        )

        show = filtered_shows[0]

        self.assertEqual(
            show.tvdb_id,
            "84021",
            f"'{show.tvdb_id}'' was not equal to expected identifier '84021'",
        )
        self.assertEqual(
            show.name,
            "Better Off Ted",
            f"'{show.name}' was not equal to expected name 'Better Off Ted'",
        )
        self.assertEqual(
            show.slug,
            "better-off-ted",
            f"'{show.slug}' was not equal to expected sluh 'Better Off Ted'",
        )
        self.assertEqual(
            show.status,
            StatusName.ENDED,
            f"'{show.status}' was not equal to expected status '{StatusName.ENDED}'",
        )
        self.assertEqual(
            show.first_air_time,
            datetime.date(2009, 3, 18),
            f"'{show.first_air_time}' was not equal to expected first_aired '{datetime.date(2009, 3, 18)}'",
        )
        self.assertEqual(
            show.aliases,
            ["Better off Ted - Die Chaos AG", "Mejor Ted"],
            f"'{show.aliases}' was not equal to expected aliases '['Better off Ted - Die Chaos AG', 'Mejor Ted']'",
        )
        self.assertEqual(
            show.network,
            "ABC (US)",
            f"'{show.network}' was not equal to expected network 'ABC (US)'",
        )
        self.assertEqual(
            show.overview[:30],
            "As the head of research and de",
            f"'{show.overview[:30]}' was not equal to expected overview fragment 'As the head of research and de'",
        )
        self.assertEqual(
            show.image_url,
            "https://artworks.thetvdb.com/banners/posters/84021-2.jpg",
            f"'{show.image_url}' was not equal to expected 'https://artworks.thetvdb.com/banners/posters/84021-2.jpg'",
        )
