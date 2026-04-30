import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ============================================================
# SYSTEMS
# ============================================================

def lorenz(n=8000, dt=0.01):
    def f(x, y, z):
        return 10*(y-x), x*(28-z)-y, x*y - 2.667*z

    xs, ys, zs = np.zeros(n), np.zeros(n), np.zeros(n)
    xs[0], ys[0], zs[0] = 0.1, 0, 0

    for i in range(n-1):
        dx, dy, dz = f(xs[i], ys[i], zs[i])
        xs[i+1] = xs[i] + dx*dt
        ys[i+1] = ys[i] + dy*dt
        zs[i+1] = zs[i] + dz*dt

    return xs, ys


def rossler(n=8000, dt=0.01):
    def f(x, y, z):
        return -y - z, x + 0.2*y, 0.2 + z*(x - 5.7)

    xs, ys, zs = np.zeros(n), np.zeros(n), np.zeros(n)
    xs[0], ys[0], zs[0] = 0.1, 0, 0

    for i in range(n-1):
        dx, dy, dz = f(xs[i], ys[i], zs[i])
        xs[i+1] = xs[i] + dx*dt
        ys[i+1] = ys[i] + dy*dt
        zs[i+1] = zs[i] + dz*dt

    return xs, ys


def kuramoto(n_agents=60, steps=3000, dt=0.05, K=2.0):
    theta = np.random.uniform(0, 2*np.pi, n_agents)
    omega = np.random.normal(0, 1, n_agents)

    r_vals = []

    for _ in range(steps):
        r = np.abs(np.mean(np.exp(1j * theta)))
        r_vals.append(r)

        coupling = np.sum(np.sin(theta[:, None] - theta), axis=1)
        theta += (omega + K * coupling / n_agents) * dt

    r_vals = np.array(r_vals)
    dr = np.gradient(r_vals)

    return r_vals, dr


# ============================================================
# PLOT
# ============================================================

fig = plt.figure(figsize=(15, 5))

# ------------------------------------------------------------
# Lorenz 3D Slice Manifold
# ------------------------------------------------------------
ax1 = fig.add_subplot(131, projection='3d')

x, y = lorenz()
t = np.linspace(0, 1, len(x))

ax1.scatter(x, y, t, c=t, cmap='plasma', s=1)

ax1.set_title("Lorenz\nSlice → 3D Manifold")
ax1.set_xlabel("x")
ax1.set_ylabel("y")
ax1.set_zlabel("time")

# ------------------------------------------------------------
# Rössler
# ------------------------------------------------------------
ax2 = fig.add_subplot(132, projection='3d')

x, y = rossler()
t = np.linspace(0, 1, len(x))

ax2.scatter(x, y, t, c=t, cmap='viridis', s=1)

ax2.set_title("Rössler\nSlice → 3D Manifold")
ax2.set_xlabel("x")
ax2.set_ylabel("y")
ax2.set_zlabel("time")

# ------------------------------------------------------------
# Kuramoto
# ------------------------------------------------------------
ax3 = fig.add_subplot(133, projection='3d')

r, dr = kuramoto()
t = np.linspace(0, 1, len(r))

ax3.scatter(r, dr, t, c=t, cmap='inferno', s=2)

ax3.set_title("Kuramoto\n(r, dr/dt, t)")
ax3.set_xlabel("r")
ax3.set_ylabel("dr/dt")
ax3.set_zlabel("time")

# ------------------------------------------------------------
# GLOBAL
# ------------------------------------------------------------

fig.suptitle(
    "NEXAH v17 — Slice → Manifold Reconstruction\n"
    "2D slice is projection of higher-dimensional structure",
    fontsize=14
)

plt.tight_layout()

# Save
output_path = "RESEARCH/visuals/nexah_slice_manifold_v17.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')

print(f"Saved visual to: {output_path}")

plt.show()
