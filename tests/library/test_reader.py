import inspect
import unittest

from nexah.library.arena import ArenaClient
from nexah.library.reader import ReaderOverlay, ReaderOverlayError
from nexah.library.registry import Registry


class ReaderOverlayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = Registry.load()
        cls.overlay = ReaderOverlay.load(cls.registry)

    def test_beginner_returns_exactly_five_canonical_works_in_curated_order(self):
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
        self.assertNotIn("START", " ".join(item["title"] for item in result["items"]))
        self.assertTrue(all(item["state"] == "canonical" for item in result["items"]))

    def test_reader_mode_is_calm_and_contains_no_internal_fields(self):
        result = self.overlay.answer("UQ-03", mode="reader")
        self.assertTrue(result["orientation"])
        self.assertEqual(
            [
                "Learn the language",
                "Practice the operators",
                "Navigate the map",
                "See the laboratory",
                "Enter the synthesis",
            ],
            [item["role"] for item in result["items"]],
        )
        forbidden = {
            "score",
            "evidence",
            "technical",
            "reference",
            "operator_id",
            "object_family",
            "curatorial_slot",
            "library_function",
            "publication_status",
            "group",
        }
        for item in result["items"]:
            self.assertTrue(item["guidance"])
            self.assertTrue(forbidden.isdisjoint(item))

    def test_explain_mode_answers_reader_questions_before_technical_details(self):
        result = self.overlay.answer("UQ-02", mode="explain")
        self.assertEqual(
            ["canonical", "proposal", "proposal"],
            [item["state"] for item in result["items"]],
        )
        for item in result["items"]:
            self.assertEqual(
                {
                    "why_this_work",
                    "what_it_adds",
                    "why_here",
                    "state_note",
                    "recommendation_source",
                },
                set(item["explanation"]),
            )
            self.assertTrue(item["evidence"][0]["class"])
            self.assertTrue(item["evidence"][0]["source"])
            self.assertIn("reference", item["technical"])
        self.assertEqual("NX-000006", result["items"][0]["technical"]["reference"])
        self.assertEqual("arena:5404576", result["items"][1]["technical"]["reference"])

    def test_water_preserves_confirmed_series_order(self):
        result = self.overlay.answer("UQ-02", mode="explain")
        self.assertEqual(3, len(result["items"]))
        self.assertEqual(
            [
                "FIELD ATLAS I — WATER",
                "FIELD ATLAS II — THE ARCHITECTURE OF AGENCY",
                "FIELD ATLAS III — MORPHOLOGY",
            ],
            [item["title"] for item in result["items"]],
        )
        self.assertTrue(
            all(
                "confirmed_series" in {evidence["class"] for evidence in item["evidence"]}
                for item in result["items"]
            )
        )

    def test_after_geometria_keeps_branches_and_librarybook_last(self):
        result = self.overlay.answer("UQ-03", mode="reader")
        self.assertEqual("THE LANGUAGE BOOK", result["items"][0]["title"])
        self.assertEqual("THE OPERATOR’S HANDBOOK", result["items"][1]["title"])
        self.assertEqual("LIBRARYBOOK", result["items"][-1]["title"])
        self.assertNotIn("score", repr(result))

    def test_transition_separates_canonical_from_inferred_groups(self):
        result = self.overlay.answer("UQ-04", mode="explain")
        groups = {group["label"]: group["positions"] for group in result["groups"]}
        self.assertTrue(groups["Canonical Operator references"])
        self.assertTrue(groups["Inferred description matches"])
        for item in result["items"]:
            evidence_classes = {evidence["class"] for evidence in item["evidence"]}
            if item["state"] == "inferred":
                self.assertEqual({"inferred_description_match"}, evidence_classes)
                self.assertNotIn("canonical_operator_reference", evidence_classes)
            elif item["state"] == "canonical":
                self.assertIn("canonical_operator_reference", evidence_classes)
        self.assertIn("Inferred results", result["notice"])

    def test_navigation_distinguishes_primary_series_and_companions(self):
        result = self.overlay.answer("UQ-05", mode="explain")
        self.assertEqual("Orientation Architecture", result["items"][0]["title"])
        self.assertEqual("Primary thematic Series", result["items"][0]["role"])
        self.assertEqual(
            ["THE LANGUAGE ATLAS", "THE ATLAS OF ATLASES"],
            [item["title"] for item in result["items"][1:]],
        )
        self.assertTrue(all(item["role"] == "Companion Work" for item in result["items"][1:]))
        self.assertEqual(4, len(result["items"][0]["editorial_sequence"]))
        self.assertEqual(
            ["Primary thematic Series", "Companion Works"],
            [group["label"] for group in result["groups"]],
        )

    def test_surprise_uses_four_deterministic_curatorial_roles(self):
        first = self.overlay.answer("UQ-06")
        second = self.overlay.answer("UQ-06")
        self.assertEqual(first, second)
        self.assertEqual(4, len(first["items"]))
        self.assertEqual(
            ["Visual Work", "Field Atlas", "Handbook", "Unexpected connection"],
            [item["role"] for item in first["items"]],
        )
        self.assertEqual(4, len({item["title"] for item in first["items"]}))

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
            all(
                item["technical"]["reference"].startswith(("arena:", "series:"))
                for item in proposed
            )
        )

    def test_registry_and_operator_counts_remain_frozen(self):
        self.assertEqual(10, len(self.registry.entities))
        self.assertEqual(17, len(self.registry.concepts))

    def test_arena_client_exposes_read_methods_only(self):
        public_methods = {
            name
            for name, value in inspect.getmembers(ArenaClient, callable)
            if not name.startswith("_")
        }
        self.assertEqual(
            {"from_environment", "get_channel", "get_contents", "get_user_channels"},
            public_methods,
        )
        self.assertFalse(
            public_methods & {"post", "put", "patch", "delete", "write", "connect"}
        )


if __name__ == "__main__":
    unittest.main()
