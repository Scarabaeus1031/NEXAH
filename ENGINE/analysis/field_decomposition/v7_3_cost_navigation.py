"""
NEXAH V7.3 — Cost Gradient Navigation

Uses the cost_map from V7.2 and computes:

→ navigation field = -∇cost

This represents optimal flow toward the target.
"""

import os
import numpy as np
import matplotlib.pyplot as plt

OUTDIR = "output/v7_3"
os.makedirs(OUTDIR, exist_ok=True)

# ------------------------------------------------------------
# LOAD COST MAP (or recompute inline if needed)
# ------------------------------------------------------------

# fallback: load from file if saved
cost_map = np.load("output/v7_2/cost_map.npy")
np.save(os.path.join(OUTDIR, "cost_map.npy"), cost_map)

# grid (must match V7.2)
x = np.linspace(6, 17, cost_map.shape[1])
y = np.linspace(22, 31, cost_map.shape[0])
X, Y = np.meshgrid(x, y)

dx = x[1] - x[0]
dy = y[1] - y[0]

# ------------------------------------------------------------
# GRADIENT → NAVIGATION FIELD
# ------------------------------------------------------------
dCdy, dCdx = np.gradient(cost_map, dy, dx)

# negative gradient = direction of decreasing cost
Nx = -dCdx
Ny = -dCdy

# normalize for visualization
norm = np.sqrt(Nx**2 + Ny**2) + 1e-6
Nx /= norm
Ny /= norm

# ------------------------------------------------------------
# TRAJECTORY IN NAVIGATION FIELD
# ------------------------------------------------------------
def sample(px, py, A):
    ix = np.clip(np.searchsorted(x, px) - 1, 0, len(x)-1)
    iy = np.clip(np.searchsorted(y, py) - 1, 0, len(y)-1)
    return A[iy, ix]

def trace_path(x0, y0, steps=200, dt=0.1):
    px, py = x0, y0
    traj = []

    for i in range(steps):
        traj.append((px, py))

        vx = sample(px, py, Nx)
        vy = sample(px, py, Ny)

        px += vx * dt
        py += vy * dt

        if px < x.min() or px > x.max() or py < y.min() or py > y.max():
            break

    return np.array(traj)

# sample starting points
starts = [
    (7, 28),
    (8, 24),
    (12, 30),
    (15, 26),
    (10, 23)
]

# ------------------------------------------------------------
# PLOT
# ------------------------------------------------------------
plt.figure(figsize=(8,6))

plt.contourf(X, Y, cost_map, levels=40, cmap="viridis", alpha=0.7)

# vector field
plt.quiver(X[::10,::10], Y[::10,::10],
           Nx[::10,::10], Ny[::10,::10],
           color="white", alpha=0.6)

# trajectories
for s in starts:
    traj = trace_path(*s)
    plt.plot(traj[:,0], traj[:,1], linewidth=2)

plt.title("V7.3 — Cost Navigation Field")
plt.tight_layout()

plt.savefig(os.path.join(OUTDIR, "v7_3_navigation.png"), dpi=150)
plt.close()

print("V7.3 done →", OUTDIR)
