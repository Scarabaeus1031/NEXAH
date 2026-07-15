import copy
import tempfile
import unittest
from pathlib import Path

import yaml

from nexah.library.cleanup import cleanup_status
from nexah.library.operations import default_review_root, load_yaml


class CleanupStatusTests(unittest.TestCase):
    def test_current_queue_has_stable_keys_and_valid_states(self):
        report = cleanup_status()
        self.assertEqual("pass", report["status"])
        self.assertEqual(16, report["summary"]["total"])
        self.assertEqual(16, report["summary"]["open"])
        self.assertEqual("ACQ-001", report["items"][0]["id"])
        self.assertEqual("ACQ-016", report["items"][-1]["id"])

    def test_invalid_state_fails_without_allocating_entity_id(self):
        queue = load_yaml(default_review_root() / "arena_manual_cleanup_queue.yaml")
        queue = copy.deepcopy(queue)
        queue["items"][0]["review_state"] = "done_automatically"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "arena_manual_cleanup_queue.yaml").write_text(
                yaml.safe_dump(queue, sort_keys=False), encoding="utf-8"
            )
            report = cleanup_status(review_root=root)
        self.assertEqual("fail", report["status"])
        self.assertFalse(any(item["id"].startswith("NX-") for item in report["items"]))

    def test_cleanup_status_does_not_modify_queue(self):
        path = default_review_root() / "arena_manual_cleanup_queue.yaml"
        before = path.read_bytes()
        cleanup_status()
        self.assertEqual(before, path.read_bytes())


if __name__ == "__main__":
    unittest.main()
