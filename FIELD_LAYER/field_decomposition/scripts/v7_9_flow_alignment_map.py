# FIELD_LAYER/field_decomposition/scripts/v7_9_flow_alignment_map.py

"""
NEXAH V7.9 — Flow Alignment Map (UPDATED)

Compares:
→ raw navigation field (Nx, Ny)
→ normalized direction field (Ux, Uy)

Goal:
→ measure alignment consistency
→ detect structural instability regions
→ highlight splinter / transition zones
"""

import os
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PATH HANDLING (ROBUST)
# ============================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

CANDIDATE_BASES = [
    os.path.join(SCRIPT_DIR, "..", "outputs"),
    os.path.join(SCRIPT_DIR, "..", "..", "outputs"),
    "FIELD_LAYER/field_decomposition/outputs",
]

BASE = None

for path in CANDIDATE_BASES:
    path = os.path.normpath(path)
    if os.path.exists(os.path.join(path, "v7_3")):
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

Nx = np.load(os.path.join(BASE, "v7_3", "nav_field_x.npy"))
Ny = np.load(os.path.join(BASE, "v7_3", "nav_field_y.npy"))

xv = np.load(os.path.join(BASE, "v7_2", "grid_x.npy"))
yv = np.load(os.path.join(BASE, "v7_2", "grid_y.npy"))

X, Y = np.meshgrid(xv, yv)

# ============================================================
# NORMALIZE FIELD
# ============================================================

norm = np.sqrt(Nx**2 + Ny**2) + 1e-8
Ux = Nx / norm
Uy = Ny / norm

# ============================================================
# ALIGNMENT COMPUTATION
# ============================================================

# dot product between raw and normalized field
alignment = Nx * Ux + Ny * Uy

# normalize again to [-1, 1]
alignment = alignment / (np.sqrt(Nx**2 + Ny**2) + 1e-8)
alignment = np.clip(alignment, -1, 1)

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(9,7))

plt.contourf(X, Y, alignment, levels=60, cmap="coolwarm")
plt.colorbar(label="Alignment (1 = stable, 0 = transition, -1 = flip)")

# overlay direction field
step = 10
plt.quiver(
    X[::step,::step], Y[::step,::step],
    Ux[::step,::step], Uy[::step,::step],
    color="white", alpha=0.4
)

plt.title("NEXAH V7.9 — Field Alignment Consistency Map")
plt.xlabel("x")
plt.ylabel("y")

plt.tight_layout()

# ============================================================
# SAVE
# ============================================================

outdir = save_figure(__file__)

np.save(os.path.join(outdir, "alignment_map.npy"), alignment)

save_run_info(
    __file__,
    extra={
        "method": "nav_vs_normalized",
        "interpretation": "alignment consistency"
    }
)

print("✓ V7.9 done.")
