#!/usr/bin/env python3
"""Verify the source-bound Clockwork p/q pair as an unlabeled X40 C2 display lift."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import struct
from pathlib import Path


HERE = Path(__file__).resolve().parent
ECOSYSTEM = HERE.parents[8]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_glb_json(path: Path) -> dict:
    raw = path.read_bytes()
    magic, version, total = struct.unpack_from("<4sII", raw, 0)
    if magic != b"glTF" or version != 2 or total != len(raw):
        raise ValueError("invalid glTF 2.0 binary header")
    length, kind = struct.unpack_from("<II", raw, 12)
    if kind != 0x4E4F534A:
        raise ValueError("first GLB chunk is not JSON")
    return json.loads(raw[20:20 + length].decode("utf-8").rstrip(" \t\r\n\x00"))


def main() -> None:
    contract = json.loads((HERE / "CONTRACT.json").read_text(encoding="utf-8"))
    checks: list[dict[str, object]] = []

    def check(name: str, passed: bool, observed: object, expected: object) -> None:
        checks.append({"name": name, "passed": bool(passed), "observed": observed, "expected": expected})

    check("extends the existing C2 factor audit", contract["identity"]["extends"] == "A0-BL-023:TRIPLE19_X40_C2_ORIENTATION_FACTOR_AUDIT:V1", contract["identity"]["extends"], "existing factor audit")
    check("creates no identity", contract["identity"]["creates"] == [], contract["identity"]["creates"], [])
    check("reuses NN readout module and crosswalk", contract["identity"]["reuses"] == ["MOD:READOUT_RECONSTRUCTION", "NN:MRB_ACR_NCS_Q106_RETURN_CROSSWALK"], contract["identity"]["reuses"], ["MOD:READOUT_RECONSTRUCTION", "NN:MRB_ACR_NCS_Q106_RETURN_CROSSWALK"])
    check("four frozen sources", len(contract["frozen_sources"]) == 4, len(contract["frozen_sources"]), 4)

    source_paths: dict[str, Path] = {}
    for source in contract["frozen_sources"]:
        path = (ECOSYSTEM / source["path"]).resolve()
        source_paths[source["source_id"]] = path
        check(f"source inside ecosystem: {source['source_id']}", path == ECOSYSTEM or ECOSYSTEM in path.parents, str(path), str(ECOSYSTEM))
        check(f"source exists: {source['source_id']}", path.is_file(), path.is_file(), True)
        actual = sha256(path) if path.is_file() else None
        check(f"source hash: {source['source_id']}", actual == source["sha256"], actual, source["sha256"])

    parent = json.loads(source_paths["SRC:CLOCKWORK_C2:PARENT_FACTOR_RESULT"].read_text(encoding="utf-8"))
    check("parent C2 factor passed", parent["status"] == "PASS_SHARED_C2_ORIENTATION_FACTOR_WITH_QUOTIENT_LOSS", parent["status"], "PASS_SHARED_C2_ORIENTATION_FACTOR_WITH_QUOTIENT_LOSS")
    check("parent factor is C2 orientation", parent["shared_factor"]["factor"] == "C2_orientation", parent["shared_factor"]["factor"], "C2_orientation")
    check("parent quotient has twenty two-state fibres", parent["quotient"]["fibres"] == 20 and parent["quotient"]["fibre_size"] == 2, [parent["quotient"]["fibres"], parent["quotient"]["fibre_size"]], [20, 2])
    check("parent orientation does not factor through X20", parent["quotient"]["orientation_factors_through_x20"] is False, parent["quotient"]["orientation_factors_through_x20"], False)

    glb = read_glb_json(source_paths["SRC:CLOCKWORK_C2:V7_REFERENCE_GLB"])
    extras = glb.get("extras", {})
    pair = extras.get("transfer_pair", {})
    gamma = extras.get("gamma_coupling", {})
    check("v7 source version", extras.get("version") == "v7-pq-conjugate-orbit", extras.get("version"), "v7-pq-conjugate-orbit")
    check("p/q mirror relation declared", pair.get("relation") == "q = mirror(p)", pair.get("relation"), "q = mirror(p)")
    check("opposite p/q tilt", pair.get("p", {}).get("tilt_deg") == -pair.get("q", {}).get("tilt_deg"), [pair.get("p", {}).get("tilt_deg"), pair.get("q", {}).get("tilt_deg")], [68, -68])
    check("mirrored p/q azimuth", pair.get("p", {}).get("azimuth_deg") + pair.get("q", {}).get("azimuth_deg") == 180, [pair.get("p", {}).get("azimuth_deg"), pair.get("q", {}).get("azimuth_deg")], [42, 138])
    check("opposite p/q turns", pair.get("p", {}).get("turns_per_48s") == -pair.get("q", {}).get("turns_per_48s"), [pair.get("p", {}).get("turns_per_48s"), pair.get("q", {}).get("turns_per_48s")], [1, -1])
    check("gamma remains visual grammar", gamma.get("status") == "VISUAL_COUPLING_GRAMMAR_ONLY", gamma.get("status"), "VISUAL_COUPLING_GRAMMAR_ONLY")
    check("sum and difference modes declared", gamma.get("equal_sum") == "(p+q)/2" and gamma.get("equal_difference") == "(p-q)/2", [gamma.get("equal_sum"), gamma.get("equal_difference")], ["(p+q)/2", "(p-q)/2"])

    roles = contract["x40_carrier"]["P4"]
    x40 = [(s, role, e) for s in range(5) for role in roles for e in (0, 1)]
    x20 = [(s, role) for s in range(5) for role in roles]
    jc = lambda x: (x[0], x[1], 1 - x[2])
    jd = lambda x: ((-x[0]) % 5, x[1], 1 - x[2])
    q = lambda x: (x[0], x[1])
    swap = {"p": "q", "q": "p"}

    labelings = [
        {0: "p", 1: "q"},
        {0: "q", 1: "p"},
    ]
    labeling_results = []
    for index, labeling in enumerate(labelings, 1):
        lift = lambda x, labeling=labeling: (q(x), labeling[x[2]])
        images = {lift(x) for x in x40}
        bijective = len(images) == 40
        projects = all(lift(x)[0] == q(x) for x in x40)
        jc_equivariant = all(lift(jc(x)) == (q(jc(x)), swap[lift(x)[1]]) for x in x40)
        jd_equivariant = all(lift(jd(x)) == (q(jd(x)), swap[lift(x)[1]]) for x in x40)
        labeling_results.append({
            "labeling": index,
            "orientation_0": labeling[0],
            "orientation_1": labeling[1],
            "bijective": bijective,
            "projection_compatible": projects,
            "J_c_sheet_swap": jc_equivariant,
            "J_d_sheet_swap": jd_equivariant,
        })

    check("X40 and display lift each have forty states", len(x40) == 40 and len(x20) * 2 == 40, [len(x40), len(x20) * 2], [40, 40])
    check("both global p/q labelings are bijective", all(row["bijective"] for row in labeling_results), [row["bijective"] for row in labeling_results], [True, True])
    check("both labelings commute with projection", all(row["projection_compatible"] for row in labeling_results), [row["projection_compatible"] for row in labeling_results], [True, True])
    check("J_c induces p/q sheet swap under both labelings", all(row["J_c_sheet_swap"] for row in labeling_results), [row["J_c_sheet_swap"] for row in labeling_results], [True, True])
    check("J_d induces p/q sheet swap under both labelings", all(row["J_d_sheet_swap"] for row in labeling_results), [row["J_d_sheet_swap"] for row in labeling_results], [True, True])

    builder_text = source_paths["SRC:CLOCKWORK_C2:V7_BUILDER"].read_text(encoding="utf-8")
    explicit_bit_assignment = any(
        pattern.search(builder_text)
        for pattern in (
            re.compile(r"\borientation_0\b"),
            re.compile(r"\borientation_bit\b"),
            re.compile(r"(?<![A-Za-z0-9_])e\s*={2,3}\s*0(?![A-Za-z0-9_])"),
        )
    )
    check("source does not silently select an orientation-bit labeling", explicit_bit_assignment is False, explicit_bit_assignment, False)
    check("exactly two admissible global labelings remain", len(labeling_results) == 2 and all(all(row[key] for key in ("bijective", "projection_compatible", "J_c_sheet_swap", "J_d_sheet_swap")) for row in labeling_results), len(labeling_results), 2)
    check("historical Janus selection remains null", parent["shared_factor"]["historical_janus_selection"] is None, parent["shared_factor"]["historical_janus_selection"], None)
    check("full carrier intertwiner remains null", parent["maps"]["full_carrier_intertwiner"] is None, parent["maps"]["full_carrier_intertwiner"], None)
    check("Triple19-to-X20 map remains null", parent["maps"]["triple19_to_x20"] is None, parent["maps"]["triple19_to_x20"], None)

    with (HERE / "PQ_C2_LABELINGS.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(labeling_results[0]))
        writer.writeheader()
        writer.writerows(labeling_results)

    with (HERE / "X40_PQ_DISPLAY_LIFT.csv").open("w", encoding="utf-8", newline="") as handle:
        fields = ["x40_state", "x20_base", "orientation_bit", "sheet_labeling_1", "sheet_labeling_2", "J_c_target", "J_d_target"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for state in x40:
            base = q(state)
            writer.writerow({
                "x40_state": f"X40:{state[0]}:{state[1]}:{state[2]}",
                "x20_base": f"X20:{base[0]}:{base[1]}",
                "orientation_bit": state[2],
                "sheet_labeling_1": labelings[0][state[2]],
                "sheet_labeling_2": labelings[1][state[2]],
                "J_c_target": f"X40:{jc(state)[0]}:{jc(state)[1]}:{jc(state)[2]}",
                "J_d_target": f"X40:{jd(state)[0]}:{jd(state)[1]}:{jd(state)[2]}",
            })

    passed = sum(1 for item in checks if item["passed"])
    ok = passed == len(checks)
    result = {
        "status": "PASS_UNLABELED_C2_DISPLAY_LIFT" if ok else "CONTRACT_INVALID",
        "classification": "CLOCKWORK_PQ_REALIZES_TWO_SHEET_DISPLAY_LIFT_WITH_GLOBAL_LABEL_AMBIGUITY" if ok else "CONTRACT_INVALID",
        "checks": {"passed": passed, "total": len(checks)},
        "clockwork_source": {
            "version": extras.get("version"),
            "relation": pair.get("relation"),
            "p": pair.get("p"),
            "q": pair.get("q"),
            "gamma_status": gamma.get("status")
        },
        "display_lift": {
            "carrier": "L_PQ=X20 x {p,q}",
            "states": 40,
            "base_states": 20,
            "fibre_size": 2,
            "admissible_global_labelings": 2,
            "canonical_orientation_bit_to_pq_labeling": None,
            "deck_flip": "p<->q",
            "compatible_x40_operators": ["J_c", "J_d"]
        },
        "gamma_basis": {
            "symmetric": "(p+q)/2 is invariant under p<->q",
            "antisymmetric": "(p-q)/2 changes sign under p<->q",
            "status": "DISPLAY_BASIS_ONLY_NOT_NUMERIC_NCS_OPERATOR"
        },
        "maps": {
            "clockwork_glb_nodes_to_x20": None,
            "x20_adjacency": None,
            "triple19_to_x20": None,
            "typed_x20_to_q106_intertwiner": None,
            "full_carrier_intertwiner": None,
            "historical_janus_selection": None
        },
        "ncs_contribution": "Clockwork v7 supplies a source-bound visual two-sheet lift for the C2 coordinate already proved to be lost by X40->X20; it supplies no X20 graph and does not choose either global bit labeling or Janus law.",
        "claim_boundary": contract["authority_boundary"],
        "checks_detail": checks
    }
    (HERE / "RESULT.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "classification": result["classification"],
        "checks": f"{passed}/{len(checks)}",
        "admissible_global_labelings": 2,
        "canonical_labeling": None,
        "x20_adjacency": None
    }, indent=2))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
