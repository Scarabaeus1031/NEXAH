"""
NEXAH V7.10 — Transition Structure Extraction (ROBUST)

Goal:
→ extract geometric transition structures
→ from alignment inconsistency (V7.9)

Improvement:
→ adaptive threshold instead of fixed cutoff
→ detects weak-alignment regions reliably
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PATH SETUP
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

print("alignment stats:")
print("min:", np.min(alignment))
print("max:", np.max(alignment))
print("mean:", np.mean(alignment))

# ============================================================
# TRANSITION EXTRACTION (KEY FIX)
# ============================================================

# adaptive threshold: lowest 15% = transition zone
threshold = np.percentile(alignment, 15)

print("threshold (auto):", threshold)

transition_mask = alignment < threshold

print("mask sum:", np.sum(transition_mask))

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(10, 7))

# background alignment
plt.contourf(X, Y, alignment, levels=50, cmap="coolwarm", alpha=0.8)

# transition contour
plt.contour(
    X, Y, transition_mask,
    levels=[0.5],
    colors="black",
    linewidths=2
)

# highlight mask
plt.imshow(
    transition_mask,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin="lower",
    cmap="gray",
    alpha=0.25
)

# vector field
step = 12
plt.quiver(
    X[::step, ::step], Y[::step, ::step],
    Nx[::step, ::step], Ny[::step, ::step],
    color="white", alpha=0.4
)

plt.title("NEXAH V7.10 — Extracted Transition Structure (Adaptive)")
plt.colorbar(label="Alignment")

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v7_10_transition_structure.png"), dpi=150)
plt.close()

# ============================================================
# SAVE
# ============================================================

np.save(os.path.join(OUTDIR, "transition_mask.npy"), transition_mask)

print("✓ V7.10 done →", OUTDIR)
