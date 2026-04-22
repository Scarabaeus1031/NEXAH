# FIELD_LAYER/field_decomposition/scripts/v8_7_decision_skeleton.py

"""
NEXAH V8.7 — Decision Skeleton (Improved)

Goal:
→ extract thin structural backbone from V8.6
→ reveal decision lines instead of blobs

Method:
→ smoothing
→ adaptive threshold
→ ridge sharpening (gradient-based)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter, sobel

# ============================================================
# PATHS
# ============================================================

BASE = "FIELD_LAYER/field_decomposition/outputs"
OUTDIR = os.path.join(BASE, "v8_7")
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# LOAD
# ============================================================

decision_map = np.load(os.path.join(BASE, "v8_6", "decision_structure.npy"))

# ============================================================
# SMOOTH
# ============================================================

smooth = gaussian_filter(decision_map, sigma=1.2)

# ============================================================
# GRADIENT (ridge detection)
# ============================================================

gx = sobel(smooth, axis=1)
gy = sobel(smooth, axis=0)

grad_mag = np.sqrt(gx**2 + gy**2)

# invert gradient → ridges = low gradient inside high regions
ridge_score = smooth - 0.5 * grad_mag

# ============================================================
# THRESHOLD (adaptive)
# ============================================================

threshold = np.percentile(ridge_score, 94)

mask = ridge_score > threshold

print("threshold:", threshold)
print("active points:", np.sum(mask))

# ============================================================
# GRID
# ============================================================

ny, nx = decision_map.shape
x = np.linspace(6, 17, nx)
y = np.linspace(22, 31, ny)

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(10, 7))

# background
plt.imshow(
    smooth,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin="lower",
    cmap="gray",
    alpha=0.25
)

# skeleton
plt.imshow(
    mask,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin="lower",
    cmap="inferno",
    alpha=0.95
)

plt.title("NEXAH V8.7 — Decision Skeleton (Improved)")

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v8_7_decision_skeleton.png"), dpi=150)
plt.close()

# ============================================================
# SAVE
# ============================================================

np.save(os.path.join(OUTDIR, "decision_skeleton.npy"), mask)

print("✓ V8.7 done →", OUTDIR)
