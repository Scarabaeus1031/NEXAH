# ENGINE/analysis/field_decomposition/scripts/v8_2_distance_to_boundary_vs_lyapunov.py

import os
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import distance_transform_edt

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

if not os.path.exists(boundary_path):
    raise FileNotFoundError(f"Missing: {boundary_path}")

if not os.path.exists(lyap_path):
    raise FileNotFoundError(f"Missing: {lyap_path}")

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
# DISTANCE TRANSFORM
# ============================================================

# distance to nearest boundary (invert mask!)
distance_map = distance_transform_edt(~boundary_mask)

# normalize (optional but helpful for plotting)
distance_map = distance_map / (np.max(distance_map) + 1e-9)

# ============================================================
# SCATTER DATA
# ============================================================

dist_flat = distance_map.flatten()
lyap_flat = L.flatten()

# ============================================================
# PLOT
# ============================================================

fig, axs = plt.subplots(1, 2, figsize=(15, 6))

# ------------------------------------------------------------
# Q1 — distance map
# ------------------------------------------------------------
im1 = axs[0].imshow(
    distance_map,
    origin="lower",
    extent=[xv.min(), xv.max(), yv.min(), yv.max()],
    aspect="auto",
    cmap="viridis"
)
axs[0].set_title("Distance to Boundary")
axs[0].set_xlabel("x")
axs[0].set_ylabel("y")
plt.colorbar(im1, ax=axs[0])

# ------------------------------------------------------------
# Q2 — scatter: distance vs Lyapunov
# ------------------------------------------------------------
axs[1].scatter(dist_flat, lyap_flat, s=3, alpha=0.3)

axs[1].set_title("Distance vs Lyapunov")
axs[1].set_xlabel("Distance to Boundary")
axs[1].set_ylabel("Lyapunov exponent")

# optional trend line (very useful!)
try:
    z = np.polyfit(dist_flat, lyap_flat, 1)
    p = np.poly1d(z)
    x_line = np.linspace(dist_flat.min(), dist_flat.max(), 200)
    axs[1].plot(x_line, p(x_line), color="red", lw=2, label="trend")
    axs[1].legend()
except:
    pass

plt.tight_layout()

# ============================================================
# SAVE
# ============================================================

outdir = save_figure(__file__)

np.save(os.path.join(outdir, "distance_map.npy"), distance_map)

save_run_info(
    __file__,
    extra={
        "mean_distance": float(np.mean(dist_flat)),
        "mean_lyapunov": float(np.mean(lyap_flat)),
    }
)

print("Done.")
