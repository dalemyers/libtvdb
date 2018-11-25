"""Test searching for shows."""

from tests.context import BaseTVDBTest, libtvdb


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
            with self.assertRaises(libtvdb.exceptions.ShowNotFoundException):
                _ = self.client().search_show(show_name)
