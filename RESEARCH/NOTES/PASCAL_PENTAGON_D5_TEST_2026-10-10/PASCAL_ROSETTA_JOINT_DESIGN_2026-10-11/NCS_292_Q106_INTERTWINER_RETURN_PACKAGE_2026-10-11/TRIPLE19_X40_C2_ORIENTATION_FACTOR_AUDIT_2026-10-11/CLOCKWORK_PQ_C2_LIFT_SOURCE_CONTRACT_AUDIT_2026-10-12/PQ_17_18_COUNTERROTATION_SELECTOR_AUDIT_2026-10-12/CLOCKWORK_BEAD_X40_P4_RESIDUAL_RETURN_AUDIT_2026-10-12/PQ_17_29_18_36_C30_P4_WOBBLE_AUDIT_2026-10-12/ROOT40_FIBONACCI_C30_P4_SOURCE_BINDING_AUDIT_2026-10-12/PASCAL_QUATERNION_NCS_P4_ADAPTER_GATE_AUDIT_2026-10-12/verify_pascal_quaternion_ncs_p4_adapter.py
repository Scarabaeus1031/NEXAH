#!/usr/bin/env python3
import csv
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ECOSYSTEM = next(parent for parent in HERE.parents if parent.name == "NEXAH ECOSYSTEM")
A052 = ECOSYSTEM / "30 SCIENCE LAB/NEXAH-Science-Lab/SCIENCE_LAB/CASE_STUDIES/A0_BL_052_PASCAL_QUATERNION_FOUR_CHANNEL_RETURN_2026-10-11"
A053 = ECOSYSTEM / "30 SCIENCE LAB/NEXAH-Science-Lab/SCIENCE_LAB/CASE_STUDIES/A0_BL_053_PASCAL_QUATERNION_SYMBOLIC_PROOF_REVIEW_2026-10-11"
NCS_PACKAGE = HERE.parents[6]
TYPED_AUDIT = NCS_PACKAGE / "NCS_X20_TYPED_CARRIER_PCPD_Q106_INTERTWINER_AUDIT_2026-10-11"

SOURCES = {
    "contract": HERE / "CONTRACT.json",
    "pascal_result": A052 / "artifacts/PRIMARY_RESULT.json",
    "pascal_assessment": A052 / "02_RESULT_ASSESSMENT.md",
    "pascal_all_n_closure": A053 / "06_OWNER_CLOSURE_RECORD.md",
    "ncs_contract": NCS_PACKAGE / "CONTRACT.json",
    "typed_p4_contract": TYPED_AUDIT / "CONTRACT.json",
    "typed_p4_result": TYPED_AUDIT / "RESULT.json",
    "root40_gate_result": HERE.parent / "RESULT.json",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cycle_signature(action, points):
    seen = set()
    sizes = []
    for point in points:
        if point in seen:
            continue
        current = point
        size = 0
        while current not in seen:
            seen.add(current)
            size += 1
            current = action[current]
        sizes.append(size)
    return tuple(sorted(sizes))


def canonical_action(action, roles):
    return tuple(action[role] for role in roles)


def main():
    checks = []

    def need(condition, name, observed=None, expected=None):
        passed = bool(condition)
        checks.append({"name": name, "passed": passed, "observed": observed, "expected": expected})
        if not passed:
            raise AssertionError(name)

    for name, path in SOURCES.items():
        need(path.is_file(), f"source exists: {name}", str(path), "file")

    contract = json.loads(SOURCES["contract"].read_text())
    pascal = json.loads(SOURCES["pascal_result"].read_text())
    ncs = json.loads(SOURCES["ncs_contract"].read_text())
    typed_contract = json.loads(SOURCES["typed_p4_contract"].read_text())
    typed_result = json.loads(SOURCES["typed_p4_result"].read_text())
    root40_gate = json.loads(SOURCES["root40_gate_result"].read_text())
    pascal_assessment = SOURCES["pascal_assessment"].read_text()
    all_n_closure = SOURCES["pascal_all_n_closure"].read_text()

    need(contract["identity"]["creates"] == [], "audit creates no identity")
    need(pascal["classification"] == "EXACT_FOUR_CHANNEL_CONNECTOR_PASS", "closed Pascal connector retained")
    need("Phi(a,b,c) = (a+b+c)1 + ai + bj + ck" in pascal_assessment, "Pascal connector formula source-bound")
    need("OWNER_ACCEPTED_INTERNAL_RESULT / CLOSED" in all_n_closure, "all-N symbolic result Owner-accepted and closed")
    need(root40_gate["root40_pascal_connector_test"]["in_pascal_phi_image"] is False, "Root-40 remains outside Pascal Phi image")
    need(typed_result["classification"] == "SOURCE_CONTRACT_UNRECOVERED", "prior NCS source-contract boundary retained")

    slots = contract["source_carrier"]["slots"]
    roles = contract["target_carrier"]["roles"]
    need(slots == ["scalar", "i", "j", "k"], "canonical Pascal slots retained", slots)
    need(roles == ["carrier", "frame_cut", "transform_view", "return_record"], "declared NCS roles retained", roles)
    need(typed_contract["declared_source_carrier"]["P4"] == roles, "typed NCS audit agrees on P4 roles")
    need(ncs["declared_carrier"]["rotation"] == "r(s,p,e)=(s+1 mod 5,p,e)", "NCS rotation fixes P4 role")
    need("p,1-e" in ncs["janus_hypotheses"]["commuting"] and "p,1-e" in ncs["janus_hypotheses"]["dihedral"], "both NCS Janus laws fix P4 role")

    gamma = {"scalar": "scalar", "i": "j", "j": "k", "k": "i"}
    identity_roles = {role: role for role in roles}
    need(cycle_signature(gamma, slots) == (1, 3), "Pascal action has cycle type (1,3)")
    need(cycle_signature(identity_roles, roles) == (1, 1, 1, 1), "declared NCS role action is identity")

    rows = []
    induced_actions = {}
    static_return_count = 0
    equivariant_count = 0
    lexical_map = {"scalar": "carrier", "i": "frame_cut", "j": "transform_view", "k": "return_record"}
    lexical_equivariant = None

    for index, role_perm in enumerate(itertools.permutations(roles), start=1):
        adapter = dict(zip(slots, role_perm))
        inverse = {role: slot for slot, role in adapter.items()}
        exact_return = len(inverse) == 4 and all(inverse[adapter[slot]] == slot for slot in slots)
        static_return_count += int(exact_return)
        equivariant = all(adapter[gamma[slot]] == identity_roles[adapter[slot]] for slot in slots)
        equivariant_count += int(equivariant)

        induced = {}
        for role in roles:
            slot = inverse[role]
            induced[role] = adapter[gamma[slot]]
        key = canonical_action(induced, roles)
        induced_actions.setdefault(key, {"action": induced, "adapter_count": 0})["adapter_count"] += 1

        is_lexical = adapter == lexical_map
        if is_lexical:
            lexical_equivariant = equivariant
        rows.append({
            "candidate": index,
            **{f"{slot}_to": adapter[slot] for slot in slots},
            "exact_address_return": str(exact_return).lower(),
            "c3_to_declared_ncs_identity_equivariant": str(equivariant).lower(),
            "lexical_candidate": str(is_lexical).lower(),
            "induced_role_action": ";".join(f"{role}->{induced[role]}" for role in roles),
        })

    need(len(rows) == 24, "all 24 static bijections enumerated", len(rows), 24)
    need(static_return_count == 24, "all 24 bijections have exact address Return", static_return_count, 24)
    need(equivariant_count == 0, "no bijection intertwines Pascal C3 with declared NCS identity action", equivariant_count, 0)
    need(len(induced_actions) == 8, "chosen adapters induce eight distinct role C3 actions", len(induced_actions), 8)
    need(all(item["adapter_count"] == 3 for item in induced_actions.values()), "each induced role C3 action admits three adapters")
    need(all(cycle_signature(item["action"], roles) == (1, 3) for item in induced_actions.values()), "all induced role actions have cycle type (1,3)")
    need(canonical_action(identity_roles, roles) not in induced_actions, "declared NCS identity is not an induced Pascal C3 action")
    need(lexical_equivariant is False, "lexical candidate fails operator-intertwiner gate")
    need(typed_result["source_contract"]["x20_edge_set"] is None, "X20 adjacency remains null")
    need(typed_result["candidate_gate"]["typed_intertwiner_to_q106"] is None, "Q106 intertwiner remains null")

    with (HERE / "ADAPTER_CANDIDATES.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    result = {
        "status": "PASS_NO_OPERATOR_EQUIVARIANT_ADAPTER_UNDER_DECLARED_NCS_ACTION",
        "classification": "STATIC_24_RETURN_BIJECTIONS_ZERO_C3_INTERTWINERS",
        "checks": {"passed": len(checks), "total": len(checks)},
        "identity_effect": "REUSES_EXISTING_IDENTITIES_CREATES_NONE",
        "source_action": {
            "carrier": "Pascal quaternion slots",
            "slots": slots,
            "operator": gamma,
            "cycle_type": [1, 3],
        },
        "target_action": {
            "carrier": "NCS P4 role set",
            "roles": roles,
            "declared_operator": identity_roles,
            "cycle_type": [1, 1, 1, 1],
            "reason": "NCS rotation and both Janus candidates preserve p",
        },
        "enumeration": {
            "static_bijections": 24,
            "exact_address_return": 24,
            "operator_equivariant_adapters": 0,
            "distinct_induced_role_c3_actions": 8,
            "adapters_per_induced_action": 3,
        },
        "lexical_candidate": {
            "map": lexical_map,
            "source_declared": False,
            "operator_equivariant": False,
            "selected": False,
        },
        "decision": {
            "canonical_ncs_p4_adapter": None,
            "root40_used_as_adapter": False,
            "wobble_phase_supplies_role_semantics": False,
            "x20_adjacency": None,
            "typed_x20_to_q106_intertwiner": None,
        },
        "minimal_new_source_input": [
            "complete declared four-slot-to-role map",
            "or an NCS role operator of cycle type (1,3) plus one typed slot-to-role anchor",
        ],
        "induced_action_boundary": "A chosen bijection can define f gamma f^-1 on role labels, but that transported action is not a recovered NCS source law.",
        "sources": [
            {"name": name, "path": str(path.relative_to(ECOSYSTEM)), "sha256": sha256(path)}
            for name, path in SOURCES.items()
        ],
        "claim_boundary": "Formal source-bound adapter audit only. The result distinguishes 24 reversible address encodings from zero operator-equivariant adapters under the declared NCS role action. It does not modify A0, declare an NCS C3 role law, select a semantic assignment, define X20 adjacency, create a Q106 intertwiner, recover a historical mechanism, admit a Study or authorize publication.",
        "checks_detail": checks,
    }
    (HERE / "RESULT.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({
        "status": result["status"],
        "checks": result["checks"],
        "static_bijections": 24,
        "exact_address_return": 24,
        "operator_equivariant_adapters": 0,
        "distinct_induced_role_c3_actions": 8,
        "canonical_ncs_p4_adapter": None,
    }, indent=2))


if __name__ == "__main__":
    main()
