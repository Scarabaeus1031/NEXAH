"""
NEXAH Lorenz Potential Landscape

Converts the resilience map into a quasi-potential landscape.

Idea:

tau(x,z) = time until regime switch

Potential:

V(x,z) = 1 / tau

Interpretation:

high V  -> unstable region
low V   -> stable region

Outputs:

APPLICATIONS/outputs/lorenz_potential/
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# ---------------------------------------------------
# paths
# ---------------------------------------------------

INPUT_FILE = "APPLICATIONS/outputs/lorenz_resilience/lorenz_resilience_map.csv"

OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_potential"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---------------------------------------------------
# load resilience map
# ---------------------------------------------------

tau = np.loadtxt(INPUT_FILE, delimiter=",")

rows, cols = tau.shape

xs = np.linspace(-4,4,cols)
zs = np.linspace(15,35,rows)

X, Z = np.meshgrid(xs, zs)


# ---------------------------------------------------
# potential function
# ---------------------------------------------------

epsilon = 1e-6

V = 1.0 / (tau + epsilon)


# normalize for visualization
V = (V - V.min()) / (V.max() - V.min())


# ---------------------------------------------------
# 2D heatmap
# ---------------------------------------------------

plt.figure(figsize=(8,8))

plt.imshow(
    V,
    extent=[xs[0], xs[-1], zs[0], zs[-1]],
    origin="lower",
    cmap="magma",
    aspect="auto"
)

plt.colorbar(label="instability potential")

plt.xlabel("X")
plt.ylabel("Z")

plt.title("Lorenz Potential Landscape")

path = os.path.join(
    OUTPUT_DIR,
    "lorenz_potential_map.png"
)

plt.savefig(path, dpi=300)

print("Saved:", path)

plt.show()

plt.close()


# ---------------------------------------------------
# 3D surface
# ---------------------------------------------------

fig = plt.figure(figsize=(9,7))

ax = fig.add_subplot(111, projection="3d")

ax.plot_surface(
    X,
    Z,
    V,
    cmap="magma",
    linewidth=0,
    antialiased=True
)

ax.set_xlabel("X")
ax.set_ylabel("Z")
ax.set_zlabel("Instability Potential")

ax.set_title("Lorenz Stability Landscape")

path = os.path.join(
    OUTPUT_DIR,
    "lorenz_potential_surface.png"
)

plt.savefig(path, dpi=300)

print("Saved:", path)

plt.show()
