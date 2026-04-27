# ============================================================
# 🧭 NEXAH — State Space Control (v5.1 STABLE)
# ============================================================
#
# Goal:
# Stabilize field-based control in (x, v) space
# without numerical explosion.
#
# Key Fix:
# → bounded control
# → blending instead of overriding dynamics
# → gradient normalization
#
# ============================================================

import numpy as np


# ------------------------------------------------------------
# STATE SPACE
# ------------------------------------------------------------

def build_state_space(x):
    v = np.gradient(x)
    return np.stack([x, v], axis=1)


# ------------------------------------------------------------
# FIELD (density + gradient)
# ------------------------------------------------------------

def compute_density_field(states, bins=40):
    x = states[:, 0]
    v = states[:, 1]

    H, xedges, yedges = np.histogram2d(x, v, bins=bins)
    H = H.T  # correct orientation

    # small smoothing to avoid zero gradients
    H = H + 1e-6

    grad_y, grad_x = np.gradient(H)

    return H, grad_x, grad_y, xedges, yedges


# ------------------------------------------------------------
# CORE CONTROL LOGIC
# ------------------------------------------------------------

def apply_state_space_control(
    x,
    risk,
    strength=0.1,
    threshold=0.8,
    bins=40
):
    """
    Apply stable trajectory-aligned control.

    Parameters
    ----------
    x : np.ndarray
        input signal
    risk : np.ndarray
        risk signal (same length)
    strength : float
        control strength
    threshold : float
        activation threshold
    bins : int
        grid resolution

    Returns
    -------
    x_controlled : np.ndarray
    """

    states = build_state_space(x)
    _, grad_x, grad_y, xedges, yedges = compute_density_field(states, bins)

    x_controlled = x.copy()

    for t in range(2, len(x) - 1):

        # activate only on high-risk
        if risk[t] < threshold:
            continue

        px, pv = states[t]

        ix = np.searchsorted(xedges, px) - 1
        iy = np.searchsorted(yedges, pv) - 1

        if not (0 <= ix < bins and 0 <= iy < bins):
            continue

        # --- local gradient ---
        gx = grad_x[ix, iy]
        gy = grad_y[ix, iy]

        grad_vec = np.array([gx, gy])

        # --- current motion ---
        dx = x_controlled[t] - x_controlled[t - 1]

        # -------------------------
        # 🔥 STABILITY FIXES
        # -------------------------

        # 1. limit motion
        dx = np.clip(dx, -1.0, 1.0)

        # 2. normalize gradient
        grad_norm = np.linalg.norm(grad_vec) + 1e-8
        grad_unit = grad_vec / grad_norm

        # 3. bounded correction
        correction = strength * dx * grad_unit[0]
        correction = np.clip(correction, -0.1, 0.1)

        # 4. blend (CRITICAL)
        new_dx = (1 - strength) * dx - correction

        # integrate
        x_controlled[t + 1] = x_controlled[t] + new_dx

    return x_controlled


# ------------------------------------------------------------
# OPTIONAL: INTERNAL TEST (standalone)
# ------------------------------------------------------------

def _demo():
    import matplotlib.pyplot as plt

    # simple signal
    t = np.linspace(0, 20, 500)
    x = np.sin(t) + 0.3 * np.sin(5 * t)

    # simple risk
    flow = np.abs(np.gradient(x))
    accel = np.abs(np.gradient(flow))
    risk = flow * accel
    risk = (risk - np.min(risk)) / (np.max(risk) + 1e-8)

    x_ctrl = apply_state_space_control(x, risk)

    plt.figure(figsize=(12, 5))
    plt.plot(x, label="Original")
    plt.plot(x_ctrl, "--", label="Controlled")

    peaks = np.where(risk > 0.8)[0]
    plt.scatter(peaks, x[peaks], color="red", label="High Risk")

    plt.legend()
    plt.title("State Space Control v5.1")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    _demo()
