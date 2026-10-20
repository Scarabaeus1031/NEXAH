#!/usr/bin/env python3
"""Validate the finite Lissajous–Möbius return candidate.

This is deterministic formal-design validation, not an admitted Lab run.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
DESIGN = HERE.parent
ARTIFACTS = DESIGN.parent / "SCC_003_REFERENCE" / "artifacts"
D30_CONTRACT = DESIGN / "D30_BRANCH_WORD_AUDIT_2026-10-11" / "D30_CONTRACT.json"
ARCHAEOLOGY = (
    Path(__file__).resolve().parents[4]
    / "HISTORY"
    / "PASCAL_FIBONACCI_MOBIUS_LEO_LILITH_ARCHAEOLOGY_2026-10-10"
    / "README.md"
)

State = tuple[int, int, int]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reflect_register(register: int) -> int:
    return (-register) % 5


def signed_register(register: int) -> int:
    return (0, 1, 2, -2, -1)[register]


def phase_signature(phase: int) -> tuple[int, int]:
    return phase % 6, phase % 5


def display_point(phase: int) -> tuple[float, float]:
    theta = 2.0 * math.pi * phase / 30.0
    return round(math.cos(5.0 * theta), 12), round(math.sin(6.0 * theta), 12)


def step(state: State, delta: int, twisted: bool) -> State:
    register, phase, orientation = state
    if delta not in (-1, 1):
        raise ValueError("delta must be -1 or +1")
    next_phase = (phase + delta) % 30
    crosses_seam = (delta == 1 and phase == 29) or (delta == -1 and phase == 0)
    if twisted and crosses_seam:
        register = reflect_register(register)
        orientation = -orientation
    return register, next_phase, orientation


def walk(state: State, deltas: list[int], twisted: bool) -> State:
    for delta in deltas:
        state = step(state, delta, twisted)
    return state


def boundary_component_count(twisted: bool) -> int:
    adjacency: dict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
    for side in (-1, 1):
        for phase in range(29):
            left = phase, side
            right = phase + 1, side
            adjacency[left].add(right)
            adjacency[right].add(left)
        seam_side = -side if twisted else side
        left = 29, side
        right = 0, seam_side
        adjacency[left].add(right)
        adjacency[right].add(left)

    unseen = set(adjacency)
    components = 0
    while unseen:
        components += 1
        stack = [unseen.pop()]
        while stack:
            node = stack.pop()
            for neighbour in adjacency[node]:
                if neighbour in unseen:
                    unseen.remove(neighbour)
                    stack.append(neighbour)
    return components


def validate() -> dict[str, object]:
    contract_path = HERE / "CONTRACT.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    d30 = json.loads(D30_CONTRACT.read_text(encoding="utf-8"))
    checks: list[dict[str, object]] = []

    def check(name: str, passed: bool, observed: object, expected: object) -> None:
        checks.append({
            "name": name,
            "status": "PASS" if passed else "FAIL",
            "observed": observed,
            "expected": expected,
        })

    check(
        "identity reused without creation",
        contract["identity"]["reuse"] == "A0OE:PASCAL_PENTAGON_D5_TEST"
        and contract["identity"]["creates"] == [],
        contract["identity"],
        {"reuse": "A0OE:PASCAL_PENTAGON_D5_TEST", "creates": []},
    )
    check(
        "parent D30 contract is the signed unit lift",
        d30["phase_lift"]["modulus"] == 30
        and d30["phase_lift"]["left_increment"] == -1
        and d30["phase_lift"]["right_increment"] == 1,
        d30["phase_lift"],
        {"modulus": 30, "left_increment": -1, "right_increment": 1},
    )

    signatures = [phase_signature(phase) for phase in range(30)]
    check(
        "C6 x C5 phase signature is an exact C30 chart",
        len(set(signatures)) == 30,
        len(set(signatures)),
        30,
    )
    signature_return = {
        signature: phase for phase, signature in enumerate(signatures)
    }
    check(
        "phase signature reconstructs every phase",
        all(signature_return[phase_signature(phase)] == phase for phase in range(30)),
        len(signature_return),
        30,
    )

    display_points = [display_point(phase) for phase in range(30)]
    display_profile = Counter(display_points)
    check(
        "Lissajous display projection is lossy as declared",
        len(display_profile) == 20 and sorted(display_profile.values()) == [1] * 10 + [2] * 10,
        {"unique_points": len(display_profile), "fibre_profile": dict(Counter(display_profile.values()))},
        {"unique_points": 20, "fibre_profile": {1: 10, 2: 10}},
    )

    reflection_chart = {
        f"D{register + 1}": {
            "reflected": f"D{reflect_register(register) + 1}",
            "v": signed_register(register) / 2,
            "reflected_v": signed_register(reflect_register(register)) / 2,
        }
        for register in range(5)
    }
    check(
        "D-register reflection compiles to v negation",
        all(item["reflected_v"] == -item["v"] for item in reflection_chart.values()),
        reflection_chart,
        "v(reflect(j))=-v(j)",
    )

    states = [
        (register, phase, orientation)
        for register in range(5)
        for phase in range(30)
        for orientation in (-1, 1)
    ]
    check("candidate state cardinality", len(states) == 300, len(states), 300)

    cylinder_one_turn = [walk(state, [1] * 30, False) for state in states]
    mobius_one_turn = [walk(state, [1] * 30, True) for state in states]
    mobius_two_turns = [walk(state, [1] * 60, True) for state in states]
    check(
        "cylinder one-turn exact return",
        cylinder_one_turn == states,
        sum(left == right for left, right in zip(cylinder_one_turn, states)),
        300,
    )
    expected_mobius_one_turn = [
        (reflect_register(register), phase, -orientation)
        for register, phase, orientation in states
    ]
    check(
        "Mobius one-turn monodromy",
        mobius_one_turn == expected_mobius_one_turn,
        sum(left == right for left, right in zip(mobius_one_turn, expected_mobius_one_turn)),
        300,
    )
    check(
        "Mobius two-turn exact return",
        mobius_two_turns == states,
        sum(left == right for left, right in zip(mobius_two_turns, states)),
        300,
    )
    apparent_returns_without_orientation = sum(
        (left[0], left[1]) == (right[0], right[1])
        for left, right in zip(mobius_one_turn, states)
    )
    check(
        "orientation fibre prevents false fixed-register return",
        apparent_returns_without_orientation == 60
        and all(left != right for left, right in zip(mobius_one_turn, states)),
        {"apparent_returns_without_e": apparent_returns_without_orientation, "exact_returns": 0},
        {"apparent_returns_without_e": 60, "exact_returns": 0},
    )

    seam_inverse_failures = 0
    for state in states:
        if step(step(state, 1, True), -1, True) != state:
            seam_inverse_failures += 1
        if step(step(state, -1, True), 1, True) != state:
            seam_inverse_failures += 1
    check(
        "forward and reverse Mobius steps are mutual inverses",
        seam_inverse_failures == 0,
        seam_inverse_failures,
        0,
    )

    boundary_counts = {
        "cylinder": boundary_component_count(False),
        "mobius": boundary_component_count(True),
    }
    check(
        "cylinder and Mobius boundary controls separate",
        boundary_counts == {"cylinder": 2, "mobius": 1},
        boundary_counts,
        {"cylinder": 2, "mobius": 1},
    )

    words = [
        "".join(bits)
        for length in range(7)
        for bits in itertools.product("LR", repeat=length)
    ]
    word_failures = 0
    phase_failures = 0
    for state in states:
        for word in words:
            deltas = [-1 if letter == "L" else 1 for letter in word]
            endpoint = walk(state, deltas, True)
            inverse = [-delta for delta in reversed(deltas)]
            if walk(endpoint, inverse, True) != state:
                word_failures += 1
            expected_phase = (state[1] + sum(deltas)) % 30
            if endpoint[1] != expected_phase:
                phase_failures += 1
    check(
        "all bounded Pascal words have exact inverse transport",
        len(words) == 127 and word_failures == 0,
        {"words": len(words), "state_word_cases": len(states) * len(words), "failures": word_failures},
        {"words": 127, "state_word_cases": 38100, "failures": 0},
    )
    check(
        "branch transport retains signed D30 endpoint phase",
        phase_failures == 0,
        phase_failures,
        0,
    )

    with (ARTIFACTS / "face_incidence.csv").open(newline="", encoding="utf-8") as handle:
        incidences = list(csv.DictReader(handle))
    charts = []
    for row in incidences:
        register = int(row["face"])
        depth = int(row["n"])
        branch_index = int(row["k"])
        phase = (2 * branch_index - depth) % 30
        charts.append({
            "register": register,
            "phase": phase,
            "u": phase / 30,
            "v": signed_register(register) / 2,
        })
    check(
        "all frozen Pascal incidences receive a candidate strip chart",
        len(charts) == 140 and all(0 <= item["u"] < 1 and -1 <= item["v"] <= 1 for item in charts),
        {"charted": len(charts), "unique_register_phase": len({(item["register"], item["phase"]) for item in charts})},
        {"charted": 140, "unique_register_phase": 65},
    )

    passed = all(item["status"] == "PASS" for item in checks)
    return {
        "schema": "nexah.pascal-lissajous-mobius-return-candidate-result/1.0.0",
        "status": "PASS_WITH_BOUNDARY" if passed else "FAIL",
        "classification": "FORMAL_DESIGN_VALIDATION_NOT_SCIENCE_RUN_NOT_PENT_08",
        "identity_reused": contract["identity"]["reuse"],
        "creates": [],
        "summary": {
            "checks_passed": sum(item["status"] == "PASS" for item in checks),
            "checks_total": len(checks),
            "candidate_states": len(states),
            "exact_lissajous_phase_states": len(set(signatures)),
            "display_points": len(display_profile),
            "cylinder_boundary_components": boundary_counts["cylinder"],
            "mobius_boundary_components": boundary_counts["mobius"],
            "bounded_branch_words": len(words),
            "state_word_cases": len(states) * len(words),
            "frozen_pascal_incidences_charted": len(charts),
        },
        "checks": checks,
        "input_hashes": {
            "contract": sha256(contract_path),
            "d30_contract": sha256(D30_CONTRACT),
            "face_incidence": sha256(ARTIFACTS / "face_incidence.csv"),
            "archaeology": sha256(ARCHAEOLOGY),
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
    return 0 if result["status"] == "PASS_WITH_BOUNDARY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
