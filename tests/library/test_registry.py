from pathlib import Path
import unittest

from nexah.library.registry import Registry


class RegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = Registry.load()

    def test_registry_is_valid(self):
        self.assertEqual([], self.registry.validate())

    def test_pilot_counts(self):
        self.assertEqual(10, len(self.registry.entities))
        self.assertEqual(17, len(self.registry.concepts))

    def test_handbook_is_a_book(self):
        handbook = self.registry.entity("NX-000003")
        self.assertEqual("book", handbook["type"])
        self.assertEqual("handbook", handbook["form"])
        self.assertEqual("practice", handbook["library_function"])

    def test_interactive_collection_is_not_registered(self):
        titles = {item["canonical_title"] for item in self.registry.entities.values()}
        self.assertNotIn("GEOMETRIA NOVA — Interactive Collection", titles)


if __name__ == "__main__":
    unittest.main()
