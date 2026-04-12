import numpy as np


# =========================================
# RESIDUAL (STABLE)
# =========================================

def compute_residual(c, dc, d2c, params):
    a, p, q = params

    # avoid invalid values
    c_safe = np.abs(c) + 1e-8
    dc_safe = np.abs(dc) + 1e-8

    pred = a * (c_safe ** p) * (dc_safe ** q)

    # clamp to avoid overflow
    pred = np.clip(pred, -1e6, 1e6)

    return d2c - pred


# =========================================
# DISTANCE
# =========================================

def compute_distance(c, dc, rift_points):
    dists = []

    for i in range(len(c)):
        point = np.array([c[i], dc[i]])

        if not np.isfinite(point).all():
            dists.append(np.nan)
            continue

        dist = np.min(np.linalg.norm(rift_points - point, axis=1))
        dists.append(dist)

    return np.array(dists)
