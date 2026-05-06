"""
NEXAH V7.6 — Controlled Boundary Crossing (Splinter Crossing)

Goal:
→ test if trajectories can cross the splinter boundary
→ measure minimal control needed
→ visualize crossing paths

This is the first ACTIVE INTERVENTION layer
"""

import os
import numpy as np
import matplotlib.pyplot as plt

OUTDIR = "output/v7_6"
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# LOAD DATA
# ============================================================

cost_map = np.load("output/v7_2/cost_map.npy")
Nx = np.load("output/v7_3/nav_field_x.npy")
Ny = np.load("output/v7_3/nav_field_y.npy")

# grid reconstruction
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

def trace_controlled(x0, y0, control_vec, strength=0.5, steps=300, dt=0.12):

    px, py = x0, y0
    traj = []
    crossed = False

    for i in range(steps):

        traj.append((px, py))

        # base navigation field
        vx = sample(px, py, Nx)
        vy = sample(px, py, Ny)

        # add control (constant push direction)
        vx += strength * control_vec[0]
        vy += strength * control_vec[1]

        # normalize
        norm = np.sqrt(vx**2 + vy**2) + 1e-8
        vx /= norm
        vy /= norm

        px += vx * dt
        py += vy * dt

        # check if reached target region
        dist = np.linalg.norm(np.array([px,py]) - TARGET)
        if dist < 0.2:
            crossed = True
            break

        # bounds
        if px < x.min() or px > x.max() or py < y.min() or py > y.max():
            break

    return np.array(traj), crossed

# ============================================================
# START POINTS (FAILURE SIDE)
# ============================================================

starts = [
    (10.5, 27.5),
    (10.2, 26.5),
    (10.8, 28.0),
    (11.0, 27.0),
]

# control directions (probe directions)
controls = [
    np.array([1, 0]),     # push right
    np.array([0.5, -0.5]),
    np.array([0.8, 0.2]),
    np.array([1, -0.2]),
]

# ============================================================
# RUN EXPERIMENT
# ============================================================

plt.figure(figsize=(9,7))

# background
plt.contourf(X, Y, cost_map, levels=60, cmap="viridis", alpha=0.8)

results = []

for s in starts:
    for c in controls:

        traj, success = trace_controlled(s[0], s[1], c)

        if len(traj) > 1:
            if success:
                plt.plot(traj[:,0], traj[:,1], linewidth=2, color="lime")
            else:
                plt.plot(traj[:,0], traj[:,1], linewidth=1.5, color="red")

        results.append((s, c, success))

# target
plt.scatter(TARGET[0], TARGET[1], color="white", s=80, edgecolor="black")

plt.title("V7.6 — Controlled Splinter Crossing")
plt.tight_layout()

plt.savefig(os.path.join(OUTDIR, "v7_6_crossing.png"), dpi=150)
plt.close()

print("✓ V7.6 done →", OUTDIR)
