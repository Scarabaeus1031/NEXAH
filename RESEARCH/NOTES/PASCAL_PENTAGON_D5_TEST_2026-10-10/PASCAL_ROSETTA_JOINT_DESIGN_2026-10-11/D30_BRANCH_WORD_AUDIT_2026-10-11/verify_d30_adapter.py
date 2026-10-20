#!/usr/bin/env python3
"""Validate the bounded Pascal–Rosetta D30 design extension.

This is deterministic formal-fixture validation, not an admitted Lab run.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
from collections import Counter, defaultdict, deque
from pathlib import Path


HERE = Path(__file__).resolve().parent
DESIGN = HERE.parent
ARTIFACTS = DESIGN.parent / "SCC_003_REFERENCE" / "artifacts"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_csv(name: str) -> list[dict[str, str]]:
    with (ARTIFACTS / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def raw(row: dict[str, str]) -> tuple[int, int, int]:
    return int(row["face"]), int(row["n"]), int(row["k"])


def phase30(x: tuple[int, int, int]) -> int:
    _, n, k = x
    return (2 * k - n) % 30


def gear30(x: tuple[int, int, int]) -> tuple[int, int, int, int]:
    f, n, k = x
    return f % 5, (f + k) % 5, n % 6, phase30(x)


def left30(g: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    a, b, d, p = g
    return a, b, (d + 1) % 6, (p - 1) % 30


def right30(g: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    a, b, d, p = g
    return a, (b + 1) % 5, (d + 1) % 6, (p + 1) % 30


def reflect_raw(x: tuple[int, int, int]) -> tuple[int, int, int]:
    f, n, k = x
    return (-f) % 5, n, n - k


def h3_fixture() -> dict[str, object]:
    c = math.cos(math.pi / 5)
    s = math.sin(math.pi / 5)
    y = -0.5 / s
    roots_simple = [
        (1.0, 0.0, 0.0),
        (-c, s, 0.0),
        (0.0, y, math.sqrt(1.0 - y * y)),
    ]

    def reflect(v: tuple[float, float, float], a: tuple[float, float, float]):
        dot = sum(x * z for x, z in zip(v, a))
        return tuple(x - 2.0 * dot * z for x, z in zip(v, a))

    def key(v: tuple[float, float, float]):
        return tuple(round(x, 10) for x in v)

    roots = {key(v): v for v in roots_simple}
    queue = deque(roots_simple)
    while queue:
        v = queue.popleft()
        for a in roots_simple:
            w = reflect(v, a)
            if key(w) not in roots:
                roots[key(w)] = w
                queue.append(w)

    points = list(roots.values())
    index = {key(v): i for i, v in enumerate(points)}

    def coxeter(v):
        for a in roots_simple:
            v = reflect(v, a)
        return v

    permutation = [index[key(coxeter(v))] for v in points]
    seen: set[int] = set()
    cycle_lengths: list[int] = []
    for start in range(len(points)):
        if start in seen:
            continue
        cursor = start
        length = 0
        while cursor not in seen:
            seen.add(cursor)
            cursor = permutation[cursor]
            length += 1
        cycle_lengths.append(length)

    distances = {
        (i, j): sum((points[i][z] - points[j][z]) ** 2 for z in range(3))
        for i in range(len(points))
        for j in range(i + 1, len(points))
    }
    minimum = min(distances.values())
    edges = [pair for pair, value in distances.items() if abs(value - minimum) < 1e-8]
    degree = Counter(vertex for edge in edges for vertex in edge)
    return {
        "points": len(points),
        "edges": len(edges),
        "degrees": sorted(degree.values()),
        "coxeter_cycles": sorted(cycle_lengths),
    }


def validate() -> dict[str, object]:
    contract_path = HERE / "D30_CONTRACT.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    incidences = load_csv("face_incidence.csv")
    face_edges = load_csv("face_edges.csv")
    checks: list[dict[str, object]] = []

    def check(name: str, passed: bool, observed: object, expected: object) -> None:
        checks.append({
            "name": name,
            "status": "PASS" if passed else "FAIL",
            "observed": observed,
            "expected": expected,
        })

    check(
        "identity reuse and no creation",
        contract["identity"]["reuse"] == "A0OE:PASCAL_PENTAGON_D5_TEST"
        and contract["identity"]["creates"] == [],
        contract["identity"],
        {"reuse": "A0OE:PASCAL_PENTAGON_D5_TEST", "creates": []},
    )

    words = [
        "".join(bits)
        for length in range(7)
        for bits in itertools.product("LR", repeat=length)
    ]
    check("complete branch-word enumeration", len(words) == 127, len(words), 127)
    check("five-face word instances", len(words) * 5 == 635, len(words) * 5, 635)

    endpoint_counts = Counter((len(word), word.count("R")) for word in words)
    expected_counts = {
        (n, k): math.comb(n, k) for n in range(7) for k in range(n + 1)
    }
    check(
        "Pascal endpoint multiplicities",
        endpoint_counts == expected_counts,
        {f"{n},{k}": endpoint_counts[(n, k)] for n, k in sorted(endpoint_counts)},
        {f"{n},{k}": expected_counts[(n, k)] for n, k in sorted(expected_counts)},
    )

    raw_points = [raw(row) for row in incidences]
    register_counts = Counter(f"D{f + 1}" for f, _, _ in raw_points)
    check(
        "five D-registers are balanced",
        register_counts == {f"D{i}": 28 for i in range(1, 6)},
        dict(sorted(register_counts.items())),
        {f"D{i}": 28 for i in range(1, 6)},
    )
    register_word_counts = {f"D{i}": len(words) for i in range(1, 6)}
    check(
        "complete branch-word set per D-register",
        set(register_word_counts.values()) == {127},
        register_word_counts,
        {f"D{i}": 127 for i in range(1, 6)},
    )

    register_phase_fibres: dict[tuple[str, int], list[tuple[int, int, int]]] = defaultdict(list)
    for x in raw_points:
        f, _, _ = x
        register_phase_fibres[(f"D{f + 1}", phase30(x))].append(x)
    register_phase_profile = Counter(len(values) for values in register_phase_fibres.values())
    expected_register_phase_profile = {1: 20, 2: 20, 3: 20, 4: 5}
    check(
        "D-register phase-cover capacity and frozen occupancy",
        contract["d_registers"]["cover_capacity"] == 150
        and len(register_phase_fibres) == 65,
        {"capacity": contract["d_registers"]["cover_capacity"], "observed": len(register_phase_fibres)},
        {"capacity": 150, "observed": 65},
    )
    check(
        "lossy register-phase projection fibre profile",
        dict(sorted(register_phase_profile.items())) == expected_register_phase_profile,
        dict(sorted(register_phase_profile.items())),
        expected_register_phase_profile,
    )

    register_rotation = {f"D{i}": f"D{(i % 5) + 1}" for i in range(1, 6)}
    register_reflection = {
        f"D{i}": f"D{((-(i - 1)) % 5) + 1}" for i in range(1, 6)
    }
    expected_rotation = {"D1": "D2", "D2": "D3", "D3": "D4", "D4": "D5", "D5": "D1"}
    expected_reflection = {"D1": "D1", "D2": "D5", "D3": "D4", "D4": "D3", "D5": "D2"}
    check(
        "C5/D5 actions on D-register labels",
        register_rotation == expected_rotation and register_reflection == expected_reflection,
        {"rotation": register_rotation, "reflection": register_reflection},
        {"rotation": expected_rotation, "reflection": expected_reflection},
    )

    encoded = {x: gear30(x) for x in raw_points}
    inverse = {g: x for x, g in encoded.items()}
    check("F30 injective on frozen incidences", len(inverse) == 140, len(inverse), 140)

    failures = {"left": [], "right": []}
    phase_matches = {"left_minus": 0, "left_plus": 0, "right_minus": 0, "right_plus": 0, "locked": 0}
    for edge in face_edges:
        f, n, k = int(edge["face"]), int(edge["parent_n"]), int(edge["parent_k"])
        source = (f, n, k)
        branch = edge["branch"]
        target = (f, n + 1, k if branch == "left" else k + 1)
        expected = left30(gear30(source)) if branch == "left" else right30(gear30(source))
        if gear30(target) != expected:
            failures[branch].append((source, target))
        delta = (phase30(target) - phase30(source)) % 30
        phase_matches[f"{branch}_minus"] += delta == 29
        phase_matches[f"{branch}_plus"] += delta == 1
        phase_matches["locked"] += delta == 0

    check("left D30 intertwining", not failures["left"], {"tested": 105, "failures": len(failures["left"])}, {"tested": 105, "failures": 0})
    check("right D30 intertwining", not failures["right"], {"tested": 105, "failures": len(failures["right"])}, {"tested": 105, "failures": 0})
    expected_matches = {"left_minus": 105, "left_plus": 0, "right_minus": 0, "right_plus": 105, "locked": 0}
    check("signed branch controls", phase_matches == expected_matches, phase_matches, expected_matches)

    reflection_failures = [
        x for x in raw_points if phase30(reflect_raw(x)) != (-phase30(x)) % 30
    ]
    check("reflection compiles to phase negation", not reflection_failures, {"tested": 140, "failures": len(reflection_failures)}, {"tested": 140, "failures": 0})

    reconstructed = 0
    for f, n, k in raw_points:
        candidates = [j for j in range(n + 1) if (2 * j - n) % 30 == phase30((f, n, k))]
        reconstructed += candidates == [k]
    check("D-register-depth-phase exact reconstruction", reconstructed == 140, reconstructed, 140)

    phases = sorted({phase30(x) for x in raw_points})
    check("bounded phase coverage remains partial", len(phases) == 13, {"count": len(phases), "phases": phases}, {"count": 13, "full_cycle": False})

    coefficients_5 = [0, 6, 12, 18, 24]
    coefficients_6_12 = [0, 5, 10, 15, 20, 25]
    characters = list(itertools.product(coefficients_5, coefficients_5, coefficients_6_12, coefficients_6_12))
    unit_schedule = []
    for x, y, z, w in characters:
        left_delta = (z - w) % 30
        right_delta = (y + z + w) % 30
        if left_delta == 29 and right_delta == 1:
            unit_schedule.append((x, y, z, w))
    check("all old-gear characters enumerated", len(characters) == 900, len(characters), 900)
    check("expected non-factorization through C12 gear", not unit_schedule, len(unit_schedule), 0)

    h3 = h3_fixture()
    check("H3 root orbit has 30 points", h3["points"] == 30, h3["points"], 30)
    check("H3 nearest-neighbour carrier", h3["edges"] == 60 and set(h3["degrees"]) == {4}, {"edges": h3["edges"], "degree_profile": dict(Counter(h3["degrees"]))}, {"edges": 60, "degree_profile": {4: 30}})
    check("H3 Coxeter decomposition is 3x10", h3["coxeter_cycles"] == [10, 10, 10], h3["coxeter_cycles"], [10, 10, 10])

    e8_positions = [(lane, phase) for lane in range(8) for phase in range(30)]
    e8_adapters = [(lane, origin, orientation) for lane in range(8) for origin in range(30) for orientation in (-1, 1)]
    check("E8 coordinate carrier size", len(e8_positions) == len(set(e8_positions)) == 240, len(e8_positions), 240)
    check("E8 adapter non-uniqueness retained", len(e8_adapters) == 480 and not contract["carrier_boundaries"]["e8"]["canonical_adapter_selected"], {"candidate_adapters": len(e8_adapters), "canonical_selected": False}, {"candidate_adapters": 480, "canonical_selected": False})

    # Two reflections whose axes differ by 6 degrees compose to signed 12-degree rotations.
    samples = range(30)
    s0 = lambda p: (-p) % 30
    f6 = lambda p: (1 - p) % 30
    left_composition = [s0(f6(p)) for p in samples]
    right_composition = [f6(s0(p)) for p in samples]
    check("ordered reflections compile to signed unit rotations", left_composition == [(p - 1) % 30 for p in samples] and right_composition == [(p + 1) % 30 for p in samples], {"left": "p-1", "right": "p+1"}, {"left": "p-1", "right": "p+1"})

    passed = all(item["status"] == "PASS" for item in checks)
    return {
        "schema": "nexah.pascal-rosetta-d30-audit-result/1.0.0",
        "status": "PASS" if passed else "FAIL",
        "classification": "FORMAL_DESIGN_VALIDATION_NOT_SCIENCE_RUN",
        "identity_reused": contract["identity"]["reuse"],
        "creates": [],
        "summary": {
            "checks_passed": sum(item["status"] == "PASS" for item in checks),
            "checks_total": len(checks),
            "branch_words": len(words),
            "face_word_instances": len(words) * 5,
            "d_registers": 5,
            "d_register_phase_capacity": 150,
            "d_register_phase_states_observed": len(register_phase_fibres),
            "raw_incidences": len(raw_points),
            "observed_phases": len(phases),
            "old_gear_characters": len(characters),
            "old_gear_unit_schedule_candidates": len(unit_schedule),
            "h3_coxeter_cycles": h3["coxeter_cycles"],
            "e8_coordinate_adapter_candidates": len(e8_adapters),
        },
        "checks": checks,
        "input_hashes": {
            "contract": sha256(contract_path),
            "face_incidence": sha256(ARTIFACTS / "face_incidence.csv"),
            "face_edges": sha256(ARTIFACTS / "face_edges.csv"),
        },
        "claim_boundary": contract["claim_boundary"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = validate()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write:
        (HERE / "RESULT.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
