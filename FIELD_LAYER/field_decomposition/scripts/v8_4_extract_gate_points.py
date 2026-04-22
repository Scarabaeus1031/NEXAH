# ENGINE/analysis/field_decomposition/scripts/v8_4_extract_gate_points.py

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

BASE = "ENGINE/analysis/field_decomposition/outputs"

boundary_path = os.path.join(BASE, "v7_4", "boundary_map.npy")
lyap_path     = os.path.join(BASE, "v8_0_lyapunov_map", "lyapunov_map.npy")
x_path        = os.path.join(BASE, "v8_0_lyapunov_map", "grid_x.npy")
y_path        = os.path.join(BASE, "v8_0_lyapunov_map", "grid_y.npy")

# ============================================================
# LOAD
# ============================================================

boundary = np.load(boundary_path)
L        = np.load(lyap_path)
xv       = np.load(x_path)
yv       = np.load(y_path)

X, Y = np.meshgrid(xv, yv)

# ============================================================
# ALIGN (falls nötig)
# ============================================================

if boundary.shape != L.shape:
    print("Resampling boundary to match Lyapunov grid...")

    by, bx = boundary.shape
    ly, lx = L.shape

    x_old = np.linspace(8, 16, bx)
    y_old = np.linspace(23, 30, by)

    tmp = np.zeros((by, lx))
    for i in range(by):
        tmp[i, :] = np.interp(xv, x_old, boundary[i, :])

    new = np.zeros((ly, lx))
    for j in range(lx):
        new[:, j] = np.interp(yv, y_old, tmp[:, j])

    boundary = new

# ============================================================
# BOUNDARY MASK
# ============================================================

boundary_mask = boundary > 0.5

# ============================================================
# EXTRACT POINTS
# ============================================================

points = np.column_stack((X[boundary_mask], Y[boundary_mask]))
values = L[boundary_mask]

# ============================================================
# SELECT TOP GATE POINTS
# ============================================================

# höchste Lyapunov = weniger negativ = instabiler
N_TOP = 10

idx_sorted = np.argsort(values)[::-1]  # descending
top_idx = idx_sorted[:N_TOP]

gate_points = points[top_idx]
gate_values = values[top_idx]

print("\n--- GATE POINTS ---")
for i, (p, v) in enumerate(zip(gate_points, gate_values)):
    print(f"G{i+1}: ({p[0]:.3f}, {p[1]:.3f})  λ={v:.6f}")

# ============================================================
# VISUALIZATION
# ============================================================

plt.figure(figsize=(10, 6))

# Lyapunov background
plt.contourf(X, Y, L, levels=60, cmap="inferno")

# Boundary
plt.contour(
    X, Y, boundary_mask.astype(float),
    levels=[0.5],
    colors="cyan",
    linewidths=2
)

# Gate points
plt.scatter(
    gate_points[:, 0],
    gate_points[:, 1],
    c="white",
    edgecolor="black",
    s=120,
    label="Gate Points"
)

# annotate
for i, p in enumerate(gate_points):
    plt.text(p[0]+0.05, p[1]+0.05, f"G{i+1}", color="white")

plt.title("V8.4 — Gate Point Extraction (Top Lyapunov along Boundary)")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()

plt.tight_layout()

# ============================================================
# SAVE
# ============================================================

outdir = save_figure(__file__)

np.save(os.path.join(outdir, "gate_points.npy"), gate_points)
np.save(os.path.join(outdir, "gate_values.npy"), gate_values)

save_run_info(
    __file__,
    extra={
        "num_boundary_points": int(len(points)),
        "num_gate_points": int(N_TOP),
        "max_lyapunov": float(gate_values.max()),
        "min_lyapunov": float(gate_values.min()),
    }
)

print("Done.")
