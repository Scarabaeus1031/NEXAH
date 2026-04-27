import numpy as np


def build_state_space(x):
    """
    Build phase space: (x, dx/dt)
    """
    v = np.gradient(x)
    return np.column_stack([x, v])


def build_risk_grid(states, risk, bins=50):
    """
    Map risk onto 2D grid
    """
    x = states[:, 0]
    v = states[:, 1]

    H, xedges, yedges = np.histogram2d(
        x, v, bins=bins, weights=risk
    )

    counts, _, _ = np.histogram2d(x, v, bins=bins)

    # avoid division by zero
    avg_risk = np.divide(H, counts + 1e-8)

    return avg_risk, xedges, yedges


def compute_gradient_field(risk_grid):
    """
    Compute spatial gradient of risk field
    """
    grad_y, grad_x = np.gradient(risk_grid)
    return grad_x, grad_y


def apply_state_space_control(x, risk, strength=0.1, bins=50):
    """
    Apply control based on spatial risk gradient
    """
    states = build_state_space(x)

    risk_grid, xedges, yedges = build_risk_grid(states, risk, bins=bins)
    grad_x, grad_y = compute_gradient_field(risk_grid)

    x_controlled = x.copy()

    for t in range(1, len(x) - 1):
        px, pv = states[t]

        # find grid index
        ix = np.searchsorted(xedges, px) - 1
        iy = np.searchsorted(yedges, pv) - 1

        if 0 <= ix < bins and 0 <= iy < bins:
            gx = grad_x[ix, iy]

            # steer opposite to gradient
            x_controlled[t + 1] = x_controlled[t] - strength * gx

    return x_controlled
