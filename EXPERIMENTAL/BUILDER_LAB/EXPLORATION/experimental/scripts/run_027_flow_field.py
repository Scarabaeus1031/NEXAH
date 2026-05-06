# ============================================================
# RUN 027 — FLOW FIELD RECONSTRUCTION
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.ndimage import gaussian_filter1d

# ------------------------------------------------------------
# OUTPUT
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR.parent / "outputs" / "run_027_flow_field"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FIG_PATH = OUTPUT_DIR / "figure_01_flow_field.png"


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
# MAIN
# ------------------------------------------------------------
print("\n=== RUN 027 — FLOW FIELD RECONSTRUCTION ===\n")

t, V = make_scenario()
x = embedding(t, V)

# ------------------------------------------------------------
# Compute local velocity vectors
# ------------------------------------------------------------
dx = np.gradient(x, axis=0)

# ------------------------------------------------------------
# Build grid
# ------------------------------------------------------------
grid_size = 25

x_min, x_max = x[:,0].min(), x[:,0].max()
y_min, y_max = x[:,1].min(), x[:,1].max()

gx = np.linspace(x_min, x_max, grid_size)
gy = np.linspace(y_min, y_max, grid_size)

field = np.zeros((grid_size, grid_size, 2))
counts = np.zeros((grid_size, grid_size))

# ------------------------------------------------------------
# Accumulate vectors into grid
# ------------------------------------------------------------
for i in range(len(x)):
    xi, yi = x[i]
    vxi, vyi = dx[i]

    ix = np.searchsorted(gx, xi) - 1
    iy = np.searchsorted(gy, yi) - 1

    if 0 <= ix < grid_size and 0 <= iy < grid_size:
        field[ix, iy] += [vxi, vyi]
        counts[ix, iy] += 1

# ------------------------------------------------------------
# Normalize field
# ------------------------------------------------------------
for i in range(grid_size):
    for j in range(grid_size):
        if counts[i,j] > 0:
            field[i,j] /= counts[i,j]

# ------------------------------------------------------------
# PLOT
# ------------------------------------------------------------
plt.figure(figsize=(8,6))

# plot trajectory
plt.plot(x[:,0], x[:,1], color="lightgray", alpha=0.5)

# plot vector field
for i in range(grid_size):
    for j in range(grid_size):
        if counts[i,j] > 3:
            plt.arrow(
                gx[i], gy[j],
                field[i,j,0], field[i,j,1],
                head_width=0.005,
                color="black",
                alpha=0.6
            )

plt.title("Flow Field Reconstruction (State Space)")
plt.xlabel("V")
plt.ylabel("dV")
plt.grid(alpha=0.3)

plt.savefig(FIG_PATH, dpi=150)
plt.close()

print(f"Saved to: {FIG_PATH}")
