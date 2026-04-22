import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from scipy.ndimage import gaussian_filter

OUTPUT_DIR = "FIELD_LAYER/outputs/plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# =========================
# 1. LORENZ
# =========================

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


# =========================
# 2. PCA PROJECTION
# =========================

def compute_basis(X):
    pca = PCA(n_components=3)
    pca.fit(X)
    return pca.components_


def project(X, e1, e2):
    alpha = X @ e1
    beta = X @ e2
    return alpha, beta


# =========================
# 3. DENSITY + FLUX FIELD
# =========================

def density_field(alpha, beta, bins=180, sigma=2.0):
    H, xedges, yedges = np.histogram2d(alpha, beta, bins=bins)
    H = gaussian_filter(H, sigma=sigma)
    return H, xedges, yedges


def estimate_flux_field(alpha, beta, bins=180, sigma=2.0):
    da = np.diff(alpha, prepend=alpha[0])
    db = np.diff(beta, prepend=beta[0])

    P, xedges, yedges = np.histogram2d(alpha, beta, bins=bins)
    Fx, _, _ = np.histogram2d(alpha, beta, bins=[xedges, yedges], weights=da)
    Fy, _, _ = np.histogram2d(alpha, beta, bins=[xedges, yedges], weights=db)

    P = gaussian_filter(P, sigma=sigma)
    Fx = gaussian_filter(Fx, sigma=sigma)
    Fy = gaussian_filter(Fy, sigma=sigma)

    eps = 1e-8
    Vx = Fx / (P + eps)
    Vy = Fy / (P + eps)

    Vx = gaussian_filter(Vx, sigma=1.0)
    Vy = gaussian_filter(Vy, sigma=1.0)

    xc = 0.5 * (xedges[:-1] + xedges[1:])
    yc = 0.5 * (yedges[:-1] + yedges[1:])

    return P, Vx, Vy, xedges, yedges, xc, yc


# =========================
# 4. NODES (same style as before)
# =========================

def extract_nodes(H, threshold_quantile=0.992, min_dist=6):
    thresh = np.quantile(H, threshold_quantile)
    coords = np.argwhere(H > thresh)

    if len(coords) == 0:
        return np.empty((0, 2), dtype=int)

    values = np.array([H[c[0], c[1]] for c in coords])
    order = np.argsort(values)[::-1]
    coords = coords[order]

    nodes = []
    for c in coords:
        if len(nodes) == 0:
            nodes.append(c)
            continue

        d = np.sqrt(np.sum((np.array(nodes) - c) ** 2, axis=1))
        if np.min(d) > min_dist:
            nodes.append(c)

    return np.array(nodes, dtype=int)


def grid_to_coords(nodes, xedges, yedges):
    xs = 0.5 * (xedges[:-1] + xedges[1:])
    ys = 0.5 * (yedges[:-1] + yedges[1:])
    return np.array([[xs[i], ys[j]] for i, j in nodes], dtype=float)


# =========================
# 5. ENTRY POINTS
# =========================
# Using the same example set you used in V12.3.1.
# You can later replace this with real extracted entries.

def get_entry_points():
    return np.array([
        [8.5, 22.0],
        [9.2, 27.5],
        [12.5, 31.0],
        [7.5, 18.5],
        [13.0, 13.5],
        [10.8, 26.2],
        [11.3, 25.7],
        [9.9, 24.8]
    ], dtype=float)


# =========================
# 6. ENTRY -> NODE MAPPING
# =========================

def map_entries_to_nodes(entries, nodes):
    mappings = []
    for i, e in enumerate(entries):
        dists = np.linalg.norm(nodes - e, axis=1)
        nearest_idx = np.argmin(dists)
        mappings.append((i, nearest_idx, dists[nearest_idx]))
    return mappings


# =========================
# 7. ENTRY CLUSTERING
# =========================

def cluster_entries(entry_points, eps=1.5, min_samples=2):
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(entry_points)
    return clustering.labels_


# =========================
# 8. PLOT
# =========================

def main():
    print("Running V12.3.2 Overlay Flow + Structure...")

    # Generate + project
    X = generate_lorenz()
    e1, e2, _ = compute_basis(X)
    alpha, beta = project(X, e1, e2)

    # Density + flux field
    P, Vx, Vy, xedges, yedges, xc, yc = estimate_flux_field(alpha, beta, bins=180, sigma=2.0)

    # Nodes from density
    H, _, _ = density_field(alpha, beta, bins=180, sigma=2.0)
    nodes_grid = extract_nodes(H, threshold_quantile=0.992, min_dist=6)
    node_points = grid_to_coords(nodes_grid, xedges, yedges)

    print(f"Detected nodes: {len(node_points)}")

    # Entry points
    entry_points = get_entry_points()
    mappings = map_entries_to_nodes(entry_points, node_points)

    # Clustering
    labels = cluster_entries(entry_points, eps=1.5, min_samples=2)
    unique_labels = sorted(set(labels))

    # Figure
    fig, ax = plt.subplots(figsize=(10, 8))

    # Background density
    ax.imshow(
        P.T,
        origin="lower",
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
        aspect="auto",
        cmap="viridis"
    )

    # Flow field
    Xg, Yg = np.meshgrid(xc, yc, indexing="ij")
    step = 8
    ax.quiver(
        Xg[::step, ::step],
        Yg[::step, ::step],
        Vx[::step, ::step],
        Vy[::step, ::step],
        color="white",
        alpha=0.28,
        scale=35,
        width=0.0025
    )

    # A few long stream trajectories for orientation
    sample_idxs = np.linspace(4200, 4999, 8).astype(int)
    for idx in sample_idxs:
        path = np.stack([alpha[max(0, idx-80):idx+1], beta[max(0, idx-80):idx+1]], axis=1)
        ax.plot(path[:, 0], path[:, 1], color="white", alpha=0.12, linewidth=1.5)

    # Nodes
    for i, (x, y) in enumerate(node_points):
        ax.scatter(x, y, s=220, c="yellow", edgecolor="black", zorder=5)
        ax.text(x, y, f"N{i}", fontsize=9, ha="center", va="center", zorder=6)

    # Cluster colors
    cmap = plt.cm.tab10(np.linspace(0, 1, max(1, len(unique_labels))))
    label_to_color = {}
    color_idx = 0
    for label in unique_labels:
        if label == -1:
            label_to_color[label] = "gray"
        else:
            label_to_color[label] = cmap[color_idx]
            color_idx += 1

    # Plot entries + cluster centers
    cluster_centers = {}
    for label in unique_labels:
        pts = entry_points[labels == label]
        if len(pts) == 0:
            continue

        color = label_to_color[label]

        if label == -1:
            ax.scatter(pts[:, 0], pts[:, 1], c=[color], s=90, label="noise", zorder=7)
        else:
            ax.scatter(pts[:, 0], pts[:, 1], c=[color], s=110, label=f"cluster {label}", zorder=7)
            center = pts.mean(axis=0)
            cluster_centers[label] = center
            ax.scatter(center[0], center[1], c=[color], s=260, marker="X",
                       edgecolor="white", linewidth=1.5, zorder=8)

            # Funnel lines
            for p in pts:
                ax.plot([p[0], center[0]], [p[1], center[1]],
                        color=color, alpha=0.45, linewidth=1.5, zorder=6)

    # Entry -> nearest node mapping lines
    for entry_idx, node_idx, dist in mappings:
        e = entry_points[entry_idx]
        n = node_points[node_idx]
        ax.plot([e[0], n[0]], [e[1], n[1]],
                color="cyan", linewidth=1.6, alpha=0.7, zorder=6)

    ax.set_title("V12.3.2 Overlay Flow + Structure")
    ax.set_xlabel("α")
    ax.set_ylabel("β")
    ax.legend(loc="upper left")

    out = os.path.join(OUTPUT_DIR, "v12_3_2_overlay_flow_and_structure.png")
    plt.savefig(out, dpi=200, bbox_inches="tight")
    plt.close()

    print(f"Saved: {out}")
    print("\nEntry -> Node Mapping:")
    for entry_idx, node_idx, dist in mappings:
        print(f"  Entry {entry_idx} -> Node N{node_idx} | dist={dist:.3f}")

    print("\nEntry Clusters:")
    for label in unique_labels:
        if label == -1:
            continue
        pts = entry_points[labels == label]
        print(f"  Cluster {label}: {len(pts)} points")


if __name__ == "__main__":
    main()
