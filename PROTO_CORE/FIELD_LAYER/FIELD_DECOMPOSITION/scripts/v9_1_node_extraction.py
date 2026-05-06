# FIELD_LAYER/field_decomposition/scripts/v9_1_node_extraction.py

"""
NEXAH V9.1 — Flow Node Extraction

Goal:
→ detect real nodes from flow trajectories

Method:
→ count trajectory density
→ extract peaks (high-density regions)

Result:
→ true dynamic nodes
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# ============================================================
# PATHS
# ============================================================

BASE = "FIELD_LAYER/field_decomposition/outputs"
OUTDIR = os.path.join(BASE, "v9_1")
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# LOAD EDGES (from V9.0)
# ============================================================

edges = np.load(os.path.join(BASE, "v9_0", "flow_edges.npy"), allow_pickle=True)

# grid size
ny, nx = 200, 200

# ============================================================
# BUILD DENSITY MAP
# ============================================================

density = np.zeros((ny, nx))

for edge in edges:
    for (iy, ix) in edge:
        if 0 <= iy < ny and 0 <= ix < nx:
            density[iy, ix] += 1

print("✓ density built")

# smooth → makes peaks clearer
density_smooth = gaussian_filter(density, sigma=2)

# normalize
density_norm = density_smooth / (np.max(density_smooth) + 1e-8)

# ============================================================
# NODE EXTRACTION
# ============================================================

threshold = np.percentile(density_norm, 97)

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

# density background
plt.imshow(
    density_norm,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin="lower",
    cmap="viridis",
    alpha=0.6
)

# nodes
ys, xs = np.where(node_mask)
plt.scatter(x[xs], y[ys], color="red", s=8, label="nodes")

plt.legend()
plt.title("NEXAH V9.1 — Flow Nodes")

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v9_1_nodes.png"), dpi=150)
plt.close()

# ============================================================
# SAVE
# ============================================================

np.save(os.path.join(OUTDIR, "node_mask.npy"), node_mask)
np.save(os.path.join(OUTDIR, "density_map.npy"), density_norm)

print("✓ V9.1 done →", OUTDIR)
