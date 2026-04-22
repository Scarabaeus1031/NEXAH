# FIELD_LAYER/field_decomposition/scripts/v8_4_decision_outcome_map.py

"""
NEXAH V8.4 — Decision Outcome Map

Goal:
→ test if delay region produces different outcomes
→ classify attractor per starting point

Result:
→ color-coded outcome map
→ reveals if "decision zone" is real or not
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PATHS
# ============================================================

BASE = "FIELD_LAYER/field_decomposition/outputs"
OUTDIR = os.path.join(BASE, "v8_4")
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# LOAD FIELD
# ============================================================

Nx = np.load(os.path.join(BASE, "v7_3", "nav_field_x.npy"))
Ny = np.load(os.path.join(BASE, "v7_3", "nav_field_y.npy"))

ny, nx = Nx.shape

x = np.linspace(6, 17, nx)
y = np.linspace(22, 31, ny)

# ============================================================
# NORMALIZE FIELD
# ============================================================

def normalize(vx, vy):
    n = np.sqrt(vx**2 + vy**2) + 1e-8
    return vx/n, vy/n

Nx, Ny = normalize(Nx, Ny)

# ============================================================
# SAMPLING
# ============================================================

def sample(px, py):
    ix = np.clip(np.searchsorted(x, px) - 1, 0, nx-1)
    iy = np.clip(np.searchsorted(y, py) - 1, 0, ny-1)
    return Nx[iy, ix], Ny[iy, ix]

# ============================================================
# TRAJECTORY SIMULATION
# ============================================================

def simulate(px, py, steps=300, dt=0.12):
    traj = []

    for _ in range(steps):
        vx, vy = sample(px, py)

        px += vx * dt
        py += vy * dt

        traj.append([px, py])

        if px < x.min() or px > x.max() or py < y.min() or py > y.max():
            break

    return np.array(traj)

# ============================================================
# OUTCOME CLASSIFICATION
# ============================================================

def classify_endpoint(px, py):
    # simple 2-attractor split
    if px < 12.5:
        return 0  # left basin
    else:
        return 1  # right basin

# ============================================================
# MAIN GRID
# ============================================================

outcome_map = np.zeros((ny, nx))

for j in range(ny):
    for i in range(nx):

        px = x[i]
        py = y[j]

        traj = simulate(px, py)

        if len(traj) == 0:
            outcome_map[j, i] = -1
            continue

        end_x, end_y = traj[-1]

        outcome_map[j, i] = classify_endpoint(end_x, end_y)

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(10,7))

plt.imshow(
    outcome_map,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin="lower",
    cmap="coolwarm"
)

plt.title("NEXAH V8.4 — Decision Outcome Map")
plt.colorbar(label="0 = left attractor, 1 = right attractor")

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v8_4_outcome_map.png"), dpi=150)
plt.close()

# ============================================================
# SAVE
# ============================================================

np.save(os.path.join(OUTDIR, "outcome_map.npy"), outcome_map)

print("✓ V8.4 done →", OUTDIR)
