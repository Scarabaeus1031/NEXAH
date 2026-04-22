"""
NEXAH V7.7 — Minimal Control Energy Map

Goal:
→ compute minimal control strength needed to reach target
→ reveal weak spots in splinter boundary
→ quantify barrier hardness
"""

import os
import numpy as np
import matplotlib.pyplot as plt

OUTDIR = "output/v7_7"
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# LOAD DATA
# ============================================================

cost_map = np.load("output/v7_2/cost_map.npy")
Nx = np.load("output/v7_3/nav_field_x.npy")
Ny = np.load("output/v7_3/nav_field_y.npy")

nx, ny = cost_map.shape[1], cost_map.shape[0]

x = np.linspace(6, 17, nx)
y = np.linspace(22, 31, ny)
X, Y = np.meshgrid(x, y)

TARGET = np.array([13, 26])

# ============================================================
# SAMPLING
# ============================================================

def sample(px, py, A):
    ix = np.clip(np.searchsorted(x, px) - 1, 0, len(x)-1)
    iy = np.clip(np.searchsorted(y, py) - 1, 0, len(y)-1)
    return A[iy, ix]

# ============================================================
# CONTROLLED TRAJECTORY
# ============================================================

def reaches_target(x0, y0, control_vec, strength, steps=250, dt=0.12):

    px, py = x0, y0

    for i in range(steps):

        vx = sample(px, py, Nx)
        vy = sample(px, py, Ny)

        # apply control
        vx += strength * control_vec[0]
        vy += strength * control_vec[1]

        norm = np.sqrt(vx**2 + vy**2) + 1e-8
        vx /= norm
        vy /= norm

        px += vx * dt
        py += vy * dt

        dist = np.linalg.norm(np.array([px,py]) - TARGET)
        if dist < 0.2:
            return True

        if px < x.min() or px > x.max() or py < y.min() or py > y.max():
            return False

    return False

# ============================================================
# CONTROL DIRECTIONS (important!)
# ============================================================

control_dirs = [
    np.array([1, 0]),
    np.array([0.8, -0.3]),
    np.array([0.8, 0.3]),
    np.array([0.5, -0.5]),
]

# ============================================================
# ENERGY MAP
# ============================================================

energy_map = np.full_like(cost_map, np.nan)

strength_levels = np.linspace(0.0, 2.0, 20)

for i in range(nx):
    for j in range(ny):

        px = x[i]
        py = y[j]

        found = False

        for c in control_dirs:
            for s in strength_levels:

                if reaches_target(px, py, c, s):
                    energy_map[j, i] = s
                    found = True
                    break

            if found:
                break

# replace NaN (unreachable)
energy_map = np.nan_to_num(energy_map, nan=2.5)

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(9,7))

plt.contourf(X, Y, energy_map, levels=50, cmap="inferno")

plt.scatter(TARGET[0], TARGET[1], color="cyan", s=80, edgecolor="black")

plt.title("NEXAH V7.7 — Minimal Control Energy Map")
plt.colorbar(label="control strength required")

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v7_7_energy_map.png"), dpi=150)
plt.close()

print("✓ V7.7 done →", OUTDIR)
