# NEXAH v18 — Manifold → Navigation Field
#
# Idea:
# 2D slice is not the full structure.
# We reconstruct a lifted manifold-like space and derive a navigation field on it.
#
# Systems:
# - Lorenz
# - Rössler
# - Kuramoto
#
# Output:
# NEXAH_DEMONSTRATOR/visuals/nexah_manifold_navigation_field_v18.png

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


# ============================================================
# SYSTEMS
# ============================================================

def lorenz(n=9000, dt=0.01):
    def f(x, y, z):
        return 10 * (y - x), x * (28 - z) - y, x * y - 2.667 * z

    xs, ys, zs = np.zeros(n), np.zeros(n), np.zeros(n)
    xs[0], ys[0], zs[0] = 0.1, 0.0, 0.0

    for i in range(n - 1):
        dx, dy, dz = f(xs[i], ys[i], zs[i])
        xs[i + 1] = xs[i] + dx * dt
        ys[i + 1] = ys[i] + dy * dt
        zs[i + 1] = zs[i] + dz * dt

    return xs[1000:], ys[1000:]


def rossler(n=10000, dt=0.01):
    def f(x, y, z):
        return -y - z, x + 0.2 * y, 0.2 + z * (x - 5.7)

    xs, ys, zs = np.zeros(n), np.zeros(n), np.zeros(n)
    xs[0], ys[0], zs[0] = 0.1, 0.0, 0.0

    for i in range(n - 1):
        dx, dy, dz = f(xs[i], ys[i], zs[i])
        xs[i + 1] = xs[i] + dx * dt
        ys[i + 1] = ys[i] + dy * dt
        zs[i + 1] = zs[i] + dz * dt

    return xs[1500:], ys[1500:]


def kuramoto(n_agents=64, steps=3500, dt=0.04, K=2.2, seed=7):
    rng = np.random.default_rng(seed)
    theta = rng.uniform(0, 2 * np.pi, n_agents)
    omega = rng.normal(0.0, 0.55, n_agents)

    r_vals = np.zeros(steps)

    for t in range(steps):
        order = np.mean(np.exp(1j * theta))
        r = np.abs(order)
        psi = np.angle(order)

        r_vals[t] = r

        theta_dot = omega + K * r * np.sin(psi - theta)
        theta = np.mod(theta + dt * theta_dot, 2 * np.pi)

    dr = np.gradient(r_vals)
    return r_vals[300:], (dr * 25.0)[300:]


# ============================================================
# FIELD HELPERS
# ============================================================

def density_field(x, y, grid_n=220):
    x = np.asarray(x)
    y = np.asarray(y)

    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask]
    y = y[mask]

    # avoid KDE singularity
    x = x + np.random.normal(0, 1e-6, len(x))
    y = y + np.random.normal(0, 1e-6, len(y))

    kde = gaussian_kde(np.vstack([x, y]))

    xmin, xmax = x.min(), x.max()
    ymin, ymax = y.min(), y.max()

    X, Y = np.mgrid[xmin:xmax:complex(grid_n), ymin:ymax:complex(grid_n)]
    Z = kde(np.vstack([X.ravel(), Y.ravel()])).reshape(X.shape)

    return X, Y, Z, [xmin, xmax, ymin, ymax]


def navigation_field(Z):
    # navigation proxy:
    # move toward high-density stable structure
    # while avoiding low-density gate/void areas
    dZdx, dZdy = np.gradient(Z)

    mag = np.sqrt(dZdx**2 + dZdy**2) + 1e-12
    Fx = dZdx / mag
    Fy = dZdy / mag

    return Fx, Fy


def detect_gates(Z, percentile=18):
    return Z < np.percentile(Z, percentile)


def gate_points(mask, extent, shape, max_points=700):
    gx, gy = np.where(mask)

    gx = np.interp(gx, [0, shape[0]], [extent[0], extent[1]])
    gy = np.interp(gy, [0, shape[1]], [extent[2], extent[3]])

    if len(gx) > max_points:
        idx = np.linspace(0, len(gx) - 1, max_points).astype(int)
        gx = gx[idx]
        gy = gy[idx]

    return gx, gy


def lift_manifold(x, y, Z, extent):
    # lifted manifold coordinate:
    # z_lift = normalized density sampled from the field
    xmin, xmax, ymin, ymax = extent

    xi = np.clip(((x - xmin) / (xmax - xmin) * (Z.shape[0] - 1)).astype(int), 0, Z.shape[0] - 1)
    yi = np.clip(((y - ymin) / (ymax - ymin) * (Z.shape[1] - 1)).astype(int), 0, Z.shape[1] - 1)

    z = Z[xi, yi]
    z = (z - z.min()) / (z.max() - z.min() + 1e-12)

    return z


# ============================================================
# RUN
# ============================================================

systems = [
    ("Lorenz", lorenz, "S(x) = (x, y)"),
    ("Rössler", rossler, "S(x) = (x, y)"),
    ("Kuramoto", kuramoto, "S(θ) = (r, dr/dt)"),
]

fig = plt.figure(figsize=(18, 13))

for row, (name, fn, slice_label) in enumerate(systems):
    x, y = fn()

    X, Y, Z, extent = density_field(x, y)
    Fx, Fy = navigation_field(Z)
    gates = detect_gates(Z)
    gx, gy = gate_points(gates, extent, Z.shape)

    z_lift = lift_manifold(x, y, Z, extent)

    # --------------------------------------------------------
    # 1. Slice field
    # --------------------------------------------------------
    ax1 = fig.add_subplot(3, 3, row * 3 + 1)

    ax1.imshow(np.rot90(Z), cmap="viridis", extent=extent, aspect="auto")
    ax1.plot(x, y, color="white", lw=0.65, alpha=0.75)

    ax1.scatter(gx, gy, s=80, c="cyan", alpha=0.12, edgecolors="none")
    ax1.scatter(gx, gy, s=16, c="yellow", alpha=0.8, edgecolors="black", linewidths=0.2)

    ax1.set_title(f"{name}\nSlice Field\n{slice_label}")
    ax1.axis("off")

    # --------------------------------------------------------
    # 2. Lifted manifold
    # --------------------------------------------------------
    ax2 = fig.add_subplot(3, 3, row * 3 + 2, projection="3d")

    t = np.linspace(0, 1, len(x))

    ax2.scatter(
        x,
        y,
        z_lift,
        c=t,
        cmap="plasma",
        s=1.4,
        alpha=0.75,
    )

    ax2.set_title("Lifted Manifold\nz = density support")
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.set_zticks([])
    ax2.view_init(elev=25, azim=235)

    # --------------------------------------------------------
    # 3. Navigation field
    # --------------------------------------------------------
    ax3 = fig.add_subplot(3, 3, row * 3 + 3)

    ax3.imshow(np.rot90(Z), cmap="inferno", extent=extent, aspect="auto")

    ax3.quiver(
        X[::15, ::15],
        Y[::15, ::15],
        Fx[::15, ::15],
        Fy[::15, ::15],
        color="white",
        scale=35,
        width=0.002,
        alpha=0.55,
    )

    ax3.plot(x, y, color="white", lw=0.55, alpha=0.6)

    ax3.scatter(gx, gy, s=100, c="cyan", alpha=0.14, edgecolors="none")
    ax3.scatter(gx, gy, s=18, c="yellow", alpha=0.85, edgecolors="black", linewidths=0.25)

    ax3.set_title("Navigation Field\nflow over gates")
    ax3.axis("off")


fig.suptitle(
    "NEXAH v18 — Manifold → Navigation Field\n"
    "Slice structure is lifted into a navigable field geometry",
    fontsize=16,
)

plt.tight_layout(rect=[0, 0, 1, 0.94])

out = "NEXAH_DEMONSTRATOR/visuals/nexah_manifold_navigation_field_v18.png"

plt.savefig(out, dpi=300, bbox_inches="tight")

print(f"Saved visual to: {out}")

plt.show()
