"""Test searching for shows."""

import datetime

from tests.context import BaseTVDBTest, libtvdb


class UtilitiesTestSuite(BaseTVDBTest):
    """Show search test cases."""

    def test_parse_date(self):
        """Test that the parse_date function parses correctly."""

        valid_test_cases = [
            ("2000-01-01", datetime.date(year=2000, month=1, day=1)),
            ("2999-12-31", datetime.date(year=2999, month=12, day=31)),
            ("2012-02-29", datetime.date(year=2012, month=2, day=29)),
        ]

        invalid_test_cases = [
            "0000-01-01",
            "2010-03-40",
            "2013-02-29",
            "2014-03",
            None,
            "",
            "2014-march-03",
            "2019-MAR-03",
        ]

        for date_string, date_value in valid_test_cases:
            self.assertEqual(date_value, libtvdb.utilities.parse_date(date_string), f"{date_string} was not equal to the expected: {date_value}")

        for date_string in invalid_test_cases:
            with self.assertRaises(ValueError):
                _ = libtvdb.utilities.parse_date(date_string)
