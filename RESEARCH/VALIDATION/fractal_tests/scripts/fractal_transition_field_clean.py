import numpy as np
import matplotlib.pyplot as plt
import os

OUTPUT_DIR = "RESEARCH/VALIDATION/fractal_tests/scripts/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ================================
# LOAD DATA
# ================================
data = np.genfromtxt(
    os.path.join(OUTPUT_DIR, "transition_probability_data.csv"),
    delimiter=",",
    skip_header=1
)

delta = data[:,0]
distance = data[:,1]
transition = data[:,2]

# remove invalid (distance = -1 inside Mandelbrot)
mask = distance >= 0
delta = delta[mask]
distance = distance[mask]
transition = transition[mask]

# ================================
# GRID
# ================================
grid_x = np.linspace(min(delta), max(delta), 100)
grid_y = np.linspace(min(distance), max(distance), 100)

X, Y = np.meshgrid(grid_x, grid_y)

# ================================
# KERNEL FIELD
# ================================
sigma_d = 2.0
sigma_dist = 10.0

field = np.zeros_like(X)
weight = np.zeros_like(X)

for d, dist, t in zip(delta, distance, transition):

    # Gaussian kernel
    K = np.exp(
        -((X - d)**2 / (2*sigma_d**2) +
          (Y - dist)**2 / (2*sigma_dist**2))
    )

    field += K * t
    weight += K

# normalize
prob = np.zeros_like(field)
mask = weight > 1e-6
prob[mask] = field[mask] / weight[mask]

# ================================
# PLOT
# ================================
plt.figure(figsize=(8,6))

plt.imshow(
    prob,
    origin='lower',
    extent=[grid_x[0], grid_x[-1], grid_y[0], grid_y[-1]],
    aspect='auto',
    vmin=0,
    vmax=1
)

plt.colorbar(label="P(transition)")
plt.xlabel("Δ")
plt.ylabel("continuous distance")
plt.title("Transition Field (Kernel Smoothed)")

plt.savefig(os.path.join(OUTPUT_DIR, "transition_field_clean.png"), dpi=150)
plt.close()

# ================================
# SCATTER OVERLAY
# ================================
plt.figure(figsize=(8,6))

plt.imshow(
    prob,
    origin='lower',
    extent=[grid_x[0], grid_x[-1], grid_y[0], grid_y[-1]],
    aspect='auto',
    vmin=0,
    vmax=1,
    alpha=0.8
)

colors = ["red" if t==1 else "blue" for t in transition]
plt.scatter(delta, distance, c=colors, s=20, edgecolors='k')

plt.xlabel("Δ")
plt.ylabel("distance")
plt.title("Transition Field + Data")

plt.savefig(os.path.join(OUTPUT_DIR, "transition_field_overlay.png"), dpi=150)
plt.close()

print("Clean transition field generated.")
