import os
import math
import random
from collections import defaultdict, Counter

import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from scipy.ndimage import gaussian_filter

OUTPUT_DIR = "FIELD_LAYER/outputs/plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# 1. SHARED SYSTEM
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


def compute_basis(X):
    pca = PCA(n_components=3)
    pca.fit(X)
    return pca.components_


def project(X, e1, e2):
    return X @ e1, X @ e2


def density_field(alpha, beta, bins=180, sigma=2.0):
    H, xedges, yedges = np.histogram2d(alpha, beta, bins=bins)
    H = gaussian_filter(H, sigma=sigma)
    return H, xedges, yedges


def get_nodes():
    return np.array([
        [11.0, 26.0], [10.5, 25.5], [12.0, 24.8], [13.0, 26.0],
        [12.0, 23.5], [11.5, 24.0], [10.8, 27.8],
        [9.8, 25.2], [13.5, 25.5], [11.5, 28.5], [10.2, 24.2]
    ], dtype=float)


node_to_cluster = {
    0: 0, 1: 0, 7: 0, 10: 0,
    2: 1, 4: 1, 5: 1,
    3: 2, 8: 2,
    6: 3, 9: 3
}


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


def build_cluster_centroids(nodes, node_to_cluster):
    groups = defaultdict(list)
    for n_idx, c_idx in node_to_cluster.items():
        groups[c_idx].append(nodes[n_idx])

    centroids = {}
    for c_idx, pts in groups.items():
        centroids[c_idx] = np.mean(np.array(pts), axis=0)
    return centroids, groups


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
# 2. MULTI-TARGET ENERGY
# ============================================================

def multi_target_energy(src, dst, base_p, primary, fallback, escape, centroids, eps=1e-9):
    """
    Weighted target function:
    - primary is best
    - fallback is acceptable
    - escape is discouraged unless necessary
    """
    src_center = centroids[src]
    dst_center = centroids[dst]

    d_primary = np.linalg.norm(dst_center - centroids[primary])
    d_fallback = np.linalg.norm(dst_center - centroids[fallback])
    d_escape = np.linalg.norm(dst_center - centroids[escape])

    native_cost = -math.log(base_p + eps)

    # weighted objective
    score = (
        1.00 * d_primary +
        0.45 * d_fallback -
        0.15 * d_escape
    )

    # mild improvement reward
    src_score = (
        1.00 * np.linalg.norm(src_center - centroids[primary]) +
        0.45 * np.linalg.norm(src_center - centroids[fallback]) -
        0.15 * np.linalg.norm(src_center - centroids[escape])
    )

    improvement = src_score - score
    geom_cost = max(0.0, -improvement)

    return native_cost + geom_cost


def build_multi_target_table(prob_adj, centroids, primary, fallback, escape):
    table = {}
    for src, choices in prob_adj.items():
        for dst, base_p in choices:
            table[(src, dst)] = multi_target_energy(
                src, dst, base_p,
                primary, fallback, escape,
                centroids
            )
    return table


def choose_step(current, prob_adj, energy_table, bias_strength=2.4):
    choices = prob_adj.get(current, [])
    if not choices:
        return current

    dsts, weights = [], []
    for dst, _ in choices:
        e = energy_table[(current, dst)]
        w = math.exp(-bias_strength * e)
        dsts.append(dst)
        weights.append(w)

    if sum(weights) <= 0:
        weights = [1.0] * len(dsts)

    return random.choices(dsts, weights=weights)[0]


def simulate_multi_target(prob_adj, energy_table, start=0, steps=120, bias_strength=2.4):
    path = [start]
    current = start
    for _ in range(steps):
        current = choose_step(current, prob_adj, energy_table, bias_strength=bias_strength)
        path.append(current)
    return path


def make_spatial_path(cluster_path, centroids, jitter=0.14):
    return np.array([centroids[c] + np.random.normal(scale=jitter, size=2) for c in cluster_path])


# ============================================================
# 3. PLOT
# ============================================================

def plot_multi(H, xedges, yedges, nodes, groups, centroids,
               path, pts, primary, fallback, escape):
    cluster_colors = {0: "#1f77b4", 1: "#d62728", 2: "#e377c2", 3: "#17becf"}

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(
        H.T, origin="lower",
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
        aspect="auto", cmap="viridis"
    )

    for c_idx, node_list in groups.items():
        arr = np.array(node_list)
        ax.scatter(arr[:, 0], arr[:, 1], s=250, c=cluster_colors[c_idx],
                   edgecolor="black", alpha=0.95, zorder=5)

    for i, (x, y) in enumerate(nodes):
        ax.text(x, y, f"N{i}", fontsize=9, ha="center", va="center", zorder=6)

    for c_idx, center in centroids.items():
        ax.scatter(center[0], center[1], s=420, c=cluster_colors[c_idx],
                   marker="X", edgecolor="white", linewidth=1.8, zorder=7)
        ax.text(center[0], center[1] + 0.35, f"C{c_idx}",
                color="white", fontsize=11, ha="center", va="bottom", zorder=8)

    # target rings
    ax.scatter(*centroids[primary], s=760, facecolors="none", edgecolors="yellow", linewidths=2.8, zorder=9)
    ax.scatter(*centroids[fallback], s=700, facecolors="none", edgecolors="lime", linewidths=2.2, zorder=9)
    ax.scatter(*centroids[escape], s=640, facecolors="none", edgecolors="red", linewidths=2.0, zorder=9)

    ax.plot(pts[:, 0], pts[:, 1], color="white", linewidth=1.4, alpha=0.6, zorder=4)
    ax.scatter(pts[:, 0], pts[:, 1], c=[cluster_colors[c] for c in path], s=18, alpha=0.95, zorder=6)

    ax.scatter(pts[0, 0], pts[0, 1], s=220, c="white", edgecolor="black", zorder=10)
    ax.scatter(pts[-1, 0], pts[-1, 1], s=220, c="yellow", edgecolor="black", zorder=10)

    txt = "\n".join([f"C{k}: {Counter(path)[k]}" for k in sorted(set(path))])
    txt += f"\nprimary: C{primary}"
    txt += f"\nfallback: C{fallback}"
    txt += f"\nescape: C{escape}"
    ax.text(
        0.02, 0.98, txt,
        transform=ax.transAxes,
        ha="left", va="top",
        fontsize=10, color="white",
        bbox=dict(facecolor="black", alpha=0.45, edgecolor="white")
    )

    ax.set_title("V16.2 Multi-Target Navigation")
    ax.set_xlabel("α")
    ax.set_ylabel("β")
    ax.set_xlim(6.0, 16.5)
    ax.set_ylim(21.0, 30.8)

    out = os.path.join(OUTPUT_DIR, "v16_2_multi_target_navigation.png")
    plt.savefig(out, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out}")


# ============================================================
# 4. MAIN
# ============================================================

def main():
    print("Running V16.2 Multi-Target Navigation...")

    X = generate_lorenz()
    e1, e2, _ = compute_basis(X)
    alpha, beta = project(X, e1, e2)
    H, xedges, yedges = density_field(alpha, beta)

    nodes = get_nodes()
    centroids, groups = build_cluster_centroids(nodes, node_to_cluster)
    prob_adj = build_probabilities(cluster_edges)

    primary = 2
    fallback = 0
    escape = 3
    start = 1

    energy_table = build_multi_target_table(prob_adj, centroids, primary, fallback, escape)
    path = simulate_multi_target(prob_adj, energy_table, start=start, steps=120, bias_strength=2.6)
    pts = make_spatial_path(path, centroids)

    print("\nVisit counts:")
    vc = Counter(path)
    for c in sorted(set(node_to_cluster.values())):
        print(f"  C{c}: {vc[c]}")

    print(f"\nTargets: primary=C{primary}, fallback=C{fallback}, escape=C{escape}")

    plot_multi(H, xedges, yedges, nodes, groups, centroids,
               path, pts, primary, fallback, escape)


if __name__ == "__main__":
    main()
