"""
NEXAH V7.9 — Flow Alignment Map

Compares:
→ natural navigation field (V7.3)
→ optimal control direction (V7.8)

Goal:
→ measure alignment between them
→ identify conflict zones (splinter)
"""

import os
import numpy as np
import matplotlib.pyplot as plt

OUTDIR = "output/v7_9"
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# LOAD DATA
# ============================================================

Nx = np.load("output/v7_3/nav_field_x.npy")
Ny = np.load("output/v7_3/nav_field_y.npy")

best_dx = np.load("output/v7_8/best_dx.npy")
best_dy = np.load("output/v7_8/best_dy.npy")

nx, ny = Nx.shape[1], Nx.shape[0]

x = np.linspace(6, 17, nx)
y = np.linspace(22, 31, ny)
X, Y = np.meshgrid(x, y)

# ============================================================
# ALIGNMENT COMPUTATION
# ============================================================

# dot product = alignment
alignment = Nx * best_dx + Ny * best_dy

# normalize to [-1, 1]
alignment = np.clip(alignment, -1, 1)

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(9,7))

# heatmap
plt.contourf(X, Y, alignment, levels=50, cmap="coolwarm")

plt.colorbar(label="Flow Alignment (1 = aligned, -1 = opposite)")

# optional: overlay vectors
step = 12
plt.quiver(
    X[::step,::step], Y[::step,::step],
    Nx[::step,::step], Ny[::step,::step],
    color="white", alpha=0.4
)

plt.title("NEXAH V7.9 — Flow vs Optimal Control Alignment")
plt.tight_layout()

plt.savefig(os.path.join(OUTDIR, "v7_9_alignment.png"), dpi=150)
plt.close()

print("✓ V7.9 done →", OUTDIR)
