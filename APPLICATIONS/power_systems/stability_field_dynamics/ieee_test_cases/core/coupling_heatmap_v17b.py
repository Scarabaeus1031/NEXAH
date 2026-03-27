# APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/coupling_heatmap_v17b.py

import numpy as np


# =========================
# LOCAL FLOW PERSISTENCE
# =========================
def compute_local_flow_persistence(Fx, Fy):
    """
    Local directional coherence map in [0, 1].
    """
    mag = np.sqrt(Fx**2 + Fy**2) + 1e-8
    nx = Fx / mag
    ny = Fy / mag

    h, w = Fx.shape
    P_local = np.zeros((h, w), dtype=float)

    for y in range(1, h - 1):
        for x in range(1, w - 1):
            dots = []

            vx = nx[y, x]
            vy = ny[y, x]

            for yy, xx in [
                (y - 1, x),
                (y + 1, x),
                (y, x - 1),
                (y, x + 1),
            ]:
                d = vx * nx[yy, xx] + vy * ny[yy, xx]
                dots.append(abs(d))

            P_local[y, x] = np.mean(dots)

    return np.clip(P_local, 0.0, 1.0)


# =========================
# LOCAL RECURRENCE CONCENTRATION
# =========================
def normalize_field(field):
    fmin = np.min(field)
    fmax = np.max(field)

    if np.isclose(fmax, fmin):
        return np.zeros_like(field)

    return (field - fmin) / (fmax - fmin)


def smooth_box(field, radius=2):
    """
    Simple box smoothing without extra dependencies.
    """
    h, w = field.shape
    out = np.zeros_like(field, dtype=float)

    for y in range(h):
        y0 = max(0, y - radius)
        y1 = min(h, y + radius + 1)

        for x in range(w):
            x0 = max(0, x - radius)
            x1 = min(w, x + radius + 1)

            patch = field[y0:y1, x0:x1]
            out[y, x] = np.mean(patch)

    return out


def compute_local_recurrence_concentration(M):
    """
    Local recurrence concentration map in [0, 1].
    """
    M_norm = normalize_field(M)
    R_local = smooth_box(M_norm, radius=2)
    return normalize_field(R_local)


# =========================
# LOOP OCCUPANCY MAP
# =========================
def compute_loop_occupancy(loops, shape):
    """
    Build local map of where loops pass through the field.
    """
    h, w = shape
    L_local = np.zeros((h, w), dtype=float)

    for loop in loops:
        for p in loop:
            x = int(round(p[0]))
            y = int(round(p[1]))

            if 0 <= x < w and 0 <= y < h:
                L_local[y, x] += 1.0

    return normalize_field(L_local)


# =========================
# LOCAL COUPLING HEATMAP
# =========================
def compute_coupling_heatmap(Fx, Fy, M, loops):
    """
    Local coupling:
        C_local = P_local * R_local * (L_local + eps)
    """
    P_local = compute_local_flow_persistence(Fx, Fy)
    R_local = compute_local_recurrence_concentration(M)
    L_local = compute_loop_occupancy(loops, M.shape)

    C_local = P_local * R_local * (L_local + 1e-3)
    C_local = normalize_field(C_local)

    return {
        "C_local": C_local,
        "P_local": P_local,
        "R_local": R_local,
        "L_local": L_local,
    }
