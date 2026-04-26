# ============================================================
# NEXAH — IEEE GATE DETECTION v78
# Gate-Permissive Sheet-Aware π-Control
# ============================================================
#
# FILE:
# ieee_gate_detection_v78_gate_permissive_sheet_pi_control.py
#
# PURPOSE:
# --------
# Fix v77 by keeping sheet-awareness as a soft guide only.
#
# v77:
#   sheet constraint became too dominant
#   -> reached gates: 0/2
#
# v78:
#   sheets guide the path,
#   but gates override sheets when transition is needed.
#
# CORE IDEA:
# ----------
# Structure should guide navigation, not block it.
#
# CONTROL:
# --------
# u = flow + gate + sheet
#
# but:
#   sheet_weight decreases near gates
#   gate_weight increases near gates
#   direction changes remain π-smoothed
#
# OUTPUTS:
# --------
# v78_gate_permissive_sheet_pi_control.png
# v78_turning_profile.png
# v78_sheet_profile.png
# v78_control_summary.txt
#
# ============================================================

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from ieee_gate_detection_v38_control_layer import run_v38_control


# ------------------------------------------------------------
# Utils
# ------------------------------------------------------------

def wrap_theta(theta):
    return (theta + np.pi) % (2 * np.pi) - np.pi


def unit_vector(v):
    n = np.linalg.norm(v)
    if n < 1e-12:
        return np.zeros_like(v)
    return v / n


def state_distance(a, b):
    return np.linalg.norm([
        a[0] - b[0],
        wrap_theta(a[1] - b[1])
    ])


def unit_vector_to_target(s, target):
    dr = target[0] - s[0]
    dtheta = wrap_theta(target[1] - s[1])
    return unit_vector(np.array([dr, dtheta]))


def angle_of(v):
    return np.arctan2(v[0], v[1])


def smooth_direction(prev_u, desired_u, smoothness=0.93):
    if np.linalg.norm(prev_u) < 1e-12:
        return unit_vector(desired_u)

    u = smoothness * prev_u + (1.0 - smoothness) * desired_u
    return unit_vector(u)


def gate_activation(distance, radius=0.55):
    return np.exp(-(distance ** 2) / (2 * radius ** 2))


# ------------------------------------------------------------
# Build field
# ------------------------------------------------------------

def build_field():

    t = np.linspace(0, 80, 3000)

    x = (
        np.sin(t)
        + 0.25 * np.sin(3.1 * t)
        + 0.02 * t * np.sin(0.7 * t)
    )

    result = run_v38_control(x, dt=t[1] - t[0], bins=80)

    field = np.column_stack([result["r"], result["theta"]])

    return field


# ------------------------------------------------------------
# Flow estimation
# ------------------------------------------------------------

def estimate_flow_direction(field, state, k=28):

    dr = field[:, 0] - state[0]
    dtheta = np.array([wrap_theta(th - state[1]) for th in field[:, 1]])
    dists = np.sqrt(dr**2 + dtheta**2)

    idx = np.argsort(dists)[:k]
    idx = np.sort(idx)

    local = field[idx]

    if len(local) < 3:
        return np.zeros(2)

    velocities = np.gradient(local, axis=0)
    flow = np.mean(velocities, axis=0)
    flow[1] = wrap_theta(flow[1])

    return unit_vector(flow)


# ------------------------------------------------------------
# Sheet model
# ------------------------------------------------------------

def build_sheet_centers(field, n_sheets=5):
    r_values = field[:, 0]
    percentiles = np.linspace(10, 90, n_sheets)
    return np.array(sorted(np.percentile(r_values, percentiles)))


def assign_sheet(state, sheet_centers):
    distances = np.abs(sheet_centers - state[0])
    return int(np.argmin(distances))


def sheet_direction(state, sheet_centers):
    sheet_index = assign_sheet(state, sheet_centers)
    target_r = sheet_centers[sheet_index]
    return unit_vector(np.array([target_r - state[0], 0.0])), sheet_index


# ------------------------------------------------------------
# Structure
# ------------------------------------------------------------

def load_structure():

    basins = {
        0: np.array([0.8715, 0.6494]),
        1: np.array([0.9310, -2.3343]),
        3: np.array([1.6242, -1.3514]),
    }

    gates = {
        (0, 3): np.array([1.1488, -0.1580]),
        (3, 1): np.array([1.4856, -1.5620]),
    }

    path = [0, 3, 1]

    return basins, gates, path


# ------------------------------------------------------------
# v78 control
# ------------------------------------------------------------

def run_v78_control(
    field,
    basins,
    gates,
    path,
    sheet_centers,
    max_steps=620,
    step_size=0.026,
    base_flow_weight=0.48,
    base_gate_weight=0.36,
    base_sheet_weight=0.16,
    smoothness=0.925,
    gate_radius=0.18,
    target_radius=0.24
):

    state = basins[path[0]].copy()
    target_basin = basins[path[-1]]

    controlled = [state.copy()]
    turn_log = []
    sheet_log = []
    gate_weight_log = []
    sheet_weight_log = []
    gate_distance_log = []

    gate_index = 0
    prev_u = np.zeros(2)
    prev_angle = None

    for _ in range(max_steps):

        if gate_index < len(path) - 1:
            edge = (path[gate_index], path[gate_index + 1])
            target = gates[edge]
        else:
            target = target_basin

        d_gate = state_distance(state, target)
        g_act = gate_activation(d_gate, radius=0.55)

        # Gate-permissive weighting:
        # near gate: gate dominates, sheet relaxes
        # far from gate: flow + sheet guide
        flow_weight = base_flow_weight
        gate_weight = base_gate_weight + 0.42 * g_act
        sheet_weight = base_sheet_weight * (1.0 - 0.85 * g_act)

        flow_dir = estimate_flow_direction(field, state)
        target_dir = unit_vector_to_target(state, target)
        sheet_dir, sheet_index = sheet_direction(state, sheet_centers)

        desired_u = unit_vector(
            flow_weight * flow_dir
            + gate_weight * target_dir
            + sheet_weight * sheet_dir
        )

        u = smooth_direction(prev_u, desired_u, smoothness=smoothness)

        angle = angle_of(u)

        if prev_angle is None:
            turn = 0.0
        else:
            turn = wrap_theta(angle - prev_angle)

        prev_angle = angle
        prev_u = u.copy()

        state = state + step_size * u
        state[1] = wrap_theta(state[1])

        controlled.append(state.copy())
        turn_log.append(turn)
        sheet_log.append(sheet_index)
        gate_weight_log.append(gate_weight)
        sheet_weight_log.append(sheet_weight)
        gate_distance_log.append(d_gate)

        if gate_index < len(path) - 1:
            if state_distance(state, target) < gate_radius:
                gate_index += 1
        else:
            if state_distance(state, target_basin) < target_radius:
                break

    return {
        "controlled": np.array(controlled),
        "turns": np.array(turn_log),
        "sheets": np.array(sheet_log),
        "gate_weights": np.array(gate_weight_log),
        "sheet_weights": np.array(sheet_weight_log),
        "gate_distances": np.array(gate_distance_log),
        "reached_gates": gate_index,
        "final_distance": state_distance(controlled[-1], target_basin),
    }


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main():

    field = build_field()
    basins, gates, path = load_structure()
    sheet_centers = build_sheet_centers(field, n_sheets=5)

    result = run_v78_control(
        field,
        basins,
        gates,
        path,
        sheet_centers
    )

    controlled = result["controlled"]

    CORE_DIR = os.path.dirname(CURRENT_DIR)
    OUT_DIR = os.path.join(CORE_DIR, "outputs", "ieee_gates")
    os.makedirs(OUT_DIR, exist_ok=True)

    # --------------------------------------------------------
    # Main plot
    # --------------------------------------------------------

    fig, ax = plt.subplots(figsize=(9, 7))

    ax.scatter(
        field[:, 1],
        field[:, 0],
        s=2,
        alpha=0.12,
        label="field"
    )

    for i, r_sheet in enumerate(sheet_centers):
        ax.axhline(
            r_sheet,
            linewidth=0.8,
            alpha=0.35,
            linestyle="--"
        )
        ax.text(-3.05, r_sheet, f"S{i}", fontsize=7)

    ax.plot(
        controlled[:, 1],
        controlled[:, 0],
        linewidth=2.4,
        color="red",
        label="gate-permissive sheet π-control"
    )

    for bid, b in basins.items():
        ax.scatter(b[1], b[0], s=90, edgecolor="black")
        ax.text(b[1], b[0], f"B{bid}", fontsize=9)

    for edge, g in gates.items():
        ax.scatter(g[1], g[0], s=120, marker="x", color="black")
        ax.text(g[1], g[0], f"G{edge[0]}->{edge[1]}", fontsize=8)

    ax.set_xlabel("theta")
    ax.set_ylabel("r")
    ax.set_title(
        "NEXAH v78 — Gate-Permissive Sheet-Aware π-Control\n"
        f"reached={result['reached_gates']}/{len(path)-1}, "
        f"final_dist={result['final_distance']:.4f}"
    )
    ax.legend()

    out_path = os.path.join(
        OUT_DIR,
        "v78_gate_permissive_sheet_pi_control.png"
    )

    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)

    # --------------------------------------------------------
    # Turning profile
    # --------------------------------------------------------

    fig2, ax2 = plt.subplots(figsize=(9, 4))

    ax2.plot(result["turns"], linewidth=1.5)
    ax2.axhline(0.0, linestyle="--", linewidth=1)

    ax2.set_xlabel("step")
    ax2.set_ylabel("Δ direction angle")
    ax2.set_title("NEXAH v78 — Turning Profile")

    turn_path = os.path.join(
        OUT_DIR,
        "v78_turning_profile.png"
    )

    fig2.tight_layout()
    fig2.savefig(turn_path, dpi=200)
    plt.close(fig2)

    # --------------------------------------------------------
    # Sheet profile
    # --------------------------------------------------------

    fig3, ax3 = plt.subplots(figsize=(9, 4))

    ax3.step(
        np.arange(len(result["sheets"])),
        result["sheets"],
        where="post",
        linewidth=1.5
    )

    ax3.set_xlabel("step")
    ax3.set_ylabel("sheet index")
    ax3.set_title("NEXAH v78 — Sheet Index over Control Path")

    sheet_path = os.path.join(
        OUT_DIR,
        "v78_sheet_profile.png"
    )

    fig3.tight_layout()
    fig3.savefig(sheet_path, dpi=200)
    plt.close(fig3)

    # --------------------------------------------------------
    # Weight profile
    # --------------------------------------------------------

    fig4, ax4 = plt.subplots(figsize=(9, 4))

    ax4.plot(result["gate_weights"], label="gate weight")
    ax4.plot(result["sheet_weights"], label="sheet weight")

    ax4.set_xlabel("step")
    ax4.set_ylabel("weight")
    ax4.set_title("NEXAH v78 — Gate vs Sheet Weight")
    ax4.legend()

    weight_path = os.path.join(
        OUT_DIR,
        "v78_gate_sheet_weights.png"
    )

    fig4.tight_layout()
    fig4.savefig(weight_path, dpi=200)
    plt.close(fig4)

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    summary_path = os.path.join(
        OUT_DIR,
        "v78_control_summary.txt"
    )

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("NEXAH v78 — Gate-Permissive Sheet-Aware π-Control\n")
        f.write("================================================\n\n")

        f.write(f"Path: {path}\n")
        f.write(f"Reached gates: {result['reached_gates']}/{len(path)-1}\n")
        f.write(f"Final distance to target: {result['final_distance']:.6f}\n\n")

        f.write("Sheet centers:\n")
        for i, r_sheet in enumerate(sheet_centers):
            f.write(f"  S{i}: r={r_sheet:.6f}\n")

        f.write("\nπ-consistency metrics:\n")
        f.write(f"  max |turn|:  {np.max(np.abs(result['turns'])):.6f}\n")
        f.write(f"  mean |turn|: {np.mean(np.abs(result['turns'])):.6f}\n")
        f.write(f"  total turn:  {np.sum(np.abs(result['turns'])):.6f}\n\n")

        f.write("Sheet/navigation metrics:\n")
        f.write(f"  unique sheets visited: {sorted(set(result['sheets'].tolist()))}\n")
        f.write(f"  mean gate weight:  {np.mean(result['gate_weights']):.6f}\n")
        f.write(f"  mean sheet weight: {np.mean(result['sheet_weights']):.6f}\n")

    print("NEXAH v78 complete")
    print(f"Reached gates: {result['reached_gates']}/{len(path)-1}")
    print(f"Final distance: {result['final_distance']:.6f}")
    print(f"Saved: {out_path}")
    print(f"Saved: {turn_path}")
    print(f"Saved: {sheet_path}")
    print(f"Saved: {weight_path}")
    print(f"Saved: {summary_path}")


if __name__ == "__main__":
    main()
