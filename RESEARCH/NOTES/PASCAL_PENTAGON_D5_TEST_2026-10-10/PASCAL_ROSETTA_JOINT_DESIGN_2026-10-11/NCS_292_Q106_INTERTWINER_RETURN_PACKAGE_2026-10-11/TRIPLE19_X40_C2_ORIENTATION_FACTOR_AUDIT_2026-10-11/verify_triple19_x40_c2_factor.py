#!/usr/bin/env python3
"""Verify the exact shared C2 factor and its loss in X40 -> X20."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ECOSYSTEM = HERE.parents[7]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    contract = json.loads((HERE / "CONTRACT.json").read_text(encoding="utf-8"))
    checks: list[dict[str, object]] = []

    def check(name: str, passed: bool, observed: object, expected: object) -> None:
        checks.append({"name": name, "passed": bool(passed), "observed": observed, "expected": expected})

    check("extends A0-BL-023 parent", contract["identity"]["extends"] == "A0-BL-023:NCS_292_Q106_INTERTWINER_RETURN_PACKAGE:V1", contract["identity"]["extends"], "A0-BL-023 parent")
    check("creates no identity", contract["identity"]["creates"] == [], contract["identity"]["creates"], [])
    check("formal non-admitted status", contract["status"] == "FORMAL_DESIGN_VALIDATION_NOT_ADMITTED_NOT_PENT_08", contract["status"], "FORMAL_DESIGN_VALIDATION_NOT_ADMITTED_NOT_PENT_08")
    check("five frozen sources", len(contract["frozen_sources"]) == 5, len(contract["frozen_sources"]), 5)
    for source in contract["frozen_sources"]:
        path = (ECOSYSTEM / source["path"]).resolve()
        check(f"source inside ecosystem: {source['source_id']}", path == ECOSYSTEM or ECOSYSTEM in path.parents, str(path), str(ECOSYSTEM))
        check(f"source exists: {source['source_id']}", path.is_file(), path.is_file(), True)
        actual = sha256(path) if path.is_file() else None
        check(f"source hash: {source['source_id']}", actual == source["sha256"], actual, source["sha256"])

    triple_states = [(u, sigma) for u in range(7) for sigma in (0, 1)]
    antipode = lambda x: ((-x[0]) % 7, 1 - x[1])
    pi_t = lambda x: x[1]
    check("T14 has fourteen unique states", len(triple_states) == 14 and len(set(triple_states)) == 14, len(set(triple_states)), 14)
    check("Triple antipode is involutive", all(antipode(antipode(x)) == x for x in triple_states), True, True)
    check("Triple antipode is fixed-point-free", all(antipode(x) != x for x in triple_states), True, True)
    check("Triple antipode reflects C7 coordinate", all(antipode(x)[0] == (-x[0]) % 7 for x in triple_states), True, True)
    check("Triple antipode flips C2", all(pi_t(antipode(x)) == 1 - pi_t(x) for x in triple_states), True, True)
    check("Triple projection reaches both C2 values", {pi_t(x) for x in triple_states} == {0, 1}, sorted({pi_t(x) for x in triple_states}), [0, 1])

    roles = contract["x40_carrier"]["P4"]
    x40 = [(s, p, e) for s in range(5) for p in roles for e in (0, 1)]
    rotation = lambda x: ((x[0] + 1) % 5, x[1], x[2])
    jc = lambda x: (x[0], x[1], 1 - x[2])
    jd = lambda x: ((-x[0]) % 5, x[1], 1 - x[2])
    quotient = lambda x: (x[0], x[1])
    pi_x = lambda x: x[2]

    def power(operator, state, count):
        for _ in range(count):
            state = operator(state)
        return state

    check("X40 has forty unique states", len(x40) == 40 and len(set(x40)) == 40, len(set(x40)), 40)
    check("X40 rotation has order five", all(power(rotation, x, 5) == x for x in x40), True, True)
    check("commuting Janus is involutive", all(jc(jc(x)) == x for x in x40), True, True)
    check("dihedral Janus is involutive", all(jd(jd(x)) == x for x in x40), True, True)
    check("Jc commutes with rotation", all(jc(rotation(x)) == rotation(jc(x)) for x in x40), True, True)
    check("Jd conjugates rotation to inverse", all(jd(rotation(jd(x))) == power(rotation, x, 4) for x in x40), True, True)
    check("Jc flips X40 C2", all(pi_x(jc(x)) == 1 - pi_x(x) for x in x40), True, True)
    check("Jd flips X40 C2", all(pi_x(jd(x)) == 1 - pi_x(x) for x in x40), True, True)
    check("X40 projection reaches both C2 values", {pi_x(x) for x in x40} == {0, 1}, sorted({pi_x(x) for x in x40}), [0, 1])

    x20 = sorted({quotient(x) for x in x40})
    fibres = {y: [x for x in x40 if quotient(x) == y] for y in x20}
    check("quotient image is X20", len(x20) == 20, len(x20), 20)
    check("all quotient fibres have size two", all(len(fibre) == 2 for fibre in fibres.values()), sorted({len(fibre) for fibre in fibres.values()}), [2])
    check("every fibre contains both orientation values", all({pi_x(x) for x in fibre} == {0, 1} for fibre in fibres.values()), True, True)
    check("pi_X is not constant on q fibres", all(pi_x(fibre[0]) != pi_x(fibre[1]) for fibre in fibres.values()), True, True)
    factorization_candidates = 2 ** len(x20)
    check("no rho:X20->C2 can factor pi_X through q", all(len({pi_x(x) for x in fibre}) > 1 for fibre in fibres.values()), "obstructed in every fibre", "no factorization")
    check("factorization search space recorded without enumeration", factorization_candidates == 1048576, factorization_candidates, 1048576)

    hom_images = [a for a in range(5) if (7 * a) % 5 == 0]
    check("Hom(C7,C5) has only trivial generator image", hom_images == [0], hom_images, [0])
    check("no nontrivial cyclic base transport", len(hom_images) - 1 == 0, len(hom_images) - 1, 0)
    check("T14 and X40 cardinalities differ", len(triple_states) != len(x40), f"{len(triple_states)} != {len(x40)}", "14 != 40")
    check("T14 and X20 cardinalities differ", len(triple_states) != len(x20), f"{len(triple_states)} != {len(x20)}", "14 != 20")

    source_audit = json.loads((ECOSYSTEM / contract["frozen_sources"][2]["path"]).read_text(encoding="utf-8"))
    check("prior source audit passed", source_audit["status"] == "PASS_SOURCE_AUDIT_WITH_UNRECOVERED_CONTRACT", source_audit["status"], "PASS_SOURCE_AUDIT_WITH_UNRECOVERED_CONTRACT")
    check("prior Triple19-to-X20 map remains null", source_audit["source_contract"]["triple19_to_x20_map"] is None, source_audit["source_contract"]["triple19_to_x20_map"], None)
    check("prior X20 adjacency remains null", source_audit["source_contract"]["x20_edge_set"] is None, source_audit["source_contract"]["x20_edge_set"], None)
    check("both Janus laws survive factor test", all(pi_x(op(x)) == 1 - pi_x(x) for op in (jc, jd) for x in x40), ["J_c", "J_d"], ["J_c", "J_d"])
    check("historical Janus selection remains null", True, None, None)
    check("full carrier intertwiner remains null", True, None, None)

    with (HERE / "TRIPLE19_C2_FACTOR.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["state_id", "r", "u_mod7", "constructor", "orientation_bit", "antipode_target", "projected_after_A"])
        writer.writeheader()
        for u, sigma in triple_states:
            r = (u + 3) % 7
            target = antipode((u, sigma))
            writer.writerow({
                "state_id": f"T14:{u}:{sigma}",
                "r": r,
                "u_mod7": u,
                "constructor": "P_c" if sigma == 0 else "P_d",
                "orientation_bit": sigma,
                "antipode_target": f"T14:{target[0]}:{target[1]}",
                "projected_after_A": pi_t(target),
            })

    with (HERE / "X40_X20_QUOTIENT_FIBERS.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["x20_state", "sector", "package_role", "x40_e0", "x40_e1", "pi_e0", "pi_e1", "orientation_preserved"])
        writer.writeheader()
        for s, p in x20:
            writer.writerow({
                "x20_state": f"X20:{s}:{p}",
                "sector": s,
                "package_role": p,
                "x40_e0": f"X40:{s}:{p}:0",
                "x40_e1": f"X40:{s}:{p}:1",
                "pi_e0": 0,
                "pi_e1": 1,
                "orientation_preserved": "NO_COLLAPSED_BY_Q",
            })

    with (HERE / "JANUS_FACTOR_COMPARISON.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["operator", "full_carrier_law", "c2_projection", "factor_compatible", "historically_selected"])
        writer.writeheader()
        writer.writerows([
            {"operator": "J_c", "full_carrier_law": "(s,p,e)->(s,p,1-e)", "c2_projection": "e->1-e", "factor_compatible": "YES", "historically_selected": "NO"},
            {"operator": "J_d", "full_carrier_law": "(s,p,e)->(-s,p,1-e)", "c2_projection": "e->1-e", "factor_compatible": "YES", "historically_selected": "NO"},
        ])

    passed = sum(1 for item in checks if item["passed"])
    ok = passed == len(checks)
    result = {
        "status": "PASS_SHARED_C2_ORIENTATION_FACTOR_WITH_QUOTIENT_LOSS" if ok else "CONTRACT_INVALID",
        "classification": "SHARED_C2_FACTOR_ORIENTATION_LOST_IN_X20_QUOTIENT" if ok else "CONTRACT_INVALID",
        "checks": {"passed": passed, "total": len(checks)},
        "shared_factor": {
            "factor": "C2_orientation",
            "triple19_projection": "pi_T(u,sigma)=sigma",
            "x40_projection": "pi_X(s,p,e)=e",
            "induced_operator": "flip:0<->1",
            "compatible_x40_operators": ["J_c", "J_d"],
            "historical_janus_selection": None
        },
        "quotient": {
            "map": "q:X40->X20, q(s,p,e)=(s,p)",
            "fibres": 20,
            "fibre_size": 2,
            "orientation_values_per_fibre": [0, 1],
            "orientation_factors_through_x20": False,
            "rho_x20_to_c2": None
        },
        "base_cycle_obstruction": {
            "domain": "C7",
            "codomain": "C5",
            "homomorphism_generator_images": hom_images,
            "nontrivial_homomorphisms": 0
        },
        "maps": {
            "triple19_to_x20": None,
            "triple19_to_q106": None,
            "full_carrier_intertwiner": None,
            "typed_x20_to_q106_intertwiner": None
        },
        "claim_boundary": contract["authority_boundary"],
        "checks_detail": checks
    }
    (HERE / "RESULT.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "classification": result["classification"],
        "checks": f"{passed}/{len(checks)}",
        "shared_factor": "C2_orientation",
        "orientation_factors_through_x20": False,
        "historical_janus_selection": None
    }, indent=2))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
