from pathlib import Path
import unittest
from unittest.mock import patch

from nexah.library.arena import ArenaClient, compare_entity
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

    def test_user_channel_inventory_reads_every_page_and_filters_types(self):
        pages = [
            {
                "data": [
                    {"id": 1, "type": "Channel"},
                    {"id": 2, "type": "Block"},
                ],
                "meta": {"has_more_pages": True},
            },
            {
                "data": [{"id": 3, "type": "Channel"}],
                "meta": {"has_more_pages": False},
            },
        ]
        client = ArenaClient()
        with patch.object(ArenaClient, "_get", side_effect=pages) as get:
            channels = client.get_user_channels("nexah", per=100, delay=0)

        self.assertEqual([1, 3], [channel["id"] for channel in channels])
        self.assertEqual(2, get.call_count)
        self.assertEqual(1, get.call_args_list[0].args[1]["page"])
        self.assertEqual(2, get.call_args_list[1].args[1]["page"])


if __name__ == "__main__":
    unittest.main()
