# NEXAH v25 — Unified Gate Operator
#
# Gate = low density + low coherence + low rotation
#
# Output:
# NEXAH_DEMONSTRATOR/visuals/nexah_unified_gate_operator_v25.png

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde


# ============================================================
# 1. SYSTEM
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


# ============================================================
# 2. FIELD
# ============================================================

def density_field(x, y, grid_n=240):
    x += np.random.normal(0, 1e-7, len(x))
    y += np.random.normal(0, 1e-7, len(y))

    kde = gaussian_kde(np.vstack([x, y]))

    xmin, xmax = x.min(), x.max()
    ymin, ymax = y.min(), y.max()

    X, Y = np.mgrid[xmin:xmax:complex(grid_n), ymin:ymax:complex(grid_n)]
    Z = kde(np.vstack([X.ravel(), Y.ravel()])).reshape(X.shape)

    return X, Y, Z, [xmin, xmax, ymin, ymax]


# ============================================================
# 3. FLOW / COHERENCE / ROTATION
# ============================================================

def flow_field(Z):
    dZdx, dZdy = np.gradient(Z)
    mag = np.sqrt(dZdx**2 + dZdy**2) + 1e-9
    Fx = -dZdx / mag
    Fy = -dZdy / mag
    return Fx, Fy, dZdx, dZdy


def coherence_field(Fx, Fy, dZdx, dZdy):
    dot = Fx * dZdx + Fy * dZdy
    mag1 = np.sqrt(Fx**2 + Fy**2)
    mag2 = np.sqrt(dZdx**2 + dZdy**2) + 1e-9
    C = dot / (mag1 * mag2 + 1e-9)
    return C


def rotation_field(Fx, Fy):
    dFy_dx = np.gradient(Fy, axis=0)
    dFx_dy = np.gradient(Fx, axis=1)
    return dFy_dx - dFx_dy


# ============================================================
# 4. NORMALIZE + GATE OPERATOR
# ============================================================

def normalize(A):
    return (A - np.min(A)) / (np.max(A) - np.min(A) + 1e-9)


def gate_operator(Z, C, curl):
    Zn = normalize(Z)
    Cn = normalize(np.abs(C))
    Rn = normalize(np.abs(curl))

    # low everything → gate
    G = (1 - Zn) * (1 - Cn) * (1 - Rn)
    return G


# ============================================================
# 5. RUN
# ============================================================

x, y = simulate_lorenz()

X, Y, Z, extent = density_field(x, y)

Fx, Fy, dZdx, dZdy = flow_field(Z)
C = coherence_field(Fx, Fy, dZdx, dZdy)
curl = rotation_field(Fx, Fy)

G = gate_operator(Z, C, curl)

threshold = np.percentile(G, 92)
mask = G > threshold

gx, gy = np.where(mask)
gx = np.interp(gx, [0, Z.shape[0]], [extent[0], extent[1]])
gy = np.interp(gy, [0, Z.shape[1]], [extent[2], extent[3]])


# ============================================================
# 6. PLOT
# ============================================================

fig, axes = plt.subplots(1, 5, figsize=(20, 5))

# Raw
axes[0].plot(x, y, lw=0.4)
axes[0].set_title("Dynamics")
axes[0].axis("off")

# Density
axes[1].imshow(np.rot90(Z), cmap="viridis", extent=extent)
axes[1].set_title("Density")
axes[1].axis("off")

# Coherence
axes[2].imshow(np.rot90(C), cmap="coolwarm", extent=extent)
axes[2].set_title("Coherence")
axes[2].axis("off")

# Rotation
axes[3].imshow(np.rot90(curl), cmap="coolwarm", extent=extent)
axes[3].set_title("Rotation")
axes[3].axis("off")

# Gates
axes[4].imshow(np.rot90(G), cmap="inferno", extent=extent)
axes[4].scatter(gx, gy, s=12, c="cyan")
axes[4].set_title("Unified Gates")
axes[4].axis("off")

fig.suptitle(
    "NEXAH v25 — Unified Gate Operator\n"
    "G = (1-ρ)(1-C)(1-R)",
    fontsize=14
)

plt.tight_layout()

plt.savefig(
    "NEXAH_DEMONSTRATOR/visuals/nexah_unified_gate_operator_v25.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
