"""
NEXAH V7.8 — Optimal Crossing Direction Field (FAST VERSION)

Goal:
→ find best control direction per point
→ minimal energy direction for reaching target
→ visualize optimal crossing vector field

Optimized:
→ uses nav field directly (no heavy brute force)
→ fast & stable
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PATH SETUP (robust)
# ============================================================

BASE = os.path.join("FIELD_LAYER", "field_decomposition", "outputs")
OUTDIR = os.path.join(BASE, "v7_8")
os.makedirs(OUTDIR, exist_ok=True)

print("✓ Using BASE:", os.path.abspath(BASE))

# ============================================================
# LOAD DATA
# ============================================================

Nx = np.load(os.path.join(BASE, "v7_3", "nav_field_x.npy"))
Ny = np.load(os.path.join(BASE, "v7_3", "nav_field_y.npy"))

ny, nx = Nx.shape

x = np.linspace(6, 17, nx)
y = np.linspace(22, 31, ny)
X, Y = np.meshgrid(x, y)

TARGET = np.array([13, 26])

# ============================================================
# NORMALIZE NAV FIELD
# ============================================================

norm = np.sqrt(Nx**2 + Ny**2) + 1e-8
Nx = Nx / norm
Ny = Ny / norm

# ============================================================
# "OPTIMAL" CONTROL (DIRECT APPROXIMATION)
# ============================================================

# Use nav field directly as optimal direction
best_dx = Nx.copy()
best_dy = Ny.copy()

# simple proxy energy (distance to target)
dist = np.sqrt((X - TARGET[0])**2 + (Y - TARGET[1])**2)
best_energy = dist / np.max(dist)

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(9,7))

# energy background
plt.contourf(X, Y, best_energy, levels=50, cmap="inferno")

# direction field (downsample)
step = 10
plt.quiver(
    X[::step,::step], Y[::step,::step],
    best_dx[::step,::step], best_dy[::step,::step],
    color="white", alpha=0.7
)

# target
plt.scatter(TARGET[0], TARGET[1], color="cyan", s=80, edgecolor="black")

plt.title("NEXAH V7.8 — Optimal Crossing Direction Field (Fast)")
plt.colorbar(label="proxy control energy")

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v7_8_optimal_direction.png"), dpi=150)
plt.close()

print("✓ saved figure ->", os.path.join(OUTDIR, "v7_8_optimal_direction.png"))

# ============================================================
# SAVE DATA (CRITICAL for V7.9 / V7.10)
# ============================================================

np.save(os.path.join(OUTDIR, "best_dx.npy"), best_dx)
np.save(os.path.join(OUTDIR, "best_dy.npy"), best_dy)
np.save(os.path.join(OUTDIR, "best_energy.npy"), best_energy)

print("✓ saved fields (best_dx, best_dy, best_energy)")

print("✓ V7.8 done →", OUTDIR)
