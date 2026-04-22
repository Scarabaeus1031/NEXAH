# FIELD_LAYER/field_decomposition/scripts/v9_5_orbit_entry_channels.py

"""
NEXAH V9.5 — TRUE Orbit Entry Channels (FIXED)

Goal:
→ extract real transition channels (NOT full ring)
→ combine Delay + Entropy + Entry boundary

Result:
→ sparse channel points (true transversal ports)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter, binary_erosion

# ============================================================
# PATHS
# ============================================================

BASE = "FIELD_LAYER/field_decomposition/outputs"
OUTDIR = os.path.join(BASE, "v9_5")
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# LOAD DATA
# ============================================================

entry = np.load(os.path.join(BASE, "v9_4", "orbit_entry.npy")).astype(bool)
delay = np.load(os.path.join(BASE, "v8_2", "decision_delay.npy"))
entropy = np.load(os.path.join(BASE, "v8_5", "entropy_map.npy"))

# ============================================================
# NORMALIZE
# ============================================================

def normalize(A):
    A = A - np.min(A)
    return A / (np.max(A) + 1e-8)

delay_n = normalize(delay)
entropy_n = normalize(entropy)

# ============================================================
# ENTRY BOUNDARY
# ============================================================

boundary = entry & (~binary_erosion(entry))

# ============================================================
# SMOOTH (important)
# ============================================================

delay_s = gaussian_filter(delay_n, sigma=1.0)
entropy_s = gaussian_filter(entropy_n, sigma=1.0)

# ============================================================
# THRESHOLDS (tunable)
# ============================================================

delay_thr = np.percentile(delay_s, 80)
entropy_thr = np.percentile(entropy_s, 75)

print("delay_thr:", delay_thr)
print("entropy_thr:", entropy_thr)

# ============================================================
# TRUE CHANNEL DETECTION
# ============================================================

channels = (
    boundary &
    (delay_s > delay_thr) &
    (entropy_s > entropy_thr)
)

print("channel points:", np.sum(channels))

# ============================================================
# GRID
# ============================================================

ny, nx = entry.shape
x = np.linspace(6, 17, nx)
y = np.linspace(22, 31, ny)

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(10, 7))

# background
plt.imshow(
    delay_s,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin="lower",
    cmap="plasma",
    alpha=0.4
)

# boundary
plt.contour(
    x, y, boundary.astype(float),
    levels=[0.5],
    colors="white",
    linewidths=1
)

# channels (REAL)
ys, xs = np.where(channels)

plt.scatter(
    x[xs],
    y[ys],
    color="cyan",
    s=20,
    label="true entry channels"
)

plt.legend()
plt.title("NEXAH V9.5 — TRUE Orbit Entry Channels")

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v9_5_true_channels.png"), dpi=150)
plt.close()

# ============================================================
# SAVE
# ============================================================

np.save(os.path.join(OUTDIR, "true_channels.npy"), channels)

print("✓ V9.5 (fixed) done →", OUTDIR)
