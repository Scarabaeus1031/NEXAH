import os
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

import yaml

from nexah.library.arena import ArenaClient
from nexah.library.editorial_writer import (
    ArenaEditorialClient,
    apply_editorial_plan,
    build_editorial_plan,
    run_sandbox,
)
from nexah.library.operations import OperationError
from nexah.library.snapshot import sequence_fingerprint


class MutableReader:
    def __init__(self, channels, contents):
        self.channels = channels
        self.contents = contents
        self.calls = []
        self._next_item = 9000
        self._next_connection = 19000
        for channel_id in contents:
            self._normalize(channel_id)

    def _normalize(self, channel_id):
        values = self.contents[channel_id]
        for position, item in enumerate(reversed(values), start=1):
            item.setdefault("connection", {})["position"] = position

    def get_channel(self, channel_id):
        self.calls.append(("get_channel", channel_id))
        return {"data": deepcopy(self.channels[channel_id])}

    def get_contents(self, channel_id):
        self.calls.append(("get_contents", channel_id))
        return deepcopy(self.contents[channel_id])

    def get_user_channels(self, user_slug):
        self.calls.append(("get_user_channels", user_slug))
        return [deepcopy(value) for value in self.channels.values()]

    def create_text(self, channel_id, value):
        self._next_item += 1
        self._next_connection += 1
        item = {
            "id": self._next_item,
            "type": "Text",
            "content": {"markdown": value, "plain": value},
            "connection": {"id": self._next_connection},
        }
        self.contents[channel_id].append(item)
        self._normalize(channel_id)
        return {"data": deepcopy(item)}

    def create_channel_connection(self, source_id, target_id):
        self._next_connection += 1
        target = deepcopy(self.channels[target_id])
        target["type"] = "Channel"
        target["connection"] = {"id": self._next_connection}
        self.contents[source_id].append(target)
        self._normalize(source_id)
        return {"data": [{"id": self._next_connection}]}

    def move(self, connection_id):
        for channel_id, values in self.contents.items():
            for index, item in enumerate(values):
                if item.get("connection", {}).get("id") == connection_id:
                    values.insert(0, values.pop(index))
                    self._normalize(channel_id)
                    return
        raise AssertionError(f"unknown connection {connection_id}")

    def update_description(self, channel_id, description):
        self.channels[channel_id]["description"] = {
            "markdown": description,
            "plain": description,
        }


class CoupledWriter:
    def __init__(self, reader):
        self.reader = reader
        self.calls = []

    def create_text_block(self, channel_id, value):
        self.calls.append(("create_text_block", channel_id, value))
        return self.reader.create_text(channel_id, value)

    def create_channel_connection(self, source_id, target_id):
        self.calls.append(("create_channel_connection", source_id, target_id))
        return self.reader.create_channel_connection(source_id, target_id)

    def move_connection(self, connection_id, movement):
        self.calls.append(("move_connection", connection_id, movement))
        self.reader.move(connection_id)
        return {"data": {"id": connection_id}}

    def update_description(self, channel_id, description):
        self.calls.append(("update_description", channel_id, description))
        self.reader.update_description(channel_id, description)
        return {"data": deepcopy(self.reader.channels[channel_id])}


class CoupledSandboxWriter(CoupledWriter):
    def delete_test_block(self, block_id):
        for channel_id, values in self.reader.contents.items():
            self.reader.contents[channel_id] = [
                item for item in values if item.get("id") != block_id
            ]
            self.reader._normalize(channel_id)
        return {}

    def remove_test_connection(self, connection_id):
        for channel_id, values in self.reader.contents.items():
            self.reader.contents[channel_id] = [
                item
                for item in values
                if item.get("connection", {}).get("id") != connection_id
            ]
            self.reader._normalize(channel_id)
        return {}


class EditorialWriterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "source_snapshots").mkdir()
        self.queue_path = self.root / "arena_manual_cleanup_queue.yaml"

    def tearDown(self):
        self.temp.cleanup()

    def write_sources(self, state="accepted", fingerprint=None, description="Stable"):
        queue = {
            "policy": {"command_may_update_queue": False},
            "items": [
                {
                    "id": "ACQ-001",
                    "review_state": state,
                    "affected_channel": {"arena_channel_id": 1, "title": "START"},
                    "writer": {
                        "kind": "top_sequence",
                        "entries": [
                            {"order": 10, "kind": "text", "value": "Choose a path"},
                            {"order": 20, "kind": "text", "value": "Beginner →"},
                            {
                                "order": 30,
                                "kind": "channel",
                                "target_channel_id": 2,
                                "target_title": "Guide",
                            },
                        ],
                    },
                },
                {
                    "id": "ACQ-013",
                    "review_state": state,
                    "affected_channel": {"arena_channel_id": 3, "title": "Morphology"},
                    "writer": {
                        "kind": "description_remove_exact",
                        "remove_exact": " residue",
                    },
                },
            ],
        }
        self.queue_path.write_text(yaml.safe_dump(queue), encoding="utf-8")
        base_contents = [
            {
                "id": 2,
                "type": "Channel",
                "title": "Guide",
                "connection": {"id": 102, "position": 1},
            }
        ]
        snapshot = {
            "snapshot_id": "arena-test",
            "source": {"user_slug": "test"},
            "channels": [
                {
                    "arena_channel_id": 1,
                    "sequence_fingerprint": fingerprint or sequence_fingerprint(base_contents),
                },
                {
                    "arena_channel_id": 3,
                    "sequence_fingerprint": sequence_fingerprint([]),
                    "description": description,
                },
            ],
        }
        (self.root / "source_snapshots" / "arena-test.yaml").write_text(
            yaml.safe_dump(snapshot), encoding="utf-8"
        )
        return base_contents

    @staticmethod
    def reader(base_contents, description="Stable residue"):
        channels = {
            1: {"id": 1, "type": "Channel", "title": "START", "description": None},
            2: {"id": 2, "type": "Channel", "title": "Guide", "description": None},
            3: {
                "id": 3,
                "type": "Channel",
                "title": "Morphology",
                "description": {"markdown": description, "plain": description},
            },
        }
        return MutableReader(channels, {1: deepcopy(base_contents), 3: []})

    def test_missing_write_token_is_rejected(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(OperationError, "ARENA_WRITE_TOKEN"):
                ArenaEditorialClient.from_environment()

    def test_production_writer_exposes_no_delete_or_registry_methods(self):
        public = {
            name
            for name in dir(ArenaEditorialClient)
            if not name.startswith("_")
            and callable(getattr(ArenaEditorialClient, name))
        }
        self.assertFalse(
            public
            & {
                "delete",
                "rename",
                "set_visibility",
                "set_owner",
                "update_queue",
                "update_registry",
            }
        )
        self.assertEqual(
            {
                "create_channel_connection",
                "create_text_block",
                "from_environment",
                "move_connection",
                "update_description",
            },
            public,
        )

    def test_pending_actions_are_ignored_without_live_reads(self):
        base = self.write_sources(state="pending")
        reader = self.reader(base)
        before = self.queue_path.read_bytes()
        plan = build_editorial_plan(["ACQ-001"], reader, review_root=self.root)
        self.assertEqual([], plan["accepted_actions"])
        self.assertEqual([{"id": "ACQ-001", "review_state": "pending"}], plan["ignored_actions"])
        self.assertEqual([], reader.calls)
        self.assertEqual(before, self.queue_path.read_bytes())

    def test_unknown_action_aborts(self):
        base = self.write_sources()
        with self.assertRaisesRegex(OperationError, "Unknown Action"):
            build_editorial_plan(["ACQ-999"], self.reader(base), review_root=self.root)

    def test_changed_fingerprint_aborts(self):
        base = self.write_sources(fingerprint="wrong")
        with self.assertRaisesRegex(OperationError, "changed since Snapshot"):
            build_editorial_plan(["ACQ-001"], self.reader(base), review_root=self.root)

    def test_metadata_change_since_snapshot_aborts(self):
        base = self.write_sources()
        snapshot_path = self.root / "source_snapshots" / "arena-test.yaml"
        snapshot = yaml.safe_load(snapshot_path.read_text(encoding="utf-8"))
        snapshot["channels"][0]["title"] = "Expected title"
        snapshot_path.write_text(yaml.safe_dump(snapshot), encoding="utf-8")
        with self.assertRaisesRegex(OperationError, "metadata changed"):
            build_editorial_plan(["ACQ-001"], self.reader(base), review_root=self.root)

    def test_dry_run_is_stable_and_does_not_mutate(self):
        base = self.write_sources()
        reader = self.reader(base)
        before_queue = self.queue_path.read_bytes()
        before_contents = deepcopy(reader.contents)
        first = build_editorial_plan(["ACQ-001"], reader, review_root=self.root)
        second = build_editorial_plan(["ACQ-001"], reader, review_root=self.root)
        self.assertEqual(first["plan_id"], second["plan_id"])
        self.assertEqual(0, first["mutations_performed"])
        self.assertEqual(before_queue, self.queue_path.read_bytes())
        self.assertEqual(before_contents, reader.contents)

    def test_apply_requires_exact_plan_id(self):
        base = self.write_sources()
        reader = self.reader(base)
        plan = build_editorial_plan(["ACQ-001"], reader, review_root=self.root)
        with self.assertRaisesRegex(OperationError, "Plan ID"):
            apply_editorial_plan(plan, reader, CoupledWriter(reader), approved_plan_id="wrong")

    def test_apply_builds_and_verifies_exact_top_sequence(self):
        base = self.write_sources()
        reader = self.reader(base)
        before_queue = self.queue_path.read_bytes()
        plan = build_editorial_plan(["ACQ-001"], reader, review_root=self.root)
        result = apply_editorial_plan(
            plan,
            reader,
            CoupledWriter(reader),
            approved_plan_id=plan["plan_id"],
        )
        top = reader.get_contents(1)[:3]
        self.assertEqual(["Text", "Text", "Channel"], [item["type"] for item in top])
        self.assertEqual("Choose a path", top[0]["content"]["markdown"])
        self.assertEqual("Beginner →", top[1]["content"]["markdown"])
        self.assertEqual(2, top[2]["id"])
        self.assertTrue(result["verified"])
        self.assertEqual(5, result["mutations_performed"])
        self.assertEqual(before_queue, self.queue_path.read_bytes())

    def test_description_cleanup_preserves_everything_else(self):
        base = self.write_sources(description="Stable residue")
        reader = self.reader(base, description="Stable residue")
        plan = build_editorial_plan(["ACQ-013"], reader, review_root=self.root)
        result = apply_editorial_plan(
            plan,
            reader,
            CoupledWriter(reader),
            approved_plan_id=plan["plan_id"],
        )
        self.assertEqual("Stable", reader.channels[3]["description"]["markdown"])
        self.assertEqual(1, result["mutations_performed"])

    def test_fingerprint_change_between_plan_and_apply_aborts_without_write(self):
        base = self.write_sources()
        reader = self.reader(base)
        plan = build_editorial_plan(["ACQ-001"], reader, review_root=self.root)
        reader.create_text(1, "concurrent edit")
        writer = CoupledWriter(reader)
        with self.assertRaisesRegex(OperationError, "fingerprint changed"):
            apply_editorial_plan(
                plan, reader, writer, approved_plan_id=plan["plan_id"]
            )
        self.assertEqual([], writer.calls)

    def test_existing_read_client_remains_read_only(self):
        public = {
            name
            for name in dir(ArenaClient)
            if not name.startswith("_") and callable(getattr(ArenaClient, name))
        }
        self.assertEqual(
            {"from_environment", "get_channel", "get_contents", "get_user_channels"},
            public,
        )

    def test_sandbox_cleanup_is_complete_and_private(self):
        channels = {
            2: {"id": 2, "type": "Channel", "title": "Guide", "visibility": "closed"},
            10: {
                "id": 10,
                "type": "Channel",
                "title": "NEXAH API SANDBOX",
                "visibility": "private",
            },
        }
        reader = MutableReader(channels, {10: []})
        result = run_sandbox(reader, CoupledSandboxWriter(reader), target_channel_id=2)
        self.assertEqual("pass", result["status"])
        self.assertEqual([], reader.get_contents(10))
        self.assertEqual(0, result["production_mutations"])
        self.assertEqual(5, len(result["journal"]))


if __name__ == "__main__":
    unittest.main()
