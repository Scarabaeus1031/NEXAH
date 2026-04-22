# FIELD_LAYER/field_decomposition/scripts/v9_0_flow_graph.py

"""
NEXAH V9.0 — Flow-Constrained Graph

Goal:
→ combine skeleton (structure) + trajectories (dynamics)
→ extract real edges

Result:
→ graph based on actual motion
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PATHS
# ============================================================

BASE = "FIELD_LAYER/field_decomposition/outputs"
OUTDIR = os.path.join(BASE, "v9_0")
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# LOAD
# ============================================================

skeleton = np.load(os.path.join(BASE, "v8_7", "decision_skeleton.npy"))

ny, nx = skeleton.shape

# ============================================================
# FIELD (same as V8.2)
# ============================================================

x = np.linspace(6, 17, nx)
y = np.linspace(22, 31, ny)
X, Y = np.meshgrid(x, y)

def gaussian(x, y, cx, cy, sigma=1.5):
    return np.exp(-((x - cx)**2 + (y - cy)**2) / (2 * sigma**2))

V = (
    -2.0 * gaussian(X, Y, 10.5, 25.0, sigma=1.8)
    -2.0 * gaussian(X, Y, 14.5, 26.5, sigma=1.8)
)

Vy, Vx = np.gradient(V)
Fx = -Vx
Fy = -Vy

def rotation(x, y, cx, cy):
    dx = x - cx
    dy = y - cy
    return -dy, dx

Rx1, Ry1 = rotation(X, Y, 10.5, 25.0)
Rx2, Ry2 = rotation(X, Y, 14.5, 26.5)

Rx = 0.6 * Rx1 + 0.6 * Rx2
Ry = 0.6 * Ry1 + 0.6 * Ry2

Fx_total = Fx + 0.3 * Rx
Fy_total = Fy + 0.3 * Ry

norm = np.sqrt(Fx_total**2 + Fy_total**2) + 1e-8
Fx_total /= norm
Fy_total /= norm

# ============================================================
# SAMPLING
# ============================================================

def sample(px, py):
    ix = np.clip(np.searchsorted(x, px) - 1, 0, nx - 1)
    iy = np.clip(np.searchsorted(y, py) - 1, 0, ny - 1)
    return Fx_total[iy, ix], Fy_total[iy, ix], iy, ix

# ============================================================
# TRAJECTORY EXTRACTION
# ============================================================

edges = []

num_traj = 200
steps = 200
dt = 0.08

for _ in range(num_traj):

    # random start
    px = np.random.uniform(x.min(), x.max())
    py = np.random.uniform(y.min(), y.max())

    path = []
    skeleton_hits = 0

    for _ in range(steps):

        vx, vy, iy, ix = sample(px, py)

        px += vx * dt
        py += vy * dt

        path.append((iy, ix))

        # check skeleton
        if skeleton[iy, ix]:
            skeleton_hits += 1

    # keep only trajectories that meaningfully interact
    if skeleton_hits > 15:
        edges.append(path)

print("✓ extracted edges:", len(edges))

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(10, 7))

# skeleton background
plt.imshow(
    skeleton,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin="lower",
    cmap="gray",
    alpha=0.2
)

# edges
for edge in edges:
    pts = np.array(edge)
    plt.plot(x[pts[:,1]], y[pts[:,0]], color="cyan", linewidth=1.5)

plt.title("NEXAH V9.0 — Flow-Constrained Graph")

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v9_0_flow_graph.png"), dpi=150)
plt.close()

# ============================================================
# SAVE
# ============================================================

np.save(os.path.join(OUTDIR, "flow_edges.npy"), np.array(edges, dtype=object))

print("✓ V9.0 done →", OUTDIR)
