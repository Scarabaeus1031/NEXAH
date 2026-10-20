#!/usr/bin/env python3
"""Replay the source-contract gate without constructing structure from Q106."""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ECOSYSTEM = HERE.parents[7]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    contract = json.loads((HERE / "CONTRACT.json").read_text(encoding="utf-8"))
    ledger = json.loads((HERE / "SOURCE_LEDGER.json").read_text(encoding="utf-8"))
    checks: list[dict[str, object]] = []

    def check(name: str, passed: bool, observed: object, expected: object) -> None:
        checks.append({"name": name, "passed": bool(passed), "observed": observed, "expected": expected})

    check("contract identity extends A0-BL-023", contract["identity"]["extends"] == "A0-BL-023:NCS_292_Q106_INTERTWINER_RETURN_PACKAGE:V1", contract["identity"]["extends"], "A0-BL-023 parent")
    check("no new identity", contract["identity"]["creates"] == [], contract["identity"]["creates"], [])
    check("formal non-admitted status", contract["status"] == "FORMAL_DESIGN_VALIDATION_NOT_ADMITTED_NOT_PENT_08", contract["status"], "FORMAL_DESIGN_VALIDATION_NOT_ADMITTED_NOT_PENT_08")
    check("source ledger schema", ledger["schema"] == "nexah.formal-source-contract-ledger/1.0.0", ledger["schema"], "nexah.formal-source-contract-ledger/1.0.0")
    check("eleven source-side records", len(ledger["sources"]) == 11, len(ledger["sources"]), 11)

    source_ids = [source["source_id"] for source in ledger["sources"]]
    check("source IDs unique", len(source_ids) == len(set(source_ids)), len(set(source_ids)), len(source_ids))
    for source in ledger["sources"]:
        path = (ECOSYSTEM / source["path"]).resolve()
        inside = path == ECOSYSTEM or ECOSYSTEM in path.parents
        check(f"source inside ecosystem: {source['source_id']}", inside, str(path), str(ECOSYSTEM))
        check(f"source exists: {source['source_id']}", path.is_file(), path.is_file(), True)
        actual = sha256(path) if path.is_file() else None
        check(f"source hash: {source['source_id']}", actual == source["sha256"], actual, source["sha256"])

    roles = contract["declared_source_carrier"]["P4"]
    states = [(sector, role) for sector in range(5) for role in roles]
    check("X20 has twenty unique source coordinates", len(states) == 20 and len(set(states)) == 20, len(set(states)), 20)

    rotation = {(s, p): ((s + 1) % 5, p) for s, p in states}
    reflection = {(s, p): ((-s) % 5, p) for s, p in states}

    def apply(mapping: dict[tuple[int, str], tuple[int, str]], state: tuple[int, str], count: int = 1) -> tuple[int, str]:
        for _ in range(count):
            state = mapping[state]
        return state

    check("r_X has order five", all(apply(rotation, x, 5) == x for x in states), True, True)
    check("j_X is involutive", all(apply(reflection, x, 2) == x for x in states), True, True)
    dihedral = all(reflection[rotation[reflection[x]]] == apply(rotation, x, 4) for x in states)
    check("j_X r_X j_X equals r_X inverse", dihedral, dihedral, True)
    check("X20 edge set remains null", contract["declared_source_carrier"]["edge_set"] is None, contract["declared_source_carrier"]["edge_set"], None)
    check("X20 edge types remain null", contract["declared_source_carrier"]["edge_types"] is None, contract["declared_source_carrier"]["edge_types"], None)
    check("source review agrees edge set null", ledger["review_conclusion"]["x20_edge_set"] is None, ledger["review_conclusion"]["x20_edge_set"], None)
    check("source review agrees edge types null", ledger["review_conclusion"]["x20_edge_types"] is None, ledger["review_conclusion"]["x20_edge_types"], None)

    triple = contract["triple19_typing"]
    check("P_c and P_d typed as constructors", triple["constructors"] == ["P_c", "P_d"], triple["constructors"], ["P_c", "P_d"])
    triple_states = [(r, sign) for r in range(7) for sign in (1, -1)]
    antipode = {(r, sign): (6 - r, -sign) for r, sign in triple_states}
    check("Triple-19 has fourteen oriented states", len(triple_states) == triple["oriented_state_count"], len(triple_states), 14)
    check("A is involutive", all(antipode[antipode[x]] == x for x in triple_states), True, True)
    check("A is fixed-point-free on oriented states", all(antipode[x] != x for x in triple_states), True, True)
    check("Triple-19 carrier is not X20 by cardinality", len(triple_states) != len(states), f"{len(triple_states)} != {len(states)}", "14 != 20")
    check("Triple-19 to X20 map remains null", triple["map_to_x20"] is None and ledger["review_conclusion"]["triple19_to_x20_map"] is None, None, None)
    check("Triple-19 to Q106 map remains null", triple["map_to_q106"] is None and ledger["review_conclusion"]["triple19_to_q106_map"] is None, None, None)

    permutations = list(itertools.permutations((1, 2, 3, 4)))
    check("twenty-four inherited D5 orbit charts", len(permutations) == 24, len(permutations), 24)
    gate_rows = []
    for index, permutation in enumerate(permutations, start=1):
        gate_rows.append({
            "candidate_id": f"D5-{index:02d}",
            "source_role_order": "|".join(roles),
            "target_orbit_order": "|".join(str(value) for value in permutation),
            "adjacency_test": "NOT_EVALUATED",
            "pcpd_test": "NOT_EVALUATED",
            "status": "BLOCKED_SOURCE_CONTRACT_UNRECOVERED",
        })
    check("all charts blocked before target fit", all(row["status"] == "BLOCKED_SOURCE_CONTRACT_UNRECOVERED" for row in gate_rows), 24, 24)
    check("no adjacency chart test executed", all(row["adjacency_test"] == "NOT_EVALUATED" for row in gate_rows), True, True)
    check("no Pc/Pd chart test executed", all(row["pcpd_test"] == "NOT_EVALUATED" for row in gate_rows), True, True)
    check("target evaluation not permitted", ledger["review_conclusion"]["target_chart_evaluation_permitted"] is False, ledger["review_conclusion"]["target_chart_evaluation_permitted"], False)
    check("source contract incomplete", ledger["review_conclusion"]["source_contract_complete"] is False, ledger["review_conclusion"]["source_contract_complete"], False)

    with (HERE / "X20_SOURCE_STATES.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["state_id", "sector", "package_role", "rotation_target", "reflection_target", "adjacency"])
        writer.writeheader()
        for s, role in states:
            writer.writerow({
                "state_id": f"X20:{s}:{role}",
                "sector": s,
                "package_role": role,
                "rotation_target": f"X20:{(s + 1) % 5}:{role}",
                "reflection_target": f"X20:{(-s) % 5}:{role}",
                "adjacency": "UNDEFINED",
            })

    with (HERE / "X20_CHART_GATE.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(gate_rows[0]))
        writer.writeheader()
        writer.writerows(gate_rows)

    passed = sum(1 for item in checks if item["passed"])
    result = {
        "status": "PASS_SOURCE_AUDIT_WITH_UNRECOVERED_CONTRACT" if passed == len(checks) else "CONTRACT_INVALID",
        "classification": "SOURCE_CONTRACT_UNRECOVERED" if passed == len(checks) else "CONTRACT_INVALID",
        "checks": {"passed": passed, "total": len(checks)},
        "source_contract": {
            "x20_states": 20,
            "x20_edge_set": None,
            "x20_edge_types": None,
            "triple19_oriented_states": 14,
            "triple19_to_x20_map": None,
            "triple19_to_q106_map": None,
        },
        "candidate_gate": {
            "d5_equivariant_charts": 24,
            "adjacency_tests_executed": 0,
            "pcpd_tests_executed": 0,
            "selected_chart": None,
            "typed_intertwiner_to_q106": None,
        },
        "correction": "P_c and P_d are oriented-state constructors; A is the Triple-19 involution.",
        "next_required_input": "An independently sourced or explicitly Human-declared X20 edge set, edge types and Triple-19-to-X20 map, frozen before Q106 comparison.",
        "claim_boundary": contract["authority_boundary"],
        "checks_detail": checks,
    }
    (HERE / "RESULT.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "classification": result["classification"],
        "checks": f"{passed}/{len(checks)}",
        "d5_charts": 24,
        "charts_evaluated": 0,
        "typed_intertwiner_to_q106": None,
    }, indent=2))
    if passed != len(checks):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
