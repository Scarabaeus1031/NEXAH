# ============================================================
# RUN 023 — ROTATION EVENT DETECTOR
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks


# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------
OUT_DIR = Path("outputs/run_023_rotation_events")
OUT_DIR.mkdir(parents=True, exist_ok=True)


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
    print("\n=== RUN 023 — ROTATION EVENT DETECTOR ===\n")

    t, V = make_scenario()
    x = embedding(t, V)

    rot = rotation_metric(x)

    # --------------------------------------------------------
    # Detect peaks (rotation events)
    # --------------------------------------------------------
    peaks, props = find_peaks(rot, height=0.2, distance=5)

    print("Number of rotation events:", len(peaks))
    print("Event times:", t[peaks])

    # --------------------------------------------------------
    # PLOT 1 — rotation + events
    # --------------------------------------------------------
    plt.figure(figsize=(10,5))
    plt.plot(t, rot, label="rotation signal")
    plt.scatter(t[peaks], rot[peaks], color="red", label="events")

    plt.title("Rotation Events Detection")
    plt.legend()
    plt.grid(alpha=0.3)

    plt.savefig(OUT_DIR / "figure_01_rotation_events.png", dpi=150)
    plt.close()

    # --------------------------------------------------------
    # PLOT 2 — zoom into transition
    # --------------------------------------------------------
    plt.figure(figsize=(10,5))
    mask = (t > 0) & (t < 40)

    plt.plot(t[mask], rot[mask])
    plt.scatter(t[peaks], rot[peaks], color="red")

    plt.title("Rotation Events (Transition Phase)")
    plt.grid(alpha=0.3)

    plt.savefig(OUT_DIR / "figure_02_transition_zoom.png", dpi=150)
    plt.close()

    print(f"\nSaved to: {OUT_DIR}")
