from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from .arena import ArenaClient, ArenaError
from .operations import OperationError, default_review_root, latest_snapshot, load_yaml
from .snapshot import sequence_fingerprint


BATCH_01_ACTIONS = ("ACQ-001", "ACQ-002", "ACQ-006", "ACQ-013")
ALLOWED_OPERATION_TYPES = {
    "create_text_block",
    "create_channel_connection",
    "move_connection",
    "update_description",
}
SANDBOX_TITLE = "NEXAH API SANDBOX"
SANDBOX_TEST_TEXT = "NEXAH editorial writer sandbox test"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _response_data(payload: dict[str, Any]) -> Any:
    return payload.get("data", payload)


def _markdown_value(item: dict[str, Any], field: str) -> str:
    value = item.get(field)
    if isinstance(value, dict):
        return str(value.get("markdown") or value.get("plain") or "").strip()
    return str(value or "").strip()


def _channel_description(channel: dict[str, Any]) -> str:
    value = channel.get("description")
    if isinstance(value, dict):
        return str(value.get("plain") or value.get("markdown") or "").strip()
    return str(value or "").strip()


def _channel_description_markdown(channel: dict[str, Any]) -> str:
    return _markdown_value(channel, "description")


def _connection_id(item: dict[str, Any]) -> int:
    value = item.get("connection", {}).get("id")
    if not isinstance(value, int):
        raise OperationError(f"Are.na item {item.get('id')} has no Connection ID")
    return value


@dataclass(frozen=True)
class ArenaEditorialClient:
    """Write-only Are.na surface for approved editorial operations.

    The existing ArenaClient remains the sole read connector. This client has no
    delete, rename, visibility, ownership, Registry, or queue mutation methods.
    """

    token: str
    base_url: str = "https://api.are.na/v3"
    timeout: float = 30.0

    @classmethod
    def from_environment(cls) -> "ArenaEditorialClient":
        token = os.environ.get("ARENA_WRITE_TOKEN", "").strip()
        if not token:
            raise OperationError("ARENA_WRITE_TOKEN is required for --apply")
        return cls(token=token)

    def _request(self, method: str, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        if method not in {"POST", "PUT"}:
            raise OperationError(f"Editorial Writer forbids HTTP method {method}")
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        request = Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "User-Agent": "nexah-library-editorial-writer/1.0",
            },
            method=method,
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                return json.load(response)
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise ArenaError(
                f"Are.na {method} {path} failed with HTTP {exc.code}: {body[:300]}"
            ) from exc
        except (URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise ArenaError(f"Are.na {method} {path} failed: {exc}") from exc

    def create_text_block(self, channel_id: int, value: str) -> dict[str, Any]:
        return self._request(
            "POST",
            "blocks",
            {"value": value, "channels": [{"id": channel_id}]},
        )

    def create_channel_connection(
        self, source_channel_id: int, target_channel_id: int
    ) -> dict[str, Any]:
        return self._request(
            "POST",
            "connections",
            {
                "connectable_id": target_channel_id,
                "connectable_type": "Channel",
                "channels": [{"id": source_channel_id}],
            },
        )

    def move_connection(self, connection_id: int, movement: str) -> dict[str, Any]:
        if movement not in {"move_to_top", "move_to_bottom", "move_up", "move_down"}:
            raise OperationError(f"Editorial Writer forbids movement {movement}")
        return self._request(
            "POST", f"connections/{connection_id}/move", {"movement": movement}
        )

    def update_description(self, channel_id: int, description: str) -> dict[str, Any]:
        return self._request(
            "PUT", f"channels/{quote(str(channel_id), safe='')}", {"description": description}
        )


@dataclass(frozen=True)
class ArenaSandboxClient(ArenaEditorialClient):
    """Destructive test cleanup isolated from the production writer surface."""

    def _sandbox_request(
        self, method: str, path: str, payload: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        request = Request(
            url,
            data=(json.dumps(payload).encode("utf-8") if payload is not None else None),
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "User-Agent": "nexah-library-editorial-sandbox/1.0",
            },
            method=method,
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                body = response.read()
                return json.loads(body) if body else {}
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise ArenaError(
                f"Are.na sandbox {method} {path} failed with HTTP {exc.code}: {body[:300]}"
            ) from exc
        except (URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise ArenaError(f"Are.na sandbox {method} {path} failed: {exc}") from exc

    def create_private_channel(self) -> dict[str, Any]:
        return self._sandbox_request(
            "POST", "channels", {"title": SANDBOX_TITLE, "visibility": "private"}
        )

    def remove_test_connection(self, connection_id: int) -> dict[str, Any]:
        return self._sandbox_request("DELETE", f"connections/{connection_id}")

def _queue_items(root: Path) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    queue = load_yaml(root / "arena_manual_cleanup_queue.yaml")
    if queue.get("policy", {}).get("command_may_update_queue") is not False:
        raise OperationError("Editorial Writer requires a read-only Action Queue")
    items = queue.get("items", [])
    by_id = {item.get("id"): item for item in items}
    if len(by_id) != len(items):
        raise OperationError("Editorial Writer refuses a Queue with duplicate Action IDs")
    return queue, by_id


def _snapshot_record(snapshot: dict[str, Any], channel_id: int) -> dict[str, Any]:
    matches = [
        record
        for record in snapshot.get("channels", [])
        if record.get("arena_channel_id") == channel_id
    ]
    if len(matches) != 1:
        raise OperationError(
            f"Channel {channel_id} is missing or duplicated in the verified Source Snapshot"
        )
    return matches[0]


def _assert_channel_matches_snapshot(
    channel: dict[str, Any], baseline: dict[str, Any], channel_id: int
) -> None:
    checks = {
        "title": channel.get("title"),
        "description": _channel_description(channel),
        "slug": channel.get("slug"),
        "visibility": channel.get("visibility"),
        "member_count": channel.get("counts", {}).get("contents"),
        "updated_at": channel.get("updated_at"),
    }
    changed = [
        field
        for field, live_value in checks.items()
        if field in baseline and baseline.get(field) != live_value
    ]
    if changed:
        raise OperationError(
            f"Channel {channel_id} metadata changed since Source Snapshot: {', '.join(changed)}"
        )


def _plan_id(value: dict[str, Any]) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _validate_writer_action(action: dict[str, Any]) -> None:
    action_id = action.get("id")
    writer = action.get("writer")
    if not isinstance(writer, dict):
        raise OperationError(f"{action_id}: accepted Action has no structured writer plan")
    kind = writer.get("kind")
    if kind not in {"top_sequence", "description_remove_exact"}:
        raise OperationError(f"{action_id}: unsupported writer plan {kind}")
    if kind == "top_sequence":
        entries = writer.get("entries")
        if not isinstance(entries, list) or not entries:
            raise OperationError(f"{action_id}: top_sequence must contain entries")
        for entry in entries:
            if entry.get("kind") not in {"text", "channel"}:
                raise OperationError(f"{action_id}: unsupported sequence entry")
            if not isinstance(entry.get("order"), int):
                raise OperationError(f"{action_id}: sequence entry needs integer order")
    if kind == "description_remove_exact" and not writer.get("remove_exact"):
        raise OperationError(f"{action_id}: description cleanup needs remove_exact")


def build_editorial_plan(
    action_ids: list[str] | tuple[str, ...],
    reader: ArenaClient,
    *,
    review_root: Path | str | None = None,
) -> dict[str, Any]:
    root = Path(review_root) if review_root else default_review_root()
    _, by_id = _queue_items(root)
    requested = list(dict.fromkeys(action_ids))
    unknown = sorted(set(requested) - set(by_id))
    if unknown:
        raise OperationError(f"Unknown Action ID(s): {', '.join(unknown)}")
    accepted = [by_id[action_id] for action_id in requested if by_id[action_id].get("review_state") == "accepted"]
    ignored = [
        {"id": action_id, "review_state": by_id[action_id].get("review_state")}
        for action_id in requested
        if by_id[action_id].get("review_state") != "accepted"
    ]
    for action in accepted:
        _validate_writer_action(action)

    snapshot_path = latest_snapshot(root)
    if snapshot_path is None:
        raise OperationError("Editorial Writer requires a verified Source Snapshot")
    snapshot = load_yaml(snapshot_path)

    grouped: dict[int, list[dict[str, Any]]] = {}
    descriptions: list[dict[str, Any]] = []
    for action in accepted:
        channel_id = action.get("affected_channel", {}).get("arena_channel_id")
        if not isinstance(channel_id, int):
            raise OperationError(f"{action.get('id')}: affected Channel ID is missing")
        writer = action["writer"]
        if writer["kind"] == "top_sequence":
            for entry in writer["entries"]:
                grouped.setdefault(channel_id, []).append({**entry, "action_id": action["id"]})
        else:
            descriptions.append(
                {
                    "action_id": action["id"],
                    "operation": "update_description",
                    "channel_id": channel_id,
                    "remove_exact": writer["remove_exact"],
                }
            )

    channel_plans: list[dict[str, Any]] = []
    for channel_id, entries in sorted(grouped.items()):
        baseline = _snapshot_record(snapshot, channel_id)
        live_contents = reader.get_contents(channel_id)
        live_fingerprint = sequence_fingerprint(live_contents)
        if live_fingerprint != baseline.get("sequence_fingerprint"):
            raise OperationError(
                f"Channel {channel_id} changed since Snapshot {snapshot.get('snapshot_id')}; aborting"
            )
        live_channel = _response_data(reader.get_channel(channel_id))
        if live_channel.get("id") != channel_id:
            raise OperationError(f"Channel {channel_id} is unavailable")
        _assert_channel_matches_snapshot(live_channel, baseline, channel_id)
        desired = sorted(entries, key=lambda item: (item["order"], item["action_id"]))
        operations: list[dict[str, Any]] = []
        resolved: list[dict[str, Any]] = []
        for entry in desired:
            if entry["kind"] == "text":
                matches = [
                    item
                    for item in live_contents
                    if item.get("type") == "Text"
                    and _markdown_value(item, "content") == str(entry.get("value", "")).strip()
                ]
                if len(matches) > 1:
                    raise OperationError(
                        f"Channel {channel_id} contains duplicate text marker {entry.get('value')!r}"
                    )
                if matches:
                    item = matches[0]
                    resolved.append({**entry, "item_id": item["id"], "connection_id": _connection_id(item)})
                else:
                    operations.append(
                        {
                            "action_id": entry["action_id"],
                            "operation": "create_text_block",
                            "channel_id": channel_id,
                            "value": entry["value"],
                        }
                    )
                    resolved.append({**entry, "item_id": None, "connection_id": None})
            else:
                target_id = entry.get("target_channel_id")
                matches = [
                    item
                    for item in live_contents
                    if item.get("type") == "Channel" and item.get("id") == target_id
                ]
                if len(matches) > 1:
                    raise OperationError(
                        f"Channel {channel_id} contains duplicate connection to {target_id}"
                    )
                if matches:
                    item = matches[0]
                    resolved.append({**entry, "item_id": item["id"], "connection_id": _connection_id(item)})
                else:
                    operations.append(
                        {
                            "action_id": entry["action_id"],
                            "operation": "create_channel_connection",
                            "channel_id": channel_id,
                            "target_channel_id": target_id,
                        }
                    )
                    resolved.append({**entry, "item_id": target_id, "connection_id": None})
        operations.extend(
            {
                "action_id": entry["action_id"],
                "operation": "move_connection",
                "channel_id": channel_id,
                "movement": "move_to_top",
                "entry": {
                    key: entry.get(key)
                    for key in ["kind", "value", "target_channel_id", "order"]
                    if entry.get(key) is not None
                },
            }
            for entry in reversed(resolved)
        )
        channel_plans.append(
            {
                "channel_id": channel_id,
                "title": live_channel.get("title"),
                "expected_fingerprint": live_fingerprint,
                "desired_top_sequence": desired,
                "operations": operations,
            }
        )

    for operation in descriptions:
        channel_id = operation["channel_id"]
        baseline = _snapshot_record(snapshot, channel_id)
        live_contents = reader.get_contents(channel_id)
        live_fingerprint = sequence_fingerprint(live_contents)
        if live_fingerprint != baseline.get("sequence_fingerprint"):
            raise OperationError(
                f"Channel {channel_id} changed since Snapshot {snapshot.get('snapshot_id')}; aborting"
            )
        live_channel = _response_data(reader.get_channel(channel_id))
        if live_channel.get("id") != channel_id:
            raise OperationError(f"Channel {channel_id} is unavailable")
        _assert_channel_matches_snapshot(live_channel, baseline, channel_id)
        current = _channel_description_markdown(live_channel)
        fragment = operation["remove_exact"]
        if current.count(fragment) != 1:
            raise OperationError(
                f"{operation['action_id']}: expected description fragment occurs {current.count(fragment)} times"
            )
        operation["before"] = current
        operation["after"] = current.replace(fragment, "", 1).rstrip()
        channel_plans.append(
            {
                "channel_id": channel_id,
                "title": live_channel.get("title"),
                "expected_fingerprint": live_fingerprint,
                "desired_top_sequence": [],
                "operations": [operation],
            }
        )

    plan_core = {
        "batch": "BATCH-01" if tuple(requested) == BATCH_01_ACTIONS else "custom",
        "baseline": snapshot.get("snapshot_id"),
        "baseline_file": snapshot_path.name,
        "requested_actions": requested,
        "accepted_actions": [item["id"] for item in accepted],
        "ignored_actions": ignored,
        "channels": channel_plans,
    }
    return {
        "schema_version": "1.0",
        "report_type": "editorial_write_plan",
        "mode": "dry_run",
        "write_policy": "explicit_apply_only",
        "plan_id": _plan_id(plan_core),
        **plan_core,
        "allowed_operations": sorted(ALLOWED_OPERATION_TYPES),
        "mutations_performed": 0,
    }


def _find_entry(contents: list[dict[str, Any]], entry: dict[str, Any]) -> dict[str, Any]:
    if entry["kind"] == "text":
        matches = [
            item
            for item in contents
            if item.get("type") == "Text"
            and _markdown_value(item, "content") == str(entry["value"]).strip()
        ]
    else:
        matches = [
            item
            for item in contents
            if item.get("type") == "Channel" and item.get("id") == entry["target_channel_id"]
        ]
    if len(matches) != 1:
        raise OperationError(f"Cannot resolve exactly one live item for {entry}")
    return matches[0]


def apply_editorial_plan(
    plan: dict[str, Any],
    reader: ArenaClient,
    writer: ArenaEditorialClient,
    *,
    approved_plan_id: str,
) -> dict[str, Any]:
    if approved_plan_id != plan.get("plan_id"):
        raise OperationError("Approved Plan ID does not match the current Dry Run")
    if not plan.get("accepted_actions"):
        raise OperationError("No accepted Actions are eligible for --apply")
    journal: list[dict[str, Any]] = []

    for channel_plan in plan["channels"]:
        channel_id = channel_plan["channel_id"]
        expected = channel_plan["expected_fingerprint"]

        def guard() -> list[dict[str, Any]]:
            contents = reader.get_contents(channel_id)
            observed = sequence_fingerprint(contents)
            if observed != expected:
                raise OperationError(
                    f"Channel {channel_id} fingerprint changed before mutation; aborting"
                )
            return contents

        for operation in channel_plan["operations"]:
            before_contents = guard()
            before_fingerprint = expected
            kind = operation["operation"]
            if kind == "create_text_block":
                writer.create_text_block(channel_id, operation["value"])
            elif kind == "create_channel_connection":
                writer.create_channel_connection(channel_id, operation["target_channel_id"])
            elif kind == "move_connection":
                item = _find_entry(before_contents, operation["entry"])
                writer.move_connection(_connection_id(item), operation["movement"])
            elif kind == "update_description":
                live = _response_data(reader.get_channel(channel_id))
                if _channel_description_markdown(live) != operation["before"]:
                    raise OperationError(
                        f"Channel {channel_id} description changed before mutation; aborting"
                    )
                writer.update_description(channel_id, operation["after"])
            else:
                raise OperationError(f"Forbidden operation {kind}")

            after_contents = reader.get_contents(channel_id)
            after_fingerprint = sequence_fingerprint(after_contents)
            if kind == "update_description":
                verified = _channel_description_markdown(
                    _response_data(reader.get_channel(channel_id))
                )
                if verified != operation["after"]:
                    raise OperationError(f"Channel {channel_id} description verification failed")
                if after_fingerprint != before_fingerprint:
                    raise OperationError(
                        f"Channel {channel_id} sequence changed during description update"
                    )
            else:
                if kind.startswith("create_") and after_fingerprint == before_fingerprint:
                    raise OperationError(f"Channel {channel_id} mutation was not observable")
            expected = after_fingerprint
            journal.append(
                {
                    "action_id": operation["action_id"],
                    "operation": kind,
                    "channel_id": channel_id,
                    "before_fingerprint": before_fingerprint,
                    "after_fingerprint": after_fingerprint,
                    "verified": True,
                }
            )

        desired = channel_plan.get("desired_top_sequence", [])
        if desired:
            final_contents = reader.get_contents(channel_id)
            expected_ids = [_find_entry(final_contents, item)["id"] for item in desired]
            observed_ids = [item.get("id") for item in final_contents[: len(expected_ids)]]
            if observed_ids != expected_ids:
                raise OperationError(f"Channel {channel_id} final top sequence verification failed")

    return {
        **plan,
        "mode": "apply",
        "applied_at": _utc_now(),
        "mutations_performed": len(journal),
        "journal": journal,
        "verified": True,
    }


def run_sandbox(
    reader: ArenaClient,
    client: ArenaSandboxClient,
    *,
    target_channel_id: int = 5404615,
) -> dict[str, Any]:
    """Run destructive API checks only inside a private, purpose-built Channel."""
    channels = reader.get_user_channels("nexah-scarabaeus1031")
    matches = [channel for channel in channels if channel.get("title") == SANDBOX_TITLE]
    if len(matches) > 1:
        raise OperationError("Multiple NEXAH API SANDBOX Channels exist")
    if matches:
        sandbox = matches[0]
    else:
        sandbox = _response_data(client.create_private_channel())
    if sandbox.get("visibility") != "private":
        raise OperationError("Sandbox Channel must be private")
    sandbox_id = sandbox.get("id")
    if not isinstance(sandbox_id, int):
        raise OperationError("Sandbox Channel creation returned no ID")

    journal: list[dict[str, Any]] = []
    baseline = reader.get_contents(sandbox_id)
    expected = sequence_fingerprint(baseline)

    created = _response_data(client.create_text_block(sandbox_id, SANDBOX_TEST_TEXT))
    created_id = created.get("id")
    after_create = reader.get_contents(sandbox_id)
    created_items = [item for item in after_create if item.get("id") == created_id]
    if len(created_items) != 1:
        raise OperationError("Sandbox text block verification failed")
    journal.append(
        {
            "operation": "create_text_block",
            "block_id": created_id,
            "connection_id": _connection_id(created_items[0]),
            "verified": True,
        }
    )
    expected = sequence_fingerprint(after_create)

    if sequence_fingerprint(reader.get_contents(sandbox_id)) != expected:
        raise OperationError("Sandbox fingerprint changed before text cleanup")
    client.remove_test_connection(_connection_id(created_items[0]))
    after_delete = reader.get_contents(sandbox_id)
    if any(item.get("id") == created_id for item in after_delete):
        raise OperationError("Sandbox test block cleanup failed")
    journal.append(
        {
            "operation": "remove_test_block_connection",
            "block_id": created_id,
            "connection_id": _connection_id(created_items[0]),
            "verified": True,
            "sandbox_only": True,
            "api_semantics": "Are.na removes a Block from a Channel by destroying its Connection",
        }
    )
    expected = sequence_fingerprint(after_delete)

    if sequence_fingerprint(reader.get_contents(sandbox_id)) != expected:
        raise OperationError("Sandbox fingerprint changed before connection test")
    response = _response_data(client.create_channel_connection(sandbox_id, target_channel_id))
    connections = response if isinstance(response, list) else [response]
    if len(connections) != 1 or not isinstance(connections[0].get("id"), int):
        raise OperationError("Sandbox connection creation returned no Connection ID")
    connection_id = connections[0]["id"]
    after_connection = reader.get_contents(sandbox_id)
    target = _find_entry(
        after_connection, {"kind": "channel", "target_channel_id": target_channel_id}
    )
    journal.append(
        {
            "operation": "create_channel_connection",
            "connection_id": connection_id,
            "verified": True,
        }
    )
    expected = sequence_fingerprint(after_connection)

    if sequence_fingerprint(reader.get_contents(sandbox_id)) != expected:
        raise OperationError("Sandbox fingerprint changed before move test")
    client.move_connection(_connection_id(target), "move_to_top")
    after_move = reader.get_contents(sandbox_id)
    if not after_move or after_move[0].get("id") != target_channel_id:
        raise OperationError("Sandbox move-to-top verification failed")
    journal.append(
        {
            "operation": "move_connection",
            "connection_id": connection_id,
            "verified": True,
        }
    )
    expected = sequence_fingerprint(after_move)

    if sequence_fingerprint(reader.get_contents(sandbox_id)) != expected:
        raise OperationError("Sandbox fingerprint changed before connection cleanup")
    client.remove_test_connection(connection_id)
    after_remove = reader.get_contents(sandbox_id)
    if any(item.get("id") == target_channel_id for item in after_remove):
        raise OperationError("Sandbox test connection cleanup failed")
    journal.append(
        {
            "operation": "remove_test_connection",
            "connection_id": connection_id,
            "verified": True,
            "sandbox_only": True,
        }
    )

    return {
        "schema_version": "1.0",
        "report_type": "editorial_writer_sandbox",
        "sandbox_channel_id": sandbox_id,
        "sandbox_title": SANDBOX_TITLE,
        "visibility": "private",
        "status": "pass",
        "journal": journal,
        "production_mutations": 0,
    }


def run_batch_aftercare(
    registry: Any,
    applied: dict[str, Any],
    reader: ArenaClient,
    before_traversability: dict[str, Any],
    *,
    review_root: Path | str | None = None,
    report_path: Path | str | None = None,
) -> dict[str, Any]:
    """Capture the immutable post-write evidence and render Batch 01 verification."""
    from .editorial import run_editorial_diff
    from .health import build_health
    from .release import build_release_check
    from .snapshot import build_source_snapshot, write_source_snapshot
    from .traversability import run_traversability

    root = Path(review_root) if review_root else default_review_root()
    baseline_path = root / "source_snapshots" / applied["baseline_file"]
    baseline = load_yaml(baseline_path)
    checked = _utc_now()
    stamp = checked.replace(":", "").replace("+00:00", "Z")
    snapshot_path = root / "source_snapshots" / f"arena-{stamp}.yaml"
    snapshot = build_source_snapshot(
        registry,
        reader,
        user_slug=baseline.get("source", {}).get("user_slug", "nexah-scarabaeus1031"),
        observed_at=checked,
    )
    snapshot["snapshot_id"] = f"arena-{stamp}"
    write_source_snapshot(snapshot, snapshot_path)

    after_traversability = run_traversability(reader, review_root=root, checked_at=checked)
    editorial_diff = run_editorial_diff(
        registry,
        reader,
        review_root=root,
        baseline=baseline,
        checked_at=checked,
    )
    health = build_health(registry, review_root=root)
    release = build_release_check(registry, review_root=root)

    expected_channels = {item["channel_id"] for item in applied.get("journal", [])}
    deviations = [
        record
        for record in editorial_diff["records"]
        if record["categories"] != ["no_change"]
        and record["arena_channel_id"] not in expected_channels
    ]
    warnings = list(health.get("warnings", []))
    if deviations:
        warnings.append(f"{len(deviations)} unexpected Channel differences require review")
    errors = list(health.get("failures", []))
    if release.get("result") == "fail":
        errors.append("release-check failed")

    result = {
        "batch": applied.get("batch"),
        "plan_id": applied.get("plan_id"),
        "applied_at": applied.get("applied_at"),
        "actions": applied.get("accepted_actions", []),
        "journal": applied.get("journal", []),
        "snapshot_id": snapshot["snapshot_id"],
        "snapshot_file": str(snapshot_path),
        "traversability_before": before_traversability.get("summary", {}),
        "traversability_after": after_traversability.get("summary", {}),
        "editorial_diff": editorial_diff.get("summary", {}),
        "health": health.get("status"),
        "release_check": release.get("result"),
        "warnings": warnings,
        "errors": errors,
        "deviations": deviations,
        "queue_modified": False,
    }
    output = Path(report_path) if report_path else root / "BATCH_01_VERIFICATION.md"
    output.write_text(render_batch_verification(result), encoding="utf-8")
    result["report"] = str(output)
    return result


def run_sandbox_aftercare(
    registry: Any,
    reader: ArenaClient,
    *,
    review_root: Path | str | None = None,
) -> dict[str, Any]:
    """Run the required read-only operational checks after a successful Batch 0."""
    from .editorial import run_editorial_diff
    from .health import build_health
    from .release import build_release_check
    from .snapshot import build_source_snapshot, write_source_snapshot

    root = Path(review_root) if review_root else default_review_root()
    baseline_path = latest_snapshot(root)
    if baseline_path is None:
        raise OperationError("Sandbox aftercare requires a verified public Source Snapshot")
    baseline = load_yaml(baseline_path)
    checked = _utc_now()
    stamp = checked.replace(":", "").replace("+00:00", "Z")
    snapshot_path = root / "source_snapshots" / f"arena-{stamp}.yaml"
    snapshot = build_source_snapshot(
        registry,
        reader,
        user_slug=baseline.get("source", {}).get("user_slug", "nexah-scarabaeus1031"),
        observed_at=checked,
    )
    snapshot["snapshot_id"] = f"arena-{stamp}"
    write_source_snapshot(snapshot, snapshot_path)
    diff = run_editorial_diff(
        registry,
        reader,
        review_root=root,
        baseline=baseline,
        checked_at=checked,
    )
    health = build_health(registry, review_root=root)
    release = build_release_check(registry, review_root=root)
    return {
        "source_snapshot": {"id": snapshot["snapshot_id"], "file": str(snapshot_path)},
        "editorial_diff": diff["summary"],
        "health": health["status"],
        "release_check": release["result"],
        "errors": list(health["failures"]),
        "warnings": list(health["warnings"]),
    }


def render_batch_verification(report: dict[str, Any]) -> str:
    before = report["traversability_before"]
    after = report["traversability_after"]
    lines = [
        "# NEXAH Library — Batch 01 Verification",
        "",
        f"- Batch: `{report['batch']}`",
        f"- Plan: `{report['plan_id']}`",
        f"- Applied: `{report['applied_at']}`",
        f"- Snapshot: `{report['snapshot_id']}`",
        f"- Health: `{report['health']}`",
        f"- Release check: `{report['release_check']}`",
        "- Action Queue modified: `false`",
        "",
        "## Executed actions",
        "",
    ]
    lines.extend(f"- `{action_id}`" for action_id in report["actions"])
    lines.extend(["", "## Before / after", ""])
    for item in report["journal"]:
        lines.append(
            f"- `{item['action_id']}` · `{item['operation']}` · Channel "
            f"`{item['channel_id']}` · `{item['before_fingerprint']}` → "
            f"`{item['after_fingerprint']}`"
        )
    lines.extend(
        [
            "",
            "## Traversability",
            "",
            f"- Before: {before.get('present', 0)} / {before.get('transitions', 0)} directly walkable",
            f"- After: {after.get('present', 0)} / {after.get('transitions', 0)} directly walkable",
            "",
            "## Editorial Diff",
            "",
        ]
    )
    lines.extend(
        f"- {key}: {value}" for key, value in report["editorial_diff"].items()
    )
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {value}" for value in report["warnings"] or ["None"])
    lines.extend(["", "## Errors", ""])
    lines.extend(f"- {value}" for value in report["errors"] or ["None"])
    lines.extend(["", "## Deviations", ""])
    if report["deviations"]:
        lines.extend(
            f"- Channel `{item['arena_channel_id']}`: {', '.join(item['categories'])}"
            for item in report["deviations"]
        )
    else:
        lines.append("- None")
    lines.extend(
        [
            "",
            "Queue review states remain a human-edited repository decision.",
            "",
        ]
    )
    return "\n".join(lines)
