# ==========================================================
# NEXAH — Field Frame Stability Test
# ==========================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from scipy.interpolate import griddata
import os

# ----------------------------------------------------------
# CONFIG
# ----------------------------------------------------------

CSV_PATH = "APPLICATIONS/power_systems/stability_field_dynamics/data/ieee_noisy.csv"

GRID_SIZES = [40, 80, 120]   # different resolutions
SMOOTH_SIGMA = 2.0

OUTPUT_PATH = "outputs/demo/nexah_field_frame_stability.png"

# ----------------------------------------------------------
# LOAD DATA
# ----------------------------------------------------------

df = pd.read_csv(CSV_PATH)

signal = df["voltage"].values.astype(float)
signal = (signal - signal.min()) / (signal.max() - signal.min())

grad = np.gradient(signal)

# phase space
x = signal
y = grad

# normalize (IMPORTANT: fixed reference frame)
x = (x - x.mean()) / (x.std() + 1e-8)
y = (y - y.mean()) / (y.std() + 1e-8)

dx = np.gradient(x)
dy = np.gradient(y)

# global bounds (fixed frame!)
xmin, xmax = x.min(), x.max()
ymin, ymax = y.min(), y.max()

# ----------------------------------------------------------
# FUNCTION: BUILD FIELD
# ----------------------------------------------------------

def build_field(grid_size):
    xi = np.linspace(xmin, xmax, grid_size)
    yi = np.linspace(ymin, ymax, grid_size)

    X, Y = np.meshgrid(xi, yi)

    U = griddata((x, y), dx, (X, Y), method='linear')
    V = griddata((x, y), dy, (X, Y), method='linear')

    U = np.nan_to_num(U)
    V = np.nan_to_num(V)

    U = gaussian_filter(U, sigma=SMOOTH_SIGMA)
    V = gaussian_filter(V, sigma=SMOOTH_SIGMA)

    return xi, yi, U, V

# ----------------------------------------------------------
# BUILD FIELDS (different frames)
# ----------------------------------------------------------

fields = []
for gs in GRID_SIZES:
    xi, yi, U, V = build_field(gs)
    fields.append((xi, yi, U, V))

# ----------------------------------------------------------
# REFERENCE FIELD (middle resolution)
# ----------------------------------------------------------

ref_xi, ref_yi, ref_U, ref_V = fields[1]  # 80 grid

# ----------------------------------------------------------
# INTERPOLATE ALL FIELDS TO SAME GRID (for comparison)
# ----------------------------------------------------------

def resample_to_ref(xi, yi, U, V):
    Xr, Yr = np.meshgrid(ref_xi, ref_yi)

    X, Y = np.meshgrid(xi, yi)

    U_r = griddata((X.flatten(), Y.flatten()), U.flatten(), (Xr, Yr), method='linear')
    V_r = griddata((X.flatten(), Y.flatten()), V.flatten(), (Xr, Yr), method='linear')

    U_r = np.nan_to_num(U_r)
    V_r = np.nan_to_num(V_r)

    return U_r, V_r

# ----------------------------------------------------------
# COMPUTE DIFFERENCES
# ----------------------------------------------------------

diff_maps = []

for xi, yi, U, V in fields:
    U_r, V_r = resample_to_ref(xi, yi, U, V)

    diff = np.sqrt((U_r - ref_U)**2 + (V_r - ref_V)**2)
    diff_maps.append(diff)

# ----------------------------------------------------------
# PLOT
# ----------------------------------------------------------

plt.figure(figsize=(14, 4))

for i, diff in enumerate(diff_maps):
    plt.subplot(1, len(diff_maps), i+1)
    plt.imshow(diff, cmap="inferno", origin="lower", aspect="auto")
    plt.title(f"Grid = {GRID_SIZES[i]}")
    plt.colorbar(fraction=0.046, pad=0.04)

plt.suptitle("NEXAH — Field Frame Stability (Resolution Sensitivity)")
plt.tight_layout()

# save
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
plt.savefig(OUTPUT_PATH, dpi=150)
plt.close()

# ----------------------------------------------------------
# OUTPUT
# ----------------------------------------------------------

print("\n⚡ NEXAH Field Frame Stability Test")
print(f"✔ Saved → {OUTPUT_PATH}")

print("\n🧠 Interpretation:")
print("Bright regions → unstable under frame change")
print("Dark regions   → stable structure")
print("→ reveals invariant vs visualization-dependent dynamics")
