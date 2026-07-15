from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .arena import ArenaClient
from .operations import OperationError, default_review_root, latest_snapshot, load_yaml
from .registry import Registry
from .snapshot import sequence_fingerprint, visible_channel_connections


def _description(channel: dict[str, Any]) -> str:
    value = channel.get("description")
    if not isinstance(value, dict):
        return ""
    return str(value.get("plain") or value.get("markdown") or "").strip()


def _remote_record(
    channel: dict[str, Any],
    contents: list[dict[str, Any]],
    *,
    user_slug: str,
    checked_at: str,
) -> dict[str, Any]:
    owner_slug = channel.get("owner", {}).get("slug") or user_slug
    slug = channel.get("slug")
    return {
        "arena_channel_id": channel.get("id"),
        "title": str(channel.get("title") or "").strip("\n"),
        "description": _description(channel),
        "slug": slug,
        "canonical_url": f"https://www.are.na/{owner_slug}/{slug}",
        "member_count": int(channel.get("counts", {}).get("contents") or 0),
        "updated_at": channel.get("updated_at"),
        "visibility": channel.get("visibility"),
        "sequence_fingerprint": sequence_fingerprint(contents),
        "visible_channel_connections": visible_channel_connections(contents),
        "last_checked": checked_at,
    }


def _categories(before: dict[str, Any], after: dict[str, Any] | None) -> tuple[list[str], dict[str, Any]]:
    if after is None:
        return ["availability_change"], {"availability": {"before": "visible", "after": "unavailable"}}
    changed: dict[str, Any] = {}
    for field in [
        "title",
        "description",
        "slug",
        "canonical_url",
        "member_count",
        "updated_at",
        "visibility",
        "sequence_fingerprint",
        "visible_channel_connections",
    ]:
        if before.get(field) != after.get(field):
            changed[field] = {"before": before.get(field), "after": after.get(field)}
    categories: list[str] = []
    if set(changed) & {"title", "description", "slug", "canonical_url", "updated_at"}:
        categories.append("metadata_change")
    if "member_count" in changed:
        categories.append("possible_content_change")
    if "sequence_fingerprint" in changed:
        categories.append("possible_sequence_change")
    if "visible_channel_connections" in changed:
        categories.append("link_change")
    if "visibility" in changed:
        categories.append("availability_change")
    return (categories or ["no_change"], changed)


def _resolve_selector(registry: Registry, selector: str) -> int:
    if selector.startswith("NX-"):
        return registry.entity(selector)["external_ids"]["arena_channel_id"]
    if selector.startswith("arena:"):
        try:
            return int(selector.split(":", 1)[1])
        except ValueError as exc:
            raise OperationError(f"Invalid Arena selector {selector}") from exc
    raise OperationError("Editorial Diff selector must be NX-... or arena:<id>")


def run_editorial_diff(
    registry: Registry,
    client: ArenaClient,
    *,
    selector: str | None = None,
    review_root: Path | str | None = None,
    baseline: dict[str, Any] | None = None,
    checked_at: str | None = None,
) -> dict[str, Any]:
    root = Path(review_root) if review_root else default_review_root()
    snapshot_path = latest_snapshot(root) if baseline is None else None
    if baseline is None:
        if snapshot_path is None:
            raise OperationError("Editorial Diff requires a verified Source Snapshot")
        baseline = load_yaml(snapshot_path)
    checked = checked_at or datetime.now(timezone.utc).isoformat(timespec="seconds")
    baseline_records = {
        record["arena_channel_id"]: record for record in baseline.get("channels", [])
    }
    if selector:
        selected_ids = [_resolve_selector(registry, selector)]
        if selected_ids[0] not in baseline_records:
            raise OperationError(f"Selector {selector} is not present in the Source Snapshot")
        payload = client.get_channel(selected_ids[0])
        remote = payload.get("data", payload)
        live_channels = {remote.get("id"): remote}
    else:
        selected_ids = sorted(baseline_records)
        live_channels = {
            channel.get("id"): channel
            for channel in client.get_user_channels(baseline["source"]["user_slug"])
        }

    records: list[dict[str, Any]] = []
    for arena_id in selected_ids:
        before = baseline_records[arena_id]
        channel = live_channels.get(arena_id)
        after = None
        if channel is not None:
            after = _remote_record(
                channel,
                client.get_contents(arena_id),
                user_slug=baseline["source"]["user_slug"],
                checked_at=checked,
            )
        categories, changes = _categories(before, after)
        records.append(
            {
                "arena_channel_id": arena_id,
                "registered_entity_id": before.get("registered_entity_id"),
                "title": before.get("title"),
                "categories": categories,
                "changes": changes,
                "assessment": (
                    "no_change"
                    if categories == ["no_change"]
                    else "human_review_required_before_source_state_update"
                ),
                "required_action": (
                    "none"
                    if categories == ["no_change"]
                    else "review observed differences; do not mutate Registry automatically"
                ),
            }
        )
    category_counts = {
        category: sum(category in record["categories"] for record in records)
        for category in [
            "metadata_change",
            "possible_content_change",
            "possible_sequence_change",
            "link_change",
            "availability_change",
            "no_change",
        ]
    }
    return {
        "schema_version": "1.0",
        "report_type": "editorial_diff",
        "write_policy": "read_only",
        "baseline": baseline.get("snapshot_id"),
        "checked_at": checked,
        "selector": selector or "all",
        "summary": {"records": len(records), **category_counts},
        "records": records,
        "mutations": [],
    }


def render_editorial_diff_text(report: dict[str, Any]) -> str:
    lines = [
        "NEXAH Editorial Diff",
        "",
        f"Baseline: {report['baseline']}",
        f"Records: {report['summary']['records']}",
        "",
    ]
    for record in report["records"]:
        label = ", ".join(record["categories"])
        lines.append(
            f"{record['arena_channel_id']} · {record['title']} · {label}"
        )
    lines.extend(["", "No Registry or Source Snapshot data was modified."])
    return "\n".join(lines)
