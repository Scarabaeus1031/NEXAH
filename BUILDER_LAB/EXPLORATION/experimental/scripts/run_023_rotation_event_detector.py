import numpy as np
import matplotlib.pyplot as plt
import imageio
import os

from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks

# ------------------------------------------------------------
# OUTPUT
# ------------------------------------------------------------
OUTPUT_DIR = "../outputs/run_026_flowfield_animation"
os.makedirs(OUTPUT_DIR, exist_ok=True)

GIF_PATH = os.path.join(OUTPUT_DIR, "flowfield.gif")

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
# EMBEDDING (same as run_023)
# ------------------------------------------------------------
def embedding(t, V):
    V_s = gaussian_filter1d(V, sigma=2)
    dV = gaussian_filter1d(np.gradient(V_s, t), sigma=2)
    return np.vstack([V_s, dV]).T

# ------------------------------------------------------------
# ROTATION METRIC (same as run_023)
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
t, V = make_scenario()
x = embedding(t, V)

rot = rotation_metric(x)
regions = compute_regions(t)

# rotation events
peaks, _ = find_peaks(rot, height=0.2, distance=5)

# ------------------------------------------------------------
# ANIMATION
# ------------------------------------------------------------
frames = []

fig, ax = plt.subplots(figsize=(6, 5))

for i in range(len(t)):

    ax.clear()

    # trajectory
    ax.plot(x[:i,0], x[:i,1], color="gray", alpha=0.3)

    # colored path
    for j in range(1, i):
        ax.plot(
            [x[j-1,0], x[j,0]],
            [x[j-1,1], x[j,1]],
            color=get_color(regions[j]),
            linewidth=2
        )

    # current point
    ax.scatter(x[i,0], x[i,1], color="black", s=30)

    # rotation events
    for idx in peaks:
        if idx < i:
            ax.scatter(x[idx,0], x[idx,1], color="red", s=50)

    ax.set_title(f"t = {t[i]:.2f}")
    ax.set_xlabel("V")
    ax.set_ylabel("dV")

    ax.set_xlim(np.min(x[:,0])-0.05, np.max(x[:,0])+0.05)
    ax.set_ylim(np.min(x[:,1])-0.02, np.max(x[:,1])+0.02)

    ax.grid(alpha=0.3)

    # NEW buffer (fix warning)
    fig.canvas.draw()
    buffer = fig.canvas.buffer_rgba()
    frame = np.asarray(buffer)

    frames.append(frame)

# save GIF
imageio.mimsave(GIF_PATH, frames, fps=20)

print("\n=== RUN 026 — FLOWFIELD ANIMATION ===")
print(f"Saved to: {GIF_PATH}")
