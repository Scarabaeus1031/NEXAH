#!/usr/bin/env python3
import csv
import hashlib
import json
import struct
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ECOSYSTEM = next(parent for parent in HERE.parents if parent.name == "NEXAH ECOSYSTEM")
NCS_PACKAGE = HERE.parents[3]

SOURCES = {
    "ncs_contract": NCS_PACKAGE / "CONTRACT.json",
    "factor_result": HERE.parents[2] / "RESULT.json",
    "clockwork_lift_result": HERE.parents[1] / "RESULT.json",
    "selector_result": HERE.parent / "RESULT.json",
    "clockwork_builder": ECOSYSTEM / "30 SCIENCE LAB/NEXAH-Science-Lab/SCIENCE_LAB/CASE_STUDIES/NEXAH_DESKTOP_GOLD_CUSTODY_AND_NAVIGATOR_INTAKE_2026-10-07/sources/clockwork/generators/build_pq_conjugate_orbit_glb.mjs",
    "clockwork_glb": ECOSYSTEM / "30 SCIENCE LAB/NEXAH-Science-Lab/SCIENCE_LAB/CASE_STUDIES/NEXAH_DESKTOP_GOLD_CUSTODY_AND_NAVIGATOR_INTAKE_2026-10-07/sources/clockwork/reference/nexah_pq_conjugate_orbit_v7.glb",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_glb_json(path: Path) -> dict:
    data = path.read_bytes()
    if data[:4] != b"glTF" or struct.unpack_from("<I", data, 4)[0] != 2:
        raise ValueError("not a GLB v2 file")
    json_length = struct.unpack_from("<I", data, 12)[0]
    if data[16:20] != b"JSON":
        raise ValueError("first GLB chunk is not JSON")
    return json.loads(data[20:20 + json_length].decode("utf-8"))


def main() -> None:
    checks = []

    def need(condition: bool, name: str, observed=None, expected=None) -> None:
        passed = bool(condition)
        checks.append({"name": name, "passed": passed, "observed": observed, "expected": expected})
        if not passed:
            raise AssertionError(name)

    for name, path in SOURCES.items():
        need(path.is_file(), f"source exists: {name}", str(path), "file")

    contract = json.loads(SOURCES["ncs_contract"].read_text())
    factor = json.loads(SOURCES["factor_result"].read_text())
    lift = json.loads(SOURCES["clockwork_lift_result"].read_text())
    selector = json.loads(SOURCES["selector_result"].read_text())
    glb = read_glb_json(SOURCES["clockwork_glb"])

    need(contract["declared_carrier"]["states"] == "X40 = C5 x P4 x C2_J", "declared X40 carrier retained")
    need(contract["declared_carrier"]["rotation"] == "r(s,p,e)=(s+1 mod 5,p,e)", "declared X40 rotation retained")
    need(factor["shared_factor"]["compatible_x40_operators"] == ["J_c", "J_d"], "parent C2 audit leaves both Janus laws open")
    need(selector["candidate_contract"]["selected_labeling"] == {"e=1": "P / 17 / +1 turn", "e=0": "Q / 18 / -1 turn"}, "Owner-declared P/Q bit selector retained")

    names = [node.get("name", "") for node in glb["nodes"]]
    p_names = sorted(name for name in names if name.startswith("TRANSFER_ORBIT_BEAD_"))
    q_names = sorted(name for name in names if name.startswith("Q_CONJUGATE_ORBIT_BEAD_"))
    expected_p = [f"TRANSFER_ORBIT_BEAD_{i:02d}" for i in range(1, 6)]
    expected_q = [f"Q_CONJUGATE_ORBIT_BEAD_{i:02d}" for i in range(1, 6)]
    need(p_names == expected_p, "five indexed P beads recovered from GLB", p_names, expected_p)
    need(q_names == expected_q, "five indexed Q beads recovered from GLB", q_names, expected_q)

    pair = glb["extras"]["transfer_pair"]
    need(pair["relation"] == "q = mirror(p)", "same-index mirror relation retained")
    need(pair["p"]["turns_per_48s"] == 1 and pair["q"]["turns_per_48s"] == -1, "P/Q counter-rotation retained")

    x40 = [(s, p, e) for s in range(5) for p in range(4) for e in range(2)]
    x20 = [(s, p) for s in range(5) for p in range(4)]
    need(len(x40) == 40 and len(set(x40)) == 40, "X40 has forty states")
    need(len(x20) == 20 and len(set(x20)) == 20, "X20 has twenty states")

    def bead(k, state):
        s, _p, e = state
        index = ((s + k) if e == 1 else (-s + k)) % 5
        return (index, "P" if e == 1 else "Q")

    def tau(bead_state):
        i, sheet = bead_state
        return (((i + 1) if sheet == "P" else (i - 1)) % 5, sheet)

    def mirror(bead_state):
        i, sheet = bead_state
        return (i, "Q" if sheet == "P" else "P")

    def rotation(state):
        s, p, e = state
        return ((s + 1) % 5, p, e)

    def jc(state):
        s, p, e = state
        return (s, p, 1 - e)

    def jd(state):
        s, p, e = state
        return ((-s) % 5, p, 1 - e)

    chart_rows = []
    chart_summaries = []
    for k in range(5):
        equivariant = all(bead(k, rotation(x)) == tau(bead(k, x)) for x in x40)
        fibres = defaultdict(list)
        for state in x40:
            fibres[bead(k, state)].append(state)
        profile = Counter(len(values) for values in fibres.values())
        exact_return = all((s, p, e) in fibres[bead(k, (s, p, e))] for s, p, e in x40)
        jd_match = all(bead(k, jd(x)) == mirror(bead(k, x)) for x in x40)
        jc_match_count = sum(bead(k, jc(x)) == mirror(bead(k, x)) for x in x40)
        need(equivariant, f"chart {k} intertwines X40 rotation with counter-rotation")
        need(profile == Counter({4: 10}), f"chart {k} has ten four-state P4 fibres", dict(profile), {4: 10})
        need(exact_return, f"chart {k} returns exactly with P4 residual")
        need(jd_match, f"chart {k} same-index mirror realizes Jd")
        need(jc_match_count == 8, f"chart {k} Jc matches only the s=0 orbit", jc_match_count, 8)
        chart_summaries.append({
            "phase_offset_k": k,
            "rotation_equivariant": equivariant,
            "fibre_profile": {"4": 10},
            "jd_matches_all_40": jd_match,
            "jc_matches": jc_match_count,
        })
        for s, p, e in x40:
            i, sheet = bead(k, (s, p, e))
            chart_rows.append({
                "phase_offset_k": k,
                "x40_state": f"X40:{s}:{p}:{e}",
                "x20_state": f"X20:{s}:{p}",
                "sheet": sheet,
                "glb_bead": expected_p[i] if sheet == "P" else expected_q[i],
                "p4_residual": p,
            })

    need(len(chart_summaries) == 5, "five global C5 phase charts remain")
    need(all(row["jd_matches_all_40"] for row in chart_summaries), "Jd selected on displayed quotient in every phase chart")
    need(all(row["jc_matches"] < 40 for row in chart_summaries), "Jc rejected on displayed quotient in every phase chart")

    # Commuting square after forgetting the sheet and the orientation bit.
    for k in range(5):
        need(all(bead(k, x)[0] == ((x[0] + k) % 5 if x[2] == 1 else (-x[0] + k) % 5) for x in x40), f"chart {k} display address is explicit")

    with (HERE / "X40_TO_CLOCKWORK_BEAD_CHARTS.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(chart_rows[0]))
        writer.writeheader()
        writer.writerows(chart_rows)

    result = {
        "status": "PASS_CONDITIONAL_DIHEDRAL_BEAD_QUOTIENT_WITH_P4_RESIDUAL_RETURN",
        "classification": "CLOCKWORK_BEADS_REALIZE_C5_COUNTERROTATING_C2_QUOTIENT_OF_X40_WITH_FIVE_PHASE_CHARTS_AND_FOUR_STATE_P4_FIBRES",
        "checks": {"passed": len(checks), "total": len(checks)},
        "carrier_attachment": {
            "source": "X40=C5×P4×C2",
            "display": "B10=C5×{P,Q}",
            "owner_selector": {"P": {"register": 17, "e": 1, "turn": 1}, "Q": {"register": 18, "e": 0, "turn": -1}},
            "map": "d_k(s,p,1)=P[s+k]; d_k(s,p,0)=Q[-s+k], indices mod 5",
            "global_phase_charts": 5,
            "historical_phase_chart": None,
            "fibre_size": 4,
            "lost_coordinate": "p∈P4",
            "pointwise_minimal_residual_bits": 2,
            "exact_return": "R_k(d_k(s,p,e),p)=(s,p,e) once global k is declared",
        },
        "operator_result": {
            "display_mirror": "κ(i,P)=(i,Q), κ(i,Q)=(i,P)",
            "selected_on_display_quotient": "J_d(s,p,e)=(-s mod 5,p,1-e)",
            "rejected_on_display_quotient": "J_c(s,p,e)=(s,p,1-e)",
            "scope": "conditional on source bead indices, counter-rotation and same-index q=mirror(p)",
            "historical_ncs_janus_selection": None,
        },
        "glb_node_mapping": {
            "p_nodes": expected_p,
            "q_nodes": expected_q,
            "unique_glb_node_to_x40_state": None,
            "unique_glb_node_to_x20_state": None,
            "within_fixed_phase_chart_x20_candidates_per_bead": 4,
            "without_phase_chart_x20_candidates_per_bead": 20,
        },
        "chart_summaries": chart_summaries,
        "maps": {
            "x20_adjacency": None,
            "glb_nodes_to_q106": None,
            "typed_x20_to_q106_intertwiner": None,
            "triple19_to_x20": None,
        },
        "sources": [
            {"name": name, "path": str(path.relative_to(ECOSYSTEM)), "sha256": sha256(path)}
            for name, path in SOURCES.items()
        ],
        "claim_boundary": "Conditional finite carrier/display audit only. The result selects Jd only on the declared C5×C2 bead quotient; it does not recover a historical phase chart or historical NCS Janus law, represent P4 in the GLB, define X20 adjacency, map GLB nodes to Q106, establish a physical orbit, admit a Study, modify A0 evidence or authorize publication.",
        "checks_detail": checks,
    }
    (HERE / "RESULT.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({
        "status": "PASS",
        "checks": result["checks"],
        "display": result["carrier_attachment"]["display"],
        "phase_charts": 5,
        "fibre_size": 4,
        "selected_operator": "J_d on displayed quotient",
    }, indent=2))


if __name__ == "__main__":
    main()

