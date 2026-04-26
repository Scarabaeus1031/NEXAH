# ============================================================
# NEXAH — IEEE GATE DETECTION v77
# Sheet-Aware π-Control
# ============================================================
#
# FILE:
# ieee_gate_detection_v77_sheet_aware_pi_control.py
#
# PURPOSE:
# --------
# Upgrade v76 π-consistent control by adding sheet awareness.
#
# v76:
#   smooth direction changes over time
#
# v77:
#   smooth direction changes
#   + avoid sudden sheet jumps
#   + keep trajectory close to locally coherent flow layers
#
# CORE IDEA:
# ----------
# A stable transition must satisfy:
#
#   1. reach gate sequence
#   2. keep turning smooth
#   3. avoid discontinuous sheet switching
#
# OUTPUTS:
# --------
# v77_sheet_aware_pi_control.png
# v77_sheet_turning_profile.png
# v77_sheet_index_profile.png
# v77_sheet_control_summary.txt
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


def smooth_direction(prev_u, desired_u, smoothness=0.94):
    if np.linalg.norm(prev_u) < 1e-12:
        return unit_vector(desired_u)

    u = smoothness * prev_u + (1.0 - smoothness) * desired_u
    return unit_vector(u)


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
# Local flow
# ------------------------------------------------------------

def estimate_flow_direction(field, state, k=24):

    dr = field[:, 0] - state[0]
    dtheta = np.array([wrap_theta(th - state[1]) for th in field[:, 1]])
    dists = np.sqrt(dr**2 + dtheta**2)

    idx = np.argsort(dists)[:k]

    local = field[idx]
    order = np.argsort(idx)
    idx = idx[order]
    local = local[order]

    if len(local) < 3:
        return np.zeros(2)

    velocities = np.gradient(local, axis=0)
    flow = np.mean(velocities, axis=0)
    flow[1] = wrap_theta(flow[1])

    return unit_vector(flow)


# ------------------------------------------------------------
# Sheet model
# ------------------------------------------------------------

def assign_sheet(state, sheet_centers):
    distances = [
        abs(state[0] - center)
        for center in sheet_centers
    ]
    return int(np.argmin(distances))


def sheet_attraction(state, sheet_centers, sheet_index):
    target_r = sheet_centers[sheet_index]
    return np.array([target_r - state[0], 0.0])


def build_sheet_centers(field, n_sheets=5):
    r_values = field[:, 0]

    percentiles = np.linspace(10, 90, n_sheets)
    centers = np.percentile(r_values, percentiles)

    return np.array(sorted(centers))


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
# Sheet-aware π-control
# ------------------------------------------------------------

def run_sheet_aware_pi_control(
    field,
    basins,
    gates,
    path,
    sheet_centers,
    max_steps=560,
    step_size=0.024,
    flow_weight=0.58,
    gate_weight=0.30,
    sheet_weight=0.12,
    smoothness=0.955,
    gate_radius=0.17,
    target_radius=0.22,
    sheet_switch_penalty=0.65
):

    state = basins[path[0]].copy()
    target_basin = basins[path[-1]]

    controlled = [state.copy()]
    direction_log = []
    turn_log = []
    sheet_log = []
    sheet_switch_log = []

    gate_index = 0
    prev_u = np.zeros(2)
    prev_angle = None

    current_sheet = assign_sheet(state, sheet_centers)
    previous_sheet = current_sheet

    for _ in range(max_steps):

        if gate_index < len(path) - 1:
            edge = (path[gate_index], path[gate_index + 1])
            target = gates[edge]
        else:
            target = target_basin

        proposed_sheet = assign_sheet(state, sheet_centers)

        if proposed_sheet != current_sheet:
            sheet_switch = 1
            # only allow sheet update gradually
            if np.random.rand() > sheet_switch_penalty:
                current_sheet = proposed_sheet
        else:
            sheet_switch = 0

        flow_dir = estimate_flow_direction(field, state)
        target_dir = unit_vector_to_target(state, target)
        sheet_dir = unit_vector(sheet_attraction(state, sheet_centers, current_sheet))

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
        direction_log.append(u.copy())
        turn_log.append(turn)
        sheet_log.append(current_sheet)
        sheet_switch_log.append(sheet_switch)

        if gate_index < len(path) - 1:
            if state_distance(state, target) < gate_radius:
                gate_index += 1
        else:
            if state_distance(state, target_basin) < target_radius:
                break

        previous_sheet = current_sheet

    return {
        "controlled": np.array(controlled),
        "directions": np.array(direction_log),
        "turns": np.array(turn_log),
        "sheets": np.array(sheet_log),
        "sheet_switches": np.array(sheet_switch_log),
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

    result = run_sheet_aware_pi_control(
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
    # Trajectory plot
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
        ax.text(
            -3.05,
            r_sheet,
            f"S{i}",
            fontsize=7
        )

    ax.plot(
        controlled[:, 1],
        controlled[:, 0],
        linewidth=2.4,
        color="red",
        label="sheet-aware π-control"
    )

    for bid, b in basins.items():
        ax.scatter(
            b[1],
            b[0],
            s=90,
            edgecolor="black"
        )
        ax.text(b[1], b[0], f"B{bid}", fontsize=9)

    for edge, g in gates.items():
        ax.scatter(
            g[1],
            g[0],
            s=120,
            marker="x",
            color="black"
        )
        ax.text(g[1], g[0], f"G{edge[0]}->{edge[1]}", fontsize=8)

    ax.set_xlabel("theta")
    ax.set_ylabel("r")
    ax.set_title(
        "NEXAH v77 — Sheet-Aware π-Control\n"
        f"reached={result['reached_gates']}/{len(path)-1}, "
        f"final_dist={result['final_distance']:.4f}"
    )
    ax.legend()

    out_path = os.path.join(
        OUT_DIR,
        "v77_sheet_aware_pi_control.png"
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
    ax2.set_title("NEXAH v77 — Turning Profile")

    turn_path = os.path.join(
        OUT_DIR,
        "v77_sheet_turning_profile.png"
    )

    fig2.tight_layout()
    fig2.savefig(turn_path, dpi=200)
    plt.close(fig2)

    # --------------------------------------------------------
    # Sheet index profile
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
    ax3.set_title("NEXAH v77 — Sheet Index over Control Path")

    sheet_path = os.path.join(
        OUT_DIR,
        "v77_sheet_index_profile.png"
    )

    fig3.tight_layout()
    fig3.savefig(sheet_path, dpi=200)
    plt.close(fig3)

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    summary_path = os.path.join(
        OUT_DIR,
        "v77_sheet_control_summary.txt"
    )

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("NEXAH v77 — Sheet-Aware π-Control\n")
        f.write("=================================\n\n")

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

        f.write("Sheet-switch metrics:\n")
        f.write(f"  sheet switches attempted: {int(np.sum(result['sheet_switches']))}\n")
        f.write(f"  unique sheets visited: {sorted(set(result['sheets'].tolist()))}\n")

    print("NEXAH v77 complete")
    print(f"Reached gates: {result['reached_gates']}/{len(path)-1}")
    print(f"Final distance: {result['final_distance']:.6f}")
    print(f"Saved: {out_path}")
    print(f"Saved: {turn_path}")
    print(f"Saved: {sheet_path}")
    print(f"Saved: {summary_path}")


if __name__ == "__main__":
    main()
