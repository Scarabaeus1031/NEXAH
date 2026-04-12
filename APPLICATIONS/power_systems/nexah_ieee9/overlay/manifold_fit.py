import numpy as np

def fit_manifold(c, dc, d2c):
    """
    Log-space fit:
    log(d2c) = log(a) + p log(c) + q log(|dc|)
    """

    # filter valid positive values
    mask = (
        (c > 1e-6) &
        (np.abs(dc) > 1e-6) &
        (np.abs(d2c) > 1e-6) &
        np.isfinite(c) &
        np.isfinite(dc) &
        np.isfinite(d2c)
    )

    c = c[mask]
    dc = dc[mask]
    d2c = d2c[mask]

    log_c = np.log(c)
    log_dc = np.log(np.abs(dc))
    log_d2c = np.log(np.abs(d2c))

    # linear regression
    X = np.column_stack([np.ones(len(c)), log_c, log_dc])
    y = log_d2c

    coeffs, *_ = np.linalg.lstsq(X, y, rcond=None)

    log_a, p, q = coeffs
    a = np.exp(log_a)

    return np.array([a, p, q])
