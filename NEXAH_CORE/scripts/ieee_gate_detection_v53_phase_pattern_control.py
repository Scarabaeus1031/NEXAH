# ============================================================
# NEXAH v53 — Phase Pattern Control (Hybrid Adaptive)
# ============================================================

import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# Phase Pattern Definition (your structure)
# ------------------------------------------------------------

PHASES = ["engage", "lock", "release", "next"]

PHASE_MAP = {
    "engage":  [0,1,0,0],
    "lock":    [0,0,1,0],
    "release": [0,0,0,1],
    "next":    [1,0,0,0],
}

PHASE_SEQUENCE = ["engage", "lock", "release", "next"]


# ------------------------------------------------------------
# Phase Generator
# ------------------------------------------------------------

def generate_phase_mask(n, repeat=True):
    """
    Convert phase sequence into boolean mask.
    """

    pattern = []
    for p in PHASE_SEQUENCE:
        pattern.extend(PHASE_MAP[p])

    pattern = np.array(pattern)

    if repeat:
        mask = np.tile(pattern, int(np.ceil(n / len(pattern))))[:n]
    else:
        mask = pattern[:n]

    return mask.astype(bool)


# ------------------------------------------------------------
# Adaptive gating (state-aware override)
# ------------------------------------------------------------

def adaptive_override(mask, states, basin_ids, locking_score, centroids, source):
    """
    Override pattern with dynamic conditions.
    """

    target = centroids[source]

    for t in range(len(states)):

        s = states[t]

        dr = s[0] - target[0]
        dtheta = wrap_theta(s[1] - target[1])
        dist = np.sqrt(dr**2 + dtheta**2)

        L = locking_score[t]

        # --- override rules ---
        if basin_ids[t] == source:

            # near boundary → FORCE ON
            if dist > 0.25:
                mask[t] = True

            # weak locking → FORCE ON
            elif L < 0.55:
                mask[t] = True

            # strong lock → FORCE OFF
            elif L > 0.75:
                mask[t] = False

    return mask


# ------------------------------------------------------------
# Control Function
# ------------------------------------------------------------

def phase_pattern_control(
    aligned_states,
    raw_controls,
    basin_ids,
    locking_score,
    centroids,
    source_basin,
    target_centroid,
    eta=0.02,
    gain=0.065,
    base_gain=0.55,
    max_step=0.055,
    smoothing=0.15
):

    n = len(aligned_states)

    controlled = aligned_states.copy()
    active_mask = np.zeros(n, dtype=bool)

    # --- base pattern ---
    pattern_mask = generate_phase_mask(n)

    # --- adaptive override ---
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
            u_target = u_target / norm

        u = base_gain * eta * u_base + gain * u_target

        # clamp
        nrm = np.linalg.norm(u)
        if nrm > max_step:
            u = u / nrm * max_step

        # smoothing
        u = (1 - smoothing) * u + smoothing * prev

        s_new = s + u
        s_new[1] = wrap_theta(s_new[1])

        controlled[t] = s_new
        active_mask[t] = True

        prev = u

    return controlled, active_mask, pattern_mask
