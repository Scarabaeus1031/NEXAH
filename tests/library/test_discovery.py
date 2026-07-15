import unittest

from nexah.library.discovery import build_discovery, render_discovery_markdown
from nexah.library.registry import Registry


class DiscoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = Registry.load()

    def test_discovery_separates_registered_and_proposed_candidates(self):
        channels = [
            {
                "id": 5442781,
                "type": "Channel",
                "slug": "geometria-nova",
                "title": "GEOMETRIA NOVA ",
                "description": {"plain": "Foundation"},
                "counts": {"contents": 26},
                "owner": {"slug": "nexah-scarabaeus1031"},
                "visibility": "closed",
            },
            {
                "id": 999,
                "type": "Channel",
                "slug": "field-atlas-x",
                "title": "FIELD ATLAS X",
                "description": {"plain": "A field atlas"},
                "counts": {"contents": 10},
                "owner": {"slug": "nexah-scarabaeus1031"},
                "visibility": "closed",
            },
            {
                "id": 1000,
                "type": "Channel",
                "slug": "unclear",
                "title": "NEW RELEASE  UNCLEAR ",
                "description": None,
                "counts": {"contents": 1},
                "owner": {"slug": "nexah-scarabaeus1031"},
                "visibility": "closed",
            },
        ]
        discovery = build_discovery(
            self.registry, channels, user_slug="nexah-scarabaeus1031"
        )
        self.assertEqual(3, discovery["summary"]["total_public_channels"])
        self.assertEqual(1, discovery["summary"]["already_registered"])
        self.assertEqual(1, discovery["summary"]["probable_new_entities"])
        self.assertEqual(1, discovery["summary"]["needs_review"])
        unclear = next(item for item in discovery["channels"] if item["arena_channel_id"] == 1000)
        self.assertIn("temporary_release_phrase", unclear["signals"])
        self.assertIn("missing_description", unclear["signals"])
        self.assertIn("Full public inventory", render_discovery_markdown(discovery))


if __name__ == "__main__":
    unittest.main()
