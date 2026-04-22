# FIELD_LAYER/field_decomposition/scripts/v7_11_transition_ridge_extraction.py

"""
NEXAH V7.11 — Transition Ridge Extraction

Goal:
→ convert transition mask (V7.10) into cleaner ridge-like line structures
→ reveal splinter / boundary geometry as lines (not areas)

Method:
→ load transition_mask (V7.10)
→ simple morphological thinning (no heavy deps)
→ extract ridge-like skeleton via neighbor filtering
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PATH SETUP
# ============================================================

BASE = os.path.join("FIELD_LAYER", "field_decomposition", "outputs")
OUTDIR = os.path.join(BASE, "v7_11")
os.makedirs(OUTDIR, exist_ok=True)

print("✓ Using BASE:", os.path.abspath(BASE))

# ============================================================
# LOAD DATA
# ============================================================

mask_path = os.path.join(BASE, "v7_10", "transition_mask.npy")

if not os.path.exists(mask_path):
    raise FileNotFoundError("❌ transition_mask.npy not found — run V7.10 first")

mask = np.load(mask_path).astype(np.uint8)

ny, nx = mask.shape

x = np.linspace(6, 17, nx)
y = np.linspace(22, 31, ny)
X, Y = np.meshgrid(x, y)

# ============================================================
# RIDGE EXTRACTION (LESS AGGRESSIVE)
# ============================================================

ridge = np.zeros_like(mask)

for j in range(1, ny-1):
    for i in range(1, nx-1):

        if mask[j, i] == 1:

            neighbors = np.sum(mask[j-1:j+2, i-1:i+2]) - 1

            # NEW: keep boundary-like pixels
            if neighbors <= 6:
                ridge[j, i] = 1

# ============================================================
# OPTIONAL CLEANUP (remove isolated noise)
# ============================================================

clean = np.zeros_like(ridge)

for j in range(1, ny-1):
    for i in range(1, nx-1):

        if ridge[j, i] == 1:
            neighbors = np.sum(ridge[j-1:j+2, i-1:i+2]) - 1

            if neighbors >= 2:
                clean[j, i] = 1

ridge = clean

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(9,7))

# background (faint original mask)
plt.imshow(
    mask,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin="lower",
    cmap="gray",
    alpha=0.15
)

# ridge overlay
plt.scatter(
    X[ridge == 1],
    Y[ridge == 1],
    s=2,
    color="black"
)

plt.title("NEXAH V7.11 — Transition Ridge Extraction")
plt.xlabel("x")
plt.ylabel("y")

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v7_11_transition_ridge.png"), dpi=150)
plt.close()

# ============================================================
# SAVE
# ============================================================

np.save(os.path.join(OUTDIR, "ridge.npy"), ridge)

print("✓ saved ridge ->", os.path.join(OUTDIR, "ridge.npy"))
print("✓ saved figure ->", os.path.join(OUTDIR, "v7_11_transition_ridge.png"))
print("✓ V7.11 done →", OUTDIR)
