"""Test actors."""

import datetime

from tests.context import BaseTVDBTest


class ActorTestSuite(BaseTVDBTest):
    """Actor test cases."""

    def test_actor_parse(self):
        """Test that a show is parsed as we'd expect."""

        show_ids = [
            121361,  # Game of thrones
            295759,  # Supergirl
            73739,  # Lost
            281470,  # iZombie
        ]

        # for show_id in show_ids:
        #    _ = self.client().actors_from_show_id(show_id)

    def test_actor_properties(self):
        """Test that a specific actor parses as expected."""

        show_id = 121361  # Game of thrones
        actor_id = 440978  # Peter Dinklage

        actors = self.client().actors_from_show_id(show_id)

        actor = None

        for show_actor in actors:
            if show_actor.identifier == actor_id:
                actor = show_actor
                break

        # self.assertIsNotNone(actor, "Failed to find Peter Dinklage in Game of Thrones actors")

        # pylint: disable=line-too-long
        self.assertEqual(
            actor.image_author,
            235,
            f"'{actor.image_author}' was not equal to expected image author '235'",
        )
        self.assertEqual(
            actor.image_added,
            datetime.datetime(2017, 8, 17, 11, 12, 18),
            f"'{actor.image_added}' was not equal to expected image added '{datetime.datetime(2017, 8, 17, 11, 12, 18)}'",
        )
        self.assertEqual(
            actor.last_updated,
            datetime.datetime(2018, 3, 15, 17, 17, 44),
            f"'{actor.last_updated}' was not equal to expected last updated '{datetime.datetime(2018, 3, 15, 17, 17, 44)}'",
        )
        # pylint: enable=line-too-long
