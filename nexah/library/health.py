from __future__ import annotations

from pathlib import Path
from typing import Any

from .arena import ArenaClient
from .operations import default_review_root, latest_snapshot, load_yaml
from .reader import ReaderOverlay, ReaderOverlayError
from .regression import run_reader_regression
from .series import validate_series
from .registry import Registry, RegistryError


EXPECTED_ENTITY_COUNT = 10
EXPECTED_OPERATOR_COUNT = 17


def build_health(
    registry: Registry, *, review_root: Path | str | None = None
) -> dict[str, Any]:
    root = Path(review_root) if review_root else default_review_root()
    failures: list[str] = []
    warnings: list[str] = []
    registry_errors = registry.validate()
    failures.extend(f"registry: {error}" for error in registry_errors)
    if len(registry.entities) != EXPECTED_ENTITY_COUNT:
        failures.append(
            f"canonical Registry count changed: {len(registry.entities)} != {EXPECTED_ENTITY_COUNT}"
        )
    if len(registry.concepts) != EXPECTED_OPERATOR_COUNT:
        failures.append(
            f"Operator count changed: {len(registry.concepts)} != {EXPECTED_OPERATOR_COUNT}"
        )

    classification = load_yaml(root / "full_library_classification.yaml")
    proposed = [
        record
        for record in classification.get("records", [])
        if record.get("classification_state") == "proposed"
    ]
    proposal_policy = classification.get("proposal_policy", {})
    if proposal_policy.get("loads_as_canonical") is not False:
        failures.append("Proposal Overlay is not explicit-only")
    if any(record.get("registered_entity_id") for record in proposed):
        failures.append("a Proposal record resolves to a canonical Entity ID")

    decisions = load_yaml(root / "second_human_reader_review.yaml")
    accepted = [
        question.get("id")
        for question in decisions.get("questions", [])
        if question.get("human_decision") == "accept"
    ]
    if set(accepted) != {f"UQ-{value:02d}" for value in range(1, 7)}:
        failures.append("the six fixed Reader Policies are not all accepted")
    reader_failures: list[str] = []
    try:
        overlay = ReaderOverlay.load(registry, root)
        for question_id in sorted(overlay.questions):
            overlay.answer(question_id, mode="reader")
            overlay.answer(question_id, mode="explain")
        regression = run_reader_regression(registry, review_root=root)
        if regression["status"] != "pass":
            reader_failures.extend(
                error
                for question in regression["questions"]
                for error in question["errors"]
            )
            failures.append("accepted Reader regression changed")
    except (ReaderOverlayError, RegistryError) as exc:
        reader_failures.append(str(exc))
        failures.append(f"Reader Policy failed: {exc}")

    traversability = load_yaml(root / "traversability_audit.yaml")
    traversal_summary = traversability.get("summary", {})
    missing_links = int(traversal_summary.get("clickable_missing", 0))
    if missing_links:
        warnings.append(f"{missing_links} curated transitions are not directly clickable")

    series_report = validate_series(review_root=root)
    if series_report["failures"]:
        failures.extend(f"Series: {value}" for value in series_report["failures"])
    unresolved_series = [
        item for item in series_report["series"] if item["review_state"] != "confirmed"
    ]
    if unresolved_series:
        warnings.append(f"{len(unresolved_series)} Series remain editorially unresolved")

    snapshot_path = latest_snapshot(root)
    snapshot = load_yaml(snapshot_path) if snapshot_path else None
    if snapshot is None:
        warnings.append("source snapshot unavailable")
    else:
        snapshot_records = snapshot.get("channels", [])
        snapshot_ids = [record.get("arena_channel_id") for record in snapshot_records]
        if len(snapshot_ids) != len(set(snapshot_ids)):
            failures.append("source snapshot contains duplicate Arena IDs")
        if snapshot.get("summary", {}).get("channels") != len(snapshot_records):
            failures.append("source snapshot Channel count is inconsistent")
        if snapshot.get("source", {}).get("write_policy") != "read_only":
            failures.append("source snapshot does not declare read_only observation")

    cleanup_path = root / "arena_manual_cleanup_queue.yaml"
    cleanup = load_yaml(cleanup_path) if cleanup_path.exists() else None
    if cleanup is None:
        warnings.append("structured cleanup queue unavailable")
        cleanup_summary: dict[str, Any] = {"status": "unavailable"}
    else:
        items = cleanup.get("items", [])
        open_items = [
            item for item in items if item.get("review_state") in {"pending", "accepted"}
        ]
        cleanup_summary = {"total": len(items), "open": len(open_items)}
        if open_items:
            warnings.append(f"{len(open_items)} manual cleanup actions remain open")

    arena_methods = {
        name for name in dir(ArenaClient) if not name.startswith("_") and callable(getattr(ArenaClient, name))
    }
    write_methods = arena_methods & {"post", "put", "patch", "delete", "write", "connect"}
    if write_methods:
        failures.append(f"Are.na client exposes write methods: {', '.join(sorted(write_methods))}")

    status = "fail" if failures else ("pass_with_editorial_warnings" if warnings else "pass")
    return {
        "status": status,
        "as_of": snapshot.get("verified_at") if snapshot else decisions.get("accepted_at"),
        "registry_version": registry.manifest.get("registry_version"),
        "review_version": f"{decisions.get('review_stage')}/{decisions.get('schema_version')}",
        "snapshot": snapshot_path.name if snapshot_path else "unavailable",
        "live_check": False,
        "registry": {
            "valid": not registry_errors,
            "entities": len(registry.entities),
            "operators": len(registry.concepts),
        },
        "proposal_isolation": {
            "state": "explicit_only" if not failures else "check_failures",
            "proposal_records": len(proposed),
        },
        "reader_orientation": {
            "accepted_questions": accepted,
            "failures": reader_failures,
        },
        "traversability": traversal_summary,
        "series": {
            "confirmed": series_report["summary"]["confirmed"],
            "unresolved": len(unresolved_series),
            "unresolved_names": [item["series"] for item in unresolved_series],
            "validation_status": series_report["status"],
        },
        "cleanup": cleanup_summary,
        "safety": {
            "arena_write_policy": registry.manifest.get("write_policy", {}).get("arena"),
            "arena_write_methods": sorted(write_methods),
            "id_allocation": "unchanged",
        },
        "warnings": warnings,
        "failures": failures,
    }


def render_health_text(report: dict[str, Any]) -> str:
    mark = "PASS" if report["status"] != "fail" else "FAIL"
    lines = [
        "NEXAH Library Health",
        "",
        f"{mark}  Registry: {report['registry']['entities']} Entities, "
        f"{report['registry']['operators']} Operators",
        f"{mark}  Proposal isolation: {report['proposal_isolation']['state']}",
        f"{mark}  Reader Policies: {len(report['reader_orientation']['accepted_questions'])}/6 accepted",
        f"INFO  Snapshot: {report['snapshot']}",
        f"INFO  Traversability: {report['traversability'].get('clickable_present', 0)} / "
        f"{report['traversability'].get('transitions', 0)} directly clickable",
        f"INFO  Series: {report['series']['confirmed']} confirmed, "
        f"{report['series']['unresolved']} unresolved",
    ]
    lines.extend(f"WARN  {warning}" for warning in report["warnings"])
    lines.extend(f"FAIL  {failure}" for failure in report["failures"])
    lines.extend(["", f"Result: {report['status'].replace('_', ' ').upper()}"])
    return "\n".join(lines)
