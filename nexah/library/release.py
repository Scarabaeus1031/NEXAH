from __future__ import annotations

from pathlib import Path
from typing import Any

from .cleanup import cleanup_status
from .health import build_health
from .regression import run_reader_regression
from .registry import Registry, RegistryError
from .series import validate_series


def build_release_check(
    registry: Registry, *, review_root: Path | str | None = None
) -> dict[str, Any]:
    health = build_health(registry, review_root=review_root)
    try:
        regression = run_reader_regression(registry, review_root=review_root)
    except RegistryError as exc:
        regression = {
            "status": "fail",
            "questions": [],
            "failures": 1,
            "errors": [str(exc)],
        }
    series = validate_series(review_root=review_root)
    cleanup = cleanup_status(review_root=review_root)

    validators = [
        {
            "name": "Registry",
            "status": "pass" if health["registry"]["valid"] else "fail",
            "detail": f"{health['registry']['entities']} Entities",
        },
        {
            "name": "Operators",
            "status": "pass" if health["registry"]["operators"] == 17 else "fail",
            "detail": f"{health['registry']['operators']} controlled Operators",
        },
        {
            "name": "Proposal isolation",
            "status": (
                "pass"
                if health["proposal_isolation"]["state"] == "explicit_only"
                else "fail"
            ),
            "detail": health["proposal_isolation"]["state"],
        },
        {
            "name": "Reader regression",
            "status": regression["status"],
            "detail": f"{len(regression['questions'])} fixed questions",
        },
        {
            "name": "Series structure",
            "status": "fail" if series["failures"] else "pass",
            "detail": f"{series['summary']['confirmed']} confirmed; "
            f"{len(series['warnings'])} editorial warnings",
        },
        {
            "name": "Traversability",
            "status": (
                "warning"
                if health["traversability"].get("clickable_missing", 0)
                else "pass"
            ),
            "detail": f"{health['traversability'].get('clickable_present', 0)} / "
            f"{health['traversability'].get('transitions', 0)} directly clickable",
        },
        {
            "name": "Manual cleanup",
            "status": "warning" if cleanup["summary"]["open"] else "pass",
            "detail": f"{cleanup['summary']['open']} open actions",
        },
        {
            "name": "Safety",
            "status": "fail" if health["failures"] else "pass",
            "detail": "Are.na read_only; no IDs allocated",
        },
    ]
    structural_failures = [item for item in validators if item["status"] == "fail"]
    editorial_warnings = [item for item in validators if item["status"] == "warning"]
    if structural_failures:
        result = "fail"
    elif editorial_warnings or health["warnings"] or series["warnings"]:
        result = "pass_with_editorial_warnings"
    else:
        result = "pass"
    return {
        "result": result,
        "live_check": False,
        "snapshot": health["snapshot"],
        "validators": validators,
        "structural_failures": [item["name"] for item in structural_failures],
        "editorial_warnings": [item["name"] for item in editorial_warnings],
        "safety": health["safety"],
        "registry": health["registry"],
        "proposal_isolation": health["proposal_isolation"],
        "traversability": health["traversability"],
        "cleanup": cleanup["summary"],
        "series": series["summary"],
    }


def render_release_text(report: dict[str, Any]) -> str:
    lines = ["NEXAH Library Release Check", ""]
    for validator in report["validators"]:
        mark = {"pass": "PASS", "warning": "WARN", "fail": "FAIL"}[
            validator["status"]
        ]
        lines.append(f"{mark}  {validator['name']} · {validator['detail']}")
    lines.extend(
        [
            "",
            f"SAFE  Are.na client is {report['safety']['arena_write_policy']}",
            f"SAFE  ID allocation is {report['safety']['id_allocation']}",
            "",
            f"Result: {report['result'].replace('_', ' ').upper()}",
        ]
    )
    return "\n".join(lines)
