# ==========================================================
# NEXAH — IEEE Field Reconstruction (V68 CLEAN)
# ==========================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import os

# ----------------------------------------------------------
# CONFIG
# ----------------------------------------------------------

CSV_PATH = "APPLICATIONS/power_systems/stability_field_dynamics/data/ieee_noisy.csv"

GRID_SIZE = 120
SMOOTH_SIGMA = 2.0

OUTPUT_PATH = "outputs/demo/nexah_ieee_field_v68_clean.png"

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
x = (x - x.mean()) / x.std()
y = (y - y.mean()) / y.std()

# ----------------------------------------------------------
# DENSITY FIELD (continuous)
# ----------------------------------------------------------

xmin, xmax = x.min(), x.max()
ymin, ymax = y.min(), y.max()

xi = np.linspace(xmin, xmax, GRID_SIZE)
yi = np.linspace(ymin, ymax, GRID_SIZE)

density, _, _ = np.histogram2d(x, y, bins=[xi, yi])
density = gaussian_filter(density, sigma=SMOOTH_SIGMA)

# normalize
density = density / density.max()

# ----------------------------------------------------------
# FLOW (smoothed vector field)
# ----------------------------------------------------------

dx = np.gradient(x)
dy = np.gradient(y)

# normalize vectors
norm = np.sqrt(dx**2 + dy**2) + 1e-6
u = dx / norm
v = dy / norm

# downsample for clarity
step = 10

# ----------------------------------------------------------
# PLOT
# ----------------------------------------------------------

plt.figure(figsize=(10, 8))

# smooth density background
plt.imshow(
    density.T,
    extent=[xmin, xmax, ymin, ymax],
    origin="lower",
    aspect="auto",
    cmap="inferno"
)

# trajectory
plt.plot(x, y, color="cyan", alpha=0.5, linewidth=1)

# flow field
plt.quiver(
    x[::step],
    y[::step],
    u[::step],
    v[::step],
    color="white",
    scale=30,
    width=0.003
)

plt.title("NEXAH — IEEE Field (V68 CLEAN)")
plt.xlabel("state")
plt.ylabel("gradient")

plt.grid(alpha=0.15)

plt.tight_layout()

# ensure folder exists
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

plt.savefig(OUTPUT_PATH, dpi=150)
plt.close()

# ----------------------------------------------------------
# OUTPUT
# ----------------------------------------------------------

print("\n⚡ NEXAH IEEE Field Reconstruction (V68 CLEAN)")
print(f"✔ Saved → {OUTPUT_PATH}")

print("\n🧠 Interpretation:")
print("Grid artifacts removed")
print("→ continuous density field")
print("→ smoother flow representation")
print("→ closer to true system geometry")
