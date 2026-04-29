# ============================================================
# RUN 026 v2 — MULTILAYER FLOW ANIMATION
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import os

from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks


# ------------------------------------------------------------
# OUTPUT
# ------------------------------------------------------------
OUTPUT_DIR = "../outputs/run_026_multilayer_animation"
os.makedirs(OUTPUT_DIR, exist_ok=True)

GIF_PATH = os.path.join(OUTPUT_DIR, "multilayer_flow.gif")


# ------------------------------------------------------------
# SCENARIO (same as run_023)
# ------------------------------------------------------------
def make_scenario(n=500):
    t = np.linspace(0, 100, n)
    V = 1.0 - 0.002 * t - 0.0005 * t**2

    V += 0.015 * np.exp((t - 16) / 4.0) * (t < 25)
    V += 0.01 * np.sin(0.8 * t) * (t < 25)

    return t, V


# ------------------------------------------------------------
# EMBEDDING
# ------------------------------------------------------------
def embedding(t, V):
    V_s = gaussian_filter1d(V, sigma=2)
    dV = gaussian_filter1d(np.gradient(V_s, t), sigma=2)
    return np.vstack([V_s, dV]).T


# ------------------------------------------------------------
# ROTATION METRIC (real one)
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
# REGIONS (simple proxy for now)
# ------------------------------------------------------------
def compute_regions(t):
    regions = []
    for ti in t:
        if ti < 70:
            regions.append("stable")
        elif ti < 85:
            regions.append("transition")
        else:
            regions.append("collapse")
    return regions


def get_color(region):
    if region == "stable":
        return "blue"
    elif region == "transition":
        return "orange"
    else:
        return "red"


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
print("\n=== RUN 026 v2 — MULTILAYER FLOW ANIMATION ===\n")

t, V = make_scenario()
x = embedding(t, V)

rot = rotation_metric(x)
regions = compute_regions(t)

# rotation events
peaks, _ = find_peaks(rot, height=0.2, distance=5)

frames = []

fig, axs = plt.subplots(3, 1, figsize=(6, 10))

# ------------------------------------------------------------
# FRAME LOOP
# ------------------------------------------------------------
for i in range(10, len(t), 3):  # step size reduziert für Performance

    for ax in axs:
        ax.clear()

    # ========================================================
    # (1) TIME / ROTATION SIGNAL
    # ========================================================
    axs[0].plot(t[:i], rot[:i], color="blue")

    # events
    for idx in peaks:
        if idx < i:
            axs[0].scatter(t[idx], rot[idx], color="red")

    axs[0].set_title("Rotation Signal")
    axs[0].set_xlim(0, t[-1])
    axs[0].set_ylim(0, np.max(rot)*1.2)
    axs[0].grid(alpha=0.3)


    # ========================================================
    # (2) STATE SPACE
    # ========================================================
    axs[1].plot(x[:i,0], x[:i,1], color="gray", alpha=0.3)

    # colored trajectory
    for j in range(1, i):
        axs[1].plot(
            [x[j-1,0], x[j,0]],
            [x[j-1,1], x[j,1]],
            color=get_color(regions[j]),
            linewidth=2
        )

    # current point
    axs[1].scatter(x[i,0], x[i,1], color="black", s=40)

    # rotation events in state space
    for idx in peaks:
        if idx < i:
            axs[1].scatter(x[idx,0], x[idx,1], color="red", s=50)

    axs[1].set_title("State Space (V, dV)")
    axs[1].set_xlabel("V")
    axs[1].set_ylabel("dV")
    axs[1].grid(alpha=0.3)


    # ========================================================
    # (3) REGIME TIMELINE
    # ========================================================
    region_values = [
        0 if r=="stable" else 1 if r=="transition" else 2
        for r in regions[:i]
    ]

    axs[2].plot(t[:i], region_values, color="green")

    axs[2].set_yticks([0,1,2])
    axs[2].set_yticklabels(["stable", "transition", "collapse"])
    axs[2].set_xlim(0, t[-1])
    axs[2].set_title("Regime Timeline")
    axs[2].grid(alpha=0.3)


    # ========================================================
    # FRAME CAPTURE (FIXED)
    # ========================================================
    fig.canvas.draw()
    buffer = fig.canvas.buffer_rgba()
    frame = np.asarray(buffer)

    frames.append(frame)


# ------------------------------------------------------------
# SAVE GIF
# ------------------------------------------------------------
imageio.mimsave(GIF_PATH, frames, fps=15)

print(f"Saved to: {GIF_PATH}")
