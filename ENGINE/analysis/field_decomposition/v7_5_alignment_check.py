"""
NEXAH V7.5 — Alignment Check

Goal:
Compare structural boundary (FIELD_LAYER)
with operational boundary (V7.4 failure map)

→ overlay
→ difference map

This tests whether both pipelines detect the same structure.
"""

import os
import numpy as np
import matplotlib.pyplot as plt

OUTDIR = "output/v7_5"
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# LOAD DATA
# ============================================================

# --- V7.4 boundary ---
failure_boundary = np.load("output/v7_4/boundary_map.npy")

# --- FIELD_LAYER boundary (choose one you already have) ---
# 👉 IMPORTANT: replace with your actual file

# Example options:
# field_boundary = np.load("FIELD_LAYER/outputs/boundary.npy")
# field_boundary = np.load("FIELD_LAYER/outputs/ridge_map.npy")

# fallback (for now): reuse failure boundary (so script runs)
field_boundary = failure_boundary.copy()

# ============================================================
# GRID
# ============================================================

ny, nx = failure_boundary.shape

x = np.linspace(6, 17, nx)
y = np.linspace(22, 31, ny)
X, Y = np.meshgrid(x, y)

# ============================================================
# NORMALIZE INPUTS
# ============================================================

fb = (failure_boundary > 0).astype(float)
sb = (field_boundary > 0).astype(float)

# ============================================================
# ALIGNMENT METRICS
# ============================================================

intersection = fb * sb
union = np.clip(fb + sb, 0, 1)

# IoU (Intersection over Union)
iou = intersection.sum() / (union.sum() + 1e-8)

# XOR difference (mismatch)
diff = np.abs(fb - sb)

print(f"Alignment IoU: {iou:.4f}")

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(12,5))

# ------------------------------------------------------------
# LEFT: Overlay
# ------------------------------------------------------------
plt.subplot(1,2,1)

plt.imshow(fb, extent=[x.min(), x.max(), y.min(), y.max()],
           origin='lower', cmap='Blues', alpha=0.6)

plt.imshow(sb, extent=[x.min(), x.max(), y.min(), y.max()],
           origin='lower', cmap='Reds', alpha=0.6)

plt.title(f"Overlay (Blue=V7.4, Red=FIELD_LAYER)\nIoU={iou:.3f}")

# ------------------------------------------------------------
# RIGHT: Difference Map
# ------------------------------------------------------------
plt.subplot(1,2,2)

plt.imshow(diff, extent=[x.min(), x.max(), y.min(), y.max()],
           origin='lower', cmap='inferno')

plt.title("Difference Map (Mismatch Zones)")

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v7_5_alignment.png"), dpi=150)
plt.close()

print("✓ V7.5 done →", OUTDIR)
