import numpy as np


def fit_manifold(c, dc, d2c):
    """
    Stable log-space manifold fit

    log(|d2c|) = log(a) + p log(c) + q log(|dc|)
    """

    eps = 1e-6

    # =========================================
    # 1. CLEAN DATA
    # =========================================

    mask = (
        np.isfinite(c) &
        np.isfinite(dc) &
        np.isfinite(d2c) &
        (np.abs(c) > eps) &
        (np.abs(dc) > eps) &
        (np.abs(d2c) > eps)
    )

    c = c[mask]
    dc = dc[mask]
    d2c = d2c[mask]

    if len(c) < 10:
        raise ValueError("Not enough data for manifold fit")

    # =========================================
    # 2. LOG TRANSFORM (SAFE)
    # =========================================

    log_c = np.log(np.abs(c) + eps)
    log_dc = np.log(np.abs(dc) + eps)
    log_d2c = np.log(np.abs(d2c) + eps)

    # =========================================
    # 3. CLIP EXTREMES (CRITICAL)
    # =========================================

    log_c = np.clip(log_c, -10, 10)
    log_dc = np.clip(log_dc, -10, 10)
    log_d2c = np.clip(log_d2c, -10, 10)

    # =========================================
    # 4. LINEAR REGRESSION
    # =========================================

    X = np.column_stack([
        np.ones(len(log_c)),
        log_c,
        log_dc
    ])

    y = log_d2c

    coeffs, *_ = np.linalg.lstsq(X, y, rcond=None)

    log_a, p, q = coeffs

    # =========================================
    # 5. BACK TRANSFORM
    # =========================================

    a = np.exp(np.clip(log_a, -10, 10))

    # =========================================
    # 6. SAFETY CLAMP
    # =========================================

    p = np.clip(p, -5, 5)
    q = np.clip(q, -5, 5)

    return np.array([a, p, q])
