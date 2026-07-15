from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .operations import OperationError, default_review_root, load_yaml


VALID_STATES = {"pending", "accepted", "completed", "deferred", "rejected"}
VALID_PRIORITIES = {"P0", "P1", "P2"}
KEY_PATTERN = re.compile(r"^ACQ-\d{3}$")


def cleanup_status(*, review_root: Path | str | None = None) -> dict[str, Any]:
    root = Path(review_root) if review_root else default_review_root()
    queue = load_yaml(root / "arena_manual_cleanup_queue.yaml")
    items = queue.get("items", [])
    errors: list[str] = []
    keys = [item.get("id") for item in items]
    if len(keys) != len(set(keys)):
        errors.append("duplicate cleanup ID")
    for item in items:
        key = item.get("id")
        if not isinstance(key, str) or not KEY_PATTERN.fullmatch(key):
            errors.append(f"invalid cleanup ID {key}")
        if item.get("review_state") not in VALID_STATES:
            errors.append(f"{key}: invalid review state {item.get('review_state')}")
        if item.get("priority") not in VALID_PRIORITIES:
            errors.append(f"{key}: invalid priority {item.get('priority')}")
        if item.get("automatic_write_authorized") is not False:
            errors.append(f"{key}: automatic write must remain false")
    if queue.get("policy", {}).get("command_may_update_queue") is not False:
        errors.append("cleanup-status must remain read-only")

    by_state = {state: sum(item.get("review_state") == state for item in items) for state in sorted(VALID_STATES)}
    by_priority = {
        priority: sum(item.get("priority") == priority for item in items)
        for priority in sorted(VALID_PRIORITIES)
    }
    open_items = [
        item for item in items if item.get("review_state") in {"pending", "accepted"}
    ]
    return {
        "status": "fail" if errors else "pass",
        "write_policy": "read_only",
        "queue_file": "arena_manual_cleanup_queue.yaml",
        "summary": {
            "total": len(items),
            "open": len(open_items),
            "by_state": by_state,
            "by_priority": by_priority,
        },
        "items": items,
        "errors": errors,
    }


def render_cleanup_text(report: dict[str, Any]) -> str:
    lines = ["Manual Are.na Cleanup", ""]
    for priority in ["P0", "P1", "P2"]:
        selected = [item for item in report["items"] if item["priority"] == priority]
        if not selected:
            continue
        lines.append(priority)
        for item in selected:
            lines.append(
                f"{item['id']} · {item['affected_channel']['title']} · "
                f"{item['review_state']}"
            )
        lines.append("")
    lines.append(
        f"Open: {report['summary']['open']} / {report['summary']['total']} · "
        "read-only local report"
    )
    return "\n".join(lines)
