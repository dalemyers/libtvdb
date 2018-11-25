from context import libtvdb
import unittest

import keyper


class AuthenticationTestSuite(unittest.TestCase):
    """Authentication test cases."""

    def test_authentication(self):

        api_key = keyper.get_password(label="libtvdb_api_key")
        user_key = keyper.get_password(label="libtvdb_user_key")
        user_name = keyper.get_password(label="libtvdb_user_name")

        client = libtvdb.TVDBClient(
            api_key=api_key,
            user_key=user_key,
            user_name=user_name
        )

        self.assertTrue(client._authenticate(), "Failed to authenticate")


if __name__ == '__main__':
    unittest.main()