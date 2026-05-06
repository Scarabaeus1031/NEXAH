# FIELD_LAYER/field_decomposition/scripts/v8_5_directional_entropy_map.py

"""
NEXAH V8.5 — Directional Entropy Map (Stable Version)

Goal:
→ measure local directional ambiguity
→ detect regions with competing flow directions

Output:
→ entropy_map (0 = clear direction, 1 = high ambiguity)
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PATHS
# ============================================================

BASE = "FIELD_LAYER/field_decomposition/outputs"
OUTDIR = os.path.join(BASE, "v8_5")
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# LOAD FIELD (use your existing nav field!)
# ============================================================

Nx = np.load(os.path.join(BASE, "v7_3", "nav_field_x.npy"))
Ny = np.load(os.path.join(BASE, "v7_3", "nav_field_y.npy"))

ny, nx = Nx.shape

x = np.linspace(6, 17, nx)
y = np.linspace(22, 31, ny)
X, Y = np.meshgrid(x, y)

# ============================================================
# NORMALIZE FIELD
# ============================================================

norm = np.sqrt(Nx**2 + Ny**2) + 1e-8
Nx = Nx / norm
Ny = Ny / norm

# ============================================================
# ANGLES
# ============================================================

angles = np.arctan2(Ny, Nx)  # [-pi, pi]
angles = (angles + 2*np.pi) % (2*np.pi)  # [0, 2pi]

# ============================================================
# ENTROPY COMPUTATION (ROBUST)
# ============================================================

window = 5
bins = 16

entropy_map = np.zeros((ny, nx))

for j in range(ny):
    for i in range(nx):

        j0 = max(0, j - window//2)
        j1 = min(ny, j + window//2 + 1)
        i0 = max(0, i - window//2)
        i1 = min(nx, i + window//2 + 1)

        local = angles[j0:j1, i0:i1].flatten()

        if len(local) < 5:
            entropy_map[j, i] = 0
            continue

        hist, _ = np.histogram(local, bins=bins, range=(0, 2*np.pi))

        p = hist.astype(float)
        s = np.sum(p)

        if s == 0:
            entropy_map[j, i] = 0
            continue

        p /= s

        entropy = -np.sum(p * np.log(p + 1e-12))
        entropy /= np.log(bins)

        entropy_map[j, i] = entropy

print("✓ entropy computed")
print("min:", np.min(entropy_map))
print("max:", np.max(entropy_map))

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(10, 7))

plt.contourf(X, Y, entropy_map, levels=50, cmap="viridis")

plt.colorbar(label="Directional Entropy")

# optional vector overlay
step = 12
plt.quiver(
    X[::step, ::step], Y[::step, ::step],
    Nx[::step, ::step], Ny[::step, ::step],
    color="white", alpha=0.4
)

plt.title("NEXAH V8.5 — Directional Entropy Map")

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v8_5_entropy.png"), dpi=150)
plt.close()

# ============================================================
# SAVE
# ============================================================

np.save(os.path.join(OUTDIR, "entropy_map.npy"), entropy_map)

print("✓ V8.5 done →", OUTDIR)
