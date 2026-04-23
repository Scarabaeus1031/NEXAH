# ==========================================================
# NEXAH — IEEE Field Reconstruction (V69 CLEAN)
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

GRID_SIZE = 100
SMOOTH_SIGMA = 2.0

OUTPUT_PATH = "outputs/demo/nexah_ieee_field_v69_clean.png"

# ----------------------------------------------------------
# LOAD DATA
# ----------------------------------------------------------

df = pd.read_csv(CSV_PATH)

t = df["time"].values.astype(float)
signal = df["voltage"].values.astype(float)

# normalize
signal = (signal - signal.min()) / (signal.max() - signal.min())

# ----------------------------------------------------------
# PHASE SPACE (embedding)
# ----------------------------------------------------------

grad = np.gradient(signal)

x = signal
y = grad

# normalize space
x = (x - x.mean()) / (x.std() + 1e-8)
y = (y - y.mean()) / (y.std() + 1e-8)

# ----------------------------------------------------------
# FLOW (local motion)
# ----------------------------------------------------------

dx = np.gradient(x)
dy = np.gradient(y)

# ----------------------------------------------------------
# GRID (continuous field space)
# ----------------------------------------------------------

xmin, xmax = x.min(), x.max()
ymin, ymax = y.min(), y.max()

xi = np.linspace(xmin, xmax, GRID_SIZE)
yi = np.linspace(ymin, ymax, GRID_SIZE)

X, Y = np.meshgrid(xi, yi)

# ----------------------------------------------------------
# INTERPOLATION (THIS IS THE KEY STEP)
# ----------------------------------------------------------

# interpolate vector field onto grid
U = griddata((x, y), dx, (X, Y), method='linear')
V = griddata((x, y), dy, (X, Y), method='linear')

# handle NaNs (outside convex hull)
U = np.nan_to_num(U)
V = np.nan_to_num(V)

# smooth field
U = gaussian_filter(U, sigma=SMOOTH_SIGMA)
V = gaussian_filter(V, sigma=SMOOTH_SIGMA)

# ----------------------------------------------------------
# DENSITY (structure)
# ----------------------------------------------------------

density, _, _ = np.histogram2d(x, y, bins=[xi, yi])
density = gaussian_filter(density, sigma=SMOOTH_SIGMA)

density = density / (density.max() + 1e-8)

# ----------------------------------------------------------
# PLOT
# ----------------------------------------------------------

plt.figure(figsize=(10, 8))

# density background
plt.imshow(
    density.T,
    extent=[xmin, xmax, ymin, ymax],
    origin="lower",
    aspect="auto",
    cmap="inferno"
)

# FLOW FIELD (continuous now)
plt.streamplot(
    xi, yi,
    U.T, V.T,
    color="white",
    density=1.2,
    linewidth=1
)

# trajectory overlay
plt.plot(x, y, color="cyan", alpha=0.4, linewidth=1)

plt.title("NEXAH — IEEE Field (V69 CLEAN)")
plt.xlabel("state")
plt.ylabel("gradient")

plt.grid(alpha=0.15)
plt.tight_layout()

# save
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
plt.savefig(OUTPUT_PATH, dpi=150)
plt.close()

# ----------------------------------------------------------
# OUTPUT
# ----------------------------------------------------------

print("\n⚡ NEXAH IEEE Field Reconstruction (V69 CLEAN)")
print(f"✔ Saved → {OUTPUT_PATH}")

print("\n🧠 Interpretation:")
print("Discrete transitions → continuous flow field")
print("→ structure becomes movement")
print("→ reveals global system dynamics")
