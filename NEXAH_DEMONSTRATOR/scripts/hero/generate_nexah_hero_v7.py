# NEXAH v7 — Cross-System Structure Extraction
# Raw → Field → Regime Geometry → Transition Field

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from sklearn.cluster import KMeans

# -----------------------------
# 1. SYSTEM DEFINITIONS
# -----------------------------

def lorenz(x, y, z, s=10, r=28, b=2.667):
    dx = s * (y - x)
    dy = x * (r - z) - y
    dz = x * y - b * z
    return dx, dy, dz

def halvorsen(x, y, z, a=1.4):
    dx = -a*x - 4*y - 4*z - y*y
    dy = -a*y - 4*z - 4*x - z*z
    dz = -a*z - 4*x - 4*y - x*x
    return dx, dy, dz

def rossler(x, y, z, a=0.2, b=0.2, c=5.7):
    dx = -y - z
    dy = x + a*y
    dz = b + z*(x - c)
    return dx, dy, dz

# -----------------------------
# 2. SIMULATION (STABLE)
# -----------------------------

def simulate(system, steps=12000, dt=0.005):
    xs = np.zeros(steps)
    ys = np.zeros(steps)
    zs = np.zeros(steps)

    xs[0], ys[0], zs[0] = (0.1, 0.0, 0.0)

    for i in range(steps - 1):
        dx, dy, dz = system(xs[i], ys[i], zs[i])

        # CLAMP for stability (fix Halvorsen explosion)
        dx = np.clip(dx, -50, 50)
        dy = np.clip(dy, -50, 50)
        dz = np.clip(dz, -50, 50)

        xs[i+1] = xs[i] + dx * dt
        ys[i+1] = ys[i] + dy * dt
        zs[i+1] = zs[i] + dz * dt

    return xs, ys

# -----------------------------
# 3. FIELD + STRUCTURE
# -----------------------------

def compute_density(xs, ys):
    pts = np.vstack([xs, ys])

    kde = gaussian_kde(pts)
    xmin, xmax = xs.min(), xs.max()
    ymin, ymax = ys.min(), ys.max()

    X, Y = np.mgrid[xmin:xmax:200j, ymin:ymax:200j]
    grid = np.vstack([X.ravel(), Y.ravel()])
    Z = kde(grid).reshape(X.shape)

    return X, Y, Z

def compute_flow(xs, ys):
    dx = np.gradient(xs)
    dy = np.gradient(ys)
    return dx, dy

def compute_coherence(xs, ys):
    dx, dy = compute_flow(xs, ys)

    flow_norm = np.sqrt(dx**2 + dy**2) + 1e-8
    coherence = dx / flow_norm

    return coherence

# -----------------------------
# 4. REGIME GEOMETRY
# -----------------------------

def compute_regimes(xs, ys, k=3):
    data = np.vstack([xs, ys]).T
    kmeans = KMeans(n_clusters=k, n_init=10).fit(data)
    labels = kmeans.labels_
    centers = kmeans.cluster_centers_
    return labels, centers

def compute_gates(Z, coherence_field):
    Z_norm = (Z - Z.min()) / (Z.max() - Z.min())

    low_density = Z_norm < 0.2
    low_coherence = np.abs(coherence_field) < 0.2

    return low_density & low_coherence

# -----------------------------
# 5. PLOTTING
# -----------------------------

systems = [
    ("Lorenz", lorenz),
    ("Halvorsen", halvorsen),
    ("Rössler", rossler),
]

fig, axes = plt.subplots(3, 4, figsize=(18, 10))

for row, (name, system) in enumerate(systems):

    xs, ys = simulate(system)

    # FIELD
    X, Y, Z = compute_density(xs, ys)

    # COHERENCE
    coherence = compute_coherence(xs, ys)

    # REGIMES
    labels, centers = compute_regimes(xs, ys)

    # GRID coherence approx
    coherence_field = np.interp(Z, (Z.min(), Z.max()), (-1, 1))

    # GATES
    gate_mask = compute_gates(Z, coherence_field)

    # -----------------------------
    # 1. RAW
    # -----------------------------
    axes[row, 0].plot(xs, ys, lw=0.3, color="steelblue")
    axes[row, 0].set_title(f"{name}\nRaw Dynamics")
    axes[row, 0].axis("off")

    # -----------------------------
    # 2. FIELD
    # -----------------------------
    axes[row, 1].imshow(np.rot90(Z), cmap="viridis",
                        extent=[xs.min(), xs.max(), ys.min(), ys.max()])

    # flow arrows (subsample)
    idx = np.arange(0, len(xs), 200)
    dx, dy = compute_flow(xs, ys)
    axes[row, 1].quiver(xs[idx], ys[idx], dx[idx], dy[idx],
                        color="black", scale=50, width=0.002)

    axes[row, 1].set_title("Field\nDensity + Flow")
    axes[row, 1].axis("off")

    # -----------------------------
    # 3. REGIME GEOMETRY
    # -----------------------------
    axes[row, 2].scatter(xs, ys, c=labels, cmap="Pastel1", s=1, alpha=0.6)

    axes[row, 2].scatter(centers[:,0], centers[:,1],
                         color="black", s=50, marker="x", label="Basins")

    axes[row, 2].set_title("Regime Geometry\nBasins + Gates")
    axes[row, 2].axis("off")

    # -----------------------------
    # 4. TRANSITION FIELD
    # -----------------------------
    axes[row, 3].imshow(np.rot90(Z), cmap="viridis",
                        extent=[xs.min(), xs.max(), ys.min(), ys.max()])

    # highlight trajectory
    axes[row, 3].plot(xs, ys, color="white", lw=0.5)

    # gates overlay
    gx, gy = np.where(gate_mask)
    axes[row, 3].scatter(
        np.interp(gx, [0, Z.shape[0]], [xs.min(), xs.max()]),
        np.interp(gy, [0, Z.shape[1]], [ys.min(), ys.max()]),
        s=5, color="black", alpha=0.5, label="Gates"
    )

    axes[row, 3].set_title("Transition Field\nCoherence + Path")
    axes[row, 3].axis("off")

# -----------------------------
# GLOBAL TITLE
# -----------------------------
fig.suptitle(
    "NEXAH — Cross-System Structure Extraction\n"
    "Dynamics → Field → Basins/Gates → Navigable Transition Structure",
    fontsize=16
)

plt.tight_layout()

# -----------------------------
# SAVE
# -----------------------------
plt.savefig(
    "NEXAH_DEMONSTRATOR/visuals/nexah_structure_cross_system_v7.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
