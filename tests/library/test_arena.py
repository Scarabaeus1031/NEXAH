from pathlib import Path
import unittest

from nexah.library.arena import compare_entity
from nexah.library.registry import Registry


class FakeArenaClient:
    def get_channel(self, slug):
        return {
            "id": 5442781,
            "slug": "geometria-nova",
            "title": "GEOMETRIA NOVA ",
            "updated_at": "2026-07-15T01:35:23Z",
            "counts": {"contents": 26},
        }

    def get_contents(self, slug):
        return []


class ArenaComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = Registry.load()

    def test_normalized_title_and_metadata_match(self):
        result = compare_entity(self.registry, "NX-000002", FakeArenaClient())
        self.assertEqual("current", result["state"])
        self.assertEqual([], result["differences"])

    def test_difference_is_reported_without_mutation(self):
        client = FakeArenaClient()
        original = client.get_channel

        class StaleClient(FakeArenaClient):
            def get_channel(self, slug):
                data = super().get_channel(slug)
                data["counts"] = {"contents": 27}
                return data

        result = compare_entity(self.registry, "NX-000002", StaleClient())
        self.assertEqual("stale", result["state"])
        self.assertEqual("member_count", result["differences"][0]["field"])
        self.assertIs(client.get_channel.__func__, original.__func__)


if __name__ == "__main__":
    unittest.main()
