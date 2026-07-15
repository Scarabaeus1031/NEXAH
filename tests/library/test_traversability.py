import unittest

from nexah.library.arena import ArenaError
from nexah.library.traversability import run_traversability


class FakeClient:
    def __init__(self, responses):
        self.responses = responses
        self.calls = []

    def get_contents(self, channel_id):
        self.calls.append(channel_id)
        value = self.responses.get(channel_id, [])
        if isinstance(value, Exception):
            raise value
        return value


class TraversabilityTests(unittest.TestCase):
    def test_direct_channel_connection_is_present(self):
        client = FakeClient(
            {
                5178452: [
                    {
                        "id": 5404615,
                        "type": "Channel",
                        "title": "THE VISITOR’S GUIDE",
                        "connection": {"position": 1},
                    }
                ]
            }
        )
        report = run_traversability(client, journey="beginner", checked_at="now")
        self.assertEqual("present", report["transitions"][0]["clickable_status"])

    def test_title_only_reference_does_not_count(self):
        client = FakeClient(
            {5178452: [{"id": 99, "type": "Text", "content": "THE VISITOR’S GUIDE"}]}
        )
        report = run_traversability(client, journey="beginner", checked_at="now")
        self.assertEqual("missing", report["transitions"][0]["clickable_status"])

    def test_api_failure_is_not_reported_as_missing(self):
        client = FakeClient({5178452: ArenaError("offline")})
        report = run_traversability(client, journey="beginner", checked_at="now")
        self.assertEqual(
            "source_unavailable", report["transitions"][0]["clickable_status"]
        )

    def test_request_cache_is_in_memory_and_shared_across_journeys(self):
        client = FakeClient({})
        run_traversability(client, checked_at="now")
        self.assertEqual(1, client.calls.count(5178452))


if __name__ == "__main__":
    unittest.main()
