from __future__ import annotations

from pathlib import Path
import re
from typing import Any

from .operations import default_review_root, dump_yaml, load_yaml
from .reader import ReaderOverlay
from .registry import Registry


FORBIDDEN_READER_KEYS = {
    "score",
    "evidence",
    "technical",
    "reference",
    "operator_id",
    "object_family",
    "library_function",
    "publication_status",
}


def _all_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        keys = set(value)
        for child in value.values():
            keys.update(_all_keys(child))
        return keys
    if isinstance(value, list):
        keys: set[str] = set()
        for child in value:
            keys.update(_all_keys(child))
        return keys
    return set()


def _expected_items(question: dict[str, Any]) -> list[dict[str, Any]]:
    reader = question["reader_mode"]
    if "items" in reader:
        return [
            {
                "title": item["title"],
                "state": item["state"],
                "role": item["role"],
            }
            for item in reader["items"]
        ]
    items: list[dict[str, Any]] = []
    role_by_group = {
        "Canonical Operator references": "Confirmed Operator reference",
        "Inferred description matches": "Description match",
    }
    for group in reader.get("groups", []):
        for title in group["titles"]:
            items.append(
                {
                    "title": title,
                    "state": group["state"],
                    "role": role_by_group[group["label"]],
                }
            )
    return items


def _normalized_review_title(value: str) -> str:
    return " ".join(re.sub(r"[^\w]+", " ", value.casefold()).split())


def run_reader_regression(
    registry: Registry,
    *,
    review_root: Path | str | None = None,
    question_id: str | None = None,
    fixture: dict[str, Any] | None = None,
) -> dict[str, Any]:
    root = Path(review_root) if review_root else default_review_root()
    accepted = fixture or load_yaml(root / "second_human_reader_review.yaml")
    overlay = ReaderOverlay.load(registry, root)
    fixture_questions = {question["id"]: question for question in accepted["questions"]}
    selected = [question_id] if question_id else sorted(fixture_questions)
    results: list[dict[str, Any]] = []

    for current_id in selected:
        errors: list[str] = []
        expected_question = fixture_questions.get(current_id)
        if expected_question is None:
            results.append(
                {"question_id": current_id, "status": "fail", "errors": ["fixture missing"]}
            )
            continue
        if expected_question.get("human_decision") != "accept":
            errors.append("Reader Policy is not accepted")
        expected = _expected_items(expected_question)
        reader = overlay.answer(current_id, mode="reader")
        explain = overlay.answer(current_id, mode="explain")
        actual = [
            {"title": item["title"], "state": item["state"], "role": item["role"]}
            for item in reader["items"]
        ]
        comparable_actual = actual
        comparable_expected = expected
        if current_id == "UQ-04":
            comparable_actual = [
                {**item, "title": _normalized_review_title(item["title"])}
                for item in actual
            ]
            comparable_expected = [
                {**item, "title": _normalized_review_title(item["title"])}
                for item in expected
            ]
        if comparable_actual != comparable_expected:
            errors.append(f"accepted order/state/role changed: expected {expected!r}, got {actual!r}")
        forbidden = sorted(FORBIDDEN_READER_KEYS & _all_keys(reader))
        if forbidden:
            errors.append(f"Reader Mode exposes technical keys: {', '.join(forbidden)}")
        for position, item in enumerate(explain["items"], 1):
            if item.get("state") not in {"canonical", "proposal", "inferred"}:
                errors.append(f"Explain item {position} has invalid state")
            evidence = item.get("evidence")
            if not evidence or any(not value.get("class") or not value.get("source") for value in evidence):
                errors.append(f"Explain item {position} lacks evidence class or source")
        if current_id == "UQ-01":
            if len(actual) != 5 or any("START" in item["title"] for item in actual):
                errors.append("UQ-01 must contain five Works and exclude START")
            if any(item["state"] != "canonical" for item in actual):
                errors.append("UQ-01 must remain fully canonical")
        if current_id == "UQ-04":
            states = [item["state"] for item in actual]
            if states != sorted(states, key={"canonical": 0, "inferred": 1}.get):
                errors.append("UQ-04 canonical and inferred groups collapsed")
            for item in explain["items"]:
                classes = {value["class"] for value in item["evidence"]}
                if item["state"] == "inferred" and "canonical_operator_reference" in classes:
                    errors.append("an inferred match became a confirmed Operator occurrence")
        if current_id == "UQ-05":
            if not explain["items"][0].get("editorial_sequence"):
                errors.append("UQ-05 lost its editorial sequence")
        results.append(
            {
                "question_id": current_id,
                "status": "pass" if not errors else "fail",
                "expected_count": len(expected),
                "actual_count": len(actual),
                "errors": errors,
            }
        )

    failures = [result for result in results if result["status"] == "fail"]
    return {
        "status": "pass" if not failures else "fail",
        "fixture": "second_human_reader_review.yaml",
        "local_only": True,
        "questions": results,
        "failures": sum(len(result["errors"]) for result in failures),
    }


def render_reader_regression_text(report: dict[str, Any]) -> str:
    lines = ["NEXAH Reader Regression", ""]
    for question in report["questions"]:
        mark = "PASS" if question["status"] == "pass" else "FAIL"
        lines.append(
            f"{mark}  {question['question_id']} · {question['actual_count']} results"
        )
        lines.extend(f"      {error}" for error in question["errors"])
    lines.extend(["", f"Result: {report['status'].upper()}"])
    return "\n".join(lines)
