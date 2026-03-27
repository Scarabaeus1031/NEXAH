# APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/coupling_metric_v17.py

import numpy as np


# =========================
# FLOW PERSISTENCE
# =========================
def compute_flow_persistence(Fx, Fy):
    """
    Measures directional coherence of the vector field.
    Returns value in [0, 1].
    """
    mag = np.sqrt(Fx**2 + Fy**2) + 1e-8

    nx = Fx / mag
    ny = Fy / mag

    # compare neighboring directions
    dot_x = nx[:, :-1] * nx[:, 1:]
    dot_y = ny[:-1, :] * ny[1:, :]

    coherence = 0.5 * (np.mean(np.abs(dot_x)) + np.mean(np.abs(dot_y)))

    return float(np.clip(coherence, 0.0, 1.0))


# =========================
# RECURRENCE CONCENTRATION
# =========================
def compute_recurrence_concentration(M):
    """
    Measures how concentrated recurrence is.
    Returns value in [0, 1].
    """
    total = np.sum(M)

    if total <= 0:
        return 0.0

    prob = M / total
    prob = prob[prob > 0]

    entropy = -np.sum(prob * np.log(prob))
    max_entropy = np.log(len(prob)) if len(prob) > 1 else 1.0

    normalized_entropy = entropy / max_entropy

    concentration = 1.0 - normalized_entropy

    return float(np.clip(concentration, 0.0, 1.0))


# =========================
# LOOP DENSITY
# =========================
def compute_loop_density(loops, n_particles):
    """
    Number of loops normalized by particle count.
    """
    if n_particles <= 0:
        return 0.0

    return float(len(loops) / n_particles)


# =========================
# COUPLING METRIC
# =========================
def compute_coupling_metric(Fx, Fy, M, loops, n_particles):
    """
    C = P * R * L
    """
    P = compute_flow_persistence(Fx, Fy)
    R = compute_recurrence_concentration(M)
    L = compute_loop_density(loops, n_particles)

    C = P * R * L

    return {
        "C": float(C),
        "P": float(P),
        "R": float(R),
        "L": float(L),
    }
