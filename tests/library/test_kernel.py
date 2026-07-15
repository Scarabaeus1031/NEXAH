from pathlib import Path
import unittest

from nexah.library.kernel import OrientationQueries, graph_to_mermaid
from nexah.library.registry import Registry


class KernelQueryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = Registry.load()
        cls.queries = OrientationQueries(cls.registry)

    def test_reading_path_starts_at_entry(self):
        path = self.queries.reading_path()
        self.assertEqual("NX-000001", path[0]["id"])
        self.assertLess(
            [item["id"] for item in path].index("NX-000002"),
            [item["id"] for item in path].index("NX-000003"),
        )

    def test_audience_path_includes_curated_next(self):
        path_ids = [item["id"] for item in self.queries.reading_path("newcomer")]
        self.assertIn("NX-000001", path_ids)
        self.assertIn("NX-000002", path_ids)
        self.assertIn("NX-000004", path_ids)

    def test_transition_operator_query(self):
        usage = self.queries.operator_usage("NX-OP-0005")
        ids = {item["id"] for item in usage["works"]}
        self.assertEqual("Transition", usage["operator"]["name"])
        self.assertIn("NX-000006", ids)
        self.assertIn("NX-000003", ids)

    def test_graph_keeps_concepts_separate(self):
        graph = self.queries.graph()
        kinds = {node["id"]: node["kind"] for node in graph["nodes"]}
        self.assertEqual("work", kinds["NX-000002"])
        self.assertEqual("concept", kinds["NX-OP-0005"])
        self.assertIn("uses_operator", {edge["type"] for edge in graph["edges"]})
        self.assertTrue(graph_to_mermaid(graph).startswith("graph TD"))

    def test_recommendations_explain_scores(self):
        recommendations = self.queries.recommendations("NX-000004")
        ids = [item.entity_id for item in recommendations]
        self.assertIn("NX-000005", ids)
        self.assertTrue(all(item.reasons for item in recommendations))


if __name__ == "__main__":
    unittest.main()
