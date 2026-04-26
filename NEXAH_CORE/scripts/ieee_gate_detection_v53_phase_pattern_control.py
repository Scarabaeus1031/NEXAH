# ============================================================
# NEXAH v53 — Phase Pattern Control (FULL PIPELINE)
# ============================================================

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

# --- imports aus deinem System ---
from ieee_gate_detection_v38_control_layer import run_v38_control, gradient_field, make_interpolator
from ieee_gate_detection_v39_attractor_memory import stability_score, detect_stable_attractors, attractor_memory_field
from ieee_gate_detection_v41_ridge_aligned_control import ridge_aligned_control, wrap_theta
from ieee_gate_detection_v42_orbit_attractor_locking import compute_locking_score
from ieee_gate_detection_v44_basin_identity import cluster_locked_basins
from ieee_gate_detection_v45_transition_matrix import compute_transition_matrix_from_segments
from ieee_gate_detection_v47_memory_guided_control import compute_basin_centroids


# ============================================================
# PHASE PATTERN
# ============================================================

PHASE_MAP = {
    "engage":  [0,1,0,0],
    "lock":    [0,0,1,0],
    "release": [0,0,0,1],
    "next":    [1,0,0,0],
}

PHASE_SEQUENCE = ["engage", "lock", "release", "next"]


def generate_phase_mask(n):
    pattern = []
    for p in PHASE_SEQUENCE:
        pattern.extend(PHASE_MAP[p])
    pattern = np.array(pattern)

    return np.tile(pattern, int(np.ceil(n / len(pattern))))[:n].astype(bool)


# ============================================================
# ADAPTIVE OVERRIDE
# ============================================================

def adaptive_override(mask, states, basin_ids, locking_score, centroids, source):

    target = centroids[source]

    for t in range(len(states)):

        if basin_ids[t] != source:
            continue

        s = states[t]

        dr = s[0] - target[0]
        dtheta = wrap_theta(s[1] - target[1])
        dist = np.sqrt(dr**2 + dtheta**2)

        L = locking_score[t]

        if dist > 0.25:
            mask[t] = True
        elif L < 0.55:
            mask[t] = True
        elif L > 0.75:
            mask[t] = False

    return mask


# ============================================================
# CONTROL
# ============================================================

def phase_pattern_control(
    aligned_states,
    raw_controls,
    basin_ids,
    locking_score,
    centroids,
    source_basin,
    target_centroid
):

    n = len(aligned_states)

    controlled = aligned_states.copy()
    active_mask = np.zeros(n, dtype=bool)

    pattern_mask = generate_phase_mask(n)

    pattern_mask = adaptive_override(
        pattern_mask,
        aligned_states,
        basin_ids,
        locking_score,
        centroids,
        source_basin
    )

    prev = np.zeros(2)

    for t in range(n):

        if not pattern_mask[t]:
            continue
        if basin_ids[t] != source_basin:
            continue

        s = controlled[t]
        u_base = raw_controls[t]

        dr = target_centroid[0] - s[0]
        dtheta = wrap_theta(target_centroid[1] - s[1])

        u_target = np.array([dr, dtheta])
        norm = np.linalg.norm(u_target)
        if norm > 1e-9:
            u_target /= norm

        u = 0.55 * 0.02 * u_base + 0.065 * u_target

        # clamp
        nrm = np.linalg.norm(u)
        if nrm > 0.055:
            u = u / nrm * 0.055

        # smoothing
        u = 0.85 * u + 0.15 * prev

        s_new = s + u
        s_new[1] = wrap_theta(s_new[1])

        controlled[t] = s_new
        active_mask[t] = True

        prev = u

    return controlled, active_mask, pattern_mask


# ============================================================
# BUILD PIPELINE
# ============================================================

def build_pipeline():

    t = np.linspace(0, 80, 3000)

    x = np.sin(t) + 0.25*np.sin(3.1*t) + 0.02*t*np.sin(0.7*t)

    result = run_v38_control(x, dt=t[1]-t[0], bins=80)

    states = np.column_stack([result["r"], result["theta"]])
    raw_controls = result["controls"]

    rho = result["rho"]
    P = result["P_IOTA"]
    D = result["D"]
    r_grid = result["r_grid"]
    theta_grid = result["theta_grid"]

    # v39
    S = stability_score(rho, P, D)
    attractors = detect_stable_attractors(S, r_grid, theta_grid, percentile=98)
    A = attractor_memory_field(attractors, r_grid, theta_grid)

    # v41
    grad = gradient_field(rho, r_grid, theta_grid)
    grad_interp = (make_interpolator(grad[0], r_grid, theta_grid),
                   make_interpolator(grad[1], r_grid, theta_grid))

    aligned = ridge_aligned_control(states, raw_controls, grad_interp)

    # v42
    L, *_ = compute_locking_score(
        aligned,
        make_interpolator(A, r_grid, theta_grid),
        make_interpolator(D, r_grid, theta_grid),
        make_interpolator(P, r_grid, theta_grid)
    )

    # v44
    basin_ids, *_ = cluster_locked_basins(aligned, L)

    # v45
    counts, probs, basin_list, segments = compute_transition_matrix_from_segments(basin_ids)

    centroids = compute_basin_centroids(aligned, basin_ids)

    return {
        "aligned": aligned,
        "raw_controls": raw_controls,
        "basin_ids": basin_ids,
        "locking": L,
        "centroids": centroids,
        "transition_probs": probs,
        "basin_list": basin_list
    }


# ============================================================
# RECLASSIFY
# ============================================================

def assign_nearest(states, centroids):

    ids = np.zeros(len(states), dtype=int)

    for i, s in enumerate(states):

        best = None
        best_d = np.inf

        for b, c in centroids.items():
            dr = s[0] - c[0]
            dtheta = wrap_theta(s[1] - c[1])
            d = np.sqrt(dr**2 + dtheta**2)

            if d < best_d:
                best_d = d
                best = b

        ids[i] = best

    return ids


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    data = build_pipeline()

    source = 0
    target = 1

    controlled, active, pattern = phase_pattern_control(
        data["aligned"],
        data["raw_controls"],
        data["basin_ids"],
        data["locking"],
        data["centroids"],
        source,
        data["centroids"][target]
    )

    # reclassify
    controlled_ids = assign_nearest(controlled, data["centroids"])

    counts2, probs2, *_ = compute_transition_matrix_from_segments(controlled_ids)

    # compare
    i = data["basin_list"].index(source)
    j = data["basin_list"].index(target)

    p_before = data["transition_probs"][i, j]
    p_after = probs2[i, j]

    # ============================================================
    # PLOT
    # ============================================================

    plt.figure(figsize=(8,8))

    plt.scatter(data["aligned"][:,1], data["aligned"][:,0], s=2, alpha=0.2)

    plt.scatter(controlled[:,1], controlled[:,0], s=3, alpha=0.6)

    plt.scatter(controlled[active,1], controlled[active,0], s=8, label="active")

    plt.scatter(controlled[pattern,1], controlled[pattern,0], s=5, label="pattern ON")

    for b, c in data["centroids"].items():
        plt.scatter(c[1], c[0], marker="x", s=80)

    plt.title(f"v53 Pattern Control P_before={p_before:.3f} → {p_after:.3f}")

    plt.legend()
    plt.tight_layout()
    plt.show()

    print("NEXAH v53 complete")
    print(f"P before: {p_before:.4f}")
    print(f"P after:  {p_after:.4f}")
