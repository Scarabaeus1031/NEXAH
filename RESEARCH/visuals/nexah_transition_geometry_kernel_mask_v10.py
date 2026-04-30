import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from sklearn.cluster import KMeans
import json

# ============================================================
# SYSTEMS
# ============================================================

def lorenz(x, y, z, s=10, r=28, b=2.667):
    return s*(y-x), x*(r-z)-y, x*y - b*z

def simulate(system, steps=10000, dt=0.01):
    xs, ys, zs = np.zeros(steps), np.zeros(steps), np.zeros(steps)
    xs[0], ys[0], zs[0] = (0.1, 0.0, 0.0)

    for i in range(steps - 1):
        dx, dy, dz = system(xs[i], ys[i], zs[i])

        xs[i+1] = xs[i] + dx*dt
        ys[i+1] = ys[i] + dy*dt
        zs[i+1] = zs[i] + dz*dt

    return xs, ys

# ============================================================
# FIELD + STRUCTURE
# ============================================================

def density_field(xs, ys):
    kde = gaussian_kde(np.vstack([xs, ys]))

    xmin, xmax = xs.min(), xs.max()
    ymin, ymax = ys.min(), ys.max()

    X, Y = np.mgrid[xmin:xmax:250j, ymin:ymax:250j]
    Z = kde(np.vstack([X.ravel(), Y.ravel()])).reshape(X.shape)

    return X, Y, Z

def regime_partition(xs, ys, k=3):
    data = np.vstack([xs, ys]).T
    kmeans = KMeans(n_clusters=k, n_init=10).fit(data)
    return kmeans.labels_, kmeans.cluster_centers_

def detect_gates(Z):
    threshold = np.percentile(Z, 20)
    return Z < threshold

# ============================================================
# TRANSITION GRAPH
# ============================================================

def transition_graph(xs, ys, labels):
    edges = set()

    for i in range(len(labels)-1):
        a = labels[i]
        b = labels[i+1]
        if a != b:
            edges.add((int(a), int(b)))

    return list(edges)

# ============================================================
# PIPELINE
# ============================================================

systems = {
    "Lorenz": lorenz
}

results = {}

fig, axes = plt.subplots(1, 4, figsize=(18, 4))

for name, system in systems.items():

    xs, ys = simulate(system)

    # FIELD
    X, Y, Z = density_field(xs, ys)

    # REGIMES
    labels, centers = regime_partition(xs, ys)

    # GATES
    gate_mask = detect_gates(Z)

    # TRANSITION GRAPH
    edges = transition_graph(xs, ys, labels)

    # METRICS
    results[name] = {
        "num_points": int(len(xs)),
        "num_regimes": int(len(centers)),
        "num_gates": int(np.sum(gate_mask)),
        "transition_edges": edges
    }

    extent = [xs.min(), xs.max(), ys.min(), ys.max()]

    # --------------------------------------------------------
    # 1. RAW
    # --------------------------------------------------------
    axes[0].plot(xs, ys, lw=0.3)
    axes[0].set_title("Raw Dynamics")
    axes[0].axis("off")

    # --------------------------------------------------------
    # 2. FIELD
    # --------------------------------------------------------
    axes[1].imshow(np.rot90(Z), cmap="viridis", extent=extent)
    axes[1].set_title("Field")
    axes[1].axis("off")

    # --------------------------------------------------------
    # 3. REGIMES + GATES
    # --------------------------------------------------------
    axes[2].scatter(xs, ys, c=labels, s=1, cmap="Pastel1")

    gx, gy = np.where(gate_mask)
    gx = np.interp(gx, [0, Z.shape[0]], [xs.min(), xs.max()])
    gy = np.interp(gy, [0, Z.shape[1]], [ys.min(), ys.max()])

    axes[2].scatter(gx, gy, color="cyan", s=2, alpha=0.3)

    axes[2].scatter(
        centers[:,0],
        centers[:,1],
        color="black",
        s=60,
        marker="x"
    )

    axes[2].set_title("Basins + Gates")
    axes[2].axis("off")

    # --------------------------------------------------------
    # 4. KERNEL MASK (Transitions)
    # --------------------------------------------------------
    axes[3].imshow(np.rot90(Z), cmap="inferno", extent=extent)

    axes[3].scatter(gx, gy, color="cyan", s=3, alpha=0.5)

    axes[3].plot(xs, ys, color="white", lw=0.4)

    axes[3].set_title("Kernel Mask")
    axes[3].axis("off")

# ============================================================
# SAVE VISUAL
# ============================================================

plt.suptitle(
    "NEXAH v10 — Transition Geometry Kernel Mask\n"
    "Dynamics → Field → Basins/Gates → Transition Graph",
    fontsize=14
)

plt.tight_layout()

plt.savefig(
    "RESEARCH/visuals/nexah_transition_geometry_kernel_mask_v10.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ============================================================
# SAVE JSON
# ============================================================

with open("RESEARCH/visuals/nexah_transition_geometry_kernel_mask_v10.json", "w") as f:
    json.dump(results, f, indent=2)

print("Saved:")
print("- nexah_transition_geometry_kernel_mask_v10.png")
print("- nexah_transition_geometry_kernel_mask_v10.json")
