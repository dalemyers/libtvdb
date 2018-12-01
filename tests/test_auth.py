"""Test authentication."""

from tests.context import BaseTVDBTest


class AuthenticationTestSuite(BaseTVDBTest):
    """Authentication test cases."""

    def test_authentication(self):
        """Test that authentication works as expected."""

        # Will throw an exception if it fails
        self.client().authenticate()
