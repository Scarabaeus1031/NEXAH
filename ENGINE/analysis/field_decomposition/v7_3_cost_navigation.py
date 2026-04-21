"""
NEXAH V7.3 — Cost Gradient Navigation (Robust Version)

→ loads cost_map if available
→ otherwise builds fallback field
→ computes navigation field = -∇cost
→ traces trajectories
→ saves navigation field for pipeline
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# OUTPUT SETUP
# ============================================================

OUTDIR = "output/v7_3"
os.makedirs(OUTDIR, exist_ok=True)

# ------------------------------------------------------------
# LOAD GRID FROM V7.2 (WICHTIG!)
# ------------------------------------------------------------
x_path = "output/v7_2/grid_x.npy"
y_path = "output/v7_2/grid_y.npy"

if os.path.exists(x_path) and os.path.exists(y_path):
    print("✓ Loaded grid from V7.2")
    x = np.load(x_path)
    y = np.load(y_path)
else:
    print("⚠️ No grid found → using fallback grid")
    x = np.linspace(6, 17, cost_map.shape[1])
    y = np.linspace(22, 31, cost_map.shape[0])

X, Y = np.meshgrid(x, y)

dx = x[1] - x[0]
dy = y[1] - y[0]

# ============================================================
# LOAD OR FALLBACK COST MAP
# ============================================================

cost_path = "output/v7_2/cost_map.npy"

if os.path.exists(cost_path):
    print("✓ Loaded cost_map from V7.2")
    cost_map = np.load(cost_path)
else:
    print("⚠️ No cost_map found → using fallback field")

    def gaussian(x0, y0, strength=1.0, sigma=1.2):
        return strength * np.exp(-((X - x0)**2 + (Y - y0)**2) / (2 * sigma**2))

    V = (
        -2.2 * gaussian(10.6, 25.0, sigma=1.15)
        -2.0 * gaussian(13.5, 26.0, sigma=1.05)
        +1.9 * gaussian(11.5, 28.6, sigma=1.25)
    )

    # crude proxy for cost
    cost_map = np.abs(V)

# save copy (pipeline consistency)
np.save(os.path.join(OUTDIR, "cost_map_used.npy"), cost_map)

# ============================================================
# GRADIENT → NAVIGATION FIELD
# ============================================================

dC_dy, dC_dx = np.gradient(cost_map)

# scale correctly
dC_dx /= dx
dC_dy /= dy

# downhill navigation
Nx = -dC_dx
Ny = -dC_dy

# normalize
norm = np.sqrt(Nx**2 + Ny**2) + 1e-8
Nx /= norm
Ny /= norm

# save navigation field
np.save(os.path.join(OUTDIR, "nav_field_x.npy"), Nx)
np.save(os.path.join(OUTDIR, "nav_field_y.npy"), Ny)

# ============================================================
# SAMPLING FUNCTION
# ============================================================

def sample(px, py, A):
    ix = np.clip(np.searchsorted(x, px) - 1, 0, len(x)-1)
    iy = np.clip(np.searchsorted(y, py) - 1, 0, len(y)-1)
    return A[iy, ix]

# ============================================================
# TRAJECTORY TRACING
# ============================================================

def trace_path(x0, y0, steps=300, dt=0.12):
    px, py = x0, y0
    traj = []

    for i in range(steps):
        traj.append((px, py))

        vx = sample(px, py, Nx)
        vy = sample(px, py, Ny)

        # slow down near target
        dist = np.sqrt((px - 13)**2 + (py - 26)**2)
        speed_scale = 0.7 * (1 + dist)

        px += vx * dt * speed_scale
        py += vy * dt * speed_scale

        # stop near target
        if dist < 0.15:
            break

        # stop if out of bounds
        if px < x.min() or px > x.max() or py < y.min() or py > y.max():
            break

    return np.array(traj)

# ============================================================
# START POINTS
# ============================================================

starts = [
    (7, 28),
    (8, 24),
    (10, 30),
    (15, 26),
    (11, 23),
    (9, 27),
    (6.5, 26),
    (16, 28)
]

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(9,7))

# cost background
plt.contourf(X, Y, cost_map, levels=60, cmap="viridis", alpha=0.85)

# vector field
plt.quiver(
    X[::10,::10], Y[::10,::10],
    Nx[::10,::10], Ny[::10,::10],
    color="white", alpha=0.6
)

# trajectories
for s in starts:
    traj = trace_path(*s)
    if len(traj) > 1:
        plt.plot(traj[:,0], traj[:,1], linewidth=2)

# target
plt.scatter([13], [26], color="white", s=80, edgecolor="black", label="Target")

plt.title("NEXAH V7.3 — Cost Navigation Field")
plt.legend()
plt.tight_layout()

plt.savefig(os.path.join(OUTDIR, "v7_3_navigation.png"), dpi=150)
plt.close()

print("✓ V7.3 done →", OUTDIR)
