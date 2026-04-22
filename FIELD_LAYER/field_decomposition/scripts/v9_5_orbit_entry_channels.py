# FIELD_LAYER/field_decomposition/scripts/v9_5_orbit_entry_channels.py

"""
NEXAH V9.5 — Orbit Entry Channels

Goal:
→ extract discrete entry channels into orbit ring
→ detect transversal connection points

Result:
→ sparse channel nodes (true entry points)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# ============================================================
# PATHS
# ============================================================

BASE = "FIELD_LAYER/field_decomposition/outputs"
OUTDIR = os.path.join(BASE, "v9_5")
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# LOAD DATA
# ============================================================

orbit_entry = np.load(os.path.join(BASE, "v9_4", "orbit_entry.npy"))

# ============================================================
# SMOOTH (reduces pixel noise)
# ============================================================

smooth = gaussian_filter(orbit_entry.astype(float), sigma=1.0)

# ============================================================
# GRADIENT → detect boundaries
# ============================================================

gy, gx = np.gradient(smooth)
grad_mag = np.sqrt(gx**2 + gy**2)

# ============================================================
# THRESHOLD → isolate strong transitions
# ============================================================

threshold = np.percentile(grad_mag, 95)

channels = grad_mag > threshold

print("threshold:", threshold)
print("channel points:", np.sum(channels))

# ============================================================
# GRID
# ============================================================

ny, nx = orbit_entry.shape
x = np.linspace(6, 17, nx)
y = np.linspace(22, 31, ny)

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(10, 7))

# background: entry map
plt.imshow(
    orbit_entry,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin="lower",
    cmap="coolwarm",
    alpha=0.3
)

# overlay: channels
plt.imshow(
    channels,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin="lower",
    cmap="inferno",
    alpha=0.9
)

plt.title("NEXAH V9.5 — Orbit Entry Channels")

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v9_5_channels.png"), dpi=150)
plt.close()

# ============================================================
# SAVE
# ============================================================

np.save(os.path.join(OUTDIR, "orbit_entry_channels.npy"), channels)

print("✓ V9.5 done →", OUTDIR)
