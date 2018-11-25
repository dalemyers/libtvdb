"""Test authentication."""

import os
import unittest

import keyper

from tests.context import libtvdb


class AuthenticationTestSuite(unittest.TestCase):
    """Authentication test cases."""

    def _read_secret(self, secret_name):
        keychain_value = keyper.get_password(label=secret_name.lower())

        if keychain_value is not None:
            return keychain_value

        return os.environ.get(secret_name.upper())

    def test_authentication(self):
        """Test that authentication works as expected."""

        api_key = self._read_secret("libtvdb_api_key")
        user_key = self._read_secret("libtvdb_user_key")
        user_name = self._read_secret("libtvdb_user_name")

        self.assertIsNotNone(api_key)
        self.assertIsNotNone(user_key)
        self.assertIsNotNone(user_name)

        client = libtvdb.TVDBClient(
            api_key=api_key,
            user_key=user_key,
            user_name=user_name
        )

        self.assertTrue(client.authenticate(), "Failed to authenticate")


if __name__ == '__main__':
    unittest.main()