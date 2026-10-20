#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(parent for parent in HERE.parents if parent.name == "NEXAH ECOSYSTEM")
CONTRACT = json.loads((HERE / "CONTRACT.json").read_text())
checks: list[dict] = []


def check(name, observed, expected=True):
    passed = observed == expected
    checks.append({"name": name, "passed": passed, "observed": observed, "expected": expected})
    return passed


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(m: int, value: int) -> int:
    if m < 1 or not 0 <= value < 2 * m:
        raise ValueError((m, value))
    return value if value <= m - 1 else value - 1


def fold(m: int, source: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(q(m, value) for value in source)


def residual(m: int, source: tuple[int, ...]) -> tuple[int, ...]:
    target = fold(m, source)
    return tuple(source[index] - (m - 1) for index, value in enumerate(target) if value == m - 1)


def reconstruct(m: int, target: tuple[int, ...], bits: tuple[int, ...]) -> tuple[int, ...]:
    output = []
    bit_index = 0
    for value in target:
        if value < m - 1:
            output.append(value)
        elif value > m - 1:
            output.append(value + 1)
        else:
            if bit_index >= len(bits) or bits[bit_index] not in (0, 1):
                raise ValueError("missing or invalid residual bit")
            output.append(m - 1 + bits[bit_index])
            bit_index += 1
    if bit_index != len(bits):
        raise ValueError("unused residual bit")
    return tuple(output)


def expected_profile(m: int, d: int) -> Counter:
    counts = {2**k: math.comb(d, k) * (2 * m - 2) ** (d - k) for k in range(d + 1)}
    return Counter({size: count for size, count in counts.items() if count})


def observed_profile(m: int, d: int) -> Counter:
    fibres = defaultdict(int)
    for source in itertools.product(range(2 * m), repeat=d):
        fibres[fold(m, source)] += 1
    return Counter(fibres.values())


check("extends TripleSix audit", CONTRACT["identity"]["extends"], "A0-BL-023:TRIPLESIX_S3_CUBE_GRID_FOLD_BRIDGE_AUDIT:V1")
check("formal non-admitted status", CONTRACT["status"], "FORMAL_DESIGN_VALIDATION_NOT_ADMITTED_NOT_NEW_STUDY")
check("creates no identity", CONTRACT["identity"]["creates"], [])
for source in CONTRACT["frozen_sources"]:
    path = ROOT / source["path"]
    check(f"source exists: {source['source_id']}", path.exists())
    if path.exists():
        check(f"source hash: {source['source_id']}", sha256(path), source["sha256"])

profile_rows = []
case_rows = []
for m in range(1, 6):
    for d in range(1, 5):
        observed = observed_profile(m, d)
        expected = expected_profile(m, d)
        check(f"profile m={m} d={d}", dict(sorted(observed.items())), dict(sorted(expected.items())))
        check(f"target count m={m} d={d}", sum(observed.values()), (2 * m - 1) ** d)
        check(f"source count m={m} d={d}", sum(size * count for size, count in observed.items()), (2 * m) ** d)
        all_return = True
        for source in itertools.product(range(2 * m), repeat=d):
            target = fold(m, source)
            bits = residual(m, source)
            all_return &= len(bits) == sum(value == m - 1 for value in target)
            all_return &= reconstruct(m, target, bits) == source
        check(f"exact sparse Return m={m} d={d}", all_return)
        for k in range(d + 1):
            profile_rows.append({
                "m": m,
                "dimension": d,
                "central_coordinates_k": k,
                "fibre_size": 2**k,
                "target_points": math.comb(d, k) * (2 * m - 2) ** (d - k),
                "pointwise_minimal_residual_bits": k,
                "uniform_worst_case_bits": d,
            })

controls = {
    "boolean_collapse": {"m": 1, "d": 4, "profile": {"16": 1}},
    "four_to_three_cube": {"m": 2, "d": 3, "profile": {"1": 8, "2": 12, "4": 6, "8": 1}},
}
for name, control in controls.items():
    actual = observed_profile(control["m"], control["d"])
    check(f"control {name}", {str(k): v for k, v in sorted(actual.items())}, control["profile"])
    case_rows.append({"case": name, "m": control["m"], "dimension": control["d"], "profile": json.dumps(control["profile"], sort_keys=True)})

profiles_64_63 = {d: expected_profile(32, d) for d in (1, 2, 3)}
expected_64_63 = {
    1: Counter({1: 62, 2: 1}),
    2: Counter({1: 3844, 2: 124, 4: 1}),
    3: Counter({1: 238328, 2: 11532, 4: 186, 8: 1}),
}
for d in (1, 2, 3):
    check(f"recover 64-to-63 profile d={d}", dict(sorted(profiles_64_63[d].items())), dict(sorted(expected_64_63[d].items())))

for k in range(5):
    check(f"pointwise lower bound k={k}", math.ceil(math.log2(2**k)), k)
for d in range(1, 5):
    check(f"uniform lower bound d={d}", math.ceil(math.log2(2**d)), d)

check("TripleSix selected-axis capacity", 3 * 2, 6)
check("TripleSix insufficient at 3D central fibre", 6 < 2**3, True)

with (HERE / "FIBRE_PROFILE.csv").open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=profile_rows[0].keys())
    writer.writeheader()
    writer.writerows(profile_rows)

with (HERE / "RESIDUAL_RETURN_CASES.csv").open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=case_rows[0].keys())
    writer.writeheader()
    writer.writerows(case_rows)

passed = sum(item["passed"] for item in checks)
result = {
    "status": "PASS_GENERAL_COORDINATE_FOLD_PROFILE_AND_MINIMAL_RESIDUAL_RETURN" if passed == len(checks) else "FAIL",
    "classification": "EXACT_FIBRE_PROFILE_POINTWISE_K_BITS_UNIFORM_D_BITS",
    "checks": {"passed": passed, "total": len(checks)},
    "theorem": {
        "map": "Q_{m,d}=q_m^d with q_m(i)=i for i<=m-1 and i-1 for i>=m",
        "fibre_size": "2^k for a target with k central coordinates",
        "target_count": "C(d,k)(2m-2)^(d-k)",
        "target_conservation": "sum_k C(d,k)(2m-2)^(d-k)=(2m-1)^d",
        "source_conservation": "sum_k 2^k C(d,k)(2m-2)^(d-k)=(2m)^d",
    },
    "return": {
        "pointwise_minimal_bits": "k(y)",
        "uniform_fixed_width_minimal_bits": "d",
        "construction": "one side bit for each central target coordinate",
        "exact": True,
    },
    "controls": controls,
    "recovered_64_to_63_profiles": {str(d): {str(k): v for k, v in sorted(profile.items())} for d, profile in profiles_64_63.items()},
    "triplesix_boundary": {
        "supported": "three selected one-axis double fibres",
        "not_supported": "one simultaneous three-axis central fibre",
        "reason": "6 states < 8 source states",
    },
    "a0_bl_025": {
        "coordinate_fold_and_return_subproblem": "CLOSED_BY_FORMAL_DESIGN_VALIDATION",
        "full_grid_fold_channel_specification": "OPEN_ADMISSION_REQUIRED",
        "missing": ["embedding", "envelope", "channel/interface", "assembly", "update rule"],
    },
    "claim_boundary": CONTRACT["authority_boundary"],
    "checks_detail": checks,
}
(HERE / "RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"status": result["status"], "checks": result["checks"]}, indent=2))
raise SystemExit(0 if passed == len(checks) else 1)
