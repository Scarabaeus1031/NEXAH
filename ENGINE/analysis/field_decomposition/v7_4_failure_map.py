"""
NEXAH V7.4 — Failure Map (Reachability / Separatrix Detection)

Goal
-----

Classify the field into:

→ reaches target (success)
→ gets trapped (failure)

This reveals the true decision boundary (splinter / separatrix).

This is NOT a physics claim.
It is a structural navigation analysis layer.
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# OUTPUT
# ============================================================

OUTDIR = "output/v7_4"
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# GRID (must match V7.2 / V7.3)
# ============================================================

nx, ny = 200, 200

x = np.linspace(6, 17, nx)
y = np.linspace(22, 31, ny)
X, Y = np.meshgrid(x, y)

dx = x[1] - x[0]
dy = y[1] - y[0]

TARGET = np.array([13.0, 26.0])

# ============================================================
# LOAD NAV FIELD (from V7.3)
# ============================================================

nav_x_path = "output/v7_3/nav_field_x.npy"
nav_y_path = "output/v7_3/nav_field_y.npy"

if os.path.exists(nav_x_path) and os.path.exists(nav_y_path):
    print("✓ Loaded navigation field from V7.3")
    Nx = np.load(nav_x_path)
    Ny = np.load(nav_y_path)
else:
    raise RuntimeError("❌ Run V7.3 first to generate nav_field_x/y.npy")

# ============================================================
# SAMPLING
# ============================================================

def sample(px, py, A):
    ix = np.clip(np.searchsorted(x, px) - 1, 0, len(x)-1)
    iy = np.clip(np.searchsorted(y, py) - 1, 0, len(y)-1)
    return A[iy, ix]

# ============================================================
# SIMULATION
# ============================================================

def simulate(px, py, steps=300, dt=0.12):

    for i in range(steps):

        vx = sample(px, py, Nx)
        vy = sample(px, py, Ny)

        px += vx * dt
        py += vy * dt

        # distance to target
        dist = np.sqrt((px - TARGET[0])**2 + (py - TARGET[1])**2)

        # SUCCESS
        if dist < 0.25:
            return 1

        # FAILURE: stuck region (low motion)
        if np.sqrt(vx**2 + vy**2) < 0.01:
            return 0

        # out of bounds = failure
        if px < x.min() or px > x.max() or py < y.min() or py > y.max():
            return 0

    # timeout = failure
    return 0

# ============================================================
# BUILD FAILURE MAP
# ============================================================

print("→ Computing reachability map...")

failure_map = np.zeros((ny, nx))

for i in range(nx):
    for j in range(ny):

        px = x[i]
        py = y[j]

        result = simulate(px, py)

        failure_map[j, i] = result

# ============================================================
# DETECT BOUNDARY (SPLINTER)
# ============================================================

boundary = np.zeros_like(failure_map)

for i in range(1, nx-1):
    for j in range(1, ny-1):

        local = failure_map[j-1:j+2, i-1:i+2]

        if np.any(local != local[1,1]):
            boundary[j, i] = 1

# ============================================================
# SAVE
# ============================================================

np.save(os.path.join(OUTDIR, "failure_map.npy"), failure_map)
np.save(os.path.join(OUTDIR, "boundary_map.npy"), boundary)

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(8,7))

# background = success/failure
plt.imshow(
    failure_map,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin='lower',
    cmap='viridis',
    alpha=0.85
)

# boundary overlay
by, bx = np.where(boundary > 0)
plt.scatter(
    x[bx],
    y[by],
    s=5,
    color="white",
    label="Splinter Boundary"
)

# target
plt.scatter(
    TARGET[0], TARGET[1],
    color="red",
    s=80,
    label="Target"
)

plt.title("NEXAH V7.4 — Failure / Reachability Map")
plt.legend()
plt.tight_layout()

plt.savefig(os.path.join(OUTDIR, "v7_4_failure_map.png"), dpi=150)
plt.close()

print("✓ V7.4 done →", OUTDIR)
