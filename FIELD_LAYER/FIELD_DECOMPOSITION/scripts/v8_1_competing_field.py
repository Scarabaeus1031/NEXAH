# FIELD_LAYER/field_decomposition/scripts/v8_1_competing_field.py

"""
NEXAH V8.1 — Competing Attractor Field

Goal:
→ introduce real field conflict
→ generate true transition structures
→ recover splinter / gate / separatrix behavior
"""

import os
import numpy as np
import matplotlib.pyplot as plt

OUTDIR = "FIELD_LAYER/field_decomposition/outputs/v8_1"
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# GRID
# ============================================================

nx, ny = 200, 200
x = np.linspace(6, 17, nx)
y = np.linspace(22, 31, ny)
X, Y = np.meshgrid(x, y)

# ============================================================
# POTENTIAL FIELD (2 ATTRACTORS)
# ============================================================

def gaussian(x, y, cx, cy, sigma=1.5):
    return np.exp(-((x - cx)**2 + (y - cy)**2) / (2 * sigma**2))

# Two competing wells
V = (
    -2.0 * gaussian(X, Y, 10.5, 25.0, sigma=1.8)
    -2.0 * gaussian(X, Y, 14.5, 26.5, sigma=1.8)
)

# ============================================================
# GRADIENT
# ============================================================

Vy, Vx = np.gradient(V)

Fx = -Vx
Fy = -Vy

# ============================================================
# ROTATIONAL COMPONENT
# ============================================================

def rotation(x, y, cx, cy):
    dx = x - cx
    dy = y - cy
    return -dy, dx

Rx1, Ry1 = rotation(X, Y, 10.5, 25.0)
Rx2, Ry2 = rotation(X, Y, 14.5, 26.5)

# combine rotation fields
Rx = 0.6 * Rx1 + 0.6 * Rx2
Ry = 0.6 * Ry1 + 0.6 * Ry2

# ============================================================
# FINAL FIELD
# ============================================================

Fx_total = Fx + 0.3 * Rx
Fy_total = Fy + 0.3 * Ry

# normalize
norm = np.sqrt(Fx_total**2 + Fy_total**2) + 1e-8
Fx_total /= norm
Fy_total /= norm

# ============================================================
# PLOT FIELD
# ============================================================

plt.figure(figsize=(10, 7))

plt.contourf(X, Y, V, levels=50, cmap="inferno")

step = 10
plt.quiver(
    X[::step, ::step], Y[::step, ::step],
    Fx_total[::step, ::step], Fy_total[::step, ::step],
    color="white", alpha=0.7
)

plt.title("NEXAH V8.1 — Competing Attractor Field")
plt.colorbar(label="Potential")

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v8_1_field.png"), dpi=150)
plt.close()

# ============================================================
# SIMPLE TRAJECTORY SIMULATION
# ============================================================

def simulate(x0, y0, steps=200, dt=0.1):
    px, py = x0, y0
    traj = []

    for _ in range(steps):
        ix = np.clip(np.searchsorted(x, px) - 1, 0, nx - 1)
        iy = np.clip(np.searchsorted(y, py) - 1, 0, ny - 1)

        vx = Fx_total[iy, ix]
        vy = Fy_total[iy, ix]

        px += vx * dt
        py += vy * dt

        traj.append((px, py))

    return np.array(traj)

# sample trajectories
starts = [
    (9, 29),
    (12, 30),
    (15, 28),
    (11, 24),
    (13, 27),
]

plt.figure(figsize=(10, 7))
plt.contourf(X, Y, V, levels=50, cmap="inferno")

for s in starts:
    traj = simulate(*s)
    plt.plot(traj[:,0], traj[:,1], linewidth=2)

plt.title("NEXAH V8.1 — Competing Flow Trajectories")
plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v8_1_trajectories.png"), dpi=150)
plt.close()

print("✓ V8.1 done →", OUTDIR)
