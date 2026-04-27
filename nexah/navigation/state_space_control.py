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
    Trajectory-aligned control (v5)

    Instead of modifying position directly,
    we modify the direction of motion.

    This prevents drift and collapse.
    """

    states = build_state_space(x)

    risk_grid, xedges, yedges = build_risk_grid(states, risk, bins=bins)
    grad_x, grad_y = compute_gradient_field(risk_grid)

    x_controlled = x.copy()

    for t in range(2, len(x) - 1):
        px, pv = states[t]

        # grid index
        ix = np.searchsorted(xedges, px) - 1
        iy = np.searchsorted(yedges, pv) - 1

        if not (0 <= ix < bins and 0 <= iy < bins):
            continue

        # --- gradient in state space ---
        gx = grad_x[ix, iy]
        gy = grad_y[ix, iy]

        grad_vec = np.array([gx, gy])

        # --- current motion ---
        dx = x_controlled[t] - x_controlled[t - 1]
        dv = px - states[t - 1][0]  # approx velocity change

        motion_vec = np.array([dx, dv])

        # normalize (avoid explosions)
        norm = np.linalg.norm(motion_vec) + 1e-8
        motion_unit = motion_vec / norm

        # --- projection: how much motion aligns with risk ---
        projection = np.dot(motion_unit, grad_vec)

        # --- correction only along motion direction ---
        correction = strength * projection

        # --- apply ONLY to motion ---
        new_dx = dx - correction

        x_controlled[t + 1] = x_controlled[t] + new_dx

    return x_controlled
