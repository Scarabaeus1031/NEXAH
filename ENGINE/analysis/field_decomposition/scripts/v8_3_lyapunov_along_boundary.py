# ENGINE/analysis/field_decomposition/scripts/v8_3_lyapunov_along_boundary.py

import os
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# LOCAL SAVE
# ============================================================

def save_figure(script_path):
    script_name = os.path.splitext(os.path.basename(script_path))[0]
    outdir = os.path.join("ENGINE/analysis/field_decomposition/outputs", script_name)
    os.makedirs(outdir, exist_ok=True)

    outfile = os.path.join(outdir, f"{script_name}.png")
    plt.savefig(outfile, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✓ saved figure -> {outfile}")
    return outdir

def save_run_info(script_path, extra=None):
    script_name = os.path.splitext(os.path.basename(script_path))[0]
    outdir = os.path.join("ENGINE/analysis/field_decomposition/outputs", script_name)
    os.makedirs(outdir, exist_ok=True)

    info_path = os.path.join(outdir, "run_info.txt")
    with open(info_path, "w", encoding="utf-8") as f:
        f.write(f"script: {script_name}\n")
        f.write(f"time: {datetime.now()}\n")
        if extra:
            for k, v in extra.items():
                f.write(f"{k}: {v}\n")

# ============================================================
# PATHS
# ============================================================

V74_DIR = "ENGINE/analysis/field_decomposition/outputs/v7_4"
V80_DIR = "ENGINE/analysis/field_decomposition/outputs/v8_0_lyapunov_map"

boundary_path = os.path.join(V74_DIR, "boundary_map.npy")
lyap_path = os.path.join(V80_DIR, "lyapunov_map.npy")
x_path = os.path.join(V80_DIR, "grid_x.npy")
y_path = os.path.join(V80_DIR, "grid_y.npy")

# ============================================================
# LOAD DATA
# ============================================================

boundary_map = np.load(boundary_path)
L = np.load(lyap_path)
xv = np.load(x_path)
yv = np.load(y_path)

# ============================================================
# RESAMPLE BOUNDARY IF NEEDED
# ============================================================

if boundary_map.shape != L.shape:
    by, bx = boundary_map.shape
    ly, lx = L.shape

    x_old = np.linspace(8, 16, bx)
    y_old = np.linspace(23, 30, by)

    tmp = np.zeros((by, lx))
    for i in range(by):
        tmp[i, :] = np.interp(xv, x_old, boundary_map[i, :])

    boundary_resampled = np.zeros((ly, lx))
    for j in range(lx):
        boundary_resampled[:, j] = np.interp(yv, y_old, tmp[:, j])

    boundary_map = boundary_resampled

boundary_mask = boundary_map > 0.5

# ============================================================
# EXTRACT BOUNDARY POINTS
# ============================================================

indices = np.argwhere(boundary_mask)

# convert to coordinates
points = np.array([
    [xv[j], yv[i]] for i, j in indices
])

# corresponding Lyapunov values
lyap_vals = np.array([
    L[i, j] for i, j in indices
])

# ============================================================
# PARAMETRIZATION (sort along x for now)
# ============================================================

order = np.argsort(points[:, 0])
points_sorted = points[order]
lyap_sorted = lyap_vals[order]

# simple arc-length approximation
dist_along = np.zeros(len(points_sorted))
for i in range(1, len(points_sorted)):
    dist_along[i] = dist_along[i-1] + np.linalg.norm(
        points_sorted[i] - points_sorted[i-1]
    )

# normalize
dist_along = dist_along / (dist_along[-1] + 1e-9)

# ============================================================
# PLOT
# ============================================================

fig, axs = plt.subplots(1, 2, figsize=(15, 6))

# ------------------------------------------------------------
# Q1 — boundary colored by Lyapunov
# ------------------------------------------------------------
sc = axs[0].scatter(
    points[:, 0], points[:, 1],
    c=lyap_vals,
    cmap="inferno",
    s=10
)

plt.colorbar(sc, ax=axs[0], label="Lyapunov")

axs[0].set_title("Boundary colored by Lyapunov")
axs[0].set_xlabel("x")
axs[0].set_ylabel("y")

# ------------------------------------------------------------
# Q2 — Lyapunov along boundary
# ------------------------------------------------------------
axs[1].plot(dist_along, lyap_sorted, lw=1.5)

axs[1].set_title("Lyapunov along Boundary")
axs[1].set_xlabel("Normalized arc length")
axs[1].set_ylabel("Lyapunov exponent")

# highlight peaks
peaks = np.where(lyap_sorted > np.percentile(lyap_sorted, 90))[0]
axs[1].scatter(
    dist_along[peaks],
    lyap_sorted[peaks],
    c="red",
    s=20,
    label="high instability"
)

axs[1].legend()

plt.tight_layout()

# ============================================================
# SAVE
# ============================================================

outdir = save_figure(__file__)

np.save(os.path.join(outdir, "boundary_points.npy"), points)
np.save(os.path.join(outdir, "lyapunov_on_boundary.npy"), lyap_vals)

save_run_info(
    __file__,
    extra={
        "num_points": int(len(points)),
        "mean_lyapunov": float(np.mean(lyap_vals)),
        "max_lyapunov": float(np.max(lyap_vals)),
    }
)

print("Done.")
