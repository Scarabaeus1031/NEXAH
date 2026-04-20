import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from scipy.ndimage import gaussian_filter

OUTPUT_DIR = "FIELD_LAYER/outputs/plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# 1. LORENZ
# ============================================================

def generate_lorenz(n_steps=5000, dt=0.01):
    sigma = 10.0
    rho = 28.0
    beta = 8.0 / 3.0

    X = np.zeros((n_steps, 3), dtype=float)
    x, y, z = 1.0, 1.0, 1.0

    for i in range(n_steps):
        dx = sigma * (y - x)
        dy = x * (rho - z) - y
        dz = x * y - beta * z

        x += dx * dt
        y += dy * dt
        z += dz * dt

        X[i] = [x, y, z]

    return X


# ============================================================
# 2. PCA PROJECTION
# ============================================================

def compute_basis(X):
    pca = PCA(n_components=3)
    pca.fit(X)
    return pca.components_


def project(X, e1, e2):
    alpha = X @ e1
    beta = X @ e2
    return alpha, beta


# ============================================================
# 3. DENSITY FIELD
# ============================================================

def density_field(alpha, beta, bins=180, sigma=2.0):
    H, xedges, yedges = np.histogram2d(alpha, beta, bins=bins)
    H = gaussian_filter(H, sigma=sigma)
    return H, xedges, yedges


# ============================================================
# 4. NODE SET
# ============================================================
# Use the same example node set as before for consistency.
# Later you can replace this with nodes loaded from V12 output.

def get_nodes():
    return np.array([
        [11.0, 26.0],  # N0
        [10.5, 25.5],  # N1
        [12.0, 24.8],  # N2
        [13.0, 26.0],  # N3
        [12.0, 23.5],  # N4
        [11.5, 24.0],  # N5
        [10.8, 27.8],  # N6
        [9.8, 25.2],   # N7
        [13.5, 25.5],  # N8
        [11.5, 28.5],  # N9
        [10.2, 24.2],  # N10
    ], dtype=float)


# ============================================================
# 5. CLUSTER NODES
# ============================================================

def cluster_nodes(nodes, eps=1.15, min_samples=2):
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(nodes)
    return clustering.labels_


# ============================================================
# 6. INFLUENCE MAP (nearest-node Voronoi-like assignment)
# ============================================================

def make_influence_map(nodes, xlim, ylim, resolution=220):
    xs = np.linspace(xlim[0], xlim[1], resolution)
    ys = np.linspace(ylim[0], ylim[1], resolution)
    XX, YY = np.meshgrid(xs, ys)

    pts = np.stack([XX.ravel(), YY.ravel()], axis=1)
    dists = np.linalg.norm(pts[:, None, :] - nodes[None, :, :], axis=2)
    nearest = np.argmin(dists, axis=1).reshape(resolution, resolution)

    return xs, ys, nearest


# ============================================================
# 7. PLOT
# ============================================================

def main():
    print("Running V12.6 Node Clusters...")

    # background field for orientation
    X = generate_lorenz()
    e1, e2, _ = compute_basis(X)
    alpha, beta = project(X, e1, e2)
    H, xedges, yedges = density_field(alpha, beta, bins=180, sigma=2.0)

    nodes = get_nodes()
    labels = cluster_nodes(nodes, eps=1.15, min_samples=2)

    unique_labels = sorted(set(labels))
    print(f"Detected node clusters: {len([l for l in unique_labels if l != -1])}")

    # print members
    for label in unique_labels:
        idx = np.where(labels == label)[0]
        if label == -1:
            print(f"Noise nodes: {idx.tolist()}")
        else:
            print(f"Cluster {label}: nodes {idx.tolist()}")

    # pairwise distances
    print("\nClose node pairs (< 1.6):")
    n = len(nodes)
    for i in range(n):
        for j in range(i + 1, n):
            d = np.linalg.norm(nodes[i] - nodes[j])
            if d < 1.6:
                print(f"  N{i} - N{j}: dist = {d:.3f}")

    # influence map limits
    xlim = (6.0, 16.5)
    ylim = (21.0, 30.5)
    xs, ys, nearest = make_influence_map(nodes, xlim, ylim, resolution=260)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # ---------- Q1: clusters over field ----------
    ax = axes[0]
    ax.imshow(
        H.T,
        origin="lower",
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
        aspect="auto",
        cmap="viridis"
    )

    cmap = plt.cm.tab10(np.linspace(0, 1, max(1, len(unique_labels))))
    label_to_color = {}
    color_idx = 0
    for label in unique_labels:
        if label == -1:
            label_to_color[label] = "gray"
        else:
            label_to_color[label] = cmap[color_idx]
            color_idx += 1

    for i, (x, y) in enumerate(nodes):
        color = label_to_color[labels[i]]
        ax.scatter(x, y, s=260, c=[color], edgecolor="black", zorder=5)
        ax.text(x, y, f"N{i}", fontsize=10, ha="center", va="center", zorder=6)

    # draw cluster hull-ish links via center
    for label in unique_labels:
        if label == -1:
            continue
        pts = nodes[labels == label]
        center = pts.mean(axis=0)
        ax.scatter(center[0], center[1], s=320, c=[label_to_color[label]],
                   marker="X", edgecolor="white", linewidth=1.5, zorder=7)
        for p in pts:
            ax.plot([p[0], center[0]], [p[1], center[1]],
                    color=label_to_color[label], linewidth=1.5, alpha=0.7, zorder=6)

    ax.set_title("Q1 — Node Clusters in Field")
    ax.set_xlabel("α")
    ax.set_ylabel("β")
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    # ---------- Q2: influence regions ----------
    ax = axes[1]
    ax.imshow(
        nearest,
        origin="lower",
        extent=[xlim[0], xlim[1], ylim[0], ylim[1]],
        aspect="auto",
        cmap="tab20",
        alpha=0.55
    )

    # contour-ish node regions by overlaying density too
    ax.imshow(
        H.T,
        origin="lower",
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
        aspect="auto",
        cmap="gray",
        alpha=0.18
    )

    for i, (x, y) in enumerate(nodes):
        color = label_to_color[labels[i]]
        ax.scatter(x, y, s=260, c=[color], edgecolor="black", zorder=5)
        ax.text(x, y, f"N{i}", fontsize=10, ha="center", va="center", zorder=6)

    ax.set_title("Q2 — Influence Regions (Nearest Node)")
    ax.set_xlabel("α")
    ax.set_ylabel("β")
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    out = os.path.join(OUTPUT_DIR, "v12_6_node_clusters.png")
    plt.savefig(out, dpi=200, bbox_inches="tight")
    plt.close()

    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
