import unittest

from nexah.library.reader import ReaderOverlay, ReaderOverlayError
from nexah.library.registry import Registry


class ReaderOverlayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = Registry.load()
        cls.overlay = ReaderOverlay.load(cls.registry)

    def test_beginner_returns_exactly_five_works_in_curated_order(self):
        result = self.overlay.answer("UQ-01")
        self.assertEqual(5, len(result["items"]))
        self.assertEqual(
            [
                "THE VISITOR’S GUIDE",
                "THE LANGUAGE BOOK",
                "GEOMETRIA NOVA",
                "THE LANGUAGE ATLAS",
                "THE OPERATOR’S HANDBOOK",
            ],
            [item["title"] for item in result["items"]],
        )
        self.assertTrue(all(item["object_family"] == "work" for item in result["items"]))

    def test_reader_mode_has_no_scores_or_provenance(self):
        result = self.overlay.answer("UQ-03", mode="reader")
        self.assertEqual(5, len(result["items"]))
        self.assertEqual(
            [
                "THE LANGUAGE BOOK",
                "THE OPERATOR’S HANDBOOK",
                "THE LANGUAGE ATLAS",
                "THE CARTOGRAPHY LABORATORY",
                "LIBRARYBOOK",
            ],
            [item["title"] for item in result["items"]],
        )
        for item in result["items"]:
            self.assertNotIn("score", item)
            self.assertNotIn("evidence", item)
            self.assertNotIn("reference", item)

    def test_explain_mode_keeps_canonical_and_proposal_visible(self):
        result = self.overlay.answer("UQ-02", mode="explain")
        self.assertEqual(
            ["canonical", "proposal", "proposal"],
            [item["state"] for item in result["items"]],
        )
        self.assertTrue(all(item["evidence"] for item in result["items"]))
        self.assertTrue(
            all(
                "confirmed_series" in {evidence["class"] for evidence in item["evidence"]}
                for item in result["items"]
            )
        )
        self.assertEqual("NX-000006", result["items"][0]["reference"])
        self.assertEqual("arena:5404576", result["items"][1]["reference"])

    def test_transition_separates_canonical_from_inferred(self):
        result = self.overlay.answer("UQ-04", mode="explain")
        states = {item["state"] for item in result["items"]}
        self.assertIn("canonical", states)
        self.assertIn("inferred", states)
        field_atlas = next(item for item in result["items"] if item.get("reference") == "NX-000006")
        self.assertEqual("canonical", field_atlas["state"])
        self.assertIn("Inferred results", result["notice"])

    def test_navigation_answer_is_topic_entry_not_only_series(self):
        result = self.overlay.answer("UQ-05", mode="explain")
        self.assertEqual("Orientation Architecture", result["items"][0]["title"])
        self.assertEqual(
            ["THE LANGUAGE ATLAS", "THE ATLAS OF ATLASES"],
            [item["title"] for item in result["items"][1:]],
        )
        self.assertEqual(4, len(result["items"][0]["sequence"]))

    def test_surprise_uses_four_distinct_curatorial_slots(self):
        result = self.overlay.answer("UQ-06")
        self.assertEqual(4, len(result["items"]))
        self.assertEqual(
            {"visual", "field_atlas", "handbook", "unexpected"},
            {item["curatorial_slot"] for item in result["items"]},
        )
        self.assertEqual(4, len({item["title"] for item in result["items"]}))

    def test_overlay_rejects_unknown_question(self):
        with self.assertRaises(ReaderOverlayError):
            self.overlay.answer("UQ-07")

    def test_overlay_never_allocates_ids_or_mutates_registry(self):
        before = set(self.registry.entities)
        for question in [f"UQ-{value:02d}" for value in range(1, 7)]:
            self.overlay.answer(question, mode="explain")
        self.assertEqual(before, set(self.registry.entities))
        proposed = [
            item
            for question in ["UQ-02", "UQ-05", "UQ-06"]
            for item in self.overlay.answer(question, mode="explain")["items"]
            if item["state"] == "proposal"
        ]
        self.assertTrue(proposed)
        self.assertTrue(
            all(item["reference"].startswith(("arena:", "series:")) for item in proposed)
        )


if __name__ == "__main__":
    unittest.main()
