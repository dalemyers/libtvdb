"""Test authentication."""


def test_authentication(tvdb_client):
    """Test that authentication works as expected."""
    # Will throw an exception if it fails
    tvdb_client.authenticate()
