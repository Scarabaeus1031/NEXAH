from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .arena import ArenaClient
from .discovery import build_discovery
from .operations import OperationError, dump_yaml
from .registry import Registry


def sequence_fingerprint(contents: list[dict[str, Any]]) -> str:
    observed = [
        {
            "id": item.get("id"),
            "type": item.get("type"),
            "position": item.get("connection", {}).get("position"),
        }
        for item in contents
    ]
    encoded = json.dumps(
        observed, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def visible_channel_connections(contents: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "arena_channel_id": item.get("id"),
            "title": item.get("title"),
            "position": item.get("connection", {}).get("position"),
        }
        for item in contents
        if item.get("type") == "Channel" and isinstance(item.get("id"), int)
    ]


def build_source_snapshot(
    registry: Registry,
    client: ArenaClient,
    *,
    user_slug: str = "nexah-scarabaeus1031",
    observed_at: str | None = None,
) -> dict[str, Any]:
    registry.require_valid()
    checked = observed_at or datetime.now(timezone.utc).isoformat(timespec="seconds")
    channels = client.get_user_channels(user_slug)
    discovery = build_discovery(registry, channels, user_slug=user_slug)
    records: list[dict[str, Any]] = []
    for channel in discovery["channels"]:
        contents = client.get_contents(channel["arena_channel_id"])
        records.append(
            {
                "arena_channel_id": channel["arena_channel_id"],
                "registered_entity_id": channel["registered_entity_id"],
                "title": channel["current_title"],
                "description": channel["current_description"],
                "slug": channel["arena_slug"],
                "canonical_url": channel["public_url"],
                "member_count": channel["member_count"],
                "updated_at": channel["updated_at"],
                "visibility": channel["visibility"],
                "sequence_fingerprint": sequence_fingerprint(contents),
                "visible_channel_connections": visible_channel_connections(contents),
                "last_checked": checked,
            }
        )
    records.sort(key=lambda item: item["arena_channel_id"])
    return {
        "schema_version": "1.0",
        "snapshot_id": f"arena-{checked[:10]}",
        "verified_at": checked,
        "source": {
            "platform": "are.na",
            "user_slug": user_slug,
            "scope": "public_channels_visible_to_read_only_client",
            "write_policy": "read_only",
        },
        "summary": {
            "channels": len(records),
            "registered_entities": sum(
                record["registered_entity_id"] is not None for record in records
            ),
            "visible_channel_connections": sum(
                len(record["visible_channel_connections"]) for record in records
            ),
        },
        "channels": records,
        "limitations": [
            "The snapshot contains public observations only.",
            "A sequence fingerprint is evidence, not an Edition identifier.",
            "No Are.na content or Registry data was changed.",
        ],
    }


def write_source_snapshot(snapshot: dict[str, Any], path: Path) -> None:
    if path.exists():
        raise OperationError(
            f"Refusing to overwrite verified Source Snapshot {path}; choose a new path"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_yaml(snapshot), encoding="utf-8")
