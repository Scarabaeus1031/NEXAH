# FIELD_LAYER/field_decomposition/scripts/v8_3_delay_vs_lyapunov.py

"""
NEXAH V8.3 — Delay vs Lyapunov Overlay

Goal:
→ compare decision delay (V8.2) with stability (Lyapunov)
→ identify whether gates are instability-driven or delay-driven

Result:
→ overlay map
→ difference map (Delay vs Stability)
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PATHS
# ============================================================

BASE = "FIELD_LAYER/field_decomposition/outputs"

OUTDIR = os.path.join(BASE, "v8_3")
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# LOAD DATA
# ============================================================

delay_map = np.load(os.path.join(BASE, "v8_2", "delay_map.npy"))

# falls du V8.0 so gespeichert hast:
lyap_path = os.path.join(BASE, "v8_0_lyapunov_map", "lyapunov_map.npy")

if not os.path.exists(lyap_path):
    raise FileNotFoundError("Lyapunov map not found. Check V8.0 output path.")

lyap_map = np.load(lyap_path)

ny, nx = delay_map.shape

x = np.linspace(6, 17, nx)
y = np.linspace(22, 31, ny)
X, Y = np.meshgrid(x, y)

# ============================================================
# NORMALIZATION
# ============================================================

# Delay normalisieren
delay_norm = delay_map / (np.max(delay_map) + 1e-8)

# Lyapunov normalisieren (invertieren → hohe Instabilität = hoch)
lyap_shift = lyap_map - np.min(lyap_map)
lyap_norm = lyap_shift / (np.max(lyap_shift) + 1e-8)

# ============================================================
# DIFFERENCE MAP
# ============================================================

# + → delay dominiert
# - → instability dominiert
diff_map = delay_norm - lyap_norm

# ============================================================
# PLOT 1 — DELAY
# ============================================================

plt.figure(figsize=(6,5))
plt.contourf(X, Y, delay_norm, levels=50, cmap="plasma")
plt.title("V8.3 — Decision Delay")
plt.colorbar()
plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "delay.png"), dpi=150)
plt.close()

# ============================================================
# PLOT 2 — LYAPUNOV
# ============================================================

plt.figure(figsize=(6,5))
plt.contourf(X, Y, lyap_norm, levels=50, cmap="viridis")
plt.title("V8.3 — Lyapunov (normalized)")
plt.colorbar()
plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "lyapunov.png"), dpi=150)
plt.close()

# ============================================================
# PLOT 3 — OVERLAY
# ============================================================

plt.figure(figsize=(10,7))

# delay als Hintergrund
plt.contourf(X, Y, delay_norm, levels=50, cmap="plasma", alpha=0.8)

# lyapunov contour
plt.contour(
    X, Y, lyap_norm,
    levels=[0.4, 0.6, 0.8],
    colors="cyan",
    linewidths=1.5
)

plt.title("V8.3 — Delay (background) vs Lyapunov (contours)")
plt.colorbar(label="Delay")

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "overlay.png"), dpi=150)
plt.close()

# ============================================================
# PLOT 4 — DIFFERENCE MAP
# ============================================================

plt.figure(figsize=(10,7))

plt.contourf(X, Y, diff_map, levels=50, cmap="coolwarm")

plt.title("V8.3 — Delay vs Lyapunov Difference")
plt.colorbar(label="(+ Delay dominates, - Instability dominates)")

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "difference.png"), dpi=150)
plt.close()

# ============================================================
# SAVE
# ============================================================

np.save(os.path.join(OUTDIR, "delay_norm.npy"), delay_norm)
np.save(os.path.join(OUTDIR, "lyap_norm.npy"), lyap_norm)
np.save(os.path.join(OUTDIR, "diff_map.npy"), diff_map)

print("✓ V8.3 done →", OUTDIR)
