"""
NEXAH V7.10 — Transition Structure Extraction

Goal:
→ extract geometric transition structures
→ from alignment inconsistency (V7.9)

Result:
→ binary mask of transition zones
→ shows splinter / gate / interface structure explicitly
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PATH SETUP (robust)
# ============================================================

BASE = "FIELD_LAYER/field_decomposition/outputs"

OUTDIR = os.path.join(BASE, "v7_10")
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# LOAD DATA
# ============================================================

Nx = np.load(os.path.join(BASE, "v7_3", "nav_field_x.npy"))
Ny = np.load(os.path.join(BASE, "v7_3", "nav_field_y.npy"))

best_dx = np.load(os.path.join(BASE, "v7_8", "best_dx.npy"))
best_dy = np.load(os.path.join(BASE, "v7_8", "best_dy.npy"))

ny, nx = Nx.shape

x = np.linspace(6, 17, nx)
y = np.linspace(22, 31, ny)
X, Y = np.meshgrid(x, y)

# ============================================================
# NORMALIZATION
# ============================================================

def normalize(vx, vy):
    norm = np.sqrt(vx**2 + vy**2) + 1e-8
    return vx / norm, vy / norm

Nx, Ny = normalize(Nx, Ny)
best_dx, best_dy = normalize(best_dx, best_dy)

# ============================================================
# ALIGNMENT
# ============================================================

alignment = Nx * best_dx + Ny * best_dy
alignment = np.clip(alignment, -1, 1)

# ============================================================
# TRANSITION EXTRACTION
# ============================================================

# threshold: near-zero alignment = conflict / interface
threshold = 0.85   # adjust if needed (0.7–0.95 range)

transition_mask = np.abs(alignment) < threshold

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(10, 7))

# background alignment
plt.contourf(X, Y, alignment, levels=50, cmap="coolwarm", alpha=0.6)

# overlay transition structure
plt.contour(
    X, Y, transition_mask,
    levels=[0.5],
    colors="black",
    linewidths=2
)

# optional fill for clarity
plt.imshow(
    transition_mask,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin="lower",
    cmap="gray",
    alpha=0.2
)

# vector field overlay (light)
step = 12
plt.quiver(
    X[::step, ::step], Y[::step, ::step],
    Nx[::step, ::step], Ny[::step, ::step],
    color="white", alpha=0.4
)

plt.title("NEXAH V7.10 — Extracted Transition Structure")
plt.colorbar(label="Alignment")

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v7_10_transition_structure.png"), dpi=150)
plt.close()

# ============================================================
# SAVE MASK
# ============================================================

np.save(os.path.join(OUTDIR, "transition_mask.npy"), transition_mask)

print("✓ V7.10 done →", OUTDIR)
