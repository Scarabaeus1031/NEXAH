# FIELD_LAYER/field_decomposition/scripts/v10_1_boundary_map.py

"""
NEXAH V10.1 — Boundary / Transition Map

Goal:
→ detect regime transitions in space
→ highlight separatrix / switching zones

Input:
→ regime_map.npy (from V10)

Output:
→ boundary_map.png
→ boundary_strength.npy
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PATHS
# ============================================================

BASE = "FIELD_LAYER/field_decomposition/outputs"
INDIR = os.path.join(BASE, "v10_0")
OUTDIR = os.path.join(BASE, "v10_1")

os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# LOAD
# ============================================================

regime_map = np.load(os.path.join(INDIR, "regime_map.npy"))

ny, nx = regime_map.shape

# ============================================================
# BOUNDARY DETECTION
# ============================================================

boundary = np.zeros_like(regime_map, dtype=float)

for y in range(ny - 1):
    for x in range(nx - 1):

        center = regime_map[y, x]

        # compare with neighbors
        if (
            center != regime_map[y, x + 1] or
            center != regime_map[y + 1, x] or
            center != regime_map[y + 1, x + 1]
        ):
            boundary[y, x] = 1.0

# ============================================================
# OPTIONAL: SMOOTH / STRENGTH MAP
# ============================================================

# simple local density of boundaries (gives thickness / intensity)
boundary_strength = np.zeros_like(boundary)

kernel_size = 3

for y in range(ny):
    for x in range(nx):
        y0 = max(0, y - kernel_size)
        y1 = min(ny, y + kernel_size + 1)
        x0 = max(0, x - kernel_size)
        x1 = min(nx, x + kernel_size + 1)

        boundary_strength[y, x] = np.sum(boundary[y0:y1, x0:x1])

# normalize
boundary_strength /= (np.max(boundary_strength) + 1e-8)

# ============================================================
# PLOT 1 — RAW BOUNDARY
# ============================================================

plt.figure(figsize=(8, 8))
plt.imshow(boundary, cmap="gray", origin="lower")
plt.title("NEXAH V10.1 — Boundary (Separatrix)")
plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v10_1_boundary_raw.png"), dpi=160)

# ============================================================
# PLOT 2 — STRENGTH MAP
# ============================================================

plt.figure(figsize=(8, 8))
plt.imshow(boundary_strength, cmap="hot", origin="lower")
plt.title("NEXAH V10.1 — Boundary Strength (Transition Intensity)")
plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v10_1_boundary_strength.png"), dpi=160)

# ============================================================
# SAVE
# ============================================================

np.save(os.path.join(OUTDIR, "boundary_raw.npy"), boundary)
np.save(os.path.join(OUTDIR, "boundary_strength.npy"), boundary_strength)

print("✓ boundary map computed")
print("✓ V10.1 done →", OUTDIR)
