import tempfile
import unittest
from pathlib import Path

import yaml

from nexah.library.health import build_health, render_health_text
from nexah.library.registry import Registry
from nexah.library.snapshot import (
    build_source_snapshot,
    sequence_fingerprint,
    visible_channel_connections,
)


class FakeSnapshotClient:
    def get_user_channels(self, user_slug):
        return [
            {
                "id": 5442781,
                "type": "Channel",
                "slug": "geometria-nova",
                "title": "GEOMETRIA NOVA",
                "description": {"plain": "Foundation"},
                "counts": {"contents": 2},
                "owner": {"slug": user_slug},
                "visibility": "closed",
                "updated_at": "2026-07-15T00:00:00Z",
            }
        ]

    def get_contents(self, channel_id):
        return [
            {"id": 10, "type": "Image", "connection": {"position": 2}},
            {
                "id": 20,
                "type": "Channel",
                "title": "NEXT",
                "connection": {"position": 1},
            },
        ]


class HealthAndSnapshotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = Registry.load()

    def test_health_reports_counts_and_warning_classification(self):
        report = build_health(self.registry)
        self.assertEqual(10, report["registry"]["entities"])
        self.assertEqual(17, report["registry"]["operators"])
        self.assertEqual([], report["failures"])
        self.assertEqual("pass_with_editorial_warnings", report["status"])
        self.assertIn("NEXAH Library Health", render_health_text(report))

    def test_health_structural_failure_is_separate_from_warning(self):
        manifest = dict(self.registry.manifest)
        manifest["write_policy"] = {"arena": "write_enabled"}
        unsafe = Registry(
            self.registry.root,
            manifest,
            self.registry.entities,
            self.registry.concepts,
        )
        report = build_health(unsafe)
        self.assertEqual("fail", report["status"])
        self.assertTrue(any("read_only" in failure for failure in report["failures"]))

    def test_snapshot_records_sequence_and_direct_connections(self):
        snapshot = build_source_snapshot(
            self.registry,
            FakeSnapshotClient(),
            observed_at="2026-07-15T12:00:00+00:00",
        )
        self.assertEqual(1, snapshot["summary"]["channels"])
        record = snapshot["channels"][0]
        self.assertEqual(64, len(record["sequence_fingerprint"]))
        self.assertEqual(
            [{"arena_channel_id": 20, "title": "NEXT", "position": 1}],
            record["visible_channel_connections"],
        )
        self.assertEqual("read_only", snapshot["source"]["write_policy"])

    def test_sequence_fingerprint_changes_with_observed_order(self):
        first = [
            {"id": 1, "type": "Image", "connection": {"position": 1}},
            {"id": 2, "type": "Image", "connection": {"position": 2}},
        ]
        self.assertNotEqual(sequence_fingerprint(first), sequence_fingerprint(list(reversed(first))))
        self.assertEqual([], visible_channel_connections(first))


if __name__ == "__main__":
    unittest.main()
