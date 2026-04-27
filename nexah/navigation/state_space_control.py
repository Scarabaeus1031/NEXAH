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
# SIGNAL
# ------------------------------------------------------------

def generate_signal(n=500):
    t = np.linspace(0, 20, n)
    x = np.sin(t) + 0.3 * np.sin(5 * t)
    return x


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
    H = H.T  # orientation

    # smooth a bit (optional but helps)
    H = H + 1e-6

    grad_y, grad_x = np.gradient(H)

    return H, grad_x, grad_y, xedges, yedges


# ------------------------------------------------------------
# CONTROL (STABLE VERSION)
# ------------------------------------------------------------

def run_state_space_control(
    strength=0.15,
    threshold=0.8,
    bins=40
):
    x = generate_signal()
    states = build_state_space(x)

    # --- FIELD ---
    H, grad_x, grad_y, xedges, yedges = compute_density_field(states, bins)

    # --- simple risk ---
    flow = np.abs(np.gradient(x))
    accel = np.abs(np.gradient(flow))
    risk = flow * accel
    risk = (risk - np.min(risk)) / (np.max(risk) + 1e-8)

    x_controlled = x.copy()

    for t in range(2, len(x) - 1):
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

        # --- current movement ---
        dx = x_controlled[t] - x_controlled[t - 1]

        # -------------------------
        # 🔥 STABILITY FIXES
        # -------------------------

        # 1. limit raw movement
        dx = np.clip(dx, -1.0, 1.0)

        # 2. normalize gradient
        grad_norm = np.linalg.norm(grad_vec) + 1e-8
        grad_unit = grad_vec / grad_norm

        # 3. compute bounded correction
        correction = strength * dx * grad_unit[0]

        correction = np.clip(correction, -0.1, 0.1)

        # 4. blend instead of override
        new_dx = (1 - strength) * dx - correction

        # --- integrate ---
        x_controlled[t + 1] = x_controlled[t] + new_dx

    return x, x_controlled, risk


# ------------------------------------------------------------
# DEMO PLOT
# ------------------------------------------------------------

def plot_state_space_control():
    import matplotlib.pyplot as plt

    x, x_ctrl, risk = run_state_space_control()

    plt.figure(figsize=(12, 5))

    plt.plot(x, label="Original", alpha=0.7)
    plt.plot(x_ctrl, label="Controlled", linestyle="--")

    # high-risk points
    threshold = 0.8
    peaks = np.where(risk > threshold)[0]

    plt.scatter(peaks, x[peaks], color="red", s=20, label="High Risk")

    plt.title("State Space Control (v5.1 — Stable)")
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_state_space_control()

# ------------------------------------------------------------
# PUBLIC API (for demos / pipelines)
# ------------------------------------------------------------

def apply_state_space_control(**kwargs):
    """
    Standard interface for external modules (demo / pipeline).

    Returns:
        x, x_controlled, risk
    """
    return run_state_space_control(**kwargs)
