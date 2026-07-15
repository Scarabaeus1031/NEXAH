from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .operations import default_review_root, load_yaml


EXPECTED_SERIES_NAMES = [
    "The Language Series",
    "Field Atlas Series",
    "Orientation Architecture",
    "The Human Journey",
    "Operator Series",
    "Odyssey 2040",
    "NEXAH Whiteboard Series",
    "NEXAH Mathematica",
    "NEXAH XV Atlas",
]

ROMAN_VALUES = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5}


def _title_key(value: str) -> str:
    return " ".join(re.sub(r"[^\w]+", " ", value.casefold()).split())


def _volume_number(title: str) -> int | None:
    matches = re.findall(r"\b(I|II|III|IV|V)\b", title.upper())
    return ROMAN_VALUES[matches[-1]] if matches else None


def validate_series_data(
    editorial: dict[str, Any], discovery: dict[str, Any]
) -> dict[str, Any]:
    discovery_by_id = {
        record["arena_channel_id"]: record for record in discovery.get("channels", [])
    }
    results: list[dict[str, Any]] = []
    names = [item.get("series") for item in editorial.get("series", [])]
    global_failures: list[str] = []
    missing_names = [name for name in EXPECTED_SERIES_NAMES if name not in names]
    unexpected_names = [name for name in names if name not in EXPECTED_SERIES_NAMES]
    if missing_names:
        global_failures.append(f"missing editorial Series: {', '.join(missing_names)}")
    if unexpected_names:
        global_failures.append(f"unexpected editorial Series: {', '.join(unexpected_names)}")

    for series in editorial.get("series", []):
        failures: list[str] = []
        warnings: list[str] = []
        notes: list[str] = []
        ordered = series.get("ordered_members", [])
        unresolved = series.get("unresolved_members", [])
        associated = series.get("associated_members", [])
        positions = [member.get("position") for member in ordered]
        if len(positions) != len(set(positions)):
            failures.append("repeated ordered position")
        if positions and positions != list(range(1, len(positions) + 1)):
            failures.append(f"missing or non-linear positions: {positions}")

        primary = [*ordered, *unresolved, *associated]
        if series.get("navigation_hub"):
            primary.append(series["navigation_hub"])
        arena_ids = [member.get("arena_channel_id") for member in primary]
        if len(arena_ids) != len(set(arena_ids)):
            failures.append("duplicate member Arena ID")
        ordered_ids = {member.get("arena_channel_id") for member in ordered}
        associated_ids = {member.get("arena_channel_id") for member in associated}
        if ordered_ids & associated_ids:
            failures.append("associated Work is also an ordered member")

        for member in primary:
            arena_id = member.get("arena_channel_id")
            source = discovery_by_id.get(arena_id)
            if source is None:
                failures.append(f"missing Arena source {arena_id}")
                continue
            if _title_key(member.get("title", "")) != _title_key(
                source.get("current_title", "")
            ):
                warnings.append(f"title mismatch for Arena {arena_id}")
            state = member.get("classification_state")
            registered_id = member.get("registered_entity_id")
            if state == "canonical" and not registered_id:
                failures.append(f"canonical member {arena_id} lacks Registry identity")
            if state == "proposed" and registered_id:
                failures.append(f"Proposal member {arena_id} resolves as canonical")

        if series.get("sequence_mode") == "linear":
            for member in ordered:
                numeral = _volume_number(member.get("title", ""))
                if numeral is not None and numeral != member.get("position"):
                    failures.append(
                        f"volume numeral mismatch at position {member.get('position')}"
                    )

        name = series.get("series")
        if unresolved:
            warnings.append(f"{len(unresolved)} unresolved member(s)")
        if name == "NEXAH Mathematica" and len(unresolved) == 2:
            warnings.append("two distinct Mathematica IV Channels remain unresolved")
        if name == "NEXAH XV Atlas":
            notes.append(
                f"ordered core {len(ordered)}; unordered satellites {len(unresolved)}"
            )
        if series.get("sequence_mode") == "unordered_growing_universe":
            notes.append("intentionally unordered; no sequence enforced")
        if series.get("review_state") not in {"confirmed", "deferred_growing_universe"}:
            warnings.append(f"editorial state: {series.get('review_state')}")

        results.append(
            {
                "series": name,
                "review_state": series.get("review_state"),
                "sequence_mode": series.get("sequence_mode"),
                "status": "fail" if failures else ("warning" if warnings else "pass"),
                "ordered_members": len(ordered),
                "unresolved_members": len(unresolved),
                "associated_members": len(associated),
                "warnings": warnings,
                "failures": failures,
                "notes": notes,
            }
        )

    failures = global_failures + [
        failure for result in results for failure in result["failures"]
    ]
    warnings = [warning for result in results for warning in result["warnings"]]
    return {
        "status": "fail" if failures else ("pass_with_editorial_warnings" if warnings else "pass"),
        "series": results,
        "summary": {
            "total": len(results),
            "confirmed": sum(result["review_state"] == "confirmed" for result in results),
            "warnings": len(warnings),
            "failures": len(failures),
        },
        "warnings": warnings,
        "failures": failures,
    }


def validate_series(*, review_root: Path | str | None = None) -> dict[str, Any]:
    root = Path(review_root) if review_root else default_review_root()
    return validate_series_data(
        load_yaml(root / "editorial_sequence_review.yaml"),
        load_yaml(root / "full_library_discovery.yaml"),
    )


def render_series_text(report: dict[str, Any]) -> str:
    lines = ["NEXAH Series Health", ""]
    for result in report["series"]:
        mark = {"pass": "PASS", "warning": "WARN", "fail": "FAIL"}[result["status"]]
        lines.append(f"{mark}  {result['series']} · {result['sequence_mode']}")
        lines.extend(f"      {warning}" for warning in result["warnings"])
        lines.extend(f"      {failure}" for failure in result["failures"])
        lines.extend(f"      {note}" for note in result["notes"])
    lines.extend(["", f"Result: {report['status'].replace('_', ' ').upper()}"])
    return "\n".join(lines)
