import copy
import unittest

from nexah.library.operations import default_review_root, load_yaml
from nexah.library.regression import run_reader_regression
from nexah.library.registry import Registry


class ReaderRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = Registry.load()
        cls.fixture = load_yaml(
            default_review_root() / "second_human_reader_review.yaml"
        )

    def test_all_six_accepted_questions_pass(self):
        report = run_reader_regression(self.registry)
        self.assertEqual("pass", report["status"])
        self.assertEqual(6, len(report["questions"]))
        self.assertEqual(0, report["failures"])

    def test_single_question_can_be_selected(self):
        report = run_reader_regression(self.registry, question_id="UQ-03")
        self.assertEqual(["UQ-03"], [item["question_id"] for item in report["questions"]])

    def test_changed_order_fails_with_clear_message(self):
        fixture = copy.deepcopy(self.fixture)
        first = fixture["questions"][0]["reader_mode"]["items"]
        first[0], first[1] = first[1], first[0]
        report = run_reader_regression(self.registry, fixture=fixture, question_id="UQ-01")
        self.assertEqual("fail", report["status"])
        self.assertIn("accepted order/state/role changed", report["questions"][0]["errors"][0])


if __name__ == "__main__":
    unittest.main()
