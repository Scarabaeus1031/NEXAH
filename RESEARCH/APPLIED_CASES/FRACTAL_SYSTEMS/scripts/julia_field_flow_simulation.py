import numpy as np
import matplotlib.pyplot as plt

# =========================
# PARAMETERS
# =========================
resolution = 600
x_min, x_max = -2.0, 1.0
y_min, y_max = -1.5, 1.5
max_iter = 100

# =========================
# GRID
# =========================
x = np.linspace(x_min, x_max, resolution)
y = np.linspace(y_min, y_max, resolution)
X, Y = np.meshgrid(x, y)
C = X + 1j * Y

# =========================
# CONTINUOUS JULIA FIELD
# =========================
Z = np.zeros_like(C)
field = np.zeros_like(X, dtype=float)

for i in range(max_iter):
    Z = Z**2 + C
    mask = np.abs(Z) < 4

    # continuous metric (smooth field)
    field[mask] += np.exp(-np.abs(Z[mask]))

# normalize
field = (field - np.min(field)) / (np.max(field) - np.min(field) + 1e-9)

# =========================
# GRADIENT FIELD
# =========================
gy, gx = np.gradient(field)

# normalize vectors (important for stability)
norm = np.sqrt(gx**2 + gy**2) + 1e-9
gx /= norm
gy /= norm

# =========================
# PARTICLE FLOW SIMULATION
# =========================
num_particles = 150
steps = 120
dt = 0.01

# random starting points
px = np.random.uniform(x_min, x_max, num_particles)
py = np.random.uniform(y_min, y_max, num_particles)

trajectories = []

for i in range(num_particles):
    tx, ty = [px[i]], [py[i]]

    x_p, y_p = px[i], py[i]

    for _ in range(steps):

        # convert to grid index
        ix = int((x_p - x_min) / (x_max - x_min) * (resolution - 1))
        iy = int((y_p - y_min) / (y_max - y_min) * (resolution - 1))

        if ix < 0 or ix >= resolution or iy < 0 or iy >= resolution:
            break

        # move along gradient
        x_p += gx[iy, ix] * dt
        y_p += gy[iy, ix] * dt

        tx.append(x_p)
        ty.append(y_p)

    trajectories.append((tx, ty))

# =========================
# PLOT
# =========================
fig, ax = plt.subplots(figsize=(10, 8))

# background field
ax.imshow(field, extent=[x_min, x_max, y_min, y_max], origin='lower', cmap='viridis')

# gradient field (downsampled)
skip = 20
ax.quiver(
    X[::skip, ::skip],
    Y[::skip, ::skip],
    gx[::skip, ::skip],
    gy[::skip, ::skip],
    color='white',
    alpha=0.6
)

# particle trajectories
for tx, ty in trajectories:
    ax.plot(tx, ty, color='cyan', linewidth=0.7, alpha=0.7)

ax.set_title("Julia Field Flow — Gradient + Particle Dynamics")
ax.set_xlabel("Re(c)")
ax.set_ylabel("Im(c)")

plt.tight_layout()
plt.savefig("julia_field_flow.png", dpi=300)
plt.show()
