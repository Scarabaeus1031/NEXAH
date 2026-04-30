# NEXAH v23 — Cross-System Structure Extraction
#
# Systems:
# Lorenz, Rössler, Kuramoto
#
# Pipeline:
# dynamics → projection → density → gates → structure comparison
#
# Output:
# RESEARCH/visuals/nexah_cross_system_structure_v23.png

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde


# ============================================================
# 1. SYSTEMS
# ============================================================

def simulate_lorenz(steps=6000, dt=0.01):
    s, r, b = 10, 28, 2.667
    x, y, z = 0.1, 0.0, 0.0

    xs, ys = [], []

    for _ in range(steps):
        dx = s * (y - x)
        dy = x * (r - z) - y
        dz = x * y - b * z

        x += dx * dt
        y += dy * dt
        z += dz * dt

        xs.append(x)
        ys.append(y)

    return np.array(xs), np.array(ys)


def simulate_roessler(steps=6000, dt=0.01):
    a, b, c = 0.2, 0.2, 5.7
    x, y, z = 0.1, 0.0, 0.0

    xs, ys = [], []

    for _ in range(steps):
        dx = -y - z
        dy = x + a * y
        dz = b + z * (x - c)

        x += dx * dt
        y += dy * dt
        z += dz * dt

        xs.append(x)
        ys.append(y)

    return np.array(xs), np.array(ys)


def simulate_kuramoto(steps=4000, n=64, dt=0.04, K=2.1):
    theta = np.random.uniform(0, 2*np.pi, n)
    omega = np.random.normal(0, 0.6, n)

    r_hist = []

    for _ in range(steps):
        order = np.mean(np.exp(1j * theta))
        r = np.abs(order)
        psi = np.angle(order)

        r_hist.append(r)

        theta_dot = omega + K * r * np.sin(psi - theta)
        theta = np.mod(theta + dt * theta_dot, 2*np.pi)

    r_hist = np.array(r_hist)
    dr = np.gradient(r_hist)

    return r_hist, dr


# ============================================================
# 2. NEXAH FIELD
# ============================================================

def density_field(x, y, grid_n=220):
    x = np.asarray(x)
    y = np.asarray(y)

    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask]
    y = y[mask]

    x += np.random.normal(0, 1e-7, len(x))
    y += np.random.normal(0, 1e-7, len(y))

    kde = gaussian_kde(np.vstack([x, y]))

    xmin, xmax = x.min(), x.max()
    ymin, ymax = y.min(), y.max()

    X, Y = np.mgrid[xmin:xmax:complex(grid_n), ymin:ymax:complex(grid_n)]
    Z = kde(np.vstack([X.ravel(), Y.ravel()])).reshape(X.shape)

    return X, Y, Z, [xmin, xmax, ymin, ymax]


def detect_gates(Z, percentile=15):
    return Z < np.percentile(Z, percentile)


def grid_to_points(mask, extent, shape, max_points=600):
    gx, gy = np.where(mask)

    gx = np.interp(gx, [0, shape[0]], [extent[0], extent[1]])
    gy = np.interp(gy, [0, shape[1]], [extent[2], extent[3]])

    if len(gx) > max_points:
        idx = np.linspace(0, len(gx) - 1, max_points).astype(int)
        gx = gx[idx]
        gy = gy[idx]

    return gx, gy


# ============================================================
# 3. RUN SYSTEMS
# ============================================================

lx, ly = simulate_lorenz()
rx, ry = simulate_roessler()
kx, ky = simulate_kuramoto()


systems = [
    ("Lorenz", lx, ly),
    ("Rössler", rx, ry),
    ("Kuramoto", kx, ky),
]


# ============================================================
# 4. PLOT
# ============================================================

fig, axes = plt.subplots(3, 3, figsize=(14, 12))

for i, (name, x, y) in enumerate(systems):

    # --- raw ---
    axes[i, 0].plot(x, y, lw=0.5)
    axes[i, 0].set_title(f"{name} — Raw Dynamics")
    axes[i, 0].axis("off")

    # --- field ---
    X, Y, Z, extent = density_field(x, y)
    axes[i, 1].imshow(np.rot90(Z), cmap="viridis", extent=extent)
    axes[i, 1].set_title(f"{name} — Field")
    axes[i, 1].axis("off")

    # --- gates ---
    gates = detect_gates(Z)
    gx, gy = grid_to_points(gates, extent, Z.shape)

    axes[i, 2].imshow(np.rot90(Z), cmap="inferno", extent=extent)
    axes[i, 2].scatter(gx, gy, s=50, c="cyan", alpha=0.15)
    axes[i, 2].scatter(gx, gy, s=10, c="yellow")
    axes[i, 2].set_title(f"{name} — Gates")
    axes[i, 2].axis("off")


# ------------------------------------------------------------
# Title
# ------------------------------------------------------------

fig.suptitle(
    "NEXAH v23 — Cross-System Structure Extraction\n"
    "Lorenz • Rössler • Kuramoto → Same Field & Gate Structure",
    fontsize=15
)

plt.tight_layout()

plt.savefig(
    "RESEARCH/visuals/nexah_cross_system_structure_v23.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
