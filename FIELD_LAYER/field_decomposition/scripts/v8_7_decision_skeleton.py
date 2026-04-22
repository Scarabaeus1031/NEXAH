# FIELD_LAYER/field_decomposition/scripts/v8_7_decision_skeleton.py

"""
NEXAH V8.7 — Decision Skeleton

Goal:
→ extract structure from decision map (V8.6)
→ reveal decision backbone

Result:
→ thin structure of key decision regions
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

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
# SMOOTH (optional but helpful)
# ============================================================

smooth = gaussian_filter(decision_map, sigma=1.0)

# ============================================================
# THRESHOLD
# ============================================================

# keep only strongest regions
threshold = np.percentile(smooth, 92)

mask = smooth > threshold

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
    alpha=0.3
)

# skeleton
plt.imshow(
    mask,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin="lower",
    cmap="inferno",
    alpha=0.9
)

plt.title("NEXAH V8.7 — Decision Skeleton")

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v8_7_decision_skeleton.png"), dpi=150)
plt.close()

# ============================================================
# SAVE
# ============================================================

np.save(os.path.join(OUTDIR, "decision_skeleton.npy"), mask)

print("✓ V8.7 done →", OUTDIR)
