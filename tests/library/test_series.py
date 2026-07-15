import copy
import unittest

from nexah.library.operations import default_review_root, load_yaml
from nexah.library.series import validate_series, validate_series_data


class SeriesValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = default_review_root()
        cls.editorial = load_yaml(root / "editorial_sequence_review.yaml")
        cls.discovery = load_yaml(root / "full_library_discovery.yaml")

    def test_current_series_have_no_structural_failures(self):
        report = validate_series()
        self.assertNotEqual("fail", report["status"])
        self.assertEqual(4, report["summary"]["confirmed"])
        self.assertEqual([], report["failures"])

    def test_duplicate_position_is_structural_failure(self):
        editorial = copy.deepcopy(self.editorial)
        editorial["series"][0]["ordered_members"][1]["position"] = 1
        report = validate_series_data(editorial, self.discovery)
        self.assertEqual("fail", report["status"])
        self.assertTrue(any("repeated ordered position" in value for value in report["failures"]))

    def test_odyssey_is_intentionally_unordered(self):
        report = validate_series()
        odyssey = next(item for item in report["series"] if item["series"] == "Odyssey 2040")
        self.assertNotEqual("fail", odyssey["status"])
        self.assertIn("intentionally unordered; no sequence enforced", odyssey["notes"])

    def test_mathematica_iv_and_xv_satellites_remain_warnings(self):
        report = validate_series()
        mathematica = next(
            item for item in report["series"] if item["series"] == "NEXAH Mathematica"
        )
        xv = next(item for item in report["series"] if item["series"] == "NEXAH XV Atlas")
        self.assertTrue(any("Mathematica IV" in value for value in mathematica["warnings"]))
        self.assertIn("ordered core 2; unordered satellites 3", xv["notes"])


if __name__ == "__main__":
    unittest.main()
