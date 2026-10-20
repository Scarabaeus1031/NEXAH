#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ECOSYSTEM = next(parent for parent in HERE.parents if parent.name == "NEXAH ECOSYSTEM")

SOURCES = {
    "parent_factor": HERE.parent.parent / "RESULT.json",
    "clockwork_lift": HERE.parent / "RESULT.json",
    "owner_input": HERE / "OWNER_INPUT.md",
    "pent07_control": ECOSYSTEM / "10 NEXAH CORE/NEXAH/RESEARCH/NOTES/PASCAL_PENTAGON_HEXAGON_COUPLING_AUDIT_2026-10-10/RESULT.json",
    "splinter_control": ECOSYSTEM / "30 SCIENCE LAB/NEXAH-Science-Lab/SCIENCE_LAB/CASE_STUDIES/A0_BL_035_SPLINTER_LOCAL_EXTRACTION_2026-10-10/artifacts/PRIMARY_RESULT.json",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def need(condition: bool, label: str, checks: list[dict]) -> None:
    checks.append({"name": label, "passed": bool(condition)})
    if not condition:
        raise AssertionError(label)


def main() -> None:
    checks: list[dict] = []
    for name, path in SOURCES.items():
        need(path.is_file(), f"source exists: {name}", checks)

    factor = json.loads(SOURCES["parent_factor"].read_text())
    lift = json.loads(SOURCES["clockwork_lift"].read_text())
    pent07 = json.loads(SOURCES["pent07_control"].read_text())
    splinter = json.loads(SOURCES["splinter_control"].read_text())

    need(factor["shared_factor"]["factor"] == "C2_orientation", "parent factor is C2 orientation", checks)
    need(factor["shared_factor"]["induced_operator"] == "flip:0<->1", "parent operator flips the bit", checks)
    need(lift["clockwork_source"]["p"]["turns_per_48s"] == 1, "P has positive turn", checks)
    need(lift["clockwork_source"]["q"]["turns_per_48s"] == -1, "Q has negative turn", checks)
    need(lift["display_lift"]["admissible_global_labelings"] == 2, "unlabeled parent has two global labelings", checks)

    ordered = {"P": 17, "Q": 18}
    reverse = {"P": 18, "Q": 17}
    parity = {name: value % 2 for name, value in ordered.items()}
    reverse_parity = {name: value % 2 for name, value in reverse.items()}
    turns = {"P": 1, "Q": -1}

    need(parity == {"P": 1, "Q": 0}, "ordered 17/18 parity labels P=1 and Q=0", checks)
    need(all(turns[name] == 2 * parity[name] - 1 for name in turns), "ordered assignment satisfies turn=2e-1", checks)
    need(reverse_parity == {"P": 0, "Q": 1}, "reverse control swaps both bit labels", checks)
    need(all(turns[name] == 1 - 2 * reverse_parity[name] for name in turns), "reverse control remains valid under reversed sign convention", checks)
    need(pent07["status"] == "PASS_WITH_BOUNDARY", "PENT-07 remains a bounded control", checks)
    need(pent07["result"]["coupling_classes"]["pascal_carrier_intertwiner"] == "UNDEFINED_NO_NODE_EDGE_WEIGHT_OPERATOR_MAP", "PENT-07 supplies no Pascal carrier selector map", checks)
    need(splinter["classification"] == "SPLINTER_PARTIAL", "A0-BL-035 remains SPLINTER_PARTIAL", checks)
    need(splinter["smallest_sufficient_radius"] is None, "A0-BL-035 supplies no compressed selector", checks)

    result = {
        "status": "PASS_CONDITIONAL_ORDERED_17_18_SELECTOR",
        "classification": "OWNER_DECLARED_ORDER_BREAKS_GLOBAL_PQ_LABEL_AMBIGUITY_WITHIN_DECLARED_SIGN_PARITY_CONVENTION",
        "checks": {"passed": len(checks), "total": len(checks)},
        "candidate_contract": {
            "ordered_register_assignment": ordered,
            "parity": "e(n)=n mod 2",
            "turn_encoding": "turn=2e-1",
            "selected_labeling": {"e=1": "P / 17 / +1 turn", "e=0": "Q / 18 / -1 turn"},
            "deck_flip": "P<->Q corresponds to 17<->18, e<->1-e and turn<->-turn",
        },
        "reverse_control": {
            "ordered_register_assignment": reverse,
            "status": "VALID_ONLY_WITH_REVERSED_SIGN_TO_BIT_CONVENTION",
            "meaning": "The unordered pair {17,18} and counter-rotation alone do not select a global labeling.",
        },
        "authority": {
            "ordered_assignment": "OWNER_DECLARED_CANDIDATE_NOT_HISTORICALLY_RECOVERED",
            "historical_source_recovery": None,
            "canonical_within_declared_contract": True,
            "canonical_without_owner_contract": False,
        },
        "maps": {
            "clockwork_glb_nodes_to_x20": None,
            "x20_adjacency": None,
            "typed_x20_to_q106_intertwiner": None,
            "historical_janus_selection": None,
        },
        "negative_controls": {
            "PENT-07": "no direct C5/C6 identification and no Pascal-106 selector map",
            "A0-BL-035": "oriented seam separates the frozen population but yields no compressed Splinter selector",
        },
        "sources": [
            {"name": name, "path": str(path.relative_to(ECOSYSTEM)), "sha256": sha256(path)}
            for name, path in SOURCES.items()
        ],
        "claim_boundary": "Conditional Owner-declared labeling contract only. No historical recovery, X20 graph, GLB-node map, Q106 intertwiner, Janus-law selection, new Study, A0 evidence promotion, physical mechanism or publication authority follows.",
        "checks_detail": checks,
    }
    (HERE / "RESULT.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"status": "PASS", "checks": result["checks"], "selected_labeling": result["candidate_contract"]["selected_labeling"]}, indent=2))


if __name__ == "__main__":
    main()

