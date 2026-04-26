# ============================================================
# NEXAH — IEEE GATE DETECTION v56
# Pattern-Field Control (State-Structured Activation)
# ============================================================
#
# FILE:
# ieee_gate_detection_v56_pattern_field_control.py
#
# PURPOSE:
# --------
# Move from time-based control patterns to state-space patterns.
#
# v52–v53:
#     pattern(t)
#
# v56:
#     pattern(r, θ, basin, structure)
#
# CORE IDEA:
# ----------
# Control is activated in specific geometric regions of state space.
#
# Control follows:
#     - basin structure
#     - distance to centroid
#     - angular bands
#     - radial shells
#
# OUTPUTS:
# --------
# v56_pattern_field_B{source}_to_B{target}.png
# v56_pattern_field_summary_B{source}_to_B{target}.txt
# v56_pattern_field_states_B{source}_to_B{target}.npy
# v56_pattern_field_active_mask_B{source}_to_B{target}.npy
# v56_pattern_field_mask_B{source}_to_B{target}.npy
#
# ============================================================

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from ieee_gate_detection_v38_control_layer import (
    run_v38_control,
    gradient_field,
    make_interpolator
)

from ieee_gate_detection_v39_attractor_memory import (
    stability_score,
    detect_stable_attractors,
    attractor_memory_field
)

from ieee_gate_detection_v41_ridge_aligned_control import (
    ridge_aligned_control,
    wrap_theta
)

from ieee_gate_detection_v42_orbit_attractor_locking import compute_locking_score
from ieee_gate_detection_v44_basin_identity import cluster_locked_basins
from ieee_gate_detection_v45_transition_matrix import compute_transition_matrix_from_segments
from ieee_gate_detection_v47_memory_guided_control import compute_basin_centroids


# ------------------------------------------------------------
# Build baseline pipeline
# ------------------------------------------------------------

def build_pipeline():

    t = np.linspace(0, 80, 3000)

    x = (
        np.sin(t)
        + 0.25 * np.sin(3.1 * t)
        + 0.02 * t * np.sin(0.7 * t)
    )

    result = run_v38_control(x, dt=t[1] - t[0], bins=80)

    states = np.column_stack([
        result["r"],
        result["theta"]
    ])

    raw_controls = result["controls"]

    rho = result["rho"]
    P = result["P_IOTA"]
    D = result["D"]
    r_grid = result["r_grid"]
    theta_grid = result["theta_grid"]

    # --- v39 attractor memory
    S = stability_score(rho, P, D)

    attractors = detect_stable_attractors(
        S,
        r_grid,
        theta_grid,
        percentile=98
    )

    A = attractor_memory_field(
        attractors,
        r_grid,
        theta_grid
    )

    # --- v41 ridge aligned control
    grad_rho = gradient_field(rho, r_grid, theta_grid)

    grad_rho_interp = (
        make_interpolator(grad_rho[0], r_grid, theta_grid),
        make_interpolator(grad_rho[1], r_grid, theta_grid),
    )

    aligned = ridge_aligned_control(
        states,
        raw_controls,
        grad_rho_interp,
        eta=0.02,
        max_step=0.04,
        tangential_gain=1.0,
        damping=0.15
    )

    # --- v42 locking score
    A_interp = make_interpolator(A, r_grid, theta_grid)
    D_interp = make_interpolator(D, r_grid, theta_grid)
    P_interp = make_interpolator(P, r_grid, theta_grid)

    L, *_ = compute_locking_score(
        aligned,
        A_interp,
        D_interp,
        P_interp
    )

    # --- v44 basin identities
    basin_ids, *_ = cluster_locked_basins(
        aligned,
        L,
        threshold=0.5,
        eps=0.18,
        min_samples=6
    )

    centroids = compute_basin_centroids(
        aligned,
        basin_ids
    )

    counts, probs, basin_list, segments = compute_transition_matrix_from_segments(
        basin_ids
    )

    return {
        "t": t,
        "aligned": aligned,
        "controls": raw_controls,
        "basin_ids": basin_ids,
        "centroids": centroids,
        "transition_counts": counts,
        "transition_probs": probs,
        "basin_list": basin_list,
        "segments": segments,
        "locking": L,
    }


# ------------------------------------------------------------
# Pattern Field Definition
# ------------------------------------------------------------

def pattern_field_mask(
    states,
    basin_ids,
    centroids,
    source,
    inner_radius=0.20,
    outer_radius=1.00,
    theta_width=1.20
):
    """
    State-space pattern:

    Control is enabled only inside source basin and only in a
    geometric shell around the source centroid.

    This turns pattern control from:

        pattern(t)

    into:

        pattern(r, theta)
    """

    mask = np.zeros(len(states), dtype=bool)

    if source not in centroids:
        return mask

    c = centroids[source]

    for i, s in enumerate(states):

        if basin_ids[i] != source:
            continue

        r, theta = s

        dr = r - c[0]
        dtheta = wrap_theta(theta - c[1])
        dist = np.sqrt(dr**2 + dtheta**2)

        theta_band = abs(dtheta) < theta_width
        radial_band = inner_radius < dist < outer_radius

        if theta_band and radial_band:
            mask[i] = True

    return mask


# ------------------------------------------------------------
# Control
# ------------------------------------------------------------

def pattern_field_control(
    states,
    controls,
    basin_ids,
    centroids,
    source,
    target,
    eta=0.02,
    gain=0.065,
    base_gain=0.55,
    max_step=0.055,
    inner_radius=0.20,
    outer_radius=1.00,
    theta_width=1.20
):

    controlled = states.copy()

    mask = pattern_field_mask(
        states,
        basin_ids,
        centroids,
        source,
        inner_radius=inner_radius,
        outer_radius=outer_radius,
        theta_width=theta_width
    )

    active = np.zeros(len(states), dtype=bool)

    if target not in centroids:
        raise ValueError(f"Target basin {target} not found in centroids.")

    target_c = centroids[target]

    for i in range(len(states)):

        if not mask[i]:
            continue

        if basin_ids[i] != source:
            continue

        s = controlled[i]

        u_base = controls[i]

        dr = target_c[0] - s[0]
        dtheta = wrap_theta(target_c[1] - s[1])

        u_target = np.array([dr, dtheta])
        norm = np.linalg.norm(u_target)

        if norm > 1e-9:
            u_target = u_target / norm

        u = base_gain * eta * u_base + gain * u_target

        nrm = np.linalg.norm(u)
        if nrm > max_step:
            u = u / nrm * max_step

        s_new = s + u
        s_new[1] = wrap_theta(s_new[1])

        controlled[i] = s_new
        active[i] = True

    return controlled, active, mask


# ------------------------------------------------------------
# Nearest basin assignment
# ------------------------------------------------------------

def assign_nearest_basin(states, centroids):

    basin_ids = np.full(len(states), -1, dtype=int)

    for i, s in enumerate(states):

        best_basin = -1
        best_dist = np.inf

        for bid, c in centroids.items():

            dr = s[0] - c[0]
            dtheta = wrap_theta(s[1] - c[1])
            dist = np.sqrt(dr**2 + dtheta**2)

            if dist < best_dist:
                best_dist = dist
                best_basin = bid

        basin_ids[i] = best_basin

    return basin_ids


def transition_probability(probs, basin_list, source, target):

    if source not in basin_list or target not in basin_list:
        return 0.0

    i = basin_list.index(source)
    j = basin_list.index(target)

    return float(probs[i, j])


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":

    CORE_DIR = os.path.dirname(CURRENT_DIR)
    OUT_DIR = os.path.join(CORE_DIR, "outputs", "ieee_gates")
    os.makedirs(OUT_DIR, exist_ok=True)

    data = build_pipeline()

    source = 0
    target = 1

    controlled, active, mask = pattern_field_control(
        states=data["aligned"],
        controls=data["controls"],
        basin_ids=data["basin_ids"],
        centroids=data["centroids"],
        source=source,
        target=target,
        eta=0.02,
        gain=0.065,
        base_gain=0.55,
        max_step=0.055,
        inner_radius=0.20,
        outer_radius=1.00,
        theta_width=1.20
    )

    controlled_ids = assign_nearest_basin(
        controlled,
        data["centroids"]
    )

    controlled_counts, controlled_probs, controlled_basin_list, _ = (
        compute_transition_matrix_from_segments(controlled_ids)
    )

    p_before = transition_probability(
        data["transition_probs"],
        data["basin_list"],
        source,
        target
    )

    p_after = transition_probability(
        controlled_probs,
        controlled_basin_list,
        source,
        target
    )

    delta_p = p_after - p_before

    # --------------------------------------------------------
    # Plot
    # --------------------------------------------------------

    plt.figure(figsize=(8, 8))

    plt.scatter(
        data["aligned"][:, 1],
        data["aligned"][:, 0],
        s=2,
        alpha=0.20,
        label="baseline"
    )

    plt.scatter(
        controlled[:, 1],
        controlled[:, 0],
        s=3,
        alpha=0.55,
        label="v56 pattern-field controlled"
    )

    plt.scatter(
        controlled[mask, 1],
        controlled[mask, 0],
        s=8,
        alpha=0.45,
        label="pattern field mask"
    )

    plt.scatter(
        controlled[active, 1],
        controlled[active, 0],
        s=12,
        alpha=0.90,
        label="active control"
    )

    for bid, c in data["centroids"].items():
        plt.scatter(
            c[1],
            c[0],
            s=90,
            marker="x",
            label=f"basin {bid}"
        )

    plt.xlabel("theta")
    plt.ylabel("r")
    plt.title(
        f"NEXAH v56 — Pattern Field Control B{source}→B{target}\n"
        f"P before={p_before:.3f}, after={p_after:.3f}, Δ={delta_p:.3f}"
    )

    plt.legend(fontsize=7)
    plt.tight_layout()

    tag = f"B{source}_to_B{target}"

    out_path = os.path.join(
        OUT_DIR,
        f"v56_pattern_field_{tag}.png"
    )

    plt.savefig(out_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Save outputs
    # --------------------------------------------------------

    np.save(
        os.path.join(OUT_DIR, f"v56_pattern_field_states_{tag}.npy"),
        controlled
    )

    np.save(
        os.path.join(OUT_DIR, f"v56_pattern_field_active_mask_{tag}.npy"),
        active
    )

    np.save(
        os.path.join(OUT_DIR, f"v56_pattern_field_mask_{tag}.npy"),
        mask
    )

    np.save(
        os.path.join(OUT_DIR, f"v56_pattern_field_transition_probs_{tag}.npy"),
        controlled_probs
    )

    summary_path = os.path.join(
        OUT_DIR,
        f"v56_pattern_field_summary_{tag}.txt"
    )

    with open(summary_path, "w", encoding="utf-8") as f:

        f.write("NEXAH v56 — Pattern Field Control Summary\n")
        f.write("=========================================\n\n")

        f.write(f"Source basin: {source}\n")
        f.write(f"Target basin: {target}\n\n")

        f.write("Pattern-field parameters:\n")
        f.write("  inner_radius: 0.20\n")
        f.write("  outer_radius: 1.00\n")
        f.write("  theta_width:  1.20\n\n")

        f.write(f"Pattern mask states: {int(np.sum(mask))}\n")
        f.write(f"Active states:       {int(np.sum(active))}\n\n")

        f.write(f"P_before({source}->{target}): {p_before:.4f}\n")
        f.write(f"P_after({source}->{target}):  {p_after:.4f}\n")
        f.write(f"Delta P: {delta_p:.4f}\n\n")

        f.write("Baseline transition probs:\n")
        f.write(str(data["transition_probs"]))
        f.write("\n\nControlled transition probs:\n")
        f.write(str(controlled_probs))
        f.write("\n\nControlled transition counts:\n")
        f.write(str(controlled_counts))
        f.write("\n")

    print("NEXAH v56 complete")
    print(f"Source -> Target: {source} -> {target}")
    print(f"Pattern mask states: {int(np.sum(mask))}")
    print(f"Active states:       {int(np.sum(active))}")
    print(f"P before: {p_before:.4f}")
    print(f"P after:  {p_after:.4f}")
    print(f"Delta P:  {delta_p:.4f}")
    print(f"Saved: {out_path}")
    print(f"Saved: {summary_path}")
