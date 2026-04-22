# FIELD_LAYER/field_decomposition/scripts/v7_8_fast_optimal_direction.py

"""
NEXAH V7.8 (FAST) — Optimal Direction ≈ Navigation Field

Robust Version:
→ auto-detects correct outputs folder
→ no hardcoded ENGINE paths
"""

import os
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PATH HANDLING (ROBUST)
# ============================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# try multiple possible locations
CANDIDATE_BASES = [
    os.path.join(SCRIPT_DIR, "..", "outputs"),
    os.path.join(SCRIPT_DIR, "..", "..", "outputs"),
    "FIELD_LAYER/field_decomposition/outputs",
    "ENGINE/analysis/field_decomposition/outputs",
]

BASE = None

for path in CANDIDATE_BASES:
    path = os.path.normpath(path)
    if os.path.exists(os.path.join(path, "v7_2")):
        BASE = path
        break

if BASE is None:
    raise FileNotFoundError("❌ Could not locate outputs directory")

print("✓ Using BASE:", BASE)

# ============================================================
# LOCAL SAVE
# ============================================================

def save_figure(script_path):
    script_name = os.path.splitext(os.path.basename(script_path))[0]
    outdir = os.path.join(BASE, script_name)
    os.makedirs(outdir, exist_ok=True)

    outfile = os.path.join(outdir, f"{script_name}.png")
    plt.savefig(outfile, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✓ saved figure -> {outfile}")
    return outdir

def save_run_info(script_path, extra=None):
    script_name = os.path.splitext(os.path.basename(script_path))[0]
    outdir = os.path.join(BASE, script_name)
    os.makedirs(outdir, exist_ok=True)

    info_path = os.path.join(outdir, "run_info.txt")
    with open(info_path, "w", encoding="utf-8") as f:
        f.write(f"script: {script_name}\n")
        f.write(f"time: {datetime.now()}\n")
        if extra:
            for k, v in extra.items():
                f.write(f"{k}: {v}\n")

# ============================================================
# LOAD DATA
# ============================================================

cost_map = np.load(os.path.join(BASE, "v7_2", "cost_map.npy"))
Nx = np.load(os.path.join(BASE, "v7_3", "nav_field_x.npy"))
Ny = np.load(os.path.join(BASE, "v7_3", "nav_field_y.npy"))
xv = np.load(os.path.join(BASE, "v7_2", "grid_x.npy"))
yv = np.load(os.path.join(BASE, "v7_2", "grid_y.npy"))

X, Y = np.meshgrid(xv, yv)

# ============================================================
# NORMALIZE NAVIGATION FIELD
# ============================================================

norm = np.sqrt(Nx**2 + Ny**2) + 1e-8
Ux = Nx / norm
Uy = Ny / norm

# ============================================================
# CONFIDENCE FIELD
# ============================================================

confidence = norm / np.max(norm)

# ============================================================
# TARGET (visual only)
# ============================================================

TARGET = np.array([13, 26])

# ============================================================
# PLOT
# ============================================================

fig, axs = plt.subplots(1, 2, figsize=(15, 6))

# --- Q1: cost + direction field ---
axs[0].contourf(X, Y, cost_map, levels=60, cmap="inferno")

step = 6
axs[0].quiver(
    X[::step, ::step],
    Y[::step, ::step],
    Ux[::step, ::step],
    Uy[::step, ::step],
    color="white",
    alpha=0.8,
    scale=40
)

axs[0].scatter(TARGET[0], TARGET[1], color="cyan", s=90, edgecolor="black")

axs[0].set_title("Optimal Direction ≈ Navigation Field")
axs[0].set_xlabel("x")
axs[0].set_ylabel("y")

# --- Q2: confidence ---
im = axs[1].imshow(
    confidence,
    origin="lower",
    extent=[xv.min(), xv.max(), yv.min(), yv.max()],
    aspect="auto",
    cmap="viridis"
)

axs[1].set_title("Direction Field Strength")
axs[1].set_xlabel("x")
axs[1].set_ylabel("y")

plt.colorbar(im, ax=axs[1])

plt.tight_layout()

# ============================================================
# SAVE
# ============================================================

outdir = save_figure(__file__)

np.save(os.path.join(outdir, "optimal_dir_x.npy"), Ux)
np.save(os.path.join(outdir, "optimal_dir_y.npy"), Uy)
np.save(os.path.join(outdir, "direction_confidence.npy"), confidence)

save_run_info(
    __file__,
    extra={
        "method": "nav_field_direct",
        "normalized": True
    }
)

print("✓ V7.8 FAST done.")
