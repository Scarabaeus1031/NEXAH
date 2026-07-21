import tempfile
import unittest
from pathlib import Path

from nexah.library.catalog import build_website_catalog, build_work_catalog_record, write_website_catalog


class FakeArenaClient:
    def get_channel(self, channel_id):
        return {
            "id": channel_id,
            "slug": "orientation-science",
            "title": "ORIENTATION SCIENCE",
            "description": {"plain": "Research Prospectus"},
            "visibility": "public",
            "state": "available",
            "counts": {"contents": 5},
            "created_at": "2026-01-01T00:00:00Z",
            "updated_at": "2026-01-02T00:00:00Z",
        }

    def get_contents(self, channel_id, *, per=24):
        titles = ["ORIENTATION SCIENCE", "FOREWORD", "INDEX", "PART I", "APPENDIX A"]
        return [
            {
                "id": index,
                "type": "Image",
                "title": title,
                "description": None,
                "connection": {"position": 6 - index},
                "image": {
                    "src": f"https://example.test/{index}.png",
                    "width": 100,
                    "height": 150,
                    "medium": {"src": f"https://example.test/{index}-medium.png"},
                },
            }
            for index, title in enumerate(titles, start=1)
        ]


CLASSIFICATION = {
    "arena_channel_id": 1,
    "current_title": "ORIENTATION SCIENCE",
    "proposed_canonical_title": "ORIENTATION SCIENCE",
    "registered_entity_id": None,
    "classification_state": "proposed",
    "object_family": "work",
    "type": "research_report",
    "form": "prospectus",
    "library_function": "foundation",
    "publication_status": "published",
    "revision_state": "review",
    "content_maturity": "developing",
    "series": None,
    "confidence": "high",
    "human_decision": "pending",
}


class CatalogTests(unittest.TestCase):
    def test_record_preserves_source_and_marks_structural_inference(self):
        record = build_work_catalog_record(FakeArenaClient(), CLASSIFICATION)
        self.assertEqual("arena:1", record["catalog_key"])
        self.assertEqual("Research Prospectus", record["source"]["description"])
        self.assertEqual(1, len(record["structure"]["foreword"]))
        self.assertEqual(1, len(record["structure"]["index"]))
        self.assertEqual(1, len(record["structure"]["part"]))
        self.assertEqual("not_reviewed", record["evidence_policy"]["image_text"])
        self.assertEqual("research_structure", record["catalog_depth"])

    def test_writer_creates_index_and_one_record_per_work(self):
        catalog = build_website_catalog(
            FakeArenaClient(), {"records": [CLASSIFICATION]}
        )
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            write_website_catalog(catalog, output)
            self.assertTrue((output / "website_catalog.yaml").exists())
            self.assertTrue((output / "works" / "arena-1.yaml").exists())


if __name__ == "__main__":
    unittest.main()
