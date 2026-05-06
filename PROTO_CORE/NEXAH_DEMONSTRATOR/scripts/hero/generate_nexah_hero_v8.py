# NEXAH v8 — Cross-System Structure Extraction (Neon Gates)

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from sklearn.cluster import KMeans

# -----------------------------
# SYSTEMS
# -----------------------------
def lorenz(x, y, z, s=10, r=28, b=2.667):
    return s*(y-x), x*(r-z)-y, x*y-b*z

def halvorsen(x, y, z, a=1.4):
    return (
        -a*x - 4*y - 4*z - y*y,
        -a*y - 4*z - 4*x - z*z,
        -a*z - 4*x - 4*y - x*x
    )

def rossler(x, y, z, a=0.2, b=0.2, c=5.7):
    return -y-z, x+a*y, b+z*(x-c)

# -----------------------------
# SIMULATION
# -----------------------------
def simulate(system, steps=12000, dt=0.005):
    xs = np.zeros(steps)
    ys = np.zeros(steps)
    zs = np.zeros(steps)

    xs[0], ys[0], zs[0] = (0.1, 0.0, 0.0)

    for i in range(steps-1):
        dx, dy, dz = system(xs[i], ys[i], zs[i])

        dx = np.clip(dx, -50, 50)
        dy = np.clip(dy, -50, 50)
        dz = np.clip(dz, -50, 50)

        xs[i+1] = xs[i] + dx * dt
        ys[i+1] = ys[i] + dy * dt
        zs[i+1] = zs[i] + dz * dt

    return xs, ys

# -----------------------------
# FIELD
# -----------------------------
def compute_density(xs, ys):
    pts = np.vstack([xs, ys])
    kde = gaussian_kde(pts)

    xmin, xmax = xs.min(), xs.max()
    ymin, ymax = ys.min(), ys.max()

    X, Y = np.mgrid[xmin:xmax:200j, ymin:ymax:200j]
    Z = kde(np.vstack([X.ravel(), Y.ravel()])).reshape(X.shape)

    return X, Y, Z

def compute_flow(xs, ys):
    return np.gradient(xs), np.gradient(ys)

def compute_coherence(xs, ys):
    dx, dy = compute_flow(xs, ys)
    norm = np.sqrt(dx**2 + dy**2) + 1e-8
    return dx / norm

# -----------------------------
# REGIMES
# -----------------------------
def compute_regimes(xs, ys, k=3):
    data = np.vstack([xs, ys]).T
    kmeans = KMeans(n_clusters=k, n_init=10).fit(data)
    return kmeans.labels_, kmeans.cluster_centers_

# -----------------------------
# GATES
# -----------------------------
def compute_gates(Z, coherence_field):
    Z_norm = (Z - Z.min()) / (Z.max() - Z.min())
    low_density = Z_norm < 0.2
    low_coherence = np.abs(coherence_field) < 0.2
    return low_density & low_coherence

# -----------------------------
# SYSTEM LIST
# -----------------------------
systems = [
    ("Lorenz", lorenz),
    ("Halvorsen", halvorsen),
    ("Rössler", rossler),
]

fig, axes = plt.subplots(3, 4, figsize=(18, 10))

# -----------------------------
# LOOP
# -----------------------------
for row, (name, system) in enumerate(systems):

    xs, ys = simulate(system)

    X, Y, Z = compute_density(xs, ys)
    coherence = compute_coherence(xs, ys)

    labels, centers = compute_regimes(xs, ys)

    coherence_field = np.interp(Z, (Z.min(), Z.max()), (-1, 1))
    gate_mask = compute_gates(Z, coherence_field)

    # Convert gate mask to coordinates
    gx, gy = np.where(gate_mask)

    gx = np.interp(gx, [0, Z.shape[0]], [xs.min(), xs.max()])
    gy = np.interp(gy, [0, Z.shape[1]], [ys.min(), ys.max()])

    # -----------------------------
    # RAW
    # -----------------------------
    axes[row, 0].plot(xs, ys, lw=0.3, color="steelblue")
    axes[row, 0].set_title(f"{name}\nRaw Dynamics")
    axes[row, 0].axis("off")

    # -----------------------------
    # FIELD
    # -----------------------------
    axes[row, 1].imshow(np.rot90(Z), cmap="viridis",
                        extent=[xs.min(), xs.max(), ys.min(), ys.max()])

    dx, dy = compute_flow(xs, ys)
    idx = np.arange(0, len(xs), 200)

    axes[row, 1].quiver(xs[idx], ys[idx], dx[idx], dy[idx],
                        color="black", scale=50, width=0.002)

    axes[row, 1].set_title("Field\nDensity + Flow")
    axes[row, 1].axis("off")

    # -----------------------------
    # REGIME GEOMETRY + NEON GATES
    # -----------------------------
    axes[row, 2].scatter(xs, ys, c=labels, cmap="Pastel1", s=1, alpha=0.5)

    axes[row, 2].scatter(centers[:,0], centers[:,1],
                         color="black", s=60, marker="x")

    # Neon glow
    axes[row, 2].scatter(gx, gy, s=120, c="cyan", alpha=0.15, edgecolors="none")

    # Core
    axes[row, 2].scatter(gx, gy, s=25, c="yellow",
                         edgecolors="black", linewidths=0.4)

    axes[row, 2].set_title("Regime Geometry\nBasins + Gates")
    axes[row, 2].axis("off")

    # -----------------------------
    # TRANSITION FIELD + NEON GATES
    # -----------------------------
    axes[row, 3].imshow(np.rot90(Z), cmap="viridis",
                        extent=[xs.min(), xs.max(), ys.min(), ys.max()])

    axes[row, 3].plot(xs, ys, color="white", lw=0.5)

    # Glow
    axes[row, 3].scatter(gx, gy, s=140, c="cyan", alpha=0.18, edgecolors="none")

    # Core
    axes[row, 3].scatter(gx, gy, s=30, c="yellow",
                         edgecolors="black", linewidths=0.4)

    axes[row, 3].set_title("Transition Field\nCoherence + Path")
    axes[row, 3].axis("off")

# -----------------------------
# TITLE
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
    "NEXAH_DEMONSTRATOR/visuals/nexah_structure_cross_system_v8.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
