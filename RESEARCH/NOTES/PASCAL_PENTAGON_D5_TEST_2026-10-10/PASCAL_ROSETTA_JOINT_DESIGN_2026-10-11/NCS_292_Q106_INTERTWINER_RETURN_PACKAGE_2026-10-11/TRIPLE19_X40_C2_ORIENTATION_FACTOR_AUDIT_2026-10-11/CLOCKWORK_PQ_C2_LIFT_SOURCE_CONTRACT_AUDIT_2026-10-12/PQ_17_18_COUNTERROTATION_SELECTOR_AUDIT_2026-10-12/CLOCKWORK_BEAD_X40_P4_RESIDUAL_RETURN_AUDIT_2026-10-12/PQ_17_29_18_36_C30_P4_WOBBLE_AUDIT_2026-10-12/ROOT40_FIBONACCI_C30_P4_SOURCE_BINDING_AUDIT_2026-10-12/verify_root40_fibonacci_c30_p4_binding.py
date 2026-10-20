#!/usr/bin/env python3
import hashlib
import itertools
import json
import math
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ECOSYSTEM = next(parent for parent in HERE.parents if parent.name == "NEXAH ECOSYSTEM")
NCS_PACKAGE = HERE.parents[5]
ROOT7 = ECOSYSTEM / "30 SCIENCE LAB/NEXAH-Science-Lab/SCIENCE_LAB/CASE_STUDIES/NEXAH_ROOT7_EULER_MIRROR_CONCORDANCE_INTAKE_2026-09-28"
A052 = ECOSYSTEM / "30 SCIENCE LAB/NEXAH-Science-Lab/SCIENCE_LAB/CASE_STUDIES/A0_BL_052_PASCAL_QUATERNION_FOUR_CHANNEL_RETURN_2026-10-11"
A053 = ECOSYSTEM / "30 SCIENCE LAB/NEXAH-Science-Lab/SCIENCE_LAB/CASE_STUDIES/A0_BL_053_PASCAL_QUATERNION_SYMBOLIC_PROOF_REVIEW_2026-10-11"
PRIMEGRID = ECOSYSTEM / "30 SCIENCE LAB/NEXAH-Science-Lab/SCIENCE_LAB/CASE_STUDIES/NEXAH_PRIMEGRID_BLOCK02B_TRINARY_PASCAL_ANTIPODE_2026-10-07"
CON_DAO = ECOSYSTEM / "30 SCIENCE LAB/NEXAH-Science-Lab/SCIENCE_LAB/CASE_STUDIES/NEXAH_CON_DAO_JANUS_BREATH_SEQUENCER_2026-10-06"
SOURCES = {
    "wobble_result": HERE.parent / "RESULT.json",
    "ncs_contract": NCS_PACKAGE / "CONTRACT.json",
    "ncs_readme": NCS_PACKAGE / "README.md",
    "root40_contract": ROOT7 / "11_PRIME_LENS_FOLLOWON_TEST_CONTRACT.md",
    "root40_result": ROOT7 / "prime_lens_followon_results.json",
    "root40_addendum": ROOT7 / "12_PRIME_LENS_FOLLOWON_ADDENDUM.md",
    "pascal_quaternion_result": A052 / "artifacts/PRIMARY_RESULT.json",
    "pascal_quaternion_assessment": A052 / "02_RESULT_ASSESSMENT.md",
    "pascal_quaternion_all_n_assessment": A053 / "03_RESULT_ASSESSMENT.md",
    "triple19_antipode_binding": PRIMEGRID / "TRIPLE19_ANTIPODE_PAIR_BRIDGE_BINDING.json",
    "con_dao_model": CON_DAO / "breath-model.js",
    "con_dao_readme": CON_DAO / "README.md",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def find_pair_period(seed, modulus, limit=1000):
    state = tuple(value % modulus for value in seed)
    start = state
    orbit = []
    for _ in range(limit):
        orbit.append(state)
        state = (state[1], (state[0] + state[1]) % modulus)
        if state == start:
            return orbit
    raise RuntimeError("period not found")


def main() -> None:
    checks = []

    def need(condition: bool, name: str, observed=None, expected=None) -> None:
        passed = bool(condition)
        checks.append({"name": name, "passed": passed, "observed": observed, "expected": expected})
        if not passed:
            raise AssertionError(name)

    for name, path in SOURCES.items():
        need(path.is_file(), f"source exists: {name}", str(path), "file")

    wobble = json.loads(SOURCES["wobble_result"].read_text())
    ncs = json.loads(SOURCES["ncs_contract"].read_text())
    root40 = json.loads(SOURCES["root40_result"].read_text())
    ncs_readme = SOURCES["ncs_readme"].read_text()
    root40_contract = SOURCES["root40_contract"].read_text()
    root40_addendum = SOURCES["root40_addendum"].read_text()
    pascal_quaternion = json.loads(SOURCES["pascal_quaternion_result"].read_text())
    pascal_assessment = SOURCES["pascal_quaternion_assessment"].read_text()
    pascal_all_n = SOURCES["pascal_quaternion_all_n_assessment"].read_text()
    triple19 = json.loads(SOURCES["triple19_antipode_binding"].read_text())
    con_dao_model = SOURCES["con_dao_model"].read_text()
    con_dao_readme = SOURCES["con_dao_readme"].read_text()

    need(root40["passed"] is True, "existing Root-40 follow-on result passes")
    need(root40["passed_count"] == 15 and root40["check_count"] == 15, "existing Root-40 result passes 15/15")
    need(root40["classification"] == "EXISTING_VIEWS_CONNECTED_NO_NEW_RECURRENCE", "existing bounded classification retained")
    need(root40["scientific_hash"] == "cc7d402a48416df4ad08875245c92384c625d66247abc8ce00b4b06a4ec523ee", "existing scientific hash retained")
    need("Root-40" in root40_contract and "new prime law" in root40_contract, "Root-40 contract and claim ceiling retained")
    need("No infinite shell recurrence" in root40_addendum, "finite-source boundary retained")

    by_id = {item["id"]: item for item in root40["checks"]}
    need(by_id["quaternion_norm_is_40"]["observed"] == 40, "source-bound quaternion norm is 40")
    need(by_id["root40_euclidean_view"]["observed"] == 40, "source-bound Euclidean Root-40 view closes")
    need(by_id["root40_hyperbolic_view"]["observed"] == 40, "source-bound hyperbolic Root-40 view closes")
    need(by_id["binding_fibonacci_return"]["observed"] == [3, 1, 4, 5, 9, 14, 23, 37, 60, 97], "source-bound additive recurrence retained")
    need(by_id["boundary_peer_not_recurrence_successor"]["observed"] == {"boundary_peer": 101, "recurrence_successor": 157}, "97→101 remains a cut, not recurrence continuation")
    need(by_id["mirror_exact_return"]["observed"] == [1836, 1729], "whole/difference exact Return retained")

    need(pascal_quaternion["status"] == "PASS" and pascal_quaternion["classification"] == "EXACT_FOUR_CHANNEL_CONNECTOR_PASS", "existing Pascal-quaternion four-channel connector passes")
    need(pascal_quaternion["tests"]["T8_Q_DEGREE_SEPARATION"]["quaternion_slots"] == ["scalar", "i", "j", "k"], "existing connector fixes scalar/i/j/k slot semantics")
    need(pascal_quaternion["tests"]["T3_C3_EQUIVARIANCE"]["coordinate_action"] == "(a,b,c)->(c,a,b)", "existing connector fixes exact C3 coordinate action")
    need(pascal_quaternion["tests"]["T6_QUATERNION_RETURN"]["return"] == "Ad(u^-1) o Ad(u) = id", "existing connector has exact quaternion Return")
    need("Phi(a,b,c) = (a+b+c)1 + ai + bj + ck" in pascal_assessment, "existing finite connector formula retained")
    need("CORE CONNECTOR THEOREM PROVED FOR ALL N>=0" in pascal_all_n, "existing all-N symbolic generalization retained")

    address_bus = ncs["layered_test_contract"]["address_bus"]
    need(address_bus["map"] == "pi6:C30->C6, pi6(k)=k mod 6", "NCS C30→C6 address bus retained")
    need("29->0" in address_bus["expected"], "NCS phase successor 29→0 retained")
    need(wobble["c30_c5_result"]["embedded_C5_steps"] == {"P": 2, "Q": -2}, "Owner counter-step audit supplies C5 +2/-2")
    need(wobble["number_facts"]["29_prime_index"] == 10, "29=P10 retained")
    need(wobble["number_facts"]["36"] == ["6×6", "2²×3²", "2×18"], "36 decompositions retained")

    recurrence_orbit_mod4 = find_pair_period((3, 1), 4)
    expected_orbit = [(3, 1), (1, 0), (0, 1), (1, 1), (1, 2), (2, 3)]
    need(recurrence_orbit_mod4 == expected_orbit, "(3,1) recurrence has exact six-state pair orbit mod 4", recurrence_orbit_mod4, expected_orbit)
    need(len(set(recurrence_orbit_mod4)) == 6, "all six Fibonacci pair states are distinct")
    need(math.lcm(5, len(recurrence_orbit_mod4)) == 30, "C5 counter-step and Fibonacci C6 orbit close at C30")
    joint_states = {(a, b) for a in range(5) for b in range(6)}
    need(len(joint_states) == 30, "C5×C6 joint phase has thirty states")
    need(math.gcd(5, 6) == 1, "C5 and C6 periods are coprime")

    slots = ["1", "i", "j", "k"]
    coefficients = [2, 2, 4, 4]
    roles = ["carrier", "frame_cut", "transform_view", "return_record"]
    need(sum(value * value for value in coefficients) == 40, "four labelled quaternion slots reproduce norm 40")
    need(Counter(coefficients) == Counter({2: 2, 4: 2}), "coefficient values form two doublets")
    need(len(slots) == len(roles) == 4, "quaternion slots and P4 roles have equal cardinality four")
    role_bijections = list(itertools.permutations(roles))
    need(len(role_bijections) == 24, "four slots admit 24 role bijections")
    need("`P4` is the four-role set `carrier / frame_cut /" in ncs_readme, "NCS source types P4 as four roles")
    need("P4" not in SOURCES["root40_result"].read_text(), "Root-40 result declares no P4 map")
    need("P4" not in root40_contract, "Root-40 contract declares no P4 map")

    norm40_quaternions = []
    bound = int(math.isqrt(40))
    for q in itertools.product(range(-bound, bound + 1), repeat=4):
        if sum(value * value for value in q) == 40:
            norm40_quaternions.append(q)
    need(len(norm40_quaternions) == 144, "norm 40 has 144 ordered signed integer quaternion records", len(norm40_quaternions), 144)
    need(tuple(coefficients) in norm40_quaternions, "displayed quaternion is one norm-40 record")
    need(len(norm40_quaternions) > 1, "norm 40 does not identify one quaternion record")

    pascal_coordinates = coefficients[1:]
    pascal_required_scalar = sum(pascal_coordinates)
    need(pascal_required_scalar == 10, "Pascal Phi image requires scalar depth ten for Root-40 imaginary coordinates")
    need(coefficients[0] != pascal_required_scalar, "displayed Root-40 quaternion is outside the Pascal Phi image")

    need(triple19["relation"]["operator"] == "A(r,c_r,sigma)=(6-r,c_r,-sigma)", "existing Triple-19 antipode operator retained")
    need(triple19["relation"]["intertwiner"] is None, "Triple-19 full-carrier intertwiner remains null")
    need('model_id: "NEXAH:CON_DAO_BREATH:V1"' in con_dao_model, "existing CON-DAO carrier identity retained")
    need('"8+4": { label: "Octave + Four Axes"' in con_dao_model, "CON-DAO 8+4 lens retained")
    need("These are views of one carrier, not proofs that the groupings share a generator." in con_dao_readme, "CON-DAO grouping non-identity boundary retained")

    full_tag = wobble["wobble_gate"]["full_phase_tag"]
    pulse = wobble["wobble_gate"]["pulse_only"]
    need(full_tag["is_exact_P4_coordinate"] is True, "full mod-four tag carries four enumerable addresses")
    need(pulse["is_exact_P4_coordinate"] is False, "binary every-four pulse remains insufficient")

    result = {
        "status": "PASS_EXISTING_PASCAL_QUATERNION_CONNECTOR_REUSED_ROOT40_OUTSIDE_IMAGE_NCS_P4_ADAPTER_NULL",
        "classification": "C30_SCHEDULE_CLOSES_EXISTING_PASCAL_FOUR_SLOT_SEMANTICS_REUSED_WITH_TYPED_NON_IDENTITY",
        "checks": {"passed": len(checks), "total": len(checks)},
        "source_closure": {
            "root40_followon": "PASS_15_OF_15_EXISTING_VIEWS_CONNECTED_NO_NEW_RECURRENCE",
            "root40_scientific_hash": root40["scientific_hash"],
            "ncs_address_bus": "pi6:C30→C6",
            "ncs_phase_successor": "29→0",
            "owner_P_endpoint": {"value": 29, "prime_index": 10},
            "owner_Q_endpoint": {"value": 36, "forms": ["6×6", "2²×3²", "2×18"]},
        },
        "c30_schedule": {
            "c5_counter_steps": {"P": 2, "Q": -2},
            "fibonacci_pair_orbit_mod4": [list(state) for state in recurrence_orbit_mod4],
            "fibonacci_pair_period": 6,
            "joint_period": 30,
            "interpretation": "C5 counter-rotation schedule × C6 Fibonacci pair-state schedule; no state transport to X20/X40",
        },
        "root40_p4_gate": {
            "quaternion_slots": slots,
            "coefficients": coefficients,
            "norm": 40,
            "ordered_signed_integer_norm40_records": 144,
            "p4_roles": roles,
            "possible_slot_to_role_bijections": 24,
            "canonical_slot_to_role_map": None,
            "coefficient_value_classes": {"2": 2, "4": 2},
            "value_only_closes_p4": False,
            "labelled_slots_can_carry_chosen_p4_enumeration": True,
            "source_selects_enumeration": False,
        },
        "existing_pascal_quaternion_connector": {
            "status": "CLOSED_OWNER_ACCEPTED_EXACT_FOUR_CHANNEL_CONNECTOR_PASS",
            "formula": "Phi(a,b,c)=(a+b+c)1+ai+bj+ck",
            "slot_semantics": {"scalar": "depth=a+b+c", "i": "a", "j": "b", "k": "c"},
            "c3_action": "Ad_u: i→j→k→i with u=(1+i+j+k)/2",
            "inverse_return": "Ad(u^-1) o Ad(u)=id",
            "scope": "all N>=0; faithful restricted carrier-action wording requires N>=1",
        },
        "root40_pascal_connector_test": {
            "root40_quaternion": "2+2i+4j+4k",
            "imaginary_coordinates": [2, 4, 4],
            "pascal_required_scalar": pascal_required_scalar,
            "observed_scalar": coefficients[0],
            "in_pascal_phi_image": False,
            "meaning": "Root-40 is a valid four-slot quaternion record but not a state of the proved Pascal Phi connector",
        },
        "existing_operator_controls": {
            "triple19_antipode": "A(r,c_r,sigma)=(6-r,c_r,-sigma); A^2=id; full-carrier intertwiner null",
            "con_dao": "13-state Janus carrier with J^2=id and fixed STILL; 8+4 is a grouping lens, not a shared generator",
        },
        "wobble_result": {
            "full_four_phase_tag_can_carry_chosen_role_enumeration": True,
            "binary_every_four_pulse_can_carry_p4": False,
            "canonical_p4_role_assignment": None,
            "glb_wobble_to_p4": None,
        },
        "maps": {
            "fibonacci_to_x20_or_x40": None,
            "root40_slots_to_p4_roles": None,
            "x20_adjacency": None,
            "typed_x20_to_q106_intertwiner": None,
        },
        "sources": [
            {"name": name, "path": str(path.relative_to(ECOSYSTEM)), "sha256": sha256(path)}
            for name, path in SOURCES.items()
        ],
        "claim_boundary": "Source-bound arithmetic, connector reuse and typed non-identity only. The existing Pascal-quaternion connector already fixes scalar/i/j/k as depth/a/b/c and exact C3 Return, so no new four-slot discovery or 24-way Pascal slot search is claimed. Root-40's displayed quaternion is outside that connector image and its value 40 does not identify X40. The remaining null is specifically the adapter from Pascal slot semantics or Root-40 slots into the NCS P4 roles carrier/frame_cut/transform_view/return_record. Fibonacci closes a compatible C30 schedule but supplies no typed transport into X20/X40. Triple-19 and CON-DAO remain distinct exact operator controls. No physical mechanism, new identity, A0 evidence promotion, Study admission or publication authority follows.",
        "checks_detail": checks,
    }
    (HERE / "RESULT.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({
        "status": "PASS_CORRECTED_EXISTING_CONNECTOR_REUSED",
        "checks": result["checks"],
        "joint_period": 30,
        "norm40_integer_quaternions": 144,
        "p4_role_bijections": 24,
        "pascal_slot_semantics": "scalar=depth, i=a, j=b, k=c",
        "root40_in_pascal_phi_image": False,
        "canonical_ncs_p4_role_adapter": None,
    }, indent=2))


if __name__ == "__main__":
    main()
