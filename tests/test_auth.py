"""Test authentication."""

from tests.context import BaseTVDBTest


class AuthenticationTestSuite(BaseTVDBTest):
    """Authentication test cases."""

    def test_authentication(self):
        """Test that authentication works as expected."""
        self.assertTrue(self.client().authenticate(), "Failed to authenticate")
