# FIELD_LAYER/field_decomposition/scripts/v9_2_unique_flow_density.py

"""
NEXAH V9.2 — Unique Trajectory Density

Goal:
→ remove time bias from density
→ count unique trajectory visits

Result:
→ true structural flow density
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# ============================================================
# PATHS
# ============================================================

BASE = "FIELD_LAYER/field_decomposition/outputs"
OUTDIR = os.path.join(BASE, "v9_2")
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# LOAD EDGES
# ============================================================

edges = np.load(os.path.join(BASE, "v9_0", "flow_edges.npy"), allow_pickle=True)

ny, nx = 200, 200

# ============================================================
# UNIQUE DENSITY
# ============================================================

density = np.zeros((ny, nx))

for edge in edges:

    visited = set()

    for (iy, ix) in edge:
        if 0 <= iy < ny and 0 <= ix < nx:
            visited.add((iy, ix))

    # count each trajectory only once per pixel
    for (iy, ix) in visited:
        density[iy, ix] += 1

print("✓ unique density built")

# smooth
density_smooth = gaussian_filter(density, sigma=1.5)

# normalize
density_norm = density_smooth / (np.max(density_smooth) + 1e-8)

# ============================================================
# NODE EXTRACTION (optional)
# ============================================================

threshold = np.percentile(density_norm, 95)
node_mask = density_norm > threshold

print("threshold:", threshold)
print("nodes:", np.sum(node_mask))

# ============================================================
# GRID
# ============================================================

x = np.linspace(6, 17, nx)
y = np.linspace(22, 31, ny)

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(10, 7))

# density
plt.imshow(
    density_norm,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin="lower",
    cmap="viridis",
    alpha=0.8
)

# nodes
ys, xs = np.where(node_mask)
plt.scatter(x[xs], y[ys], color="red", s=6, label="nodes")

plt.legend()
plt.title("NEXAH V9.2 — Unique Flow Density")

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v9_2_unique_density.png"), dpi=150)
plt.close()

# ============================================================
# SAVE
# ============================================================

np.save(os.path.join(OUTDIR, "unique_density.npy"), density_norm)
np.save(os.path.join(OUTDIR, "node_mask.npy"), node_mask)

print("✓ V9.2 done →", OUTDIR)
