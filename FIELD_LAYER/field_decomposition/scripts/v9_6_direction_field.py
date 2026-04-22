# FIELD_LAYER/field_decomposition/scripts/v9_6_direction_field.py

"""
NEXAH V9.6 — Direction Field on Entry Channels

Goal:
→ compute local direction field along orbit entry channels
→ infer directional drift from unique flow density

Method:
→ build gradient from unique_density
→ rotate gradient to obtain tangential flow field
→ restrict vectors to V9.5 channels
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PATHS
# ============================================================

BASE = "FIELD_LAYER/field_decomposition/outputs"
OUTDIR = os.path.join(BASE, "v9_6")
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# LOAD DATA
# ============================================================

channels = np.load(os.path.join(BASE, "v9_5", "orbit_entry_channels.npy"))

density = np.load(os.path.join(BASE, "v9_2", "unique_density.npy"))

# ============================================================
# GRADIENT-BASED FLOW FIELD
# ============================================================

gy, gx = np.gradient(density)

# orthogonal rotation of gradient
dx = -gy
dy = gx

# ============================================================
# MASK CHANNELS
# ============================================================

mask = channels > 0
y_idx, x_idx = np.where(mask)

dx_c = dx[y_idx, x_idx]
dy_c = dy[y_idx, x_idx]

# ============================================================
# NORMALIZE
# ============================================================

mag = np.sqrt(dx_c**2 + dy_c**2) + 1e-8
dx_n = dx_c / mag
dy_n = dy_c / mag

angles = np.arctan2(dy_n, dx_n)

# ============================================================
# GRID
# ============================================================

ny, nx = density.shape
x = np.linspace(6, 17, nx)
y = np.linspace(22, 31, ny)

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(8, 8))

# background: density
plt.imshow(
    density,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin="lower",
    cmap="gray",
    alpha=0.3
)

# channel mask
plt.imshow(
    mask,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin="lower",
    cmap="coolwarm",
    alpha=0.2
)

# quiver on channels
plt.quiver(
    x[x_idx],
    y[y_idx],
    dx_n,
    dy_n,
    angles,
    cmap="hsv",
    scale=70,
    width=0.003
)

plt.title("NEXAH V9.6 — Direction Field on Entry Channels")
plt.colorbar(label="angle (rad)")
plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v9_6_direction_field.png"), dpi=150)
plt.close()

# ============================================================
# SAVE
# ============================================================

direction_field = np.zeros((ny, nx, 2))
direction_field[..., 0] = dx
direction_field[..., 1] = dy

np.save(os.path.join(OUTDIR, "direction_field.npy"), direction_field)

print("✓ saved direction_field.npy")
print("✓ V9.6 done →", OUTDIR)
