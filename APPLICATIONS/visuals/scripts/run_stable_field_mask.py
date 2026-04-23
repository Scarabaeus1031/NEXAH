# ==========================================================
# NEXAH — Stable Field Mask Extraction
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

GRID_SIZES = [40, 80, 120]
SMOOTH_SIGMA = 2.0

# threshold for stability (tune this!)
STABILITY_THRESHOLD = 0.15

OUTPUT_PATH = "outputs/demo/nexah_stable_field_mask.png"

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

# normalize (fixed frame!)
x = (x - x.mean()) / (x.std() + 1e-8)
y = (y - y.mean()) / (y.std() + 1e-8)

dx = np.gradient(x)
dy = np.gradient(y)

xmin, xmax = x.min(), x.max()
ymin, ymax = y.min(), y.max()

# ----------------------------------------------------------
# BUILD FIELD FUNCTION
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
# BUILD ALL FIELDS
# ----------------------------------------------------------

fields = []
for gs in GRID_SIZES:
    xi, yi, U, V = build_field(gs)
    fields.append((xi, yi, U, V))

# ----------------------------------------------------------
# REFERENCE GRID
# ----------------------------------------------------------

ref_xi, ref_yi, ref_U, ref_V = fields[1]  # 80 grid

# ----------------------------------------------------------
# RESAMPLING
# ----------------------------------------------------------

def resample(xi, yi, U, V):
    Xr, Yr = np.meshgrid(ref_xi, ref_yi)
    X, Y = np.meshgrid(xi, yi)

    U_r = griddata((X.flatten(), Y.flatten()), U.flatten(), (Xr, Yr), method='linear')
    V_r = griddata((X.flatten(), Y.flatten()), V.flatten(), (Xr, Yr), method='linear')

    U_r = np.nan_to_num(U_r)
    V_r = np.nan_to_num(V_r)

    return U_r, V_r

# ----------------------------------------------------------
# COMPUTE STABILITY
# ----------------------------------------------------------

diff_accum = np.zeros_like(ref_U)

for xi, yi, U, V in fields:
    U_r, V_r = resample(xi, yi, U, V)
    diff = np.sqrt((U_r - ref_U)**2 + (V_r - ref_V)**2)
    diff_accum += diff

diff_mean = diff_accum / len(fields)

# ----------------------------------------------------------
# STABLE MASK
# ----------------------------------------------------------

stable_mask = diff_mean < STABILITY_THRESHOLD

# ----------------------------------------------------------
# DENSITY FOR VISUAL CONTEXT
# ----------------------------------------------------------

density, _, _ = np.histogram2d(x, y, bins=[ref_xi, ref_yi])
density = gaussian_filter(density, sigma=SMOOTH_SIGMA)

density = density / (density.max() + 1e-8)

# ----------------------------------------------------------
# PLOT
# ----------------------------------------------------------

plt.figure(figsize=(10, 8))

# background density
plt.imshow(
    density.T,
    extent=[xmin, xmax, ymin, ymax],
    origin="lower",
    aspect="auto",
    cmap="inferno",
    alpha=0.6
)

# stable regions overlay
plt.imshow(
    stable_mask.T,
    extent=[xmin, xmax, ymin, ymax],
    origin="lower",
    aspect="auto",
    cmap="Greens",
    alpha=0.6
)

# trajectory
plt.plot(x, y, color="cyan", alpha=0.5)

plt.title("NEXAH — Stable Field Structure")
plt.xlabel("state")
plt.ylabel("gradient")

plt.grid(alpha=0.2)
plt.tight_layout()

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
plt.savefig(OUTPUT_PATH, dpi=150)
plt.close()

# ----------------------------------------------------------
# OUTPUT
# ----------------------------------------------------------

print("\n⚡ NEXAH Stable Field Extraction")
print(f"✔ Saved → {OUTPUT_PATH}")

print("\n🧠 Interpretation:")
print("Green = stable field structure (invariant)")
print("Dark  = unstable / frame-dependent regions")
print("→ extracted true dynamical geometry")
