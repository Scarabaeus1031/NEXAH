# NEXAH v24 — Rotation Field & Gate Detection
#
# Core Idea:
# π = perfect rotation
# NEXAH = where rotation breaks
#
# Pipeline:
# dynamics → density → flow → rotation (curl) → gates
#
# Output:
# RESEARCH/visuals/nexah_rotation_field_v24.png

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde


# ============================================================
# 1. SYSTEM (Lorenz as testbed)
# ============================================================

def simulate_lorenz(steps=7000, dt=0.01):
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


# ============================================================
# 2. FIELD
# ============================================================

def density_field(x, y, grid_n=250):
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


# ============================================================
# 3. FLOW + ROTATION
# ============================================================

def flow_field(Z):
    dZdx, dZdy = np.gradient(Z)
    mag = np.sqrt(dZdx**2 + dZdy**2) + 1e-9

    Fx = -dZdx / mag
    Fy = -dZdy / mag

    return Fx, Fy


def rotation_field(Fx, Fy):
    dFy_dx = np.gradient(Fy, axis=0)
    dFx_dy = np.gradient(Fx, axis=1)

    curl = dFy_dx - dFx_dy
    return curl


# ============================================================
# 4. GATE DETECTION (NEW)
# ============================================================

def detect_gates(Z, curl, density_p=20, rot_p=20):
    low_density = Z < np.percentile(Z, density_p)
    low_rotation = np.abs(curl) < np.percentile(np.abs(curl), rot_p)

    gates = low_density & low_rotation
    return gates


def grid_to_points(mask, extent, shape, max_points=800):
    gx, gy = np.where(mask)

    gx = np.interp(gx, [0, shape[0]], [extent[0], extent[1]])
    gy = np.interp(gy, [0, shape[1]], [extent[2], extent[3]])

    if len(gx) > max_points:
        idx = np.linspace(0, len(gx) - 1, max_points).astype(int)
        gx = gx[idx]
        gy = gy[idx]

    return gx, gy


# ============================================================
# 5. RUN
# ============================================================

x, y = simulate_lorenz()

X, Y, Z, extent = density_field(x, y)

Fx, Fy = flow_field(Z)
curl = rotation_field(Fx, Fy)

gates = detect_gates(Z, curl)
gx, gy = grid_to_points(gates, extent, Z.shape)


# ============================================================
# 6. PLOT
# ============================================================

fig, axes = plt.subplots(1, 4, figsize=(18, 5))

# ------------------------------------------------------------
# 1. Raw
# ------------------------------------------------------------
axes[0].plot(x, y, lw=0.4)
axes[0].set_title("Raw Dynamics")
axes[0].axis("off")

# ------------------------------------------------------------
# 2. Density
# ------------------------------------------------------------
axes[1].imshow(np.rot90(Z), cmap="viridis", extent=extent)
axes[1].set_title("Density Field")
axes[1].axis("off")

# ------------------------------------------------------------
# 3. Rotation (NEW)
# ------------------------------------------------------------
axes[2].imshow(np.rot90(curl), cmap="coolwarm", extent=extent)
axes[2].set_title("Rotation Field (Curl)")
axes[2].axis("off")

# ------------------------------------------------------------
# 4. Gates (NEW DEFINITION)
# ------------------------------------------------------------
axes[3].imshow(np.rot90(Z), cmap="inferno", extent=extent)
axes[3].scatter(gx, gy, s=100, c="cyan", alpha=0.15)
axes[3].scatter(gx, gy, s=12, c="yellow", edgecolors="black", linewidths=0.2)

axes[3].set_title("Gates\n(low density + rotation break)")
axes[3].axis("off")

# ------------------------------------------------------------
# Title
# ------------------------------------------------------------
fig.suptitle(
    "NEXAH v24 — Rotation Breakdown as Transition Geometry\n"
    "π = perfect rotation → Gates = where rotation collapses",
    fontsize=14
)

plt.tight_layout()

plt.savefig(
    "RESEARCH/visuals/nexah_rotation_field_v24.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
