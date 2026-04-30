# RESEARCH/visuals/nexah_slice_operator_v16.py

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# -----------------------------
# SYSTEMS
# -----------------------------

def lorenz_system(n=8000, dt=0.01):
    def f(x, y, z):
        return 10*(y-x), x*(28-z)-y, x*y - 2.667*z

    xs = np.zeros(n)
    ys = np.zeros(n)
    zs = np.zeros(n)
    xs[0], ys[0], zs[0] = 0.1, 0, 0

    for i in range(n-1):
        dx, dy, dz = f(xs[i], ys[i], zs[i])
        xs[i+1] = xs[i] + dx*dt
        ys[i+1] = ys[i] + dy*dt
        zs[i+1] = zs[i] + dz*dt

    return xs, ys


def rossler_system(n=8000, dt=0.01):
    def f(x, y, z):
        return -y - z, x + 0.2*y, 0.2 + z*(x - 5.7)

    xs = np.zeros(n)
    ys = np.zeros(n)
    zs = np.zeros(n)
    xs[0], ys[0], zs[0] = 0.1, 0, 0

    for i in range(n-1):
        dx, dy, dz = f(xs[i], ys[i], zs[i])
        xs[i+1] = xs[i] + dx*dt
        ys[i+1] = ys[i] + dy*dt
        zs[i+1] = zs[i] + dz*dt

    return xs, ys


def kuramoto_slice(n_agents=80, steps=3000, dt=0.05, K=2.0):
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


# -----------------------------
# STRUCTURE EXTRACTION
# -----------------------------

def compute_density(x, y):
    points = np.vstack([x, y])

    mask = np.isfinite(points).all(axis=0)
    points = points[:, mask]

    kde = gaussian_kde(points)

    xmin, xmax = x.min(), x.max()
    ymin, ymax = y.min(), y.max()

    X, Y = np.mgrid[xmin:xmax:200j, ymin:ymax:200j]
    pos = np.vstack([X.ravel(), Y.ravel()])
    Z = np.reshape(kde(pos).T, X.shape)

    return X, Y, Z


def detect_gates(Z, threshold=0.02):
    return Z < threshold


# -----------------------------
# SYSTEM DATA
# -----------------------------

systems = [
    ("Lorenz", lorenz_system),
    ("Rössler", rossler_system),
]

# special case Kuramoto
kuramoto_data = kuramoto_slice()

# -----------------------------
# PLOT
# -----------------------------

fig, axes = plt.subplots(3, 4, figsize=(16, 10))

titles = ["Raw", "Slice", "Density", "Gates"]

for i in range(3):
    for j in range(4):
        axes[i, j].set_xticks([])
        axes[i, j].set_yticks([])

# ---- Lorenz & Rössler ----

for i, (name, fn) in enumerate(systems):
    x, y = fn()

    # Raw
    axes[i, 0].plot(x, y, lw=0.5)
    axes[i, 0].set_title(f"{name}\nRaw")

    # Slice = identity here
    axes[i, 1].scatter(x, y, s=1)
    axes[i, 1].set_title("Slice Projection")

    # Density
    X, Y, Z = compute_density(x, y)
    axes[i, 2].imshow(np.rot90(Z), cmap='viridis',
                      extent=[x.min(), x.max(), y.min(), y.max()])
    axes[i, 2].set_title("Density Field")

    # Gates
    gates = detect_gates(Z)
    axes[i, 3].imshow(np.rot90(gates), cmap='inferno',
                      extent=[x.min(), x.max(), y.min(), y.max()])
    axes[i, 3].set_title("Gate Regions")

# ---- Kuramoto ----

r, dr = kuramoto_data

# Raw
axes[2, 0].plot(r, lw=1)
axes[2, 0].set_title("Kuramoto\nr(t)")

# Slice
axes[2, 1].scatter(r, dr, s=2)
axes[2, 1].set_title("Slice (r, dr/dt)")

# Density
X, Y, Z = compute_density(r, dr)
axes[2, 2].imshow(np.rot90(Z), cmap='viridis',
                  extent=[r.min(), r.max(), dr.min(), dr.max()])
axes[2, 2].set_title("Density Field")

# Gates
gates = detect_gates(Z)
axes[2, 3].imshow(np.rot90(gates), cmap='inferno',
                  extent=[r.min(), r.max(), dr.min(), dr.max()])
axes[2, 3].set_title("Gate Regions")

# -----------------------------
# TITLE
# -----------------------------

fig.suptitle(
    "NEXAH v16 — Slice Operator\nSystem → Slice → Density → Gates",
    fontsize=16
)

plt.tight_layout()

# -----------------------------
# SAVE
# -----------------------------

output_path = "RESEARCH/visuals/nexah_slice_operator_v16.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Saved visual to: {output_path}")

plt.show()
