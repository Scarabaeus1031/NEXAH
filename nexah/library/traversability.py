from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .arena import ArenaClient, ArenaError
from .operations import default_review_root, load_yaml


JOURNEY_NAMES = {"beginner": "Beginner", "builder": "Builder", "research": "Research"}


def run_traversability(
    client: ArenaClient,
    *,
    review_root: Path | str | None = None,
    journey: str | None = None,
    checked_at: str | None = None,
) -> dict[str, Any]:
    root = Path(review_root) if review_root else default_review_root()
    audit = load_yaml(root / "traversability_audit.yaml")
    selected_name = JOURNEY_NAMES.get(journey) if journey else None
    checked = checked_at or datetime.now(timezone.utc).isoformat(timespec="seconds")
    cache: dict[int, list[dict[str, Any]] | ArenaError] = {}
    transitions: list[dict[str, Any]] = []

    for reviewed_journey in audit.get("journeys", []):
        if selected_name and reviewed_journey.get("name") != selected_name:
            continue
        for transition in reviewed_journey.get("transitions", []):
            source_id = transition["from"]["arena_channel_id"]
            target_id = transition["to"]["arena_channel_id"]
            if source_id not in cache:
                try:
                    cache[source_id] = client.get_contents(source_id)
                except ArenaError as exc:
                    cache[source_id] = exc
            observed = cache[source_id]
            if isinstance(observed, ArenaError):
                clickable = "source_unavailable"
                visible_source = None
                observation = str(observed)
            elif not isinstance(observed, list):
                clickable = "unknown"
                visible_source = None
                observation = "unexpected public contents response"
            else:
                direct = next(
                    (
                        item
                        for item in observed
                        if item.get("type") == "Channel" and item.get("id") == target_id
                    ),
                    None,
                )
                clickable = "present" if direct else "missing"
                visible_source = (
                    {
                        "type": "direct_channel_connection",
                        "position": direct.get("connection", {}).get("position"),
                    }
                    if direct
                    else None
                )
                observation = (
                    "direct public Channel connection observed"
                    if direct
                    else "no direct public Channel connection observed"
                )
            transitions.append(
                {
                    "from": transition["from"],
                    "to": transition["to"],
                    "journey": reviewed_journey["name"],
                    "conceptual_status": transition["conceptual_status"],
                    "clickable_status": clickable,
                    "visible_link_source": visible_source,
                    "observation": observation,
                    "reader_friction": transition["reader_friction"],
                    "recommended_manual_action": transition["recommended_manual_action"],
                    "last_checked": checked,
                }
            )

    counts = {
        state: sum(item["clickable_status"] == state for item in transitions)
        for state in ["present", "missing", "unknown", "source_unavailable"]
    }
    return {
        "schema_version": "1.0",
        "report_type": "live_traversability",
        "live_check": True,
        "write_policy": "read_only",
        "last_checked": checked,
        "journey_filter": journey or "all",
        "summary": {"transitions": len(transitions), **counts},
        "transitions": transitions,
    }


def render_traversability_text(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "NEXAH Library Traversability",
        "",
        f"Checked: {report['last_checked']}",
        f"Directly clickable: {summary['present']} / {summary['transitions']}",
        "",
    ]
    for item in report["transitions"]:
        mark = "PASS" if item["clickable_status"] == "present" else "WARN"
        lines.append(
            f"{mark}  {item['journey']} · {item['from']['title']} → "
            f"{item['to']['title']} · {item['clickable_status']}"
        )
    return "\n".join(lines)
