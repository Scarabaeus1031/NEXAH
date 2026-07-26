#!/usr/bin/env python3
"""Static fail-closed inspection of the one-shot diagnostic instrument."""

from __future__ import annotations

import ast
import hashlib
import json
import sys
from pathlib import Path


EXPECTED_SEQUENCE = (
    "analyze_ieee_geometry",
    "_fresh_evaluation_campaign",
    "analyze_ieee_geometry",
    "run_ieee_geometry_probe_suite",
    "build_ieee_geometry_orientation_brief",
    "render_orientation_brief_markdown",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _call_name(node: ast.Call) -> str:
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    return ""


def main() -> int:
    sidecar = Path(__file__).resolve().parents[1]
    instrument = sidecar / "diagnostic" / "instrumented_replay.py"
    protocol = sidecar / "diagnostic" / "INSTRUMENTED_REPLAY_PROTOCOL.md"
    binding = sidecar / "diagnostic" / "instrumented_replay_approval_binding.json"
    tree = ast.parse(instrument.read_text(encoding="utf-8"))
    execute = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "execute_once"
    )
    calls = [
        (_call_name(node), node.lineno)
        for node in ast.walk(execute)
        if isinstance(node, ast.Call)
    ]
    scientific_calls = [
        (name, line) for name, line in calls if name in EXPECTED_SEQUENCE
    ]
    sequence = tuple(name for name, _ in sorted(scientific_calls, key=lambda item: item[1]))
    replay_calls = [item for item in calls if item[0] == "_fresh_evaluation_campaign"]
    forbidden_calls = sorted(
        {name for name, _ in calls if name in {"runpp", "build_summary"}}
    )
    source = instrument.read_text(encoding="utf-8")
    binding_value = json.loads(binding.read_text(encoding="utf-8"))
    checks = {
        "exactly_one_ieee14_replay_call": len(replay_calls) == 1,
        "canonical_fresh_campaign_entrypoint_used": (
            "canonical_runner._fresh_evaluation_campaign(manifest)" in source
        ),
        "scientific_call_sequence_matches_canonical": sequence == EXPECTED_SEQUENCE,
        "no_direct_solver_or_canonical_summary_call": not forbidden_calls,
        "fresh_payloads_created_after_scientific_sequence": (
            source.index('fresh = {') > source.index(
                "evaluation_brief_markdown = render_orientation_brief_markdown"
            )
        ),
        "recursive_diff_after_scientific_sequence": (
            source.index("comparisons = {") > source.index('fresh = {')
        ),
        "output_forced_outside_source": (
            "diagnostic output must be outside source root" in source
        ),
        "retry_forbidden_in_ledger": source.count('"retry_permitted": False') >= 2,
        "approval_binds_protocol": (
            binding_value.get("protocol_sha256") == _sha256(protocol)
        ),
        "approval_binds_instrumentation": (
            binding_value.get("instrumentation_sha256") == _sha256(instrument)
        ),
        "official_g4_classification_preserved": (
            "G4_clean_replay_failed" in source
        ),
        "no_comparator_import_or_output": "comparator" not in source.lower()
        or '"comparator_output_generated": False' in source,
    }
    result = {
        "status": "passed" if all(checks.values()) else "failed",
        "checks": checks,
        "scientific_call_sequence": [
            {"call": name, "line": line}
            for name, line in sorted(scientific_calls, key=lambda item: item[1])
        ],
        "replay_call_count": len(replay_calls),
        "forbidden_calls": forbidden_calls,
        "instrumentation_sha256": _sha256(instrument),
        "protocol_sha256": _sha256(protocol),
        "binding_sha256": _sha256(binding),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())
