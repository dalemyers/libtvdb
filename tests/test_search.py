"""Test searching for shows."""

import datetime

from tests.context import BaseTVDBTest
from tests.context import libtvdb

from libtvdb.model.enums import ShowStatus


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
            with self.assertRaises(libtvdb.exceptions.NotFoundException):
                _ = self.client().search_show(show_name)

    def test_show_parse_result(self):
        """Test that the show values are what we'd expect."""
        shows = self.client().search_show("Better Off Ted")
        self.assertGreater(len(shows), 0, "Failed to find any matching shows")

        filtered_shows = [show for show in shows if show.identifier == 84021]
        self.assertEqual(1, len(filtered_shows), "There should only be a single matching show for an ID")

        show = filtered_shows[0]

        self.assertEqual(show.identifier, 84021, f"'{show.identifier}'' was not equal to expected identifier '84021'")
        self.assertEqual(show.name, "Better Off Ted", f"'{show.name}' was not equal to expected name 'Better Off Ted'")
        self.assertEqual(show.slug, "better-off-ted", f"'{show.slug}' was not equal to expected sluh 'Better Off Ted'")
        self.assertEqual(show.status, ShowStatus.ended, f"'{show.status}' was not equal to expected status '{ShowStatus.ended}'")
        self.assertEqual(show.first_aired, datetime.date(2009, 3, 18), f"'{show.first_aired}' was not equal to expected first_aired '{datetime.date(2009, 3, 18)}'")
        self.assertEqual(show.aliases, [], f"'{show.aliases}' was not equal to expected aliases '[]'")
        self.assertEqual(show.network, "ABC (US)", f"'{show.network}' was not equal to expected network 'ABC (US)'")
        self.assertEqual(show.overview[:30], "As the head of research and de", f"'{show.overview[:30]}' was not equal to expected overview fragment 'As the head of research and de'")
        self.assertEqual(show.banner, "graphical/84021-g3.jpg", f"'{show.banner}' was not equal to expected banner 'graphical/84021-g3.jpg'")
