# FIELD_LAYER/field_decomposition/scripts/v8_3_delay_vs_lyapunov.py

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import RegularGridInterpolator

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

lyap_path = os.path.join(BASE, "v8_0_lyapunov_map", "lyapunov_map.npy")
lyap_map = np.load(lyap_path)

ny_d, nx_d = delay_map.shape
ny_l, nx_l = lyap_map.shape

# ============================================================
# GRIDS
# ============================================================

# Delay grid (target grid)
x_d = np.linspace(6, 17, nx_d)
y_d = np.linspace(22, 31, ny_d)

# Lyapunov grid (source grid)
x_l = np.linspace(6, 17, nx_l)
y_l = np.linspace(22, 31, ny_l)

X_d, Y_d = np.meshgrid(x_d, y_d)

# ============================================================
# INTERPOLATE LYAPUNOV → DELAY GRID
# ============================================================

interp = RegularGridInterpolator((y_l, x_l), lyap_map)

points = np.stack([Y_d.ravel(), X_d.ravel()], axis=-1)
lyap_resampled = interp(points).reshape(ny_d, nx_d)

# ============================================================
# NORMALIZATION
# ============================================================

delay_norm = delay_map / (np.max(delay_map) + 1e-8)

lyap_shift = lyap_resampled - np.min(lyap_resampled)
lyap_norm = lyap_shift / (np.max(lyap_shift) + 1e-8)

# ============================================================
# DIFFERENCE
# ============================================================

diff_map = delay_norm - lyap_norm

# ============================================================
# PLOT 1 — DELAY
# ============================================================

plt.figure(figsize=(6,5))
plt.contourf(X_d, Y_d, delay_norm, levels=50, cmap="plasma")
plt.title("V8.3 — Decision Delay")
plt.colorbar()
plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "delay.png"), dpi=150)
plt.close()

# ============================================================
# PLOT 2 — LYAPUNOV
# ============================================================

plt.figure(figsize=(6,5))
plt.contourf(X_d, Y_d, lyap_norm, levels=50, cmap="viridis")
plt.title("V8.3 — Lyapunov (resampled)")
plt.colorbar()
plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "lyapunov.png"), dpi=150)
plt.close()

# ============================================================
# PLOT 3 — OVERLAY
# ============================================================

plt.figure(figsize=(10,7))

plt.contourf(X_d, Y_d, delay_norm, levels=50, cmap="plasma", alpha=0.8)

plt.contour(
    X_d, Y_d, lyap_norm,
    levels=[0.4, 0.6, 0.8],
    colors="cyan",
    linewidths=1.5
)

plt.title("V8.3 — Delay vs Lyapunov")
plt.colorbar(label="Delay")

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "overlay.png"), dpi=150)
plt.close()

# ============================================================
# PLOT 4 — DIFFERENCE
# ============================================================

plt.figure(figsize=(10,7))

plt.contourf(X_d, Y_d, diff_map, levels=50, cmap="coolwarm")

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
