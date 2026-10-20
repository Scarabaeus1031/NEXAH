#!/usr/bin/env python3
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ECOSYSTEM = next(parent for parent in HERE.parents if parent.name == "NEXAH ECOSYSTEM")
SOURCES = {
    "owner_contract": HERE / "OWNER_CONTRACT.json",
    "bead_x40_result": HERE.parent / "RESULT.json",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def primes(count: int):
    found = []
    n = 2
    while len(found) < count:
        if all(n % p for p in found if p * p <= n):
            found.append(n)
        n += 1
    return found


def additive_order(a: int, modulus: int) -> int:
    return modulus // math.gcd(a, modulus)


def main() -> None:
    checks = []

    def need(condition: bool, name: str, observed=None, expected=None) -> None:
        passed = bool(condition)
        checks.append({"name": name, "passed": passed, "observed": observed, "expected": expected})
        if not passed:
            raise AssertionError(name)

    for name, path in SOURCES.items():
        need(path.is_file(), f"source exists: {name}", str(path), "file")

    owner = json.loads(SOURCES["owner_contract"].read_text())
    bead = json.loads(SOURCES["bead_x40_result"].read_text())
    need(owner["authority"] == "HUMAN_OWNER_DECLARED_CANDIDATE_CONTRACT", "Owner authority class retained")
    need(bead["carrier_attachment"]["source"] == "X40=C5×P4×C2", "parent X40 carrier retained")
    need(bead["carrier_attachment"]["global_phase_charts"] == 5, "parent five-chart ambiguity retained")
    need(bead["carrier_attachment"]["fibre_size"] == 4, "parent four-state P4 fibre retained")

    p0, p1 = owner["branches"]["P"]["from"], owner["branches"]["P"]["to"]
    q0, q1 = owner["branches"]["Q"]["from"], owner["branches"]["Q"]["to"]
    need((p0, p1, q0, q1) == (17, 29, 18, 36), "Owner numeric anchors retained", [p0, p1, q0, q1], [17, 29, 18, 36])
    need(primes(10)[-1] == 29, "29 is the tenth prime", primes(10)[-1], 29)
    need(q0 == 3 * 6, "18 equals 3×6", q0, 18)
    need(q1 == 6 * 6, "36 equals 6×6", q1, 36)
    need(q1 == (2 ** 2) * (3 ** 2), "36 equals 2²×3²", q1, 36)
    need(q1 == 2 * q0, "36 is twice 18", q1, 2 * q0)

    dp, dq = p1 - p0, q1 - q0
    need(dp == 12 and dq == 18, "branch increments are 12 and 18", [dp, dq], [12, 18])
    need(dp + dq == 30, "increments close one C30 cycle", dp + dq, 30)
    need(dq % 30 == (-dp) % 30, "increments are opposite in C30", dq % 30, (-dp) % 30)
    need(dp % 6 == 0 and dq % 6 == 0, "increments lie in embedded 6·C5")
    c5_steps = (dp // 6 % 5, dq // 6 % 5)
    need(c5_steps == (2, 3), "C5 steps are +2 and −2", list(c5_steps), [2, 3])
    need(c5_steps[1] == (-c5_steps[0]) % 5, "C5 branch steps counter-rotate")
    need(additive_order(dp, 30) == 5 and additive_order(dq, 30) == 5, "both C30 increments generate five-state orbits")
    need(math.gcd(c5_steps[0], 5) == 1, "+2 is a C5 generator")
    need(math.gcd(c5_steps[1], 5) == 1, "−2 is a C5 generator")

    pairs = [(p0, q0), (p1, q1)]
    mirror_rows = []
    for t, (p_value, q_value) in enumerate(pairs):
        p_address = p_value % 5
        q_signed_state = q_value % 5
        q_display_address = (-q_signed_state) % 5
        need((p_value + q_value) % 5 == 0, f"time {t} P/Q values are additive inverses in C5")
        need(p_address == q_display_address, f"time {t} numeric convention gives same-index mirror beads")
        mirror_rows.append({
            "time": t,
            "P_value": p_value,
            "Q_value": q_value,
            "P_signed_C5_state": p_address,
            "Q_signed_C5_state": q_signed_state,
            "shared_display_index_under_numeric_address_convention": p_address,
        })
    need((mirror_rows[1]["P_signed_C5_state"] - mirror_rows[0]["P_signed_C5_state"]) % 5 == 2, "P display advances +2")
    need((mirror_rows[1]["Q_signed_C5_state"] - mirror_rows[0]["Q_signed_C5_state"]) % 5 == 3, "Q signed state advances −2")

    # d_k(s,p,1)=P[s+k], d_k(s,p,0)=Q[-s+k].  Requiring the displayed
    # address to equal the numeric convention itself selects k=0; without that
    # additional requirement every k keeps the P/Q pair on one shared bead.
    chart_tests = []
    for k in range(5):
        paired = all((p_value + k) % 5 == (-q_value + k) % 5 for p_value, q_value in pairs)
        numeric_address_exact = all(
            (p_value + k) % 5 == p_value % 5 and (-q_value + k) % 5 == (-q_value) % 5
            for p_value, q_value in pairs
        )
        chart_tests.append({"k": k, "same_index_pairs": paired, "numeric_address_exact": numeric_address_exact})
    need(all(row["same_index_pairs"] for row in chart_tests), "mirror pairs alone preserve all five phase charts")
    selected = [row["k"] for row in chart_tests if row["numeric_address_exact"]]
    need(selected == [0], "numeric-address convention conditionally selects k=0", selected, [0])

    period = owner["wobble"]["period"]
    need(period == 4, "Owner wobble period is four", period, 4)
    residues = list(range(period))
    full_tag = {t: t % 4 for t in residues}
    pulse = {t: int(t % 4 == 0) for t in residues}
    need(len(set(full_tag.values())) == 4, "full residue tag represents all four P4 states")
    need(all(full_tag[t] == t for t in residues), "full residue tag gives exact P4 Return")
    pulse_fibres = defaultdict(list)
    for t, tag in pulse.items():
        pulse_fibres[tag].append(t)
    pulse_profile = Counter(len(values) for values in pulse_fibres.values())
    need(pulse_profile == Counter({1: 1, 3: 1}), "binary every-four pulse has 1/3 fibre profile", dict(pulse_profile), {1: 1, 3: 1})
    need(len(set(pulse.values())) == 2, "binary pulse carries only two labels", len(set(pulse.values())), 2)
    need(any(len(values) > 1 for values in pulse_fibres.values()), "binary pulse cannot invert P4")

    anchor_p4 = {"P17": p0 % 4, "P29": p1 % 4, "Q18": q0 % 4, "Q36": q1 % 4}
    need(anchor_p4 == {"P17": 1, "P29": 1, "Q18": 2, "Q36": 0}, "anchor residues mod 4 recorded", anchor_p4)
    need((p1 - p0) % 4 == 0, "P increment preserves numeric P4 residue")
    need((q1 - q0) % 4 == 2, "Q increment shifts numeric P4 residue by two")

    result = {
        "status": "PASS_CONDITIONAL_C30_COUNTERSTEP_WITH_P4_WOBBLE_TYPE_GATE",
        "classification": "OWNER_DECLARED_17_29_18_36_PAIR_FORMS_OPPOSITE_ORDER5_C30_STEPS_AND_CONDITIONAL_P4_TAG",
        "checks": {"passed": len(checks), "total": len(checks)},
        "c30_c5_result": {
            "P_transition": "17→29",
            "Q_transition": "18→36",
            "increments_C30": {"P": 12, "Q": 18},
            "opposite_relation": "18≡−12 mod 30",
            "orders_in_C30": {"12": 5, "18": 5},
            "embedded_C5_steps": {"P": 2, "Q": -2},
            "mirror_rows": mirror_rows,
            "same_index_mirror_compatible": True,
            "counterrotation_compatible": True,
        },
        "phase_chart_gate": {
            "charts_compatible_with_mirror_pairs_alone": 5,
            "conditional_numeric_address_convention": "P(n)=n mod 5; Q(n)=−n mod 5",
            "selected_chart_under_numeric_address_convention": 0,
            "historical_phase_chart": None,
            "chart_tests": chart_tests,
        },
        "wobble_gate": {
            "period": 4,
            "full_phase_tag": {
                "definition": "p=t mod 4",
                "values": full_tag,
                "is_exact_P4_coordinate": True,
                "closes_parent_four_state_bead_fibre": True,
                "residual_bits": 2,
            },
            "pulse_only": {
                "definition": "w=1 iff t mod 4=0",
                "values": pulse,
                "fibre_profile": {str(size): count for size, count in sorted(pulse_profile.items())},
                "is_exact_P4_coordinate": False,
                "closes_parent_four_state_bead_fibre": False,
            },
            "anchor_numeric_residues_mod4": anchor_p4,
            "source_semantics_selected": None,
        },
        "number_facts": {
            "29_prime_index": 10,
            "18": "3×6",
            "36": ["6×6", "2²×3²", "2×18"],
        },
        "maps": {
            "x20_adjacency": None,
            "glb_wobble_to_p4": None,
            "typed_x20_to_q106_intertwiner": None,
            "historical_clockwork_encoding": None,
        },
        "sources": [
            {"name": name, "path": str(path.relative_to(ECOSYSTEM)), "sha256": sha256(path)}
            for name, path in SOURCES.items()
        ],
        "claim_boundary": "Owner-declared finite arithmetic/address audit only. The number pairs are exactly compatible with opposite order-five C30/C5 steps. The full mod-4 phase tag would close P4, but a binary every-four pulse would not; the source semantics remain unselected. Phase k=0 is selected only under the explicit numeric-address convention. No historical encoding, GLB wobble-to-P4 map, X20 adjacency, Q106 intertwiner, physical mechanism, A0 evidence promotion, Study admission or publication authority follows.",
        "checks_detail": checks,
    }
    (HERE / "RESULT.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({
        "status": "PASS",
        "checks": result["checks"],
        "C30_steps": result["c30_c5_result"]["increments_C30"],
        "C5_steps": result["c30_c5_result"]["embedded_C5_steps"],
        "conditional_phase_chart": 0,
        "full_tag_closes_P4": True,
        "pulse_only_closes_P4": False,
    }, indent=2))


if __name__ == "__main__":
    main()
