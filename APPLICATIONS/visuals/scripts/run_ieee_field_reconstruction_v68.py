# ==========================================================
# NEXAH Demo — IEEE Field Reconstruction (V68-like)
# ==========================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------------------------------
# CONFIG
# ----------------------------------------------------------

CSV_PATH = "APPLICATIONS/power_systems/stability_field_dynamics/data/ieee_noisy.csv"

GRID_SIZE = 60
SMOOTH = 2

# ----------------------------------------------------------
# LOAD DATA
# ----------------------------------------------------------

df = pd.read_csv(CSV_PATH)

t = df["time"].values.astype(float)
signal = df["voltage"].values.astype(float)

# normalize
signal = (signal - signal.min()) / (signal.max() - signal.min())

# ----------------------------------------------------------
# EMBEDDING (Phase Space)
# ----------------------------------------------------------

grad = np.gradient(signal)

x = signal
y = grad

# normalize space
x = (x - x.mean()) / x.std()
y = (y - y.mean()) / y.std()

# ----------------------------------------------------------
# BUILD GRID
# ----------------------------------------------------------

xmin, xmax = x.min(), x.max()
ymin, ymax = y.min(), y.max()

xi = np.linspace(xmin, xmax, GRID_SIZE)
yi = np.linspace(ymin, ymax, GRID_SIZE)

X, Y = np.meshgrid(xi, yi)

U = np.zeros_like(X)
V = np.zeros_like(Y)
COUNT = np.zeros_like(X)

# ----------------------------------------------------------
# FLOW ESTIMATION (local vector field)
# ----------------------------------------------------------

for i in range(len(x) - 1):
    px, py = x[i], y[i]
    dx = x[i + 1] - x[i]
    dy = y[i + 1] - y[i]

    # nearest grid cell
    ix = np.argmin(np.abs(xi - px))
    iy = np.argmin(np.abs(yi - py))

    U[iy, ix] += dx
    V[iy, ix] += dy
    COUNT[iy, ix] += 1

# avoid division by zero
mask = COUNT > 0
U[mask] /= COUNT[mask]
V[mask] /= COUNT[mask]

# ----------------------------------------------------------
# DENSITY (proto V68 intensity)
# ----------------------------------------------------------

density = COUNT / COUNT.max()

# ----------------------------------------------------------
# PLOT
# ----------------------------------------------------------

plt.figure(figsize=(10, 8))

# density background
plt.imshow(
    density,
    extent=[xmin, xmax, ymin, ymax],
    origin="lower",
    aspect="auto"
)

# vector field
plt.quiver(
    X, Y,
    U, V,
    color="white",
    scale=20,
    width=0.002
)

# trajectory overlay
plt.plot(x, y, color="red", alpha=0.3, linewidth=1)

plt.title("NEXAH — IEEE Field Reconstruction (V68-like)")
plt.xlabel("state")
plt.ylabel("gradient")

plt.grid(alpha=0.2)

output_path = "outputs/demo/nexah_ieee_field_v68.png"
plt.savefig(output_path, dpi=150)
plt.close()

# ----------------------------------------------------------
# OUTPUT
# ----------------------------------------------------------

print("\n⚡ NEXAH IEEE Field Reconstruction (V68-like)")
print(f"✔ Saved → {output_path}")

print("\n🧠 Interpretation:")
print("State-space reconstructed from signal")
print("→ local flow directions extracted")
print("→ density reveals structural regions")
print("→ first approximation of system field")
