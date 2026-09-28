"""Canonical JSON, contract validation and deterministic comparison runtime."""

from __future__ import annotations

import ast
import hashlib
import json
import keyword
import math
import re
import unicodedata
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, localcontext
from pathlib import Path
from typing import Any, Iterable


PROFILE_ID = "NC01-ADVISORY-0.1"
CLAIM_CEILING = (
    "DECLARED_CONFIRMED_RECORD_COMPARISON_ONLY_NO_TRUTH_CORRECTNESS_"
    "COMPLETENESS_SAFETY_SUITABILITY_CAUSALITY_RECOMMENDATION_"
    "BUSINESS_SUCCESS_OR_PRODUCT_MARKET_FIT_CLAIM"
)
ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "schemas"
SCHEMA_BY_RECORD = {
    "nexah.compare.case-record": "case-record.schema.json",
    "nexah.compare.analysis-record": "analysis-record.schema.json",
    "nexah.compare.comparison-record": "comparison-record.schema.json",
    "nexah.compare.return-record": "return-record.schema.json",
}
ALIGNMENT_KEY_RE = re.compile(r"^[A-Z0-9][A-Z0-9._-]{0,127}$")


class CompareError(ValueError):
    """Fail-closed error with a stable machine reason code."""

    def __init__(self, code: str, detail: str, *, exit_code: int = 2) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail
        self.exit_code = exit_code


def _reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CompareError("DUPLICATE_JSON_KEY", key)
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise CompareError("NON_FINITE_NUMBER", value)


def load_json(path: Path) -> Any:
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(
                handle,
                object_pairs_hook=_reject_duplicates,
                parse_constant=_reject_constant,
            )
    except CompareError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise CompareError("INVALID_JSON_INPUT", f"{path}: {error}") from error


def canonical_bytes(value: Any) -> bytes:
    def inspect(item: Any) -> None:
        if isinstance(item, float) and not math.isfinite(item):
            raise CompareError("NON_FINITE_NUMBER", repr(item))
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


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _schema_engine() -> tuple[Any, Any, Any, Any]:
    try:
        from jsonschema import Draft202012Validator, FormatChecker
        from referencing import Registry, Resource
    except ImportError as error:
        raise CompareError(
            "SCHEMA_ENGINE_UNAVAILABLE",
            "jsonschema>=4.23 with referencing is required for Draft 2020-12",
            exit_code=4,
        ) from error
    return Draft202012Validator, FormatChecker, Registry, Resource


def validate_with_schema(record: dict[str, Any], schema_path: Path) -> None:
    if not isinstance(record, dict):
        raise CompareError("NOT_OBJECT", "record")
    Draft202012Validator, FormatChecker, Registry, Resource = _schema_engine()
    schema_paths = sorted(SCHEMA_DIR.glob("*.schema.json"))
    package_schema_dir = ROOT / "package_contract"
    if package_schema_dir.is_dir():
        schema_paths.extend(sorted(package_schema_dir.glob("*.schema.json")))
    schemas = [load_json(path) for path in schema_paths]
    registry = Registry().with_resources(
        [(schema["$id"], Resource.from_contents(schema)) for schema in schemas]
    )
    schema = load_json(schema_path)
    validator = Draft202012Validator(
        schema,
        registry=registry,
        format_checker=FormatChecker(),
    )
    errors = sorted(validator.iter_errors(record), key=lambda item: list(item.path))
    if errors:
        error = errors[0]
        location = "/".join(str(part) for part in error.absolute_path) or "$"
        raise CompareError("SCHEMA_VALIDATION_FAILED", f"{location}: {error.message}")


def validate_schema(record: dict[str, Any]) -> None:
    schema_id = record.get("schema_id") if isinstance(record, dict) else None
    schema_name = SCHEMA_BY_RECORD.get(schema_id)
    if schema_name is None:
        raise CompareError("UNKNOWN_SCHEMA_ID", str(schema_id))
    validate_with_schema(record, SCHEMA_DIR / schema_name)


def _normal_text(value: str) -> str:
    return unicodedata.normalize("NFC", value)


def _claim_payload(claim: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in claim.items() if key != "claim_id"}


def _exact_signature(claim: dict[str, Any]) -> str:
    return canonical_sha256(_claim_payload(claim))


def _claim_index(analyses: list[dict[str, Any]]) -> dict[str, tuple[str, dict[str, Any]]]:
    result: dict[str, tuple[str, dict[str, Any]]] = {}
    for analysis in analyses:
        for claim in analysis["claims"]:
            claim_id = claim["claim_id"]
            if claim_id in result:
                raise CompareError("DUPLICATE_CLAIM_ID", claim_id)
            result[claim_id] = (analysis["record_id"], claim)
    return result


def validate_links(case: dict[str, Any], analyses: list[dict[str, Any]]) -> None:
    validate_schema(case)
    if not 2 <= len(analyses) <= 4:
        raise CompareError("ANALYSIS_COUNT_OUT_OF_RANGE", str(len(analyses)))
    analysis_ids: set[str] = set()
    evidence = {item["evidence_id"]: item for item in case["evidence"]}
    for analysis in analyses:
        validate_schema(analysis)
        analysis_id = analysis["record_id"]
        if analysis_id in analysis_ids:
            raise CompareError("DUPLICATE_ANALYSIS_ID", analysis_id)
        analysis_ids.add(analysis_id)
        if analysis["case_id"] != case["record_id"]:
            raise CompareError("CASE_LINK_MISMATCH", analysis_id)
        for claim in analysis["claims"]:
            unknown = sorted(set(claim["evidence_ids"]) - set(evidence))
            if unknown:
                raise CompareError(
                    "UNKNOWN_EVIDENCE_REF", f"{claim['claim_id']}: {','.join(unknown)}"
                )
    _claim_index(analyses)


def _auto_alignment(
    case: dict[str, Any], analyses: list[dict[str, Any]], reference_id: str
) -> dict[str, Any]:
    by_analysis: dict[str, dict[str, str]] = {}
    for analysis in analyses:
        signatures: dict[str, str] = {}
        for claim in analysis["claims"]:
            signature = _exact_signature(claim)
            if signature in signatures:
                raise CompareError(
                    "AMBIGUOUS_EXACT_ALIGNMENT",
                    f"{analysis['record_id']}: {signature}",
                    exit_code=3,
                )
            signatures[signature] = claim["claim_id"]
        by_analysis[analysis["record_id"]] = signatures
    all_signatures = sorted({item for values in by_analysis.values() for item in values})
    analysis_ids = sorted(by_analysis)
    groups = []
    for index, signature in enumerate(all_signatures, start=1):
        groups.append(
            {
                "alignment_key": f"EXACT-{index:04d}-{signature[:12].upper()}",
                "mode": "EXACT",
                "criterion": "Exact canonical claim payload equality",
                "claim_ids": {
                    analysis_id: by_analysis[analysis_id].get(signature)
                    for analysis_id in analysis_ids
                },
            }
        )
    return {
        "profile_id": PROFILE_ID,
        "case_id": case["record_id"],
        "reference_analysis_id": reference_id,
        "groups": groups,
    }


def validate_alignment(
    plan: dict[str, Any], case: dict[str, Any], analyses: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    if not isinstance(plan, dict):
        raise CompareError("INVALID_ALIGNMENT_PLAN", "not an object", exit_code=3)
    required = {"profile_id", "case_id", "reference_analysis_id", "groups"}
    if set(plan) != required:
        raise CompareError(
            "INVALID_ALIGNMENT_PLAN_FIELDS", repr(sorted(set(plan) ^ required)), exit_code=3
        )
    if plan["profile_id"] != PROFILE_ID or plan["case_id"] != case["record_id"]:
        raise CompareError("ALIGNMENT_SCOPE_MISMATCH", str(plan.get("case_id")), exit_code=3)
    analysis_ids = sorted(item["record_id"] for item in analyses)
    if plan["reference_analysis_id"] not in analysis_ids:
        raise CompareError(
            "REFERENCE_NOT_IN_ANALYSES", str(plan["reference_analysis_id"]), exit_code=3
        )
    groups = plan["groups"]
    if not isinstance(groups, list) or not groups:
        raise CompareError("EMPTY_ALIGNMENT", "groups", exit_code=3)
    claims = _claim_index(analyses)
    used: set[str] = set()
    keys: set[str] = set()
    normalized: list[dict[str, Any]] = []
    for group in groups:
        if not isinstance(group, dict) or set(group) != {
            "alignment_key",
            "mode",
            "criterion",
            "claim_ids",
        }:
            raise CompareError("INVALID_ALIGNMENT_GROUP", repr(group), exit_code=3)
        key = group["alignment_key"]
        if not isinstance(key, str) or ALIGNMENT_KEY_RE.fullmatch(key) is None or key in keys:
            raise CompareError("INVALID_ALIGNMENT_KEY", str(key), exit_code=3)
        keys.add(key)
        if group["mode"] not in {"EXACT", "DECLARED_KEY"}:
            raise CompareError("INVALID_ALIGNMENT_MODE", str(group["mode"]), exit_code=3)
        if not isinstance(group["criterion"], str) or not group["criterion"].strip():
            raise CompareError("EMPTY_ALIGNMENT_CRITERION", key, exit_code=3)
        mapping = group["claim_ids"]
        if not isinstance(mapping, dict) or sorted(mapping) != analysis_ids:
            raise CompareError("ALIGNMENT_ANALYSIS_SET_MISMATCH", key, exit_code=3)
        if not any(value is not None for value in mapping.values()):
            raise CompareError("EMPTY_ALIGNMENT_GROUP", key, exit_code=3)
        for analysis_id, claim_id in mapping.items():
            if claim_id is None:
                continue
            owner = claims.get(claim_id)
            if owner is None or owner[0] != analysis_id:
                raise CompareError(
                    "ALIGNMENT_CLAIM_OWNER_MISMATCH", f"{analysis_id}:{claim_id}", exit_code=3
                )
            if claim_id in used:
                raise CompareError("CLAIM_IN_MULTIPLE_RELATIONS", claim_id, exit_code=3)
            used.add(claim_id)
        selected = [claims[item][1] for item in mapping.values() if item is not None]
        if group["mode"] == "EXACT" and len({_exact_signature(item) for item in selected}) > 1:
            raise CompareError("EXACT_ALIGNMENT_MISMATCH", key, exit_code=3)
        normalized.append(group)
    missing = sorted(set(claims) - used)
    if missing:
        raise CompareError("UNALIGNED_CLAIMS", ",".join(missing), exit_code=3)
    return sorted(normalized, key=lambda item: item["alignment_key"])


_ALLOWED_BINARY = {
    ast.Add: lambda left, right: left + right,
    ast.Sub: lambda left, right: left - right,
    ast.Mult: lambda left, right: left * right,
    ast.Div: lambda left, right: left / right,
}
_ALLOWED_UNARY = {ast.UAdd: lambda value: value, ast.USub: lambda value: -value}


def evaluate_formula(formula: str, operands: list[dict[str, Any]]) -> Decimal:
    values: dict[str, Decimal] = {}
    for operand in operands:
        name = operand["name"]
        if not name.isidentifier() or keyword.iskeyword(name):
            raise CompareError("UNSUPPORTED_OPERAND_NAME", name, exit_code=4)
        if name in values:
            raise CompareError("DUPLICATE_OPERAND_NAME", name, exit_code=4)
        try:
            values[name] = Decimal(operand["quantity"]["value"])
        except InvalidOperation as error:
            raise CompareError("INVALID_DECIMAL", name, exit_code=4) from error
    try:
        tree = ast.parse(formula, mode="eval")
    except SyntaxError as error:
        raise CompareError("UNSUPPORTED_FORMULA", formula, exit_code=4) from error

    def visit(node: ast.AST) -> Decimal:
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Name) and node.id in values:
            return values[node.id]
        if (
            isinstance(node, ast.Constant)
            and isinstance(node.value, (int, float))
            and not isinstance(node.value, bool)
        ):
            return Decimal(str(node.value))
        if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BINARY:
            return _ALLOWED_BINARY[type(node.op)](visit(node.left), visit(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_UNARY:
            return _ALLOWED_UNARY[type(node.op)](visit(node.operand))
        raise CompareError("UNSUPPORTED_FORMULA", ast.dump(node), exit_code=4)

    try:
        with localcontext() as context:
            context.prec = 50
            return visit(tree)
    except (ArithmeticError, InvalidOperation, ZeroDivisionError) as error:
        raise CompareError("FORMULA_EVALUATION_FAILED", formula, exit_code=4) from error


def _calculation_reason(claims: list[dict[str, Any]]) -> tuple[str, str, str]:
    calculations = [claim["calculation"] for claim in claims]
    try:
        for calculation in calculations:
            observed = evaluate_formula(calculation["formula"], calculation["operands"])
            expected = Decimal(calculation["result"]["value"])
            tolerance = abs(Decimal(calculation["tolerance"]))
            if abs(observed - expected) > tolerance:
                return (
                    "MISMATCH",
                    "OPERAND_MISMATCH",
                    f"Declared result {expected} differs from evaluated result {observed}",
                )
    except CompareError as error:
        return "UNRESOLVED", "REQUIRED_METADATA_UNAVAILABLE", str(error)
    results = [item["result"] for item in calculations]
    if len({(item["unit_system"], item["unit"]) for item in results}) != 1:
        return "MISMATCH", "UNIT_MISMATCH", "Result units are not identical; no conversion is authorized"
    if len({item["time_basis"] for item in results}) != 1:
        return "MISMATCH", "TIME_BASIS_MISMATCH", "Result time bases are not identical; no conversion is authorized"
    formulas = {" ".join(item["formula"].split()) for item in calculations}
    if len(formulas) != 1:
        return "MISMATCH", "FORMULA_MISMATCH", "Declared formulas differ"
    operand_views = []
    for calculation in calculations:
        operand_views.append(
            canonical_bytes(
                sorted(calculation["operands"], key=lambda item: item["name"])
            )
        )
    if len(set(operand_views)) != 1:
        return "MISMATCH", "OPERAND_MISMATCH", "Declared operands differ"
    values = [Decimal(item["value"]) for item in results]
    tolerance = max(abs(Decimal(item["tolerance"])) for item in calculations)
    if max(values) - min(values) > tolerance:
        return "MISMATCH", "OPERAND_MISMATCH", "Declared results differ beyond tolerance"
    return "MATCH", "FORMULA_MATCH", "Formula, operands, result, unit and time basis match exactly"


def _evidence_reason(
    claims: list[dict[str, Any]], evidence: dict[str, dict[str, Any]]
) -> str | None:
    statuses = []
    evidence_sets = []
    for claim in claims:
        evidence_sets.append(tuple(sorted(claim["evidence_ids"])))
        statuses.extend(evidence[item]["status"] for item in claim["evidence_ids"])
    if any(status != "ADMITTED" for status in statuses):
        return "EVIDENCE_MISSING"
    if len(set(evidence_sets)) != 1:
        return "EVIDENCE_ASYMMETRY"
    return None


def _classify_present(
    claims: list[dict[str, Any]], evidence: dict[str, dict[str, Any]]
) -> tuple[str, str, str, tuple[str, str, str] | None]:
    kinds = {claim["kind"] for claim in claims}
    if len(kinds) != 1:
        return "UNAVAILABLE", "DOMAIN_INCOMPATIBLE", "Claim kinds differ", None
    kind = claims[0]["kind"]
    calculation_check = None
    if kind == "CALCULATION":
        calculation_check = _calculation_reason(claims)
        if calculation_check[0] != "MATCH":
            return "UNAVAILABLE", calculation_check[1], calculation_check[2], calculation_check
    evidence_reason = _evidence_reason(claims, evidence)
    if evidence_reason:
        return "UNAVAILABLE", evidence_reason, "Evidence status or coverage differs", calculation_check
    payloads = [canonical_bytes(_claim_payload(claim)) for claim in claims]
    if len(set(payloads)) == 1:
        return "INVARIANT", "MATERIAL_EQUIVALENCE", "Exact canonical payload match", calculation_check
    statements = {_normal_text(claim["statement"]) for claim in claims}
    if kind == "ASSUMPTION":
        return "UNAVAILABLE", "ASSUMPTION_CONFLICT", "Assumption payloads differ", calculation_check
    if kind == "RECOMMENDATION":
        return (
            "UNAVAILABLE",
            "RECOMMENDATION_BOUNDARY_CONFLICT",
            "Recommendation statement or conditions differ",
            calculation_check,
        )
    if kind == "FACT" and len(statements) != 1:
        return (
            "UNAVAILABLE",
            "CRITERION_UNAVAILABLE",
            "Non-identical fact prose has no structured equivalence criterion",
            calculation_check,
        )
    return (
        "UNAVAILABLE",
        "CRITERION_UNAVAILABLE",
        "Claim payloads differ outside the supported exact criterion",
        calculation_check,
    )


def _severity(claims: Iterable[dict[str, Any]]) -> str:
    values = {claim["materiality"] for claim in claims}
    for level in ("CRITICAL", "MATERIAL", "CONTEXT"):
        if level in values:
            return level
    return "CONTEXT"


def _abstention_code(reason: str) -> str:
    if reason == "UNIT_MISMATCH":
        return "INCOMPATIBLE_UNITS"
    if reason == "TIME_BASIS_MISMATCH":
        return "INCOMPATIBLE_TIME_BASIS"
    if reason in {"EVIDENCE_MISSING", "EVIDENCE_ASYMMETRY"}:
        return "INSUFFICIENT_EVIDENCE"
    return "UNSUPPORTED_OPERATION"


def compare_records(
    case: dict[str, Any],
    analyses: list[dict[str, Any]],
    *,
    reference_analysis_id: str | None = None,
    alignment_plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    validate_links(case, analyses)
    analyses = sorted(analyses, key=lambda item: item["record_id"])
    analysis_by_id = {item["record_id"]: item for item in analyses}
    reference_id = reference_analysis_id or analyses[0]["record_id"]
    if reference_id not in analysis_by_id:
        raise CompareError("REFERENCE_NOT_IN_ANALYSES", reference_id, exit_code=3)
    if alignment_plan is None:
        alignment_plan = _auto_alignment(case, analyses, reference_id)
    elif reference_analysis_id is not None and alignment_plan.get("reference_analysis_id") != reference_id:
        raise CompareError("REFERENCE_ALIGNMENT_MISMATCH", reference_id, exit_code=3)
    reference_id = alignment_plan["reference_analysis_id"]
    groups = validate_alignment(alignment_plan, case, analyses)
    claims = _claim_index(analyses)
    evidence = {item["evidence_id"]: item for item in case["evidence"]}
    ordered_analysis_ids = [reference_id] + [
        item for item in sorted(analysis_by_id) if item != reference_id
    ]
    case_slug = case["record_id"].removeprefix("CASE-")
    relation_groups = []
    calculation_checks = []
    residuals = []
    abstentions = []
    for index, group in enumerate(groups, start=1):
        relation_id = f"REL-{case_slug}-{index:04d}"
        mapping = group["claim_ids"]
        present_claims = [claims[item][1] for item in mapping.values() if item is not None]
        reference_claim = mapping[reference_id]
        missing_outside = [item for item in ordered_analysis_ids if mapping[item] is None]
        calculation_check = None
        if reference_claim is not None and missing_outside:
            classification = "LOST"
            reason = "MISSING_COUNTERPART"
            detail = "Reference claim has no counterpart in one or more analyses"
        elif reference_claim is None:
            classification = "ADDED"
            reason = "PRESENT_ONLY_OUTSIDE_REFERENCE"
            detail = "Claim appears only outside the reference analysis"
        else:
            classification, reason, detail, calculation_check = _classify_present(
                present_claims, evidence
            )
        members = []
        for analysis_id in ordered_analysis_ids:
            claim_id = mapping[analysis_id]
            members.append(
                {
                    "analysis_id": analysis_id,
                    "claim_id": claim_id,
                    "role": (
                        "MISSING"
                        if claim_id is None
                        else "REFERENCE"
                        if analysis_id == reference_id
                        else "COUNTERPART"
                    ),
                }
            )
        relation_groups.append(
            {
                "relation_id": relation_id,
                "classification": classification,
                "criterion": group["criterion"],
                "reason_code": reason,
                "members": members,
            }
        )
        if calculation_check is not None:
            calculation_checks.append(
                {
                    "check_id": f"CHK-{case_slug}-{len(calculation_checks) + 1:04d}",
                    "claim_ids": sorted(item["claim_id"] for item in present_claims),
                    "status": calculation_check[0],
                    "reason_code": calculation_check[1],
                    "detail": calculation_check[2],
                }
            )
        if classification != "INVARIANT":
            severity = _severity(present_claims)
            gate_effect = (
                "ABSTAIN"
                if classification == "UNAVAILABLE" and severity in {"CRITICAL", "MATERIAL"}
                else "ABSTAIN"
                if classification == "LOST" and severity == "CRITICAL"
                else "NONE"
            )
            residual_id = f"RES-{case_slug}-{len(residuals) + 1:04d}"
            residuals.append(
                {
                    "residual_id": residual_id,
                    "relation_id": relation_id,
                    "severity": severity,
                    "reason_code": reason,
                    "expected": group["criterion"],
                    "observed": detail,
                    "gate_effect": gate_effect,
                }
            )
            if gate_effect == "ABSTAIN":
                abstentions.append(
                    {
                        "subject_id": relation_id,
                        "reason_code": _abstention_code(reason),
                        "statement": f"Comparison abstains for {group['alignment_key']}: {detail}",
                    }
                )
    comparison = {
        "schema_id": "nexah.compare.comparison-record",
        "schema_version": "0.1.0",
        "record_id": f"CMP-{case_slug}-ADVISORY-01",
        "profile_id": PROFILE_ID,
        "case_id": case["record_id"],
        "analysis_ids": sorted(analysis_by_id),
        "reference_analysis_id": reference_id,
        "relation_groups": relation_groups,
        "calculation_checks": calculation_checks,
        "residuals": residuals,
        "abstentions": abstentions,
        "claim_ceiling": CLAIM_CEILING,
    }
    validate_schema(comparison)
    return comparison
