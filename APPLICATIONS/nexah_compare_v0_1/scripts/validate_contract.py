#!/usr/bin/env python3
"""Dependency-free WP2 contract and fixture checker for NEXAH Compare v0.1."""

from __future__ import annotations

import hashlib
import csv
import json
import math
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
FIXTURES = ROOT / "fixtures"

ID_RE = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9][A-Z0-9._-]*)+$")
SHA_RE = re.compile(r"^[a-f0-9]{64}$")
CLAIM_KINDS = {"FACT", "ASSUMPTION", "CALCULATION", "RECOMMENDATION"}
CLASSIFICATIONS = {"INVARIANT", "LOST", "ADDED", "UNAVAILABLE"}
SCHEMA_FILES = {
    "nexah.compare.case-record": "case-record.schema.json",
    "nexah.compare.analysis-record": "analysis-record.schema.json",
    "nexah.compare.comparison-record": "comparison-record.schema.json",
    "nexah.compare.return-record": "return-record.schema.json",
}


class ContractError(ValueError):
    def __init__(self, code: str, detail: str) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code


def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ContractError("DUPLICATE_JSON_KEY", key)
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ContractError("NON_FINITE_NUMBER", value)


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(
            handle,
            object_pairs_hook=reject_duplicates,
            parse_constant=reject_constant,
        )


def canonical_bytes(value: Any) -> bytes:
    def inspect(item: Any) -> None:
        if isinstance(item, float) and not math.isfinite(item):
            raise ContractError("NON_FINITE_NUMBER", repr(item))
        if isinstance(item, dict):
            for child in item.values():
                inspect(child)
        elif isinstance(item, list):
            for child in item:
                inspect(child)

    inspect(value)
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def require(condition: bool, code: str, detail: str) -> None:
    if not condition:
        raise ContractError(code, detail)


def valid_id(value: Any, label: str) -> None:
    require(isinstance(value, str) and ID_RE.fullmatch(value) is not None, "INVALID_ID", label)


def valid_sha(value: Any, label: str) -> None:
    require(isinstance(value, str) and SHA_RE.fullmatch(value) is not None, "INVALID_SHA256", label)


def safe_relative_path(value: Any) -> bool:
    if not isinstance(value, str) or not value or value.startswith("/"):
        return False
    return ".." not in Path(value).parts


def check_confirmation(record: dict[str, Any]) -> None:
    confirmation = record.get("human_confirmation")
    require(isinstance(confirmation, dict), "NOT_HUMAN_CONFIRMED", "confirmation missing")
    require(confirmation.get("status") == "CONFIRMED", "NOT_HUMAN_CONFIRMED", "status")
    valid_id(confirmation.get("actor_id"), "confirmation.actor_id")
    valid_sha(confirmation.get("confirmation_sha256"), "confirmation.confirmation_sha256")


def check_common(record: dict[str, Any]) -> str:
    schema_id = record.get("schema_id")
    require(schema_id in SCHEMA_FILES, "UNKNOWN_SCHEMA_ID", str(schema_id))
    require(record.get("schema_version") == "0.1.0", "WRONG_SCHEMA_VERSION", str(record.get("schema_version")))
    require(record.get("profile_id") == "NC01-ADVISORY-0.1", "WRONG_PROFILE", str(record.get("profile_id")))
    valid_id(record.get("record_id"), "record_id")
    return str(schema_id)


def check_case(record: dict[str, Any]) -> None:
    check_confirmation(record)
    require(record.get("domain") == "BUSINESS_STRATEGY_NON_REGULATED", "OUT_OF_SCOPE_DOMAIN", str(record.get("domain")))
    options = record.get("decision_options")
    require(isinstance(options, list) and 2 <= len(options) <= 12, "OPTION_COUNT_OUT_OF_RANGE", "decision_options")
    for evidence in record.get("evidence", []):
        valid_id(evidence.get("evidence_id"), "evidence_id")
        if evidence.get("status") == "ADMITTED":
            require(safe_relative_path(evidence.get("path")), "UNSAFE_EVIDENCE_PATH", str(evidence.get("path")))
            valid_sha(evidence.get("sha256"), "evidence.sha256")


def check_analysis(record: dict[str, Any]) -> None:
    check_confirmation(record)
    valid_id(record.get("case_id"), "case_id")
    source = record.get("source")
    require(isinstance(source, dict), "MISSING_SOURCE", "source")
    valid_sha(source.get("source_sha256"), "source.source_sha256")
    claims = record.get("claims")
    require(isinstance(claims, list) and claims, "NO_CLAIMS", "claims")
    seen: set[str] = set()
    for claim in claims:
        claim_id = claim.get("claim_id")
        valid_id(claim_id, "claim_id")
        require(claim_id not in seen, "DUPLICATE_CLAIM_ID", str(claim_id))
        seen.add(claim_id)
        kind = claim.get("kind")
        require(kind in CLAIM_KINDS, "INVALID_CLAIM_KIND", str(kind))
        calculation = claim.get("calculation")
        if kind == "CALCULATION":
            require(isinstance(calculation, dict), "CALCULATION_MISSING", str(claim_id))
        else:
            require(calculation is None, "CALCULATION_ON_NON_CALCULATION", str(claim_id))


def check_comparison(record: dict[str, Any]) -> None:
    valid_id(record.get("case_id"), "case_id")
    analysis_ids = record.get("analysis_ids")
    require(isinstance(analysis_ids, list) and 2 <= len(analysis_ids) <= 4, "ANALYSIS_COUNT_OUT_OF_RANGE", str(analysis_ids))
    require(len(analysis_ids) == len(set(analysis_ids)), "DUPLICATE_ANALYSIS_ID", "analysis_ids")
    require(record.get("reference_analysis_id") in analysis_ids, "REFERENCE_NOT_IN_ANALYSES", "reference_analysis_id")
    claim_membership: set[str] = set()
    for relation in record.get("relation_groups", []):
        require(relation.get("classification") in CLASSIFICATIONS, "INVALID_CLASSIFICATION", str(relation.get("classification")))
        for member in relation.get("members", []):
            require(member.get("analysis_id") in analysis_ids, "UNKNOWN_MEMBER_ANALYSIS", str(member.get("analysis_id")))
            claim_id = member.get("claim_id")
            if member.get("role") == "MISSING":
                require(claim_id is None, "MISSING_MEMBER_HAS_CLAIM", str(claim_id))
            elif claim_id is not None:
                valid_id(claim_id, "relation.claim_id")
                require(claim_id not in claim_membership, "CLAIM_IN_MULTIPLE_RELATIONS", claim_id)
                claim_membership.add(claim_id)


def check_return(record: dict[str, Any]) -> None:
    valid_id(record.get("case_id"), "case_id")
    valid_id(record.get("comparison_id"), "comparison_id")
    valid_sha(record.get("comparison_sha256"), "comparison_sha256")
    require(record.get("human_action") in {"CONFIRM", "AMEND", "ABSTAIN", "STOP"}, "INVALID_HUMAN_ACTION", str(record.get("human_action")))


def check_record(record: dict[str, Any]) -> None:
    require(isinstance(record, dict), "NOT_OBJECT", "record")
    schema_id = check_common(record)
    if schema_id == "nexah.compare.case-record":
        check_case(record)
    elif schema_id == "nexah.compare.analysis-record":
        check_analysis(record)
    elif schema_id == "nexah.compare.comparison-record":
        check_comparison(record)
    else:
        check_return(record)


def walk_refs(value: Any) -> list[str]:
    refs: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "$ref" and isinstance(child, str):
                refs.append(child)
            else:
                refs.extend(walk_refs(child))
    elif isinstance(value, list):
        for child in value:
            refs.extend(walk_refs(child))
    return refs


def check_schemas() -> None:
    expected = {"common.schema.json", *SCHEMA_FILES.values()}
    observed = {path.name for path in SCHEMAS.glob("*.schema.json")}
    require(observed == expected, "SCHEMA_SET_MISMATCH", repr(sorted(observed)))
    for name in sorted(expected):
        schema = load_json(SCHEMAS / name)
        require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "SCHEMA_DIALECT_MISMATCH", name)
        require(isinstance(schema.get("$id"), str), "SCHEMA_ID_MISSING", name)
        for ref in walk_refs(schema):
            if ref.startswith("http") or ref.startswith("#"):
                continue
            target = ref.split("#", 1)[0]
            require((SCHEMAS / target).is_file(), "BROKEN_LOCAL_REF", f"{name}: {ref}")


def check_source_ledger() -> int:
    ledger = ROOT / "SOURCE_ADOPTION_LEDGER.csv"
    with ledger.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    require(len(rows) == 10, "SOURCE_LEDGER_COUNT_MISMATCH", str(len(rows)))
    for row in rows:
        source = (ROOT / row["source_path"]).resolve()
        require(source.is_file(), "PINNED_SOURCE_MISSING", f"{row['source_id']}: {source}")
        observed = hashlib.sha256(source.read_bytes()).hexdigest()
        require(observed == row["sha256"], "PINNED_SOURCE_HASH_MISMATCH", row["source_id"])
    return len(rows)


def check_positive(records: dict[str, dict[str, Any]]) -> None:
    for record in records.values():
        check_record(record)
        first = canonical_bytes(record)
        second = canonical_bytes(record)
        require(first == second and first.endswith(b"\n"), "CANONICAL_REPLAY_MISMATCH", record["record_id"])

    case = records["positive/case.json"]
    analyses = [records["positive/analysis-a.json"], records["positive/analysis-b.json"]]
    comparison = records["positive/comparison.json"]
    returned = records["positive/return.json"]
    evidence_ids = {item["evidence_id"] for item in case["evidence"]}
    claim_ids: set[str] = set()
    for analysis in analyses:
        require(analysis["case_id"] == case["record_id"], "CASE_LINK_MISMATCH", analysis["record_id"])
        for claim in analysis["claims"]:
            require(set(claim["evidence_ids"]) <= evidence_ids, "UNKNOWN_EVIDENCE_REF", claim["claim_id"])
            claim_ids.add(claim["claim_id"])
    require(set(comparison["analysis_ids"]) == {item["record_id"] for item in analyses}, "ANALYSIS_LINK_MISMATCH", "comparison")
    for relation in comparison["relation_groups"]:
        for member in relation["members"]:
            if member["claim_id"] is not None:
                require(member["claim_id"] in claim_ids, "UNKNOWN_CLAIM_REF", member["claim_id"])
    require(returned["comparison_id"] == comparison["record_id"], "COMPARISON_LINK_MISMATCH", "return")
    expected_hash = hashlib.sha256(canonical_bytes(comparison)).hexdigest()
    require(returned["comparison_sha256"] == expected_hash, "COMPARISON_HASH_MISMATCH", expected_hash)
    residual_ids = {item["residual_id"] for item in comparison["residuals"]}
    require(set(returned["selected_residual_ids"]) <= residual_ids, "UNKNOWN_RESIDUAL_REF", "return")


def main() -> int:
    check_schemas()
    source_count = check_source_ledger()
    expectations = load_json(FIXTURES / "fixture_expectations.json")
    positive = {name: load_json(FIXTURES / name) for name in expectations["positive"]}
    check_positive(positive)
    for name, expected_code in expectations["negative"].items():
        try:
            check_record(load_json(FIXTURES / name))
        except ContractError as error:
            require(error.code == expected_code, "WRONG_NEGATIVE_RESULT", f"{name}: {error.code}")
        else:
            raise ContractError("NEGATIVE_CONTROL_ACCEPTED", name)
    print(json.dumps({
        "status": "VALID",
        "schemas": 5,
        "positive_records": len(positive),
        "negative_controls": len(expectations["negative"]),
        "pinned_sources": source_count,
        "canonical_profile": "NEXAH_COMPARE_CANONICAL_JSON_0_1"
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
