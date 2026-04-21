"""
NEXAH V7.3 — Cost Gradient Navigation (Stable Version)

→ uses cost_map from V7.2
→ builds navigation field = -∇cost
→ traces optimal paths toward target
"""

import os
import numpy as np
import matplotlib.pyplot as plt

OUTDIR = "output/v7_3"
os.makedirs(OUTDIR, exist_ok=True)

# ------------------------------------------------------------
# LOAD COST MAP
# ------------------------------------------------------------
cost_map = np.load("output/v7_2/cost_map.npy")

# grid reconstruction
nx, ny = cost_map.shape[1], cost_map.shape[0]

x = np.linspace(6, 17, nx)
y = np.linspace(22, 31, ny)
X, Y = np.meshgrid(x, y)

dx = x[1] - x[0]
dy = y[1] - y[0]

# ------------------------------------------------------------
# GRADIENT (FIXED)
# ------------------------------------------------------------
# NOTE: order is (axis_y, axis_x)
dC_dy, dC_dx = np.gradient(cost_map)

# scale with spacing
dC_dx /= dx
dC_dy /= dy

# navigation field = downhill
Nx = -dC_dx
Ny = -dC_dy

# normalize (important for stability)
norm = np.sqrt(Nx**2 + Ny**2) + 1e-8
Nx /= norm
Ny /= norm

# ------------------------------------------------------------
# SAMPLING FUNCTION
# ------------------------------------------------------------
def sample(px, py, A):
    ix = np.clip(np.searchsorted(x, px) - 1, 0, len(x)-1)
    iy = np.clip(np.searchsorted(y, py) - 1, 0, len(y)-1)
    return A[iy, ix]

# ------------------------------------------------------------
# TRAJECTORY TRACING
# ------------------------------------------------------------
def trace_path(x0, y0, steps=250, dt=0.12):
    px, py = x0, y0
    traj = []

    for i in range(steps):
        traj.append((px, py))

        vx = sample(px, py, Nx)
        vy = sample(px, py, Ny)

        # adaptive slowdown near target
        speed_scale = 0.7
        px += vx * dt * speed_scale
        py += vy * dt * speed_scale

        # stop if near target
        if np.sqrt((px - 13)**2 + (py - 26)**2) < 0.2:
            break

    return np.array(traj)

# ------------------------------------------------------------
# START POINTS
# ------------------------------------------------------------
starts = [
    (7, 28),
    (8, 24),
    (10, 30),
    (15, 26),
    (11, 23),
    (9, 27)
]

# ------------------------------------------------------------
# PLOT
# ------------------------------------------------------------
plt.figure(figsize=(9,7))

# cost background
plt.contourf(X, Y, cost_map, levels=50, cmap="viridis", alpha=0.8)

# vector field
plt.quiver(X[::10,::10], Y[::10,::10],
           Nx[::10,::10], Ny[::10,::10],
           color="white", alpha=0.6)

# trajectories
for s in starts:
    traj = trace_path(*s)
    if len(traj) > 1:
        plt.plot(traj[:,0], traj[:,1], linewidth=2)

# target
plt.scatter([13], [26], color="white", s=60, label="Target")

plt.title("V7.3 — Cost Navigation Field")
plt.legend()
plt.tight_layout()

plt.savefig(os.path.join(OUTDIR, "v7_3_navigation.png"), dpi=150)
plt.close()

print("V7.3 done →", OUTDIR)
