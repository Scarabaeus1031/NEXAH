import copy
import unittest

from nexah.library.editorial import run_editorial_diff
from nexah.library.registry import Registry
from nexah.library.snapshot import sequence_fingerprint


class FakeEditorialClient:
    def __init__(self, channel, contents):
        self.channel = channel
        self.contents = contents

    def get_channel(self, channel_id):
        return self.channel

    def get_user_channels(self, user_slug):
        return [self.channel]

    def get_contents(self, channel_id):
        return self.contents


class EditorialDiffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = Registry.load()

    def baseline(self, *, updated_at="old", member_count=1, contents=None):
        contents = contents or [{"id": 1, "type": "Image", "connection": {"position": 1}}]
        return {
            "snapshot_id": "test",
            "source": {"user_slug": "nexah", "write_policy": "read_only"},
            "channels": [
                {
                    "arena_channel_id": 5442781,
                    "registered_entity_id": "NX-000002",
                    "title": "GEOMETRIA NOVA",
                    "description": "Foundation",
                    "slug": "geometria-nova",
                    "canonical_url": "https://www.are.na/nexah/geometria-nova",
                    "member_count": member_count,
                    "updated_at": updated_at,
                    "visibility": "closed",
                    "sequence_fingerprint": sequence_fingerprint(contents),
                    "visible_channel_connections": [],
                }
            ],
        }

    def channel(self, *, title="GEOMETRIA NOVA", updated_at="old", member_count=1):
        return {
            "id": 5442781,
            "title": title,
            "description": {"plain": "Foundation"},
            "slug": "geometria-nova",
            "owner": {"slug": "nexah"},
            "counts": {"contents": member_count},
            "updated_at": updated_at,
            "visibility": "closed",
        }

    def test_title_and_member_count_changes_are_detected(self):
        baseline = self.baseline()
        client = FakeEditorialClient(
            self.channel(title="GEOMETRIA NOVA II", member_count=2),
            [{"id": 1, "type": "Image", "connection": {"position": 1}}],
        )
        report = run_editorial_diff(
            self.registry, client, selector="NX-000002", baseline=baseline, checked_at="now"
        )
        categories = report["records"][0]["categories"]
        self.assertIn("metadata_change", categories)
        self.assertIn("possible_content_change", categories)

    def test_timestamp_only_is_not_automatic_edition_change(self):
        baseline = self.baseline(updated_at="old")
        client = FakeEditorialClient(self.channel(updated_at="new"), [
            {"id": 1, "type": "Image", "connection": {"position": 1}}
        ])
        report = run_editorial_diff(
            self.registry, client, selector="arena:5442781", baseline=baseline, checked_at="now"
        )
        categories = report["records"][0]["categories"]
        self.assertEqual(["metadata_change"], categories)
        self.assertNotIn("possible_content_change", categories)

    def test_sequence_change_detected_without_mutation(self):
        baseline = self.baseline()
        before = copy.deepcopy(baseline)
        registry_before = copy.deepcopy(self.registry.entities["NX-000002"])
        client = FakeEditorialClient(
            self.channel(),
            [{"id": 2, "type": "Image", "connection": {"position": 1}}],
        )
        report = run_editorial_diff(
            self.registry, client, selector="NX-000002", baseline=baseline, checked_at="now"
        )
        self.assertIn("possible_sequence_change", report["records"][0]["categories"])
        self.assertEqual(before, baseline)
        self.assertEqual(registry_before, self.registry.entities["NX-000002"])
        self.assertEqual([], report["mutations"])


if __name__ == "__main__":
    unittest.main()
