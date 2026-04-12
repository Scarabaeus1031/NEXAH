import numpy as np
from scipy.optimize import curve_fit


def fit_manifold(c, dc, d2c):
    """
    Robust manifold fit:
    d2c ≈ a * c^p * dc^q
    """

    # --- CLEAN INPUT ---
    mask = (
        np.isfinite(c) &
        np.isfinite(dc) &
        np.isfinite(d2c)
    )

    c = c[mask]
    dc = dc[mask]
    d2c = d2c[mask]

    # remove near-zero values (log instability)
    eps = 1e-6
    mask2 = (np.abs(c) > eps) & (np.abs(dc) > eps)

    c = c[mask2]
    dc = dc[mask2]
    d2c = d2c[mask2]

    if len(c) < 10:
        print("⚠️ Not enough data for fit → fallback")
        return np.array([1.0, 1.0, 1.0])

    # --- MODEL ---
    def f(X, a, p, q):
        c, dc = X
        return a * (np.abs(c) ** p) * (np.abs(dc) ** q)

    # --- INITIAL GUESS (CRITICAL FIX) ---
    p0 = [1.0, 1.0, 1.0]

    try:
        popt, _ = curve_fit(
            f,
            (c, dc),
            d2c,
            p0=p0,
            maxfev=20000
        )
        return popt

    except RuntimeError:
        print("⚠️ Fit failed → using fallback parameters")
        return np.array([1.0, 1.0, 1.0])
