"""
NEXAH V7.8 — Optimal Crossing Direction Field

Goal:
→ find best control direction per point
→ minimal energy direction for reaching target
→ visualize optimal crossing vector field
"""

import os
import numpy as np
import matplotlib.pyplot as plt

OUTDIR = "output/v7_8"
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
# TRAJECTORY TEST
# ============================================================

def reaches_target(x0, y0, control_vec, strength, steps=200, dt=0.12):

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

        if np.linalg.norm([px - TARGET[0], py - TARGET[1]]) < 0.2:
            return True

        if px < x.min() or px > x.max() or py < y.min() or py > y.max():
            return False

    return False

# ============================================================
# DIRECTION CANDIDATES (dense!)
# ============================================================

angles = np.linspace(0, 2*np.pi, 16)
dirs = np.stack([np.cos(angles), np.sin(angles)], axis=1)

strength_levels = np.linspace(0.0, 2.0, 15)

# ============================================================
# RESULT FIELDS
# ============================================================

best_dx = np.zeros_like(cost_map)
best_dy = np.zeros_like(cost_map)
best_energy = np.full_like(cost_map, np.inf)

# ============================================================
# MAIN LOOP
# ============================================================

for i in range(nx):
    for j in range(ny):

        px = x[i]
        py = y[j]

        for d in dirs:
            for s in strength_levels:

                if reaches_target(px, py, d, s):

                    if s < best_energy[j, i]:
                        best_energy[j, i] = s
                        best_dx[j, i] = d[0]
                        best_dy[j, i] = d[1]

                    break  # stop increasing strength

# clean unreachable
best_energy[np.isinf(best_energy)] = 2.5

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(9,7))

# energy background
plt.contourf(X, Y, best_energy, levels=50, cmap="inferno")

# direction field (downsample)
step = 10
plt.quiver(
    X[::step,::step], Y[::step,::step],
    best_dx[::step,::step], best_dy[::step,::step],
    color="white", alpha=0.7
)

# target
plt.scatter(TARGET[0], TARGET[1], color="cyan", s=80, edgecolor="black")

plt.title("NEXAH V7.8 — Optimal Crossing Direction Field")
plt.colorbar(label="minimal control energy")

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v7_8_optimal_direction.png"), dpi=150)
plt.close()

print("✓ V7.8 done →", OUTDIR)
