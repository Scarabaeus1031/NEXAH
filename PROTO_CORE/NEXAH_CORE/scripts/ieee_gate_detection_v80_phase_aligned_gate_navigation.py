# ============================================================
# NEXAH — IEEE GATE DETECTION v80
# Phase-Aligned Gate Navigation
# ============================================================
#
# FILE:
# ieee_gate_detection_v80_phase_aligned_gate_navigation.py
#
# PURPOSE:
# --------
# Fix v79 by treating gates as oriented transition targets.
#
# v79:
#   reached 1/2 gates
#   problem: gates were treated as points only
#
# v80:
#   gate = position + approach phase
#
# CORE IDEA:
# ----------
# A gate is not only WHERE you arrive.
# A gate also requires the right ANGLE OF APPROACH.
#
# CONTROL OPERATORS:
# ------------------
# π      : phase / angular alignment
# φ      : radial drift / escape
# √2     : sheet transition
# gate   : active waypoint pull
#
# OUTPUTS:
# --------
# v80_phase_aligned_gate_navigation.png
# v80_turning_profile.png
# v80_sheet_profile.png
# v80_gate_distance_profile.png
# v80_summary.txt
#
# ============================================================

import os
import numpy as np
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def wrap_angle(x):
    return (x + np.pi) % (2 * np.pi) - np.pi


def dist_state(a, b):
    return np.sqrt(
        wrap_angle(a[0] - b[0]) ** 2 +
        (a[1] - b[1]) ** 2
    )


def unit(x):
    n = np.linalg.norm(x)
    if n < 1e-12:
        return np.zeros_like(x)
    return x / n


def get_sheet_index(r, sheet_centers):
    return int(np.argmin(np.abs(sheet_centers - r)))


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main():

    # --------------------------------------------------------
    # Parameters
    # --------------------------------------------------------

    dt = 0.045
    steps = 650

    # operator gains
    k_pi = 0.75
    k_phi = 0.38
    k_sqrt = 0.22
    k_gate = 0.95

    # smoothing
    smoothness = 0.86

    # initial state
    theta = -2.5
    r = 1.1

    # final target
    final_target = np.array([0.8, 0.9])

    # gates / waypoint sequence
    gates = [
        np.array([-1.3, 1.6]),
        np.array([0.8, 0.9]),
    ]

    targets = gates + [final_target]

    # required approach directions per gate
    # angle in control-vector space
    gate_approach_angles = [
        -0.35,   # approach gate 1 with mild downward/right curvature
        0.05,    # approach gate 2 nearly horizontal/stable
    ]

    gate_radius = 0.20
    approach_tolerance = 0.55

    sheet_centers = np.array([0.54, 0.86, 1.20, 1.60, 1.99])

    # --------------------------------------------------------
    # Logs
    # --------------------------------------------------------

    theta_path = []
    r_path = []
    sheet_path = []
    turn_profile = []
    target_log = []
    gate_distance_log = []

    u_prev = np.zeros(2)
    angle_prev = None

    current_target_index = 0
    reached_gates = 0

    # --------------------------------------------------------
    # Simulation
    # --------------------------------------------------------

    for step in range(steps):

        target = targets[current_target_index]

        state = np.array([theta, r])

        dtheta = wrap_angle(target[0] - theta)
        dr = target[1] - r

        distance_to_target = np.sqrt(dtheta**2 + dr**2)

        # ----------------------------------------------------
        # Operator 1: π phase alignment
        # ----------------------------------------------------

        u_pi = np.array([
            k_pi * dtheta,
            0.0
        ])

        # ----------------------------------------------------
        # Operator 2: φ radial drift
        # softened vs v79
        # ----------------------------------------------------

        u_phi = np.array([
            0.0,
            k_phi * np.sign(dr) * (abs(dr) ** 0.65)
        ])

        # ----------------------------------------------------
        # Operator 3: √2 sheet transition
        # ----------------------------------------------------

        sheet_idx = get_sheet_index(r, sheet_centers)

        if dr > 0:
            next_sheet = min(sheet_idx + 1, len(sheet_centers) - 1)
        else:
            next_sheet = max(sheet_idx - 1, 0)

        sheet_target_r = sheet_centers[next_sheet]

        u_sqrt = np.array([
            0.0,
            k_sqrt * (sheet_target_r - r)
        ])

        # ----------------------------------------------------
        # Operator 4: active gate pull
        # ----------------------------------------------------

        u_gate = k_gate * np.array([dtheta, dr])

        # ----------------------------------------------------
        # Adaptive weights
        # ----------------------------------------------------

        near_gate = np.exp(-(distance_to_target**2) / (2 * 0.45**2))

        w_gate = 0.35 + 0.45 * near_gate
        w_pi = 0.25 + 0.25 * near_gate
        w_phi = 0.25 * (1.0 - 0.40 * near_gate)
        w_sqrt = 0.15 * (1.0 - 0.65 * near_gate)

        total_w = w_gate + w_pi + w_phi + w_sqrt

        w_gate /= total_w
        w_pi /= total_w
        w_phi /= total_w
        w_sqrt /= total_w

        desired_u = (
            w_gate * u_gate +
            w_pi * u_pi +
            w_phi * u_phi +
            w_sqrt * u_sqrt
        )

        # ----------------------------------------------------
        # Smooth direction update
        # ----------------------------------------------------

        if np.linalg.norm(u_prev) > 1e-12:
            u = smoothness * u_prev + (1.0 - smoothness) * desired_u
        else:
            u = desired_u

        # speed clamp
        speed = np.linalg.norm(u)
        max_speed = 0.85
        if speed > max_speed:
            u = u / speed * max_speed

        # ----------------------------------------------------
        # Turning metric
        # ----------------------------------------------------

        angle = np.arctan2(u[1], u[0])

        if angle_prev is None:
            turn = 0.0
        else:
            turn = wrap_angle(angle - angle_prev)

        angle_prev = angle
        u_prev = u.copy()

        # ----------------------------------------------------
        # State update
        # ----------------------------------------------------

        theta = wrap_angle(theta + dt * u[0])
        r = r + dt * u[1]

        # ----------------------------------------------------
        # Gate / target transition check
        # ----------------------------------------------------

        if current_target_index < len(gates):

            gate_angle_required = gate_approach_angles[current_target_index]
            approach_error = abs(wrap_angle(angle - gate_angle_required))

            if (
                distance_to_target < gate_radius
                and approach_error < approach_tolerance
            ):
                reached_gates += 1
                current_target_index += 1
                u_prev *= 0.35

        else:
            if distance_to_target < gate_radius:
                current_target_index += 1
                break

        # ----------------------------------------------------
        # Logs
        # ----------------------------------------------------

        theta_path.append(theta)
        r_path.append(r)
        sheet_path.append(get_sheet_index(r, sheet_centers))
        turn_profile.append(turn)
        target_log.append(current_target_index)
        gate_distance_log.append(distance_to_target)

        if current_target_index >= len(targets):
            break

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    theta_path = np.array(theta_path)
    r_path = np.array(r_path)
    sheet_path = np.array(sheet_path)
    turn_profile = np.array(turn_profile)
    gate_distance_log = np.array(gate_distance_log)

    final_distance = dist_state(
        np.array([theta, r]),
        final_target
    )

    # --------------------------------------------------------
    # Output folder
    # --------------------------------------------------------

    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    CORE_DIR = os.path.dirname(CURRENT_DIR)

    OUT_DIR = os.path.join(CORE_DIR, "outputs", "ieee_gates")
    os.makedirs(OUT_DIR, exist_ok=True)

    # --------------------------------------------------------
    # Plot 1: trajectory
    # --------------------------------------------------------

    fig, ax = plt.subplots(figsize=(9, 7))

    ax.plot(
        theta_path,
        r_path,
        color="red",
        linewidth=2.4,
        label="phase-aligned control"
    )

    for i, g in enumerate(gates):
        ax.scatter(g[0], g[1], color="black", s=90)
        ax.text(g[0], g[1], f"G{i+1}", fontsize=10)

    ax.scatter(
        final_target[0],
        final_target[1],
        color="blue",
        s=120,
        label="target"
    )

    for i, s in enumerate(sheet_centers):
        ax.axhline(s, linestyle="--", alpha=0.25)
        ax.text(-3.05, s, f"S{i}", fontsize=8)

    ax.set_xlabel("theta")
    ax.set_ylabel("r")
    ax.set_title(
        "NEXAH v80 — Phase-Aligned Gate Navigation\n"
        f"reached={reached_gates}/{len(gates)}, final_dist={final_distance:.4f}"
    )
    ax.legend()

    out_control = os.path.join(
        OUT_DIR,
        "v80_phase_aligned_gate_navigation.png"
    )

    fig.tight_layout()
    fig.savefig(out_control, dpi=200)
    plt.close(fig)

    # --------------------------------------------------------
    # Plot 2: turning profile
    # --------------------------------------------------------

    fig2, ax2 = plt.subplots(figsize=(9, 4))

    ax2.plot(turn_profile)
    ax2.axhline(0, linestyle="--", linewidth=1)

    ax2.set_title("NEXAH v80 — Turning Profile")
    ax2.set_xlabel("step")
    ax2.set_ylabel("Δ direction angle")

    out_turn = os.path.join(
        OUT_DIR,
        "v80_turning_profile.png"
    )

    fig2.tight_layout()
    fig2.savefig(out_turn, dpi=200)
    plt.close(fig2)

    # --------------------------------------------------------
    # Plot 3: sheet profile
    # --------------------------------------------------------

    fig3, ax3 = plt.subplots(figsize=(9, 4))

    ax3.step(
        np.arange(len(sheet_path)),
        sheet_path,
        where="post"
    )

    ax3.set_title("NEXAH v80 — Sheet Index")
    ax3.set_xlabel("step")
    ax3.set_ylabel("sheet")

    out_sheet = os.path.join(
        OUT_DIR,
        "v80_sheet_profile.png"
    )

    fig3.tight_layout()
    fig3.savefig(out_sheet, dpi=200)
    plt.close(fig3)

    # --------------------------------------------------------
    # Plot 4: gate distance profile
    # --------------------------------------------------------

    fig4, ax4 = plt.subplots(figsize=(9, 4))

    ax4.plot(gate_distance_log)
    ax4.axhline(gate_radius, linestyle="--", linewidth=1)

    ax4.set_title("NEXAH v80 — Active Target Distance")
    ax4.set_xlabel("step")
    ax4.set_ylabel("distance")

    out_dist = os.path.join(
        OUT_DIR,
        "v80_gate_distance_profile.png"
    )

    fig4.tight_layout()
    fig4.savefig(out_dist, dpi=200)
    plt.close(fig4)

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    summary_path = os.path.join(
        OUT_DIR,
        "v80_summary.txt"
    )

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("NEXAH v80 — Phase-Aligned Gate Navigation\n")
        f.write("========================================\n\n")
        f.write(f"Reached gates: {reached_gates}/{len(gates)}\n")
        f.write(f"Final distance: {final_distance:.6f}\n\n")

        f.write("π / turning metrics:\n")
        f.write(f"  max |turn|:  {np.max(np.abs(turn_profile)):.6f}\n")
        f.write(f"  mean |turn|: {np.mean(np.abs(turn_profile)):.6f}\n")
        f.write(f"  total turn:  {np.sum(np.abs(turn_profile)):.6f}\n\n")

        f.write("Sheet metrics:\n")
        f.write(f"  unique sheets visited: {sorted(set(sheet_path.tolist()))}\n")

    print("NEXAH v80 complete")
    print(f"Reached gates: {reached_gates}/{len(gates)}")
    print(f"Final distance: {final_distance:.6f}")
    print(f"Saved: {out_control}")
    print(f"Saved: {out_turn}")
    print(f"Saved: {out_sheet}")
    print(f"Saved: {out_dist}")
    print(f"Saved: {summary_path}")


if __name__ == "__main__":
    main()
