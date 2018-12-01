"""Shared context information for all tests."""

import sys
import os
from typing import ClassVar, Optional
import unittest

import keyper

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#pylint: disable=wrong-import-position
import libtvdb
#pylint: enable=wrong-import-position


class BaseTVDBTest(unittest.TestCase):
    """Base class for TVDB test cases."""

    _client: ClassVar[Optional[libtvdb.TVDBClient]] = None

    @classmethod
    def setUpClass(cls):
        """Setup the test class."""

        api_key = BaseTVDBTest._read_secret("libtvdb_api_key")
        user_key = BaseTVDBTest._read_secret("libtvdb_user_key")
        user_name = BaseTVDBTest._read_secret("libtvdb_user_name")

        if api_key is None:
            raise Exception("Faield to get API Key")

        if user_key is None:
            raise Exception("Faield to get user Key")

        if user_name is None:
            raise Exception("Faield to get user name")

        BaseTVDBTest._client = libtvdb.TVDBClient(
            api_key=api_key,
            user_key=user_key,
            user_name=user_name
        )

    @classmethod
    def _read_secret(cls, secret_name):
        keychain_value = keyper.get_password(label=secret_name.lower())

        if keychain_value is not None:
            return keychain_value

        return os.environ.get(secret_name.upper())

    #pylint: disable=no-self-use
    def client(self) -> libtvdb.TVDBClient:
        """A class reference to the client to clean up the tests."""
        if BaseTVDBTest._client is None:
            raise Exception("Client was not set")
        return BaseTVDBTest._client
    #pylint: enable=no-self-use
