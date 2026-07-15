import copy
import unittest
from unittest.mock import patch

from nexah.library.health import build_health
from nexah.library.registry import Registry
from nexah.library.release import build_release_check


class ReleaseCheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = Registry.load()

    def test_current_release_passes_with_editorial_warnings(self):
        report = build_release_check(self.registry)
        self.assertEqual("pass_with_editorial_warnings", report["result"])
        self.assertEqual([], report["structural_failures"])
        self.assertIn("Traversability", report["editorial_warnings"])
        self.assertIn("Manual cleanup", report["editorial_warnings"])

    def test_safety_breach_fails_release(self):
        manifest = copy.deepcopy(self.registry.manifest)
        manifest["write_policy"]["arena"] = "write_enabled"
        unsafe = Registry(
            self.registry.root,
            manifest,
            self.registry.entities,
            self.registry.concepts,
        )
        report = build_release_check(unsafe)
        self.assertEqual("fail", report["result"])
        self.assertIn("Safety", report["structural_failures"])

    def test_proposal_isolation_failure_fails_release(self):
        health = build_health(self.registry)
        health["proposal_isolation"]["state"] = "collapsed"
        health["failures"].append("Proposal became canonical")
        health["status"] = "fail"
        with patch("nexah.library.release.build_health", return_value=health):
            report = build_release_check(self.registry)
        self.assertEqual("fail", report["result"])
        self.assertIn("Proposal isolation", report["structural_failures"])


if __name__ == "__main__":
    unittest.main()
