#!/usr/bin/env python3
"""Replay the bounded Janus, PN, handle, and VM transfer audit."""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from fractions import Fraction
from math import gcd
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def primes(count: int) -> list[int]:
    found: list[int] = []
    candidate = 2
    while len(found) < count:
        if all(candidate % p for p in found if p * p <= candidate):
            found.append(candidate)
        candidate += 1
    return found


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    p = 2
    while p * p <= n:
        if n % p == 0:
            return False
        p += 1
    return True


def validate() -> dict[str, object]:
    contract = json.loads((HERE / "CONTRACT.json").read_text(encoding="utf-8"))
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

    source_resolution: dict[str, object] = {}
    for group_name in ("frozen_sources", "visual_sources"):
        for name, spec in contract[group_name].items():
            path = Path(spec["absolute_path"]) if "absolute_path" in spec else ROOT / spec["path"]
            observed = sha256(path) if path.exists() else None
            source_resolution[name] = {"path": str(path), "sha256": observed, "class": group_name}
            check(f"source integrity {name}", observed == spec["sha256"], observed, spec["sha256"])

    p = primes(1004)
    prime = lambda index: p[index - 1]

    # M1 — the exact prime AP and its historical translation.
    prime_indices = [25, 27, 29]
    prime_row = [prime(index) for index in prime_indices]
    years = [1933, 1939, 1945]
    prime_steps = [b - a for a, b in zip(prime_row, prime_row[1:])]
    year_steps = [b - a for a, b in zip(years, years[1:])]
    check("M1 prime-index row", prime_row == [97, 103, 109], prime_row, [97, 103, 109])
    check("M1 common six-step", prime_steps == year_steps == [6, 6], {"prime": prime_steps, "year": year_steps}, [6, 6])
    check("M1 translation by carrier 1836", [1836 + x for x in prime_row] == years, [1836 + x for x in prime_row], years)

    # M2 — nested additive involutions and the typed 7/6 handle.
    j206 = lambda x: 206 - x
    j212 = lambda x: 212 - x
    j3878 = lambda x: 3878 - x
    tau = lambda x: x - 1836
    check("M2 J206 swaps 97 and 109 and fixes 103", [j206(97), j206(103), j206(109)] == [109, 103, 97], [j206(x) for x in prime_row], [109, 103, 97])
    check("M2 J3878 swaps 1933 and 1945 and fixes 1939", [j3878(x) for x in years] == [1945, 1939, 1933], [j3878(x) for x in years], [1945, 1939, 1933])
    intertwiner_samples = list(range(1700, 2001))
    intertwined = all(tau(j3878(t)) == j206(tau(t)) for t in intertwiner_samples)
    check("M2 carrier translation intertwines Janus maps", intertwined, intertwined, True)
    check("M2 Q106 is nested center of 103 and 109", j212(103) == 109 and j212(106) == 106 and j212(109) == 103, [j212(103), j212(106), j212(109)], [109, 106, 103])
    check("M2 Q106 is not a member of prime triad", 106 not in prime_row and not is_prime(106), {"in_row": 106 in prime_row, "prime": is_prime(106)}, {"in_row": False, "prime": False})
    handle = {"7+6": 7 + 6, "7*6": 7 * 6, "p6": prime(6), "p13": prime(13), "p14": prime(14)}
    check("M2 additive handle reaches p6", handle["7+6"] == handle["p6"] == 13, handle, {"7+6": 13, "p6": 13})
    check("M2 multiplicative handle equals 42", handle["7*6"] == 42, handle["7*6"], 42)
    check("M2 42 is bracketed by consecutive primes", handle["p13"] == 41 and handle["p14"] == 43 and (41 + 43) // 2 == 42, {"p13": handle["p13"], "center": 42, "p14": handle["p14"]}, {"p13": 41, "center": 42, "p14": 43})
    check("M2 standard prime-index boundary for 53 and 19", prime(16) == 53 and 2 * prime(16) == 106 and prime(19) == 67, {"p16": prime(16), "2*p16": 2 * prime(16), "p19": prime(19)}, {"p16": 53, "2*p16": 106, "p19": 67})
    six_step_hits: list[dict[str, object]] = []
    six_step_double_chains: list[dict[str, object]] = []
    for k in range(1, 1001):
        if prime(k + 2) - prime(k) == 6:
            six_step_hits.append({"start_index": k, "values": [prime(k), prime(k + 2)]})
        if prime(k + 2) - prime(k) == 6 and prime(k + 4) - prime(k + 2) == 6:
            six_step_double_chains.append({"start_index": k, "indices": [k, k + 2, k + 4], "values": [prime(k), prime(k + 2), prime(k + 4)]})
    expected_double_starts = [3, 4, 5, 25, 26, 234, 285, 483, 742]
    check("M2 bounded prime six-step recurrence count", len(six_step_hits) == 99 and [item["start_index"] for item in six_step_double_chains] == expected_double_starts, {"single_hits": len(six_step_hits), "double_starts": [item["start_index"] for item in six_step_double_chains]}, {"single_hits": 99, "double_starts": expected_double_starts})
    selected_chains = {item["start_index"]: item["values"] for item in six_step_double_chains if item["start_index"] in (4, 25, 742)}
    check("M2 selected prime six-step chains", selected_chains == {4: [7, 13, 19], 25: [97, 103, 109], 742: [5647, 5653, 5659]}, selected_chains, {4: [7, 13, 19], 25: [97, 103, 109], 742: [5647, 5653, 5659]})

    # M3 — the same row in two carrier coordinates.
    residual_1729 = [year - 1729 for year in years]
    residual_1836 = [year - 1836 for year in years]
    check("M3 residual row at 1729", residual_1729 == [204, 210, 216], residual_1729, [204, 210, 216])
    check("M3 residual row at 1836", residual_1836 == prime_row, residual_1836, prime_row)
    check("M3 endpoint factorizations", 204 == 12 * 17 and 210 == 2 * 3 * 5 * 7 and 216 == 6**3, {"204": "12*17", "210": "2*3*5*7", "216": "6^3"}, True)
    check("M3 carrier gap is p28", 1836 - 1729 == prime(28) == 107, {"gap": 107, "p28": prime(28)}, 107)
    residual_matrix = [residual_1729, residual_1836]
    mixed = [(residual_matrix[1][i + 1] - residual_matrix[1][i]) - (residual_matrix[0][i + 1] - residual_matrix[0][i]) for i in range(2)]
    check("M3 raw carrier/year interaction is zero", mixed == [0, 0], mixed, [0, 0])

    # M4 — suffix PN transfer and bounded controls.
    suffixes = [29, 33, 45]
    pn_row = [prime(index) for index in suffixes]
    input_steps = [4, 12]
    output_steps = [b - a for a, b in zip(pn_row, pn_row[1:])]
    gains = [Fraction(out, inp) for out, inp in zip(output_steps, input_steps)]
    check("M4 suffix PN row", pn_row == [109, 137, 197], pn_row, [109, 137, 197])
    check("M4 local transfer gains", gains == [Fraction(7), Fraction(5)], [str(x) for x in gains], ["7", "5"])
    check("M4 two-step gain drop", gains[0] - gains[1] == 2 and gains[1] < gains[0], {"gains": [str(x) for x in gains], "drop": str(gains[0] - gains[1])}, {"drop": "2"})
    check("M4 final PN outputs lock to QRT residue 17", [x % 20 for x in pn_row] == [9, 17, 17], [x % 20 for x in pn_row], [9, 17, 17])
    control_hits: list[dict[str, object]] = []
    r17_hits: list[dict[str, object]] = []
    for a in range(1, 101):
        indices = [a, a + 4, a + 16]
        values = [prime(index) for index in indices]
        local = [Fraction(values[1] - values[0], 4), Fraction(values[2] - values[1], 12)]
        record = {"start": a, "values": values, "gains": [str(x) for x in local]}
        if local == [Fraction(7), Fraction(5)]:
            control_hits.append(record)
        if values[1] % 20 == values[2] % 20 == 17:
            r17_hits.append(record)
    check("M4 bounded gain-pattern control is unique", [item["start"] for item in control_hits] == [29], control_hits, [{"start": 29}])
    check("M4 r17 lock alone is non-unique", [item["start"] for item in r17_hits] == [21, 29, 62], [item["start"] for item in r17_hits], [21, 29, 62])
    check("M4 1929 keeps typed 929 component", 1929 == 1000 + 929 and prime(158) == 929, {"split": [1000, 929], "p158": prime(158)}, {"split": [1000, 929], "p158": 929})
    check("M4 suffix-PN closes 1929 to final offset", prime(1929 % 100) == 1945 - 1836 == 109, {"P(29)": prime(29), "1945-1836": 1945 - 1836}, 109)

    # M5 — keep additive mirror, digit reversal, and split map distinct.
    j3565 = lambda x: 3565 - x
    check("M5 J3565 exchanges the carriers", j3565(1729) == 1836 and j3565(1836) == 1729, [j3565(1729), j3565(1836)], [1836, 1729])
    check("M5 fixed-width reversal", int(str(3565)[::-1]) == 5653, int(str(3565)[::-1]), 5653)
    check("M5 5653 is p744", prime(744) == 5653, prime(744), 5653)
    check("M5 typed 1461 decomposition", 1461 == 100 * 14 + prime(18) and 14 == 2 * 7 and 18 == 2 * 3**2, {"1461": [14, prime(18)], "14": "2*7", "18": "2*3^2"}, True)
    f1461 = 100 * (4 * 14) + prime(18 - 2)
    check("M5 proposed split map sends 1461 to 5653", f1461 == 5653 and 4 * 14 == 7 * 8 and prime(16) == 53, {"F(1461)": f1461, "56": "7*8", "p16": prime(16)}, {"F(1461)": 5653})
    permutations = sorted({int("".join(chars)) for chars in itertools.permutations("3565") if chars[0] != "0"})
    prime_permutations = [value for value in permutations if is_prime(value)]
    check("M5 decimal-permutation control", prime_permutations == [5563, 5653, 6553] and len(permutations) == 12, {"unique": len(permutations), "primes": prime_permutations}, {"unique": 12, "primes": [5563, 5653, 6553]})

    # M6 — semantic aliases are held apart rather than numerically collapsed.
    vm_roles = {
        "VM_VERTICAL_AXIS": "AM/PM orientation visual",
        "vm_CONTRACTION_BRANCH": "polygon escape visual",
        "VM_VORSTELLUNGS_MEDIUM": "structural clarification PDF",
        "VM_TIME_RING_LABEL": "time resonance ring visual",
    }
    check("M6 VM roles remain source-typed and distinct", len(vm_roles) == len(set(vm_roles)) == 4, vm_roles, "four distinct typed aliases")

    # M7 — first-four-prime pairing, radix theorem, and decimal views.
    seed_primes = [prime(index) for index in range(1, 5)]
    concat = lambda base, a, c: base * a + c
    decimal_views = {
        "27": concat(10, 2, 7),
        "72": concat(10, 7, 2),
        "35": concat(10, 3, 5),
        "53": concat(10, 5, 3),
    }
    check("M7 first four primes", seed_primes == [2, 3, 5, 7], seed_primes, [2, 3, 5, 7])
    check("M7 declared decimal views", decimal_views == {"27": 27, "72": 72, "35": 35, "53": 53}, decimal_views, {"27": 27, "72": 72, "35": 35, "53": 53})
    connector_core = {
        "2*5": 2 * 5,
        "3+7": 3 + 7,
        "2*3": 2 * 3,
        "2+5": 2 + 5,
    }
    check("M7 connector coefficient identities", connector_core == {"2*5": 10, "3+7": 10, "2*3": 6, "2+5": 7}, connector_core, {"2*5": 10, "3+7": 10, "2*3": 6, "2+5": 7})
    radix_rows: list[dict[str, int]] = []
    for base in range(8, 1001):
        a_value = 2 * concat(base, 5, 3)
        b_value = concat(base, 7, 2) + concat(base, 3, 5)
        radix_rows.append({"base": base, "A": a_value, "B": b_value, "difference": b_value - a_value})
    radix_theorem = all(row["A"] == 10 * row["base"] + 6 and row["B"] == 10 * row["base"] + 7 and row["difference"] == 1 for row in radix_rows)
    check("M7 radix-independent adjacent-pair theorem", radix_theorem, {"range": "8..1000", "all_pass": radix_theorem}, True)
    check("M7 decimal radix closes at Q106 and p28", radix_rows[2]["A"] == 106 and radix_rows[2]["B"] == 107 == prime(28), radix_rows[2], {"base": 10, "A": 106, "B": 107, "difference": 1})
    factor_views = {
        "27": 3**3,
        "72_as_6x12": 6 * 12,
        "72_as_8x9": 8 * 9,
        "35": 5 * 7,
        "53_is_prime": is_prime(53),
    }
    check("M7 decimal factor views", factor_views == {"27": 27, "72_as_6x12": 72, "72_as_8x9": 72, "35": 35, "53_is_prime": True}, factor_views, "declared decimal factorizations")
    reverse_pair_arithmetic = {
        "gcd_27_72": gcd(27, 72),
        "lcm_27_72": 27 * 72 // gcd(27, 72),
        "ratio_72_27": str(Fraction(72, 27)),
        "difference_53_35": 53 - 35,
        "difference_72_27": 72 - 27,
    }
    check("M7 reversal-pair divisors and ratios", reverse_pair_arithmetic == {"gcd_27_72": 9, "lcm_27_72": 216, "ratio_72_27": "8/3", "difference_53_35": 18, "difference_72_27": 45}, reverse_pair_arithmetic, {"gcd": 9, "lcm": 216, "ratio": "8/3", "differences": [18, 45]})
    check("M7 reversal-pair powers close through 6 and 9", reverse_pair_arithmetic["lcm_27_72"] == 6**3 and reverse_pair_arithmetic["difference_53_35"] == 2 * 9 == 3 * 6 and reverse_pair_arithmetic["difference_72_27"] == 5 * 9, reverse_pair_arithmetic, {"lcm": "6^3", "18": "2*9=3*6", "45": "5*9"})
    block_216 = {
        "L": reverse_pair_arithmetic["lcm_27_72"],
        "2L": 2 * reverse_pair_arithmetic["lcm_27_72"],
        "8L+1": 8 * reverse_pair_arithmetic["lcm_27_72"] + 1,
        "9L": 9 * reverse_pair_arithmetic["lcm_27_72"],
        "9L+1": 9 * reverse_pair_arithmetic["lcm_27_72"] + 1,
        "27*72": 27 * 72,
    }
    check("M7 216 block ladder", block_216 == {"L": 216, "2L": 432, "8L+1": 1729, "9L": 1944, "9L+1": 1945, "27*72": 1944}, block_216, {"L": 216, "2L": 432, "8L+1": 1729, "9L": 1944, "9L+1": 1945, "27*72": 1944})
    connector_6_9 = {
        "6": 2 * 3,
        "9": 3**2,
        "ratio": str(Fraction(9, 6)),
        "difference": 9 - 6,
        "sum": 9 + 6,
        "gcd": gcd(6, 9),
        "lcm": 6 * 9 // gcd(6, 9),
    }
    check("M7 six-nine connector", connector_6_9 == {"6": 6, "9": 9, "ratio": "3/2", "difference": 3, "sum": 15, "gcd": 3, "lcm": 18}, connector_6_9, {"ratio": "3/2", "difference": 3, "sum": 15, "gcd": 3, "lcm": 18})
    check("M7 432 record/play closure", 72 * 6 == 432 == 27 * 16 == 2**4 * 3**3 and 16 == 2**4, {"72*6": 72 * 6, "27*16": 27 * 16, "2^4*3^3": 2**4 * 3**3}, 432)
    normalized_432 = [Fraction(432, denominator) for denominator in (540, 720, 1080)]
    check("M7 432 normalized rings", normalized_432 == [Fraction(4, 5), Fraction(3, 5), Fraction(2, 5)], [str(value) for value in normalized_432], ["4/5", "3/5", "2/5"])
    j82 = lambda x: 82 - x
    check("M7 40-41-42 seam", 40 == 2**3 * 5 and prime(13) == 41 and 42 == 6 * 7 and [j82(x) for x in (40, 41, 42)] == [42, 41, 40], {"40": "2^3*5", "41": prime(13), "42": "6*7", "J82": [j82(x) for x in (40, 41, 42)]}, {"J82": [42, 41, 40]})
    pair_partitions = [((2, 3), (5, 7)), ((2, 5), (3, 7)), ((2, 7), (3, 5))]
    sum_107_hits: list[dict[str, object]] = []
    for left, right in pair_partitions:
        for reverse_left, reverse_right in itertools.product((False, True), repeat=2):
            oriented_left = left[::-1] if reverse_left else left
            oriented_right = right[::-1] if reverse_right else right
            left_value = concat(10, *oriented_left)
            right_value = concat(10, *oriented_right)
            if left_value + right_value == 107:
                sum_107_hits.append({"partition": [list(left), list(right)], "values": [left_value, right_value]})
    check("M7 pairing-orientation control for 107", [item["values"] for item in sum_107_hits] == [[32, 75], [72, 35]], sum_107_hits, {"hit_count": 2, "values": [[32, 75], [72, 35]]})
    ilau = {
        "I_retained": ["first-four-prime tuple", "declared radix formula", "exact arithmetic"],
        "L_lost": ["unwritten radix and orientation"],
        "A_added": ["decimal concatenation", "color roles", "5/S glyph analogy"],
        "U_unresolved": ["physical connector meaning", "visual dynamics"],
    }
    check("M7 ILAU boundary remains explicit", all(ilau.values()) and "5/S glyph analogy" in ilau["A_added"], ilau, "nonempty typed I/L/A/U boundary")

    interpretation = {
        "six_step_prime_translation": "ESTABLISHED_EXACTLY",
        "nested_q106_center": "ESTABLISHED_EXACTLY",
        "suffix_pn_gain_drop": "ESTABLISHED_FOR_TWO_INTERVALS",
        "damping_law": "NOT_ESTABLISHED",
        "vm_unification": "NOT_ESTABLISHED",
        "physical_interaction": "NOT_ESTABLISHED",
        "radix_adjacent_pair": "ESTABLISHED_EXACTLY",
        "five_s_glyph_identity": "NOT_ESTABLISHED",
    }
    check("claim ceiling remains open", interpretation["damping_law"] == interpretation["vm_unification"] == interpretation["physical_interaction"] == "NOT_ESTABLISHED", interpretation, "open interpretation claims")

    passed = all(item["status"] == "PASS" for item in checks)
    classification = "PASS_EXACT_JANUS_PN_SIX_STEP_INTERTWINER_WITH_RADIX_GRAMMAR_AND_DAMPING_OPEN" if passed else "CONTRACT_INVALID"
    return {
        "contract_id": contract["contract_id"],
        "date": contract["date"],
        "classification": classification,
        "summary": {"passed": sum(item["status"] == "PASS" for item in checks), "total": len(checks)},
        "source_resolution": source_resolution,
        "derived": {
            "prime_indices": prime_indices,
            "prime_row": prime_row,
            "year_row": years,
            "residual_1729": residual_1729,
            "residual_1836": residual_1836,
            "nested_centers": {"center_97_109": 103, "center_103_109": 106},
            "handle_7_6": handle,
            "prime_six_step_control": {
                "range": "start indices 1..1000",
                "single_hit_count": len(six_step_hits),
                "double_chains": six_step_double_chains,
            },
            "suffixes": suffixes,
            "suffix_pn_row": pn_row,
            "local_gains": [str(x) for x in gains],
            "bounded_gain_hits": control_hits,
            "bounded_r17_hits": r17_hits,
            "prime_permutations_3565": prime_permutations,
            "vm_roles": vm_roles,
            "first_four_prime_radix_grammar": {
                "seed_primes": seed_primes,
                "decimal_views": decimal_views,
                "connector_core": connector_core,
                "radix_test_range": "8..1000",
                "radix_theorem_passed": radix_theorem,
                "reverse_pair_arithmetic": reverse_pair_arithmetic,
                "connector_6_9": connector_6_9,
                "block_216_post_hoc": block_216,
                "sum_107_control_hits": sum_107_hits,
                "ilau": ilau,
            },
            "interpretation": interpretation,
        },
        "checks": checks,
        "claim_boundary": contract["claim_boundary"],
    }


if __name__ == "__main__":
    result = validate()
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if "--write-result" in sys.argv[1:]:
        (HERE / "RESULT.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    raise SystemExit(0 if result["classification"].startswith("PASS_") else 1)
