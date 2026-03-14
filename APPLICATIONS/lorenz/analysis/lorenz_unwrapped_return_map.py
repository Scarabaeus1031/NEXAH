import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os

sigma = 10
rho = 28
beta = 8 / 3

dt = 0.01
steps = 180000

OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_navigation"
os.makedirs(OUTPUT_DIR, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")


def lorenz(x, y, z):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return dx, dy, dz


# --------------------------------------------------
# integrate trajectory
# --------------------------------------------------

x = np.zeros(steps)
y = np.zeros(steps)
z = np.zeros(steps)

x[0], y[0], z[0] = 1.0, 1.0, 1.0

for i in range(steps - 1):
    dx, dy, dz = lorenz(x[i], y[i], z[i])
    x[i + 1] = x[i] + dt * dx
    y[i + 1] = y[i] + dt * dy
    z[i + 1] = z[i] + dt * dz


# transient weg
x = x[5000:]
y = y[5000:]
z = z[5000:]


# --------------------------------------------------
# detect L/R switches
# --------------------------------------------------

switch_idx = []
for i in range(1, len(x)):
    if np.sign(x[i]) != np.sign(x[i - 1]):
        switch_idx.append(i)

switch_idx = np.array(switch_idx)

xs = x[switch_idx]
zs = z[switch_idx]

# --------------------------------------------------
# build return coordinate u in [0,1]
# here: normalized z on switch section
# --------------------------------------------------

zmin = np.min(zs)
zmax = np.max(zs)
u = (zs - zmin) / (zmax - zmin)

# optional: sort-like unwrapping by x sign neighborhood
# keep simple first: use normalized switch coordinate only

u_n = u[:-1]
u_np1 = u[1:]

# ideal doubling map
grid = np.linspace(0, 1, 500)
doubling = (2 * grid) % 1

# --------------------------------------------------
# Plot 1: raw return map + ideal doubling map
# --------------------------------------------------

fig, ax = plt.subplots(1, 2, figsize=(14, 6), constrained_layout=True)

ax[0].scatter(u_n, u_np1, s=6, alpha=0.5, label="Lorenz return map")
ax[0].plot(grid, doubling, color="red", linewidth=1.5, label="ideal: (2u) mod 1")
ax[0].set_xlabel("u_n")
ax[0].set_ylabel("u_{n+1}")
ax[0].set_title("Lorenz Return Map vs Doubling Map")
ax[0].legend()

# --------------------------------------------------
# Plot 2: histogram of return coordinate
# --------------------------------------------------

ax[1].hist(u, bins=60, alpha=0.85)
ax[1].set_xlabel("u")
ax[1].set_ylabel("count")
ax[1].set_title("Switch-Section Coordinate Distribution")

filename = f"{OUTPUT_DIR}/lorenz_unwrapped_return_map_{timestamp}.png"
plt.savefig(filename, dpi=300, bbox_inches="tight")
print("saved:", filename)
plt.show()

# --------------------------------------------------
# Plot 3: corridor colored by unwrapped coordinate
# --------------------------------------------------

plt.figure(figsize=(8, 8))
plt.scatter(x, z, s=0.15, alpha=0.08, label="trajectory cloud")
plt.scatter(xs, zs, c=u, s=8, cmap="plasma", label="switch points")
plt.xlabel("x")
plt.ylabel("z")
plt.title("Lorenz Switch Corridor (colored by return coordinate u)")
plt.legend()

filename2 = f"{OUTPUT_DIR}/lorenz_switch_corridor_unwrapped_{timestamp}.png"
plt.savefig(filename2, dpi=300, bbox_inches="tight")
print("saved:", filename2)
plt.show()
