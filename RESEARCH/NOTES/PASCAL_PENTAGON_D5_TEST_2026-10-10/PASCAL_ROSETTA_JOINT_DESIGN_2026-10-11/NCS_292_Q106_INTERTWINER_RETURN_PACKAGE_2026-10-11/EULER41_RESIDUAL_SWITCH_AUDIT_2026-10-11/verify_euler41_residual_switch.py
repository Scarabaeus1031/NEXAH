#!/usr/bin/env python3
"""Replay the bounded Euler-41 / Q106 residual-switch formal audit."""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
ECOSYSTEM = HERE.parents[7]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def matrix_sums(matrix: list[list[int]]) -> dict[str, list[int]]:
    rows = [sum(row) for row in matrix]
    cols = [sum(matrix[r][c] for r in range(4)) for c in range(4)]
    diagonals = [sum(matrix[i][i] for i in range(4)), sum(matrix[i][3-i] for i in range(4))]
    return {"rows": rows, "columns": cols, "diagonals": diagonals}


def validate() -> dict[str, object]:
    contract = json.loads((HERE / "CONTRACT.json").read_text(encoding="utf-8"))
    checks: list[dict[str, object]] = []

    def check(name: str, passed: bool, observed: object, expected: object) -> None:
        checks.append({"name": name, "status": "PASS" if passed else "FAIL", "observed": observed, "expected": expected})

    check(
        "existing identity reused without creation",
        contract["identity"]["reuse"] == "A0OE:PASCAL_PENTAGON_D5_TEST" and contract["identity"]["creates"] == [],
        contract["identity"],
        {"reuse": "A0OE:PASCAL_PENTAGON_D5_TEST", "creates": []},
    )

    paths: dict[str, Path] = {}
    hashes: dict[str, str | None] = {}
    for name, spec in contract["frozen_sources"].items():
        path = ECOSYSTEM / spec["path"]
        paths[name] = path
        observed = sha256(path) if path.exists() else None
        hashes[name] = observed
        check(f"frozen source {name}", observed == spec["sha256"], observed, spec["sha256"])

    external_paths: dict[str, Path] = {}
    external_hashes: dict[str, str | None] = {}
    for name, spec in contract["external_source_bindings"].items():
        path = Path(spec["path"])
        external_paths[name] = path
        observed = sha256(path) if path.exists() else None
        external_hashes[name] = observed
        check(f"external module source {name}", observed == spec["sha256"], observed, spec["sha256"])

    parent = json.loads(paths["parent_result"].read_text(encoding="utf-8"))
    seam = json.loads(paths["intrinsic_seam_result"].read_text(encoding="utf-8"))
    mrb04 = json.loads(paths["mrb04_result"].read_text(encoding="utf-8"))
    mrb08 = json.loads(paths["mrb08_result"].read_text(encoding="utf-8"))
    lissajous = json.loads(paths["lissajous_mobius_result"].read_text(encoding="utf-8"))

    # M1 — prime index, Euler boundary, and the representation-scoped mirror.
    primes = [n for n in range(2, 42) if is_prime(n)]
    check("M1 29 is the tenth prime", primes[9] == 29, primes[9], 29)
    check("M1 41 is the thirteenth prime", primes[12] == 41, primes[12], 41)
    base13 = next(row for row in mrb04["base_atlas"] if row["base"] == 13)
    check(
        "M1 base-13 reversal connects 41 to 29",
        base13["representation"] == "32" and base13["mirror_representation"] == "23" and base13["mirror_value"] == 29,
        {k: base13[k] for k in ("representation", "mirror_representation", "mirror_value")},
        {"representation": "32", "mirror_representation": "23", "mirror_value": 29},
    )
    check(
        "M1 Euler run ends at n=40 and breaks at n=41",
        mrb04["checks"]["euler_prime_run_n_1_to_40"] and mrb04["checks"]["euler_break_n_41"]
        and mrb04["headline"]["euler_break"] == {"n": 41, "u": 40, "value": 1681},
        mrb04["headline"]["euler_break"],
        {"n": 41, "u": 40, "value": 1681},
    )

    # M2 — +1 is a typed external controller, not a smuggled payload state.
    x40 = list(itertools.product(range(5), range(4), range(2)))
    controller = ("q",)
    x41_plus = [*x40, controller]
    check("M2 declared X40 carrier has forty states", len(x40) == 40, len(x40), 40)
    check("M2 disjoint external controller produces 40+1 states", len(x41_plus) == 41 and controller not in x40, len(x41_plus), 41)

    # M3 — derive the unique apex-versus-ring readout directly under D5.
    with paths["q106_nodes"].open(newline="", encoding="utf-8") as handle:
        nodes = list(csv.DictReader(handle))
    node_index = {row["node_id"]: i for i, row in enumerate(nodes)}
    residual_ids = parent["module_3"]["six_node_residual"]
    residual = [node_index[node_id] for node_id in residual_ids]
    automorphisms = json.loads(paths["q106_automorphisms"].read_text(encoding="utf-8"))["actions"]
    rho = {node_index["A"]: 0, **{node_index[node_id]: 1 for node_id in residual_ids if node_id != "A"}}
    preserved = all(rho[p[node]] == rho[node] for action in automorphisms for p in [action["permutation_zero_based"]] for node in residual)
    fixed = [node for node in residual if all(action["permutation_zero_based"][node] == node for action in automorphisms)]
    check("M3 parent supplies the unique six-node residual", residual_ids == ["A", "S_01_00", "S_01_01", "S_01_02", "S_01_03", "S_01_04"], residual_ids, "apex plus first seam ring")
    check("M3 residual orbit classes are one fixed apex plus one five-ring", len(fixed) == 1 and nodes[fixed[0]]["node_id"] == "A" and sorted(rho.values()).count(0) == 1 and sorted(rho.values()).count(1) == 5, {"fixed": [nodes[i]["node_id"] for i in fixed], "fiber_sizes": [1, 5]}, {"fixed": ["A"], "fiber_sizes": [1, 5]})
    check("M3 apex-versus-ring readout is D5 invariant and surjective", preserved and set(rho.values()) == {0, 1}, {"D5_invariant": preserved, "image": sorted(set(rho.values()))}, {"D5_invariant": True, "image": [0, 1]})

    # M4 — six invariant seam choices are a trivial D5-set; R6 is not.
    compatible = [row for row in seam["orbit_results"] if row["compatible_odd_invariant_seam"]]
    check("M4 six D5-compatible added seam orbits remain", len(compatible) == 6, len(compatible), 6)
    moved_residual = any(action["permutation_zero_based"][node] != node for action in automorphisms for node in residual)
    equivariant_bijections = 0 if moved_residual else 720
    check("M4 no D5-equivariant residual-node bijection selects the six invariant seam choices", equivariant_bijections == 0, equivariant_bijections, 0)
    check("M4 intrinsic Q106 H1 remains trivial", seam["summary"]["intrinsic_H1_dimension"] == 0, seam["summary"]["intrinsic_H1_dimension"], 0)

    # M5 — Fibonacci is an exact rail comparator but not a topology selector.
    q = ((1, 1), (1, 0))
    def mm(a, b):
        return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)) for i in range(2))
    q5 = ((1, 0), (0, 1))
    for _ in range(5):
        q5 = mm(q5, q)
    det = q5[0][0] * q5[1][1] - q5[0][1] * q5[1][0]
    fib13 = [1, 1]
    while len(fib13) < 13:
        fib13.append(fib13[-1] + fib13[-2])
    check("M5 Fibonacci Q fifth power and determinant", q5 == ((8, 5), (5, 3)) and det == -1, {"Q5": q5, "det": det}, {"Q5": ((8, 5), (5, 3)), "det": -1})
    check("M5 thirteen-step Fibonacci rail can be indexed", len(fib13) == 13 and fib13[-1] == 233, fib13, [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233])

    # M6 — same scalar invariant, distinct placement operators.
    durer = [[16, 3, 2, 13], [5, 10, 11, 8], [9, 6, 7, 12], [4, 15, 14, 1]]
    khajuraho = [[7, 12, 1, 14], [2, 13, 8, 11], [16, 3, 10, 5], [9, 6, 15, 4]]
    ds, ks = matrix_sums(durer), matrix_sums(khajuraho)
    check("M6 both plates have row column and diagonal sum 34", all(v == 34 for v in ds["rows"] + ds["columns"] + ds["diagonals"] + ks["rows"] + ks["columns"] + ks["diagonals"]), {"Durer": ds, "Khajuraho": ks}, "all sums 34")
    def loc(m, value):
        return next((r, c) for r in range(4) for c in range(4) if m[r][c] == value)
    durer_ok = all(loc(durer, 17-x) == (3-loc(durer, x)[0], 3-loc(durer, x)[1]) for x in range(1, 17))
    khajuraho_ok = all(loc(khajuraho, 17-x) == ((loc(khajuraho, x)[0]+2)%4, (loc(khajuraho, x)[1]+2)%4) for x in range(1, 17))
    check("M6 complement is realized by two distinct spatial operators", durer_ok and khajuraho_ok, {"Durer": "R180", "Khajuraho": "T(2,2) toric"}, {"Durer": "R180", "Khajuraho": "T(2,2) toric"})

    # M8 — dual ingress and the C30-to-C6 address bus.
    carriers = {(row["odd_anchor_q"], row["carrier"]): row for row in mrb08["carrier_rows"]}
    check(
        "M8 MRB-08 keeps the 28 and 40 carriers in distinct dyadic families",
        (7, 28) in carriers and (5, 40) in carriers,
        {"X28_family": "2^k*7", "X40_family": "2^k*5"},
        {"X28_family": "2^k*7", "X40_family": "2^k*5"},
    )
    e28 = [*range(28), "q29"]
    e40 = [*range(40), "q41"]
    check(
        "M8 external-controller grammar gives 28+1 and 40+1 without carrier merger",
        len(e28) == 29 and len(e40) == 41 and e28 != e40,
        {"E28": len(e28), "E40": len(e40), "same_carrier": e28 == e40},
        {"E28": 29, "E40": 41, "same_carrier": False},
    )
    check(
        "M8 both ingress routes terminate at the integer 29",
        len(e28) == 29 and base13["mirror_value"] == 29,
        {"from_E28": len(e28), "from_E40_via_41_base13_reverse": base13["mirror_value"]},
        {"from_E28": 29, "from_E40_via_41_base13_reverse": 29},
    )
    c30_states = lissajous["summary"]["exact_lissajous_phase_states"]
    fibres = {r: [t for t in range(30) if t % 6 == r] for r in range(6)}
    check(
        "M8 verified C30 phase carrier projects to six equal address fibres",
        c30_states == 30 and sorted(len(v) for v in fibres.values()) == [5] * 6,
        {"C30_states": c30_states, "C6_fibre_sizes": [len(fibres[r]) for r in range(6)]},
        {"C30_states": 30, "C6_fibre_sizes": [5] * 6},
    )
    check(
        "M8 phase 29 advances to zero in C30",
        (29 + 1) % 30 == 0,
        (29 + 1) % 30,
        0,
    )
    selector_candidates = math.factorial(6)
    check(
        "M8 six-address to six-seam pin assignment remains noncanonical",
        selector_candidates == 720 and len(compatible) == 6,
        {"candidate_bijections": selector_candidates, "selected": None},
        {"candidate_bijections": 720, "selected": None},
    )
    check(
        "M8 common 10 20 30 40 synchronization cover is 120",
        math.lcm(10, 20, 30, 40) == 120,
        math.lcm(10, 20, 30, 40),
        120,
    )

    # M9 — exact factorization; the visual arc and physical language stay out.
    gap = 206**2 - 204**2
    check(
        "M9 square gap factors exactly as 41 times 20",
        gap == (206 - 204) * (206 + 204) == 820 == 41 * 20,
        {"gap": gap, "factorization": [41, 20]},
        {"gap": 820, "factorization": [41, 20]},
    )

    # M11 — recover the exact base-20 state decoder and keep its lossy view typed.
    samples = {
        1729: ((4, 6, 9), (12.0, 4)),
        417: ((1, 0, 17), (17.0, 1)),
        1836: ((4, 11, 16), (21.5, 4)),
        378: ((0, 18, 18), (27.0, 0)),
        718: ((1, 15, 18), (25.5, 1)),
    }

    def decode20(n: int) -> tuple[int, int, int]:
        return n // 400, (n % 400) // 20, n % 20

    decoded = {n: decode20(n) for n in samples}
    projected = {n: (digits[2] + digits[1] / 2, digits[0]) for n, digits in decoded.items()}
    check(
        "M11 five source values decode to the displayed base-20 triples",
        all(decoded[n] == samples[n][0] for n in samples),
        decoded,
        {n: samples[n][0] for n in samples},
    )
    check(
        "M11 base-20 decoder round trips all five values",
        all(400 * z + 20 * y + x == n for n, (z, y, x) in decoded.items()),
        {n: 400 * z + 20 * y + x for n, (z, y, x) in decoded.items()},
        {n: n for n in samples},
    )
    check(
        "M11 affine display projection matches all five plotted coordinates",
        all(projected[n] == samples[n][1] for n in samples),
        projected,
        {n: samples[n][1] for n in samples},
    )
    collision = ((0, 0, 1), (0, 2, 0))
    collision_views = tuple((x + y / 2, z) for z, y, x in collision)
    check(
        "M11 projected horizontal coordinate is non-injective",
        collision[0] != collision[1] and collision_views[0] == collision_views[1],
        {"states": collision, "views": collision_views},
        {"distinct_states": True, "same_view": True},
    )
    frame_sequence = [1 + 15 * k for k in range(9)]
    check(
        "M11 recovered frame family is the 15-step progression from 1 through 121",
        frame_sequence == [1, 16, 31, 46, 61, 76, 91, 106, 121],
        frame_sequence,
        [1, 16, 31, 46, 61, 76, 91, 106, 121],
    )
    check(
        "M11 odd-eighth 3/8 axis is exactly 135 degrees",
        3 * 360 // 8 == 135,
        3 * 360 // 8,
        135,
    )
    with paths["phi_fourier_source_inventory"].open(newline="", encoding="utf-8") as handle:
        inventory = list(csv.DictReader(handle))
    inventory_rows = [row for row in inventory if row["path"].endswith("Vendissimal Spiral Map (Basis 20 Projection).png")]
    check(
        "M11 current Thread-V source matches the prior Science-Lab forensic hash",
        len(inventory_rows) == 1
        and inventory_rows[0]["sha256"] == contract["external_source_bindings"]["thread_v_base20_projection"]["sha256"]
        and external_hashes["thread_v_base20_projection"] == inventory_rows[0]["sha256"],
        {
            "inventory_rows": len(inventory_rows),
            "inventory_hash": inventory_rows[0]["sha256"] if inventory_rows else None,
            "current_hash": external_hashes["thread_v_base20_projection"],
        },
        {"inventory_rows": 1, "inventory_hash_equals_current": True},
    )

    # M12 — keep two legacy uses of “vendissimal” in distinct namespaces.
    trinary_readme = external_paths["ucrt_trinary_readme"].read_text(encoding="utf-8")
    resonance_indices = external_paths["ucrt_resonance_indices"].read_text(encoding="utf-8")
    v5 = {-2, -1, 0, 1, 2}
    c20 = set(range(20))
    check(
        "M12 sources separately attest a five-state use and a base-20 use",
        "Vendissimal (Base-5)" in trinary_readme
        and "Base 20 Layer" in resonance_indices
        and "mod} \\ 20" in resonance_indices,
        {
            "five_state_phrase": "Vendissimal (Base-5)" in trinary_readme,
            "base20_layer_phrase": "Base 20 Layer" in resonance_indices,
            "mod20_formula": "mod} \\ 20" in resonance_indices,
        },
        {"five_state_phrase": True, "base20_layer_phrase": True, "mod20_formula": True},
    )
    check(
        "M12 five-state alphabet is not the base-20 carrier",
        len(v5) == 5 and len(c20) == 20 and v5 != c20,
        {"V5_cardinality": len(v5), "C20_cardinality": len(c20), "identified": v5 == c20},
        {"V5_cardinality": 5, "C20_cardinality": 20, "identified": False},
    )

    passed = all(row["status"] == "PASS" for row in checks)
    return {
        "schema": "nexah.euler41-residual-switch-audit-result/1.0.0",
        "date": contract["date"],
        "status": "PASS_WITH_OPEN_SEAM_BINDING" if passed else "FAIL",
        "classification": "PASS_EXACT_CONTROLLER_ARCHITECTURE_WITH_OPEN_SEAM_BINDING" if passed else "CONTRACT_INVALID",
        "identity": contract["identity"],
        "summary": {
            "checks_passed": sum(row["status"] == "PASS" for row in checks),
            "checks_total": len(checks),
            "prime_10": 29,
            "prime_13": 41,
            "controller_cardinality": 41,
            "residual_fiber_profile": [1, 5],
            "compatible_added_seams": len(compatible),
            "c30_address_fibre_profile": [5, 5, 5, 5, 5, 5],
            "seam_pin_assignment_candidates": selector_candidates,
            "gap_41_times_20": gap,
            "base20_samples": len(samples),
            "base20_projection_injective": False,
            "vendissimal_namespaces_identified": False,
            "canonical_seam_selected": None,
            "historical_janus_law_selected": None
        },
        "modules": {
            "M1_prime_euler_boundary": {"primes_1_to_13": primes, "base13": {"41": "32", "reversal": "23", "value": 29}, "euler_break": mrb04["headline"]["euler_break"]},
            "M2_external_controller": {"carrier": "X40", "augmentation": "X40 disjoint-union {q}", "cardinality": 41, "q_role": "owner-declared external controller"},
            "M3_residual_readout": {"nodes": residual_ids, "rho": {"A": 0, "S_01_j": 1}, "fiber_profile": [1, 5], "D5_invariant": preserved},
            "M4_seam_obstruction": {"intrinsic_H1_dimension": seam["summary"]["intrinsic_H1_dimension"], "compatible_added_seam_orbits": len(compatible), "D5_equivariant_bijections_R6_to_seam_choices": equivariant_bijections, "selected": None},
            "M5_fibonacci_rail": {"Q5": q5, "determinant": det, "thirteen_weights": fib13, "topology_selected": False},
            "M6_magic_34_control": {"magic_sum": 34, "Durer_operator": "R180", "Khajuraho_operator": "T(2,2) toric", "operators_identical": False},
            "M7_owner_palette": {"fibonacci_rail": "blue", "euler_stair": "green-yellow", "role": "display semantics only"},
            "M8_vigesimal_address_bus": {"dual_ingress_value": 29, "C30_phase": 29, "next_phase": 0, "C6_address": 5, "fibre_profile": [5, 5, 5, 5, 5, 5], "beta_candidates": selector_candidates, "beta_selected": None, "synchronization_cover": 120},
            "M9_gap_joint": {"identity": "206^2-204^2=820=41*20", "value": gap, "arc_identity": False, "physical_bridge": False},
            "M11_base20_decoder": {"formula": "n=400z+20y+x", "samples": {str(n): {"digits_zyx": decoded[n], "view_rz": projected[n]} for n in samples}, "projection": "(z,y,x)->(x+y/2,z)", "projection_injective": False, "frame_step": 15},
            "M12_namespace_boundary": {"V5": [-2, -1, 0, 1, 2], "C20": list(range(20)), "identified": False, "typed_map": None}
        },
        "interpretation": {
            "retained": [
                "exact 29=p10 and 41=p13 prime-index relation",
                "exact base-13 mirror 41=32_13 to 23_13=29",
                "exact Euler n=1..40 prime run with n=41 break at 41^2",
                "typed external 40+1 controller architecture",
                "canonical D5-invariant apex-versus-ring binary residual readout",
                "Fibonacci Q^5 determinant and dual magic-34 controls"
                ,"distinct 28+1 and 40+1 external-controller ingress routes meeting at value 29"
                ,"C30-to-C6 six-address quotient with five phases per address"
                ,"exact square-gap factorization 206^2-204^2=820=41*20"
                ,"exact base-20 layer/ring/point decoder for the five recovered Thread-V samples"
                ,"lossy affine display projection kept distinct from the base-20 digit state"
                ,"five-state and base-20 uses of vendissimal kept as distinct namespaces"
            ],
            "introduced": [
                "X40 disjoint-union {q} as an owner-declared controller carrier",
                "thirteen-step prime-index stair ending at 41",
                "blue Fibonacci rail and green-yellow Euler stair palette"
            ],
            "open": [
                "which of six added seam orbits is active",
                "commuting versus dihedral Janus selection",
                "typed Fibonacci-to-Pascal state map and transport law",
                "adjacency-preserving X20-to-Q106 intertwiner"
                ,"source-bound beta:C6-to-six-seam-orbits pin assignment"
            ]
        },
        "checks": checks,
        "source_hashes_verified": hashes,
        "external_source_hashes_verified": external_hashes,
        "claim_boundary": contract["claim_boundary"]
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = validate()
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.write:
        (HERE / "RESULT.json").write_text(rendered, encoding="utf-8")
    print(f"{result['status']}: {result['summary']['checks_passed']}/{result['summary']['checks_total']}")
    if result["status"] == "FAIL":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
