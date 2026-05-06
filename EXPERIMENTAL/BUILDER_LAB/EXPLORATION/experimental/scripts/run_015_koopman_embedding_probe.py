# ============================================================
# RUN 021 — ROTATION / PHASE METRIC (EXPERIMENTAL)
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d


# ------------------------------------------------------------
# Synthetic scenario
# ------------------------------------------------------------
def make_scenario(n=500):
    t = np.linspace(0, 100, n)
    V = 1.0 - 0.002 * t - 0.0005 * t**2

    V += 0.015 * np.exp((t - 16) / 4.0) * (t < 25)
    V += 0.01 * np.sin(0.8 * t) * (t < 25)

    return t, V


# ------------------------------------------------------------
# Embedding
# ------------------------------------------------------------
def embedding(t, V):
    V_s = gaussian_filter1d(V, sigma=2)
    dV = gaussian_filter1d(np.gradient(V_s, t), sigma=2)

    return np.vstack([V_s, dV]).T


# ------------------------------------------------------------
# Rotation metric
# ------------------------------------------------------------
def rotation_metric(x):
    dx = np.gradient(x, axis=0)

    angles = []

    for i in range(1, len(dx)):
        v1 = dx[i-1]
        v2 = dx[i]

        norm = (np.linalg.norm(v1) * np.linalg.norm(v2)) + 1e-8
        cos_theta = np.dot(v1, v2) / norm

        cos_theta = np.clip(cos_theta, -1, 1)
        angle = np.arccos(cos_theta)

        angles.append(angle)

    return np.array([0] + angles)


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
if __name__ == "__main__":
    print("\n=== RUN 021 — ROTATION METRIC ===\n")

    t, V = make_scenario()
    x = embedding(t, V)

    rot = rotation_metric(x)

    print("mean rotation:", np.mean(rot))
    print("max rotation:", np.max(rot))

    # --------------------------------------------------------
    # Plot
    # --------------------------------------------------------
    plt.figure(figsize=(10,5))
    plt.plot(t, rot, label="rotation signal")
    plt.title("Rotation / Phase Signal")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.show()
