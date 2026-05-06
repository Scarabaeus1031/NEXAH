# ENGINE/analysis/field_decomposition/scripts/v8_1_overlay_splinter_vs_lyapunov.py

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

if not os.path.exists(boundary_path):
    raise FileNotFoundError(f"Missing: {boundary_path}")

if not os.path.exists(lyap_path):
    raise FileNotFoundError(f"Missing: {lyap_path}")

boundary_map = np.load(boundary_path)
L = np.load(lyap_path)
xv = np.load(x_path)
yv = np.load(y_path)

X, Y = np.meshgrid(xv, yv)

# ============================================================
# RESIZE / ALIGN BOUNDARY MAP IF NEEDED
# ============================================================

# boundary_map from v7_4 may have different resolution than Lyapunov map
if boundary_map.shape != L.shape:
    by, bx = boundary_map.shape
    ly, lx = L.shape

    x_old = np.linspace(8, 16, bx)
    y_old = np.linspace(23, 30, by)

    # interpolate boundary map onto Lyapunov grid
    tmp = np.zeros((by, lx))
    for i in range(by):
        tmp[i, :] = np.interp(xv, x_old, boundary_map[i, :])

    boundary_resampled = np.zeros((ly, lx))
    for j in range(lx):
        boundary_resampled[:, j] = np.interp(yv, y_old, tmp[:, j])

    boundary_map = boundary_resampled

# binarize boundary if needed
boundary_mask = boundary_map > 0.5

# ============================================================
# LYAPUNOV RIDGE
# ============================================================

# use upper quantile as ridge threshold
ridge_threshold = np.quantile(L, 0.90)
ridge_mask = L >= ridge_threshold

# ============================================================
# METRICS
# ============================================================

intersection = boundary_mask & ridge_mask
union = boundary_mask | ridge_mask

iou = intersection.sum() / (union.sum() + 1e-12)
overlap_boundary = intersection.sum() / (boundary_mask.sum() + 1e-12)
overlap_ridge = intersection.sum() / (ridge_mask.sum() + 1e-12)

print("\n--- V8.1 OVERLAY METRICS ---")
print(f"IoU: {iou:.4f}")
print(f"Boundary covered by ridge: {overlap_boundary:.4f}")
print(f"Ridge covered by boundary: {overlap_ridge:.4f}")
print(f"Ridge threshold: {ridge_threshold:.6f}")

# ============================================================
# PLOT
# ============================================================

fig, axs = plt.subplots(1, 2, figsize=(15, 6))

# ------------------------------------------------------------
# Q1 — overlay
# ------------------------------------------------------------
axs[0].contourf(X, Y, L, levels=60, cmap="inferno")
axs[0].contour(
    X, Y, boundary_mask.astype(float),
    levels=[0.5],
    colors="cyan",
    linewidths=2.0
)
axs[0].contour(
    X, Y, ridge_mask.astype(float),
    levels=[0.5],
    colors="white",
    linewidths=1.5,
    linestyles="--"
)

axs[0].set_title("Overlay: Splinter Boundary (cyan) vs Lyapunov Ridge (white)")
axs[0].set_xlabel("x")
axs[0].set_ylabel("y")

# markers
clusters = {
    "C0": np.array([10.0, 25.0]),
    "C1": np.array([12.0, 24.0]),
    "C2": np.array([13.5, 26.0]),
    "C3": np.array([11.0, 28.5]),
}
colors = {"C0": "dodgerblue", "C1": "orange", "C2": "limegreen", "C3": "red"}

for name, p in clusters.items():
    axs[0].scatter(p[0], p[1], s=90, c=colors[name], edgecolor="black", zorder=5)

# ------------------------------------------------------------
# Q2 — difference / intersection map
# ------------------------------------------------------------
diff = np.zeros_like(L, dtype=int)
diff[boundary_mask] = 1
diff[ridge_mask] = 2
diff[intersection] = 3

cmap = plt.cm.get_cmap("viridis", 4)
im = axs[1].imshow(
    diff,
    origin="lower",
    extent=[xv.min(), xv.max(), yv.min(), yv.max()],
    aspect="auto",
    cmap=cmap,
    vmin=0,
    vmax=3
)

axs[1].set_title(
    f"Difference Map\nIoU={iou:.3f} | boundary∩ridge={intersection.sum()}"
)
axs[1].set_xlabel("x")
axs[1].set_ylabel("y")

cbar = plt.colorbar(im, ax=axs[1], ticks=[0, 1, 2, 3])
cbar.ax.set_yticklabels([
    "none",
    "boundary only",
    "ridge only",
    "overlap"
])

plt.tight_layout()

# ============================================================
# SAVE
# ============================================================

outdir = save_figure(__file__)
np.save(os.path.join(outdir, "boundary_mask.npy"), boundary_mask.astype(np.uint8))
np.save(os.path.join(outdir, "ridge_mask.npy"), ridge_mask.astype(np.uint8))
np.save(os.path.join(outdir, "intersection_mask.npy"), intersection.astype(np.uint8))

save_run_info(
    __file__,
    extra={
        "ridge_threshold": float(ridge_threshold),
        "iou": float(iou),
        "overlap_boundary": float(overlap_boundary),
        "overlap_ridge": float(overlap_ridge),
    }
)

print("Done.")
