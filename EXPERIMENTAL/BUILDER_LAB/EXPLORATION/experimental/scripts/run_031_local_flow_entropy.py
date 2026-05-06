# ============================================================
# RUN 031 — LOCAL ENTROPY FIELD
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.ndimage import gaussian_filter1d
from collections import defaultdict
from scipy.stats import entropy

# ------------------------------------------------------------
# OUTPUT
# ------------------------------------------------------------
OUTPUT_DIR = "../outputs/run_031_local_entropy"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ------------------------------------------------------------
# SCENARIO (same as before)
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
# BUILD LOCAL TRANSITION DISTRIBUTIONS
# ------------------------------------------------------------
def compute_local_entropy(x, grid_size=40):

    x_min, x_max = x[:,0].min(), x[:,0].max()
    y_min, y_max = x[:,1].min(), x[:,1].max()

    dx = np.gradient(x, axis=0)

    cell_transitions = defaultdict(list)

    # assign transitions to cells
    for i in range(len(x)-1):
        gx = int((x[i,0] - x_min) / (x_max - x_min + 1e-8) * (grid_size-1))
        gy = int((x[i,1] - y_min) / (y_max - y_min + 1e-8) * (grid_size-1))

        # direction angle
        angle = np.arctan2(dx[i,1], dx[i,0])

        cell_transitions[(gx, gy)].append(angle)

    # compute entropy per cell
    entropy_field = np.zeros((grid_size, grid_size))

    for (gx, gy), angles in cell_transitions.items():
        if len(angles) < 3:
            continue

        # histogram of directions
        hist, _ = np.histogram(angles, bins=12, range=(-np.pi, np.pi), density=True)

        # avoid log(0)
        hist += 1e-8

        H = entropy(hist)

        entropy_field[gy, gx] = H

    return entropy_field, (x_min, x_max, y_min, y_max)

# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
print("\n=== RUN 031 — LOCAL ENTROPY FIELD ===\n")

t, V = make_scenario()
x = embedding(t, V)

entropy_field, bounds = compute_local_entropy(x)

x_min, x_max, y_min, y_max = bounds

# ------------------------------------------------------------
# VISUAL 1 — ENTROPY FIELD
# ------------------------------------------------------------
plt.figure(figsize=(8,5))
plt.imshow(
    entropy_field,
    origin="lower",
    extent=[x_min, x_max, y_min, y_max],
    aspect="auto",
    cmap="inferno"
)
plt.colorbar(label="local entropy")
plt.title("Local Flow Entropy (Multi-Valued Regions)")
plt.xlabel("V")
plt.ylabel("dV")

# overlay trajectory
plt.plot(x[:,0], x[:,1], color="white", linewidth=1)

plt.savefig(os.path.join(OUTPUT_DIR, "figure_01_entropy_field.png"))
plt.close()

# ------------------------------------------------------------
# VISUAL 2 — ENTROPY ALONG TRAJECTORY
# ------------------------------------------------------------
entropy_along_path = []

grid_size = entropy_field.shape[0]

for i in range(len(x)):
    gx = int((x[i,0] - x_min) / (x_max - x_min + 1e-8) * (grid_size-1))
    gy = int((x[i,1] - y_min) / (y_max - y_min + 1e-8) * (grid_size-1))

    entropy_along_path.append(entropy_field[gy, gx])

plt.figure(figsize=(8,4))
plt.plot(t, entropy_along_path, color="purple")
plt.title("Entropy along trajectory")
plt.xlabel("time")
plt.ylabel("local entropy")
plt.grid(alpha=0.3)

plt.savefig(os.path.join(OUTPUT_DIR, "figure_02_entropy_timeline.png"))
plt.close()

print(f"Saved to: {OUTPUT_DIR}")
