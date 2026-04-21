"""
NEXAH V6.7 — Class Detection / Transition Map

Goal:
Turn the dual-AXIOM + drift field into a class map.

This version classifies trajectories into:
- left basin capture
- right basin capture
- upper/source region influence
- transition corridor
- escape / collapse tendency

This is not a physics claim.
It is a structural-dynamical analysis layer.
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# OUTPUT SETUP
# ============================================================

OUTDIR = "output/v6_7"
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# GRID
# ============================================================

x = np.linspace(6, 17, 240)
y = np.linspace(22, 31, 220)
X, Y = np.meshgrid(x, y)

# ============================================================
# FIELD DEFINITION
# ============================================================

def gaussian(x0, y0, strength=1.0, sigma=1.2):
    return strength * np.exp(-((X - x0) ** 2 + (Y - y0) ** 2) / (2 * sigma ** 2))

# Dual basin + upper source
V = (
    -2.2 * gaussian(10.6, 25.0, sigma=1.15)   # left basin
    -2.0 * gaussian(13.5, 26.0, sigma=1.05)   # right basin
    +1.9 * gaussian(11.5, 28.6, sigma=1.25)   # upper ridge/source
)

# gradient (note axis order!)
dVdy, dVdx = np.gradient(V, y, x)

# ============================================================
# DRIFT (ASYMMETRY)
# ============================================================

epsilon = 0.10

# rotational + directional drift (break symmetry)
Dx = epsilon * (-(Y - 26.5))
Dy = epsilon * ( (X - 11.5))

# total flow field
Fx = -dVdx + Dx
Fy = -dVdy + Dy

# ============================================================
# TRAJECTORY SIMULATION
# ============================================================

def simulate_trajectory(x0, y0, steps=400, dt=0.05):
    traj = []
    x_t, y_t = x0, y0

    for _ in range(steps):
        ix = np.clip(np.searchsorted(x, x_t) - 1, 0, len(x) - 1)
        iy = np.clip(np.searchsorted(y, y_t) - 1, 0, len(y) - 1)

        vx = Fx[iy, ix]
        vy = Fy[iy, ix]

        x_t += vx * dt
        y_t += vy * dt

        traj.append((x_t, y_t))

        # stop if out of bounds
        if x_t < x.min() or x_t > x.max() or y_t < y.min() or y_t > y.max():
            break

    return np.array(traj)

# ============================================================
# CLASSIFICATION FUNCTION
# ============================================================

def classify_trajectory(traj):
    if len(traj) == 0:
        return 4  # escape

    x_end, y_end = traj[-1]

    # distances to basins
    d_left = np.hypot(x_end - 10.6, y_end - 25.0)
    d_right = np.hypot(x_end - 13.5, y_end - 26.0)
    d_top = np.hypot(x_end - 11.5, y_end - 28.6)

    if d_left < 0.6:
        return 1  # left basin
    elif d_right < 0.6:
        return 2  # right basin
    elif d_top < 0.8:
        return 3  # upper influence
    else:
        return 0  # transition / corridor

# ============================================================
# CLASS MAP
# ============================================================

class_map = np.zeros_like(X)

for i in range(0, len(x), 4):
    for j in range(0, len(y), 4):
        traj = simulate_trajectory(x[i], y[j])
        c = classify_trajectory(traj)
        class_map[j, i] = c

# ============================================================
# VISUALIZATION
# ============================================================

fig, axs = plt.subplots(1, 2, figsize=(14, 6))

# --- Q1: Class Map
im = axs[0].imshow(
    class_map,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin="lower",
    cmap="tab10",
    alpha=0.9
)
axs[0].set_title("Q1 — Class Map")
axs[0].set_xlabel("x")
axs[0].set_ylabel("y")

# --- Q2: Field + Sample Trajectories
axs[1].contourf(X, Y, V, levels=40, cmap="cividis")

# streamlines
axs[1].streamplot(x, y, Fx, Fy, color="white", density=1.2, linewidth=0.7)

# sample trajectories
starts = [
    (8, 28),   # upper-left
    (12, 27),  # center
    (10, 23),  # lower
    (15, 29)   # upper-right
]

for (sx, sy) in starts:
    traj = simulate_trajectory(sx, sy)
    if len(traj) > 0:
        axs[1].plot(traj[:, 0], traj[:, 1], linewidth=2)

axs[1].set_title("Q2 — Field + Trajectories")
axs[1].set_xlabel("x")
axs[1].set_ylabel("y")

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v6_7_class_map.png"), dpi=160)
plt.close()

# ============================================================
# SAVE META
# ============================================================

meta = {
    "version": "6.7",
    "epsilon": epsilon,
    "classes": {
        "0": "transition corridor",
        "1": "left basin",
        "2": "right basin",
        "3": "upper influence",
        "4": "escape"
    }
}

with open(os.path.join(OUTDIR, "meta.json"), "w") as f:
    json.dump(meta, f, indent=2)

print("V6.7 complete → outputs saved in:", OUTDIR)
