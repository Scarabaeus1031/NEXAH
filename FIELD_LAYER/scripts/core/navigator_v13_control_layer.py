import os
import random
from collections import defaultdict, Counter

import numpy as np
import matplotlib.pyplot as plt
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
# 4. NODE / CLUSTER DEFINITIONS
# ============================================================

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


node_to_cluster = {
    0: 0, 1: 0, 7: 0, 10: 0,   # Cluster 0
    2: 1, 4: 1, 5: 1,          # Cluster 1
    3: 2, 8: 2,                # Cluster 2
    6: 3, 9: 3                 # Cluster 3
}


def build_cluster_centroids(nodes, node_to_cluster):
    groups = defaultdict(list)
    for n_idx, c_idx in node_to_cluster.items():
        groups[c_idx].append(nodes[n_idx])

    centroids = {}
    for c_idx, pts in groups.items():
        centroids[c_idx] = np.mean(np.array(pts), axis=0)

    return centroids, groups


# ============================================================
# 5. CLUSTER TRANSITION GRAPH (from V12.7)
# ============================================================

cluster_edges = {
    (2, 1): 23,
    (0, 2): 16,
    (1, 0): 15,
    (3, 0): 15,
    (0, 1): 14,
    (1, 2): 12,
    (0, 0): 12,
    (1, 3): 9,
    (3, 3): 7,
}


def build_probabilities(cluster_edges):
    adj = defaultdict(list)
    for (src, dst), w in cluster_edges.items():
        adj[src].append((dst, w))

    prob_adj = {}
    for src, edges in adj.items():
        total = sum(w for _, w in edges)
        prob_adj[src] = [(dst, w / total) for dst, w in edges]

    return prob_adj


# ============================================================
# 6. CONTROL POLICY
# ============================================================

def controlled_step(current, prob_adj, target, centroids, control_strength=2.0):
    """
    Reweight transition probabilities toward the target cluster.
    control_strength > 1 increases preference for transitions that
    reduce centroid distance to the target.
    """
    if current not in prob_adj:
        return current

    choices = prob_adj[current]
    target_center = centroids[target]

    weighted = []
    for dst, base_p in choices:
        dst_center = centroids[dst]
        current_center = centroids[current]

        d_current = np.linalg.norm(current_center - target_center)
        d_next = np.linalg.norm(dst_center - target_center)

        # Improvement score:
        # - if next state is closer to target, boost
        # - if farther, penalize
        improvement = d_current - d_next

        factor = np.exp(control_strength * improvement)
        weighted.append((dst, base_p * factor))

    dsts = [d for d, _ in weighted]
    ws = [w for _, w in weighted]

    # fallback safety
    if sum(ws) <= 0:
        ws = [1.0] * len(dsts)

    return random.choices(dsts, weights=ws)[0]


def simulate_uncontrolled(prob_adj, start=0, steps=120):
    path = [start]
    current = start

    for _ in range(steps):
        if current not in prob_adj:
            break

        choices = prob_adj[current]
        dsts = [d for d, _ in choices]
        probs = [p for _, p in choices]
        current = random.choices(dsts, weights=probs)[0]
        path.append(current)

    return path


def simulate_controlled(prob_adj, centroids, start=0, target=2, steps=120, control_strength=2.0):
    path = [start]
    current = start

    for _ in range(steps):
        nxt = controlled_step(current, prob_adj, target, centroids, control_strength=control_strength)
        path.append(nxt)
        current = nxt

    return path


# ============================================================
# 7. BACKPROJECTION TO FIELD
# ============================================================

def make_spatial_path(cluster_path, centroids, jitter=0.16):
    pts = []
    for c in cluster_path:
        center = centroids[c].copy()
        noise = np.random.normal(scale=jitter, size=2)
        pts.append(center + noise)
    return np.array(pts)


# ============================================================
# 8. PLOTTING
# ============================================================

def plot_control_result(H, xedges, yedges, nodes, groups, centroids,
                        uncontrolled_path, controlled_path,
                        uncontrolled_pts, controlled_pts,
                        target_cluster):
    cluster_colors = {
        0: "#1f77b4",  # blue
        1: "#d62728",  # red
        2: "#e377c2",  # magenta
        3: "#17becf",  # cyan
    }

    fig, axes = plt.subplots(1, 2, figsize=(16, 7), sharex=True, sharey=True)

    for ax, title, path, pts in [
        (axes[0], "Uncontrolled Cluster Dynamics", uncontrolled_path, uncontrolled_pts),
        (axes[1], f"Controlled Cluster Dynamics (target = C{target_cluster})", controlled_path, controlled_pts),
    ]:
        ax.imshow(
            H.T,
            origin="lower",
            extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
            aspect="auto",
            cmap="viridis"
        )

        # nodes by cluster
        for c_idx, node_list in groups.items():
            arr = np.array(node_list)
            ax.scatter(
                arr[:, 0], arr[:, 1],
                s=250,
                c=cluster_colors[c_idx],
                edgecolor="black",
                alpha=0.95,
                zorder=5
            )

        # node labels
        for i, (x, y) in enumerate(nodes):
            ax.text(x, y, f"N{i}", fontsize=9, ha="center", va="center", zorder=6)

        # cluster centroids
        for c_idx, center in centroids.items():
            ax.scatter(
                center[0], center[1],
                s=420,
                c=cluster_colors[c_idx],
                marker="X",
                edgecolor="white",
                linewidth=1.8,
                zorder=7
            )
            ax.text(center[0], center[1] + 0.38, f"C{c_idx}",
                    color="white", fontsize=11, ha="center", va="bottom", zorder=8)

        # target highlight
        target_center = centroids[target_cluster]
        ax.scatter(
            target_center[0], target_center[1],
            s=760,
            facecolors="none",
            edgecolors="yellow",
            linewidths=2.5,
            zorder=9
        )

        # path
        ax.plot(pts[:, 0], pts[:, 1], color="white", linewidth=1.2, alpha=0.55, zorder=4)
        ax.scatter(pts[:, 0], pts[:, 1],
                   c=[cluster_colors[c] for c in path],
                   s=18, alpha=0.95, zorder=6)

        # start/end
        ax.scatter(pts[0, 0], pts[0, 1], s=220, c="lime", edgecolor="black", zorder=10)
        ax.scatter(pts[-1, 0], pts[-1, 1], s=220, c="yellow", edgecolor="black", zorder=10)

        counts = Counter(path)
        txt = "\n".join([f"C{k}: {counts[k]}" for k in sorted(counts)])
        ax.text(
            0.02, 0.98, txt,
            transform=ax.transAxes,
            ha="left", va="top",
            fontsize=10,
            color="white",
            bbox=dict(facecolor="black", alpha=0.45, edgecolor="white")
        )

        ax.set_title(title)
        ax.set_xlabel("α")
        ax.set_xlim(6.0, 16.5)
        ax.set_ylim(21.0, 30.8)

    axes[0].set_ylabel("β")

    out = os.path.join(OUTPUT_DIR, "v13_control_layer.png")
    plt.savefig(out, dpi=200, bbox_inches="tight")
    plt.close()

    print(f"\nSaved: {out}")


# ============================================================
# 9. MAIN
# ============================================================

def main():
    print("Running V13 Control Layer...")

    # background field
    X = generate_lorenz()
    e1, e2, _ = compute_basis(X)
    alpha, beta = project(X, e1, e2)
    H, xedges, yedges = density_field(alpha, beta, bins=180, sigma=2.0)

    # nodes / clusters
    nodes = get_nodes()
    centroids, groups = build_cluster_centroids(nodes, node_to_cluster)

    # transition probabilities
    prob_adj = build_probabilities(cluster_edges)

    # simulation parameters
    start_cluster = 0
    target_cluster = 2
    n_steps = 140
    control_strength = 2.4

    uncontrolled = simulate_uncontrolled(prob_adj, start=start_cluster, steps=n_steps)
    controlled = simulate_controlled(
        prob_adj, centroids,
        start=start_cluster,
        target=target_cluster,
        steps=n_steps,
        control_strength=control_strength
    )

    uncontrolled_pts = make_spatial_path(uncontrolled, centroids, jitter=0.16)
    controlled_pts = make_spatial_path(controlled, centroids, jitter=0.16)

    # summary
    print("\nUncontrolled Visit Counts:")
    uc = Counter(uncontrolled)
    for k in sorted(uc):
        print(f"  C{k}: {uc[k]}")

    print("\nControlled Visit Counts:")
    cc = Counter(controlled)
    for k in sorted(cc):
        print(f"  C{k}: {cc[k]}")

    print(f"\nTarget cluster: C{target_cluster}")
    print(f"Control strength: {control_strength}")

    plot_control_result(
        H, xedges, yedges,
        nodes, groups, centroids,
        uncontrolled, controlled,
        uncontrolled_pts, controlled_pts,
        target_cluster
    )


if __name__ == "__main__":
    main()
