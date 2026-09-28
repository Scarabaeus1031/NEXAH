"""WP4 case-package, report, replay and Human Return workflow."""

from __future__ import annotations

import hashlib
import html
import os
import tempfile
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any

from .runtime import (
    CLAIM_CEILING,
    PROFILE_ID,
    CompareError,
    canonical_bytes,
    canonical_sha256,
    compare_records,
    load_json,
    validate_schema,
    validate_with_schema,
)


ROOT = Path(__file__).resolve().parents[2]
PACKAGE_SCHEMAS = ROOT / "package_contract"
RUNTIME_VERSION = "0.1.0"
OUTPUT_PATHS = {
    "outputs/comparison.json",
    "outputs/report.md",
    "manifest.json",
    "receipts/run-receipt.json",
}


def _safe_relative(value: str) -> PurePosixPath:
    if not isinstance(value, str) or not value or "\\" in value:
        raise CompareError("UNSAFE_PACKAGE_PATH", repr(value))
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "." in path.parts:
        raise CompareError("UNSAFE_PACKAGE_PATH", value)
    return path


def _package_path(root: Path, relative: str, *, must_exist: bool = True) -> Path:
    pure = _safe_relative(relative)
    current = root
    for part in pure.parts:
        current = current / part
        if current.exists() and current.is_symlink():
            raise CompareError("PACKAGE_SYMLINK_REJECTED", relative)
    try:
        current.resolve(strict=False).relative_to(root.resolve(strict=True))
    except (OSError, ValueError) as error:
        raise CompareError("PACKAGE_PATH_ESCAPE", relative) from error
    if must_exist and not current.is_file():
        raise CompareError("PACKAGE_FILE_MISSING", relative)
    return current


def _inventory(root: Path) -> set[str]:
    result: set[str] = set()
    for directory, names, files in os.walk(root, followlinks=False):
        base = Path(directory)
        for name in names:
            path = base / name
            if path.is_symlink():
                raise CompareError(
                    "PACKAGE_SYMLINK_REJECTED", path.relative_to(root).as_posix()
                )
        for name in files:
            path = base / name
            relative = path.relative_to(root).as_posix()
            if path.is_symlink():
                raise CompareError("PACKAGE_SYMLINK_REJECTED", relative)
            result.add(relative)
    return result


def _assert_inventory(root: Path, allowed: set[str]) -> None:
    unexpected = sorted(_inventory(root) - allowed)
    if unexpected:
        raise CompareError("UNDECLARED_PACKAGE_FILE", ",".join(unexpected))


def _atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
        temp = Path(handle.name)
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temp, path)


def _file_entry(root: Path, relative: str, role: str) -> dict[str, Any]:
    path = _package_path(root, relative)
    payload = path.read_bytes()
    return {
        "path": relative,
        "role": role,
        "sha256": hashlib.sha256(payload).hexdigest(),
        "bytes": len(payload),
    }


def _load_descriptor(root: Path) -> dict[str, Any]:
    descriptor = load_json(_package_path(root, "package.json"))
    validate_with_schema(descriptor, PACKAGE_SCHEMAS / "case-package.schema.json")
    return descriptor


def _load_inputs(
    root: Path, descriptor: dict[str, Any]
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any] | None]:
    case = load_json(_package_path(root, descriptor["case_path"]))
    analyses = [load_json(_package_path(root, item)) for item in descriptor["analysis_paths"]]
    alignment = (
        load_json(_package_path(root, descriptor["alignment_path"]))
        if descriptor["alignment_path"] is not None
        else None
    )
    if case.get("privacy_class") != descriptor["privacy_class"]:
        raise CompareError("PRIVACY_CLASS_MISMATCH", str(case.get("privacy_class")))
    return case, analyses, alignment


def _evidence_paths(root: Path, case: dict[str, Any]) -> list[str]:
    paths: list[str] = []
    for item in case["evidence"]:
        if item["status"] != "ADMITTED":
            continue
        relative = item["path"]
        path = _package_path(root, relative)
        observed = hashlib.sha256(path.read_bytes()).hexdigest()
        if observed != item["sha256"]:
            raise CompareError("EVIDENCE_HASH_MISMATCH", item["evidence_id"])
        paths.append(relative)
    return sorted(paths)


def _base_files(descriptor: dict[str, Any], evidence_paths: list[str]) -> set[str]:
    result = {"package.json", descriptor["case_path"], *descriptor["analysis_paths"], *evidence_paths}
    if descriptor["alignment_path"] is not None:
        result.add(descriptor["alignment_path"])
    return result


def _markdown_escape(value: Any) -> str:
    text = html.escape(str(value), quote=False)
    text = text.replace("\\", "\\\\")
    for character in "`*_{}[]()#+!":
        text = text.replace(character, f"\\{character}")
    return text.replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def render_markdown(comparison: dict[str, Any]) -> bytes:
    validate_schema(comparison)
    digest = canonical_sha256(comparison)
    counts = Counter(item["classification"] for item in comparison["relation_groups"])
    lines = [
        "# NEXAH Compare v0.1 — Deterministic Comparison Report",
        "",
        f"- Comparison: `{_markdown_escape(comparison['record_id'])}`",
        f"- Case: `{_markdown_escape(comparison['case_id'])}`",
        f"- Reference analysis: `{_markdown_escape(comparison['reference_analysis_id'])}`",
        f"- Canonical comparison SHA-256: `{digest}`",
        "- Status: `MACHINE_COMPARISON_ONLY / HUMAN_RETURN_REQUIRED`",
        "",
        "## Classification counts",
        "",
        "| Invariant | Lost | Added | Unavailable |",
        "|---:|---:|---:|---:|",
        f"| {counts['INVARIANT']} | {counts['LOST']} | {counts['ADDED']} | {counts['UNAVAILABLE']} |",
        "",
        "## Relations",
        "",
        "| Relation | Classification | Reason | Criterion | Members |",
        "|---|---|---|---|---|",
    ]
    for relation in comparison["relation_groups"]:
        members = "; ".join(
            f"{item['analysis_id']}:{item['claim_id'] or 'MISSING'}:{item['role']}"
            for item in relation["members"]
        )
        lines.append(
            "| "
            + " | ".join(
                _markdown_escape(item)
                for item in (
                    relation["relation_id"],
                    relation["classification"],
                    relation["reason_code"],
                    relation["criterion"],
                    members,
                )
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Calculation checks",
            "",
            "| Check | Status | Reason | Claims | Detail |",
            "|---|---|---|---|---|",
        ]
    )
    if comparison["calculation_checks"]:
        for check in comparison["calculation_checks"]:
            lines.append(
                "| "
                + " | ".join(
                    _markdown_escape(item)
                    for item in (
                        check["check_id"],
                        check["status"],
                        check["reason_code"],
                        ", ".join(check["claim_ids"]),
                        check["detail"],
                    )
                )
                + " |"
            )
    else:
        lines.append("| — | NOT_APPLICABLE | NOT_APPLICABLE | — | No calculation group was present. |")
    lines.extend(
        [
            "",
            "## Residuals",
            "",
            "| Residual | Relation | Severity | Reason | Gate | Expected | Observed |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    if comparison["residuals"]:
        for residual in comparison["residuals"]:
            lines.append(
                "| "
                + " | ".join(
                    _markdown_escape(item if item is not None else "—")
                    for item in (
                        residual["residual_id"],
                        residual["relation_id"],
                        residual["severity"],
                        residual["reason_code"],
                        residual["gate_effect"],
                        residual["expected"],
                        residual["observed"],
                    )
                )
                + " |"
            )
    else:
        lines.append("| — | — | — | — | NONE | — | No residual was generated. |")
    lines.extend(["", "## Abstentions", ""])
    if comparison["abstentions"]:
        for item in comparison["abstentions"]:
            lines.append(
                f"- `{_markdown_escape(item['subject_id'])}` — "
                f"`{_markdown_escape(item['reason_code'])}` — "
                f"{_markdown_escape(item['statement'])}"
            )
    else:
        lines.append("- None recorded by the bounded machine comparison.")
    lines.extend(
        [
            "",
            "## Claim ceiling",
            "",
            f"`{_markdown_escape(comparison['claim_ceiling'])}`",
            "",
            "This report is a faithful projection of the canonical ComparisonRecord. "
            "It adds no recommendation, truth ranking or decision. A separate Human Return is required.",
            "",
        ]
    )
    return "\n".join(lines).encode("utf-8")


def _manifest(
    root: Path,
    descriptor: dict[str, Any],
    evidence_paths: list[str],
) -> dict[str, Any]:
    roles = {"package.json": "PACKAGE_DESCRIPTOR", descriptor["case_path"]: "CASE_INPUT"}
    roles.update({item: "ANALYSIS_INPUT" for item in descriptor["analysis_paths"]})
    if descriptor["alignment_path"] is not None:
        roles[descriptor["alignment_path"]] = "ALIGNMENT_INPUT"
    roles.update({item: "EVIDENCE" for item in evidence_paths})
    roles[descriptor["comparison_path"]] = "COMPARISON_OUTPUT"
    roles[descriptor["report_path"]] = "MARKDOWN_OUTPUT"
    result = {
        "schema_id": "nexah.compare.package-manifest",
        "schema_version": "0.1.0",
        "package_id": descriptor["package_id"],
        "profile_id": PROFILE_ID,
        "entries": [_file_entry(root, path, roles[path]) for path in sorted(roles)],
    }
    validate_with_schema(result, PACKAGE_SCHEMAS / "package-manifest.schema.json")
    return result


def _receipt(
    descriptor: dict[str, Any],
    comparison: dict[str, Any],
    manifest: dict[str, Any],
    report: bytes,
) -> dict[str, Any]:
    case_slug = comparison["case_id"].removeprefix("CASE-")
    counts = Counter(item["classification"] for item in comparison["relation_groups"])
    result = {
        "schema_id": "nexah.compare.run-receipt",
        "schema_version": "0.1.0",
        "receipt_id": f"RUN-{case_slug}-0001",
        "package_id": descriptor["package_id"],
        "profile_id": PROFILE_ID,
        "runtime_version": RUNTIME_VERSION,
        "schema_engine": "jsonschema-draft-2020-12",
        "command": "nexah-compare run-package --package .",
        "status": "VALID",
        "manifest_sha256": canonical_sha256(manifest),
        "comparison_id": comparison["record_id"],
        "comparison_sha256": canonical_sha256(comparison),
        "report_sha256": hashlib.sha256(report).hexdigest(),
        "relation_counts": {
            key: counts[key] for key in ("INVARIANT", "LOST", "ADDED", "UNAVAILABLE")
        },
        "residual_count": len(comparison["residuals"]),
        "abstention_count": len(comparison["abstentions"]),
    }
    validate_with_schema(result, PACKAGE_SCHEMAS / "run-receipt.schema.json")
    return result


def run_package(root: Path) -> dict[str, Any]:
    if root.is_symlink():
        raise CompareError("PACKAGE_SYMLINK_REJECTED", str(root))
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise CompareError("PACKAGE_ROOT_NOT_DIRECTORY", str(root))
    descriptor = _load_descriptor(root)
    case, analyses, alignment = _load_inputs(root, descriptor)
    evidence_paths = _evidence_paths(root, case)
    base = _base_files(descriptor, evidence_paths)
    allowed = base | OUTPUT_PATHS | {descriptor["return_path"]}
    _assert_inventory(root, allowed)
    if _package_path(root, descriptor["return_path"], must_exist=False).exists():
        raise CompareError("EXISTING_RETURN_BLOCKS_RERUN", descriptor["return_path"])
    comparison = compare_records(
        case,
        analyses,
        reference_analysis_id=descriptor["reference_analysis_id"],
        alignment_plan=alignment,
    )
    report = render_markdown(comparison)
    _atomic_write(_package_path(root, descriptor["comparison_path"], must_exist=False), canonical_bytes(comparison))
    _atomic_write(_package_path(root, descriptor["report_path"], must_exist=False), report)
    manifest = _manifest(root, descriptor, evidence_paths)
    _atomic_write(_package_path(root, descriptor["manifest_path"], must_exist=False), canonical_bytes(manifest))
    receipt = _receipt(descriptor, comparison, manifest, report)
    _atomic_write(_package_path(root, descriptor["receipt_path"], must_exist=False), canonical_bytes(receipt))
    return verify_package(root)


def verify_package(root: Path) -> dict[str, Any]:
    if root.is_symlink():
        raise CompareError("PACKAGE_SYMLINK_REJECTED", str(root))
    root = root.resolve(strict=True)
    descriptor = _load_descriptor(root)
    case, analyses, alignment = _load_inputs(root, descriptor)
    evidence_paths = _evidence_paths(root, case)
    base = _base_files(descriptor, evidence_paths)
    allowed = base | OUTPUT_PATHS | {descriptor["return_path"]}
    _assert_inventory(root, allowed)
    comparison_path = _package_path(root, descriptor["comparison_path"])
    comparison = load_json(comparison_path)
    validate_schema(comparison)
    if comparison_path.read_bytes() != canonical_bytes(comparison):
        raise CompareError("NONCANONICAL_COMPARISON", descriptor["comparison_path"])
    expected = compare_records(
        case,
        analyses,
        reference_analysis_id=descriptor["reference_analysis_id"],
        alignment_plan=alignment,
    )
    if canonical_bytes(expected) != canonical_bytes(comparison):
        raise CompareError("COMPARISON_REPLAY_MISMATCH", comparison["record_id"])
    report_path = _package_path(root, descriptor["report_path"])
    report = report_path.read_bytes()
    if report != render_markdown(comparison):
        raise CompareError("MARKDOWN_PROJECTION_MISMATCH", descriptor["report_path"])
    manifest_path = _package_path(root, descriptor["manifest_path"])
    manifest = load_json(manifest_path)
    validate_with_schema(manifest, PACKAGE_SCHEMAS / "package-manifest.schema.json")
    expected_manifest = _manifest(root, descriptor, evidence_paths)
    if canonical_bytes(manifest) != canonical_bytes(expected_manifest):
        raise CompareError("PACKAGE_MANIFEST_MISMATCH", descriptor["manifest_path"])
    receipt_path = _package_path(root, descriptor["receipt_path"])
    receipt = load_json(receipt_path)
    validate_with_schema(receipt, PACKAGE_SCHEMAS / "run-receipt.schema.json")
    expected_receipt = _receipt(descriptor, comparison, manifest, report)
    if canonical_bytes(receipt) != canonical_bytes(expected_receipt):
        raise CompareError("RUN_RECEIPT_MISMATCH", descriptor["receipt_path"])
    return_path = _package_path(root, descriptor["return_path"], must_exist=False)
    human_return = "ABSENT"
    if return_path.exists():
        returned = load_json(return_path)
        validate_return(returned, comparison)
        human_return = returned["human_action"]
    return {
        "status": "VALID",
        "package_id": descriptor["package_id"],
        "comparison_id": comparison["record_id"],
        "comparison_sha256": canonical_sha256(comparison),
        "manifest_sha256": canonical_sha256(manifest),
        "human_return": human_return,
    }


def validate_return(returned: dict[str, Any], comparison: dict[str, Any]) -> None:
    validate_schema(returned)
    if returned["case_id"] != comparison["case_id"]:
        raise CompareError("RETURN_CASE_MISMATCH", returned["case_id"])
    if returned["comparison_id"] != comparison["record_id"]:
        raise CompareError("RETURN_COMPARISON_MISMATCH", returned["comparison_id"])
    if returned["comparison_sha256"] != canonical_sha256(comparison):
        raise CompareError("RETURN_HASH_MISMATCH", returned["comparison_sha256"])
    residual_ids = {item["residual_id"] for item in comparison["residuals"]}
    unknown = sorted(set(returned["selected_residual_ids"]) - residual_ids)
    if unknown:
        raise CompareError("RETURN_UNKNOWN_RESIDUAL", ",".join(unknown))
    if returned["human_action"] == "AMEND" and not returned["amendments"]:
        raise CompareError("AMENDMENT_REQUIRED", returned["record_id"])
    if returned["human_action"] != "AMEND" and returned["amendments"]:
        raise CompareError("AMENDMENT_NOT_ALLOWED", returned["record_id"])
    target_ids = {
        comparison["record_id"],
        *(item["relation_id"] for item in comparison["relation_groups"]),
        *(item["residual_id"] for item in comparison["residuals"]),
        *(item["check_id"] for item in comparison["calculation_checks"]),
        *(
            member["claim_id"]
            for relation in comparison["relation_groups"]
            for member in relation["members"]
            if member["claim_id"] is not None
        ),
    }
    unknown_targets = sorted(
        item["target_id"] for item in returned["amendments"] if item["target_id"] not in target_ids
    )
    if unknown_targets:
        raise CompareError("RETURN_UNKNOWN_AMENDMENT_TARGET", ",".join(unknown_targets))


def create_return(
    root: Path,
    *,
    action: str,
    actor_id: str,
    statement: str,
    returned_at: str,
    selected_residual_ids: list[str] | None = None,
    amendments: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    if root.is_symlink():
        raise CompareError("PACKAGE_SYMLINK_REJECTED", str(root))
    root = root.resolve(strict=True)
    verification = verify_package(root)
    descriptor = _load_descriptor(root)
    return_path = _package_path(root, descriptor["return_path"], must_exist=False)
    if return_path.exists():
        raise CompareError("RETURN_ALREADY_EXISTS", descriptor["return_path"])
    comparison = load_json(_package_path(root, descriptor["comparison_path"]))
    case_slug = comparison["case_id"].removeprefix("CASE-")
    returned = {
        "schema_id": "nexah.compare.return-record",
        "schema_version": "0.1.0",
        "record_id": f"RET-{case_slug}-0001",
        "profile_id": PROFILE_ID,
        "case_id": comparison["case_id"],
        "comparison_id": comparison["record_id"],
        "comparison_sha256": verification["comparison_sha256"],
        "human_action": action,
        "selected_residual_ids": selected_residual_ids or [],
        "amendments": amendments or [],
        "human_statement": statement,
        "returned_at": returned_at,
        "actor_id": actor_id,
    }
    validate_return(returned, comparison)
    _atomic_write(return_path, canonical_bytes(returned))
    verify_package(root)
    return returned
