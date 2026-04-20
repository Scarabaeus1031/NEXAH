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
# 4. NODES / CLUSTERS
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
    0: 0, 1: 0, 7: 0, 10: 0,
    2: 1, 4: 1, 5: 1,
    3: 2, 8: 2,
    6: 3, 9: 3
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
# 5. BASE TRANSITIONS
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
# 6. SIMPLE POLICY (reuse best-to-target logic)
# ============================================================

def transition_energy(src, dst, base_p, target, centroids, eps=1e-9):
    src_center = centroids[src]
    dst_center = centroids[dst]
    tgt_center = centroids[target]

    d_src = np.linalg.norm(src_center - tgt_center)
    d_dst = np.linalg.norm(dst_center - tgt_center)

    improvement = d_src - d_dst
    native_cost = -math.log(base_p + eps)
    geom_cost = max(0.0, -improvement) + 0.25 * max(0.0, d_dst)

    return native_cost + geom_cost


def compute_policy(prob_adj, centroids, target):
    policy = {}
    for src, choices in prob_adj.items():
        best_dst = None
        best_cost = float("inf")
        for dst, base_p in choices:
            cost = transition_energy(src, dst, base_p, target, centroids)
            if cost < best_cost:
                best_cost = cost
                best_dst = dst
        policy[src] = best_dst
    return policy


# ============================================================
# 7. SPATIAL HELPERS
# ============================================================

def assign_cluster(point, centroids):
    keys = sorted(centroids.keys())
    dists = [np.linalg.norm(point - centroids[k]) for k in keys]
    idx = int(np.argmin(dists))
    return keys[idx], dists[idx]


def boundary_risk(point, centroids):
    """
    High when the two nearest cluster centers are similarly distant.
    """
    keys = sorted(centroids.keys())
    dists = np.array([np.linalg.norm(point - centroids[k]) for k in keys])
    order = np.sort(dists)
    d1, d2 = order[0], order[1]

    # if d2-d1 is small -> near boundary
    risk = math.exp(-(d2 - d1))
    return float(risk)


def instability_score(point, current_cluster, centroids, target_cluster):
    """
    Combined observer score:
    - boundary risk
    - distance to own cluster center
    - distance to target
    """
    own_center = centroids[current_cluster]
    target_center = centroids[target_cluster]

    own_dist = np.linalg.norm(point - own_center)
    tgt_dist = np.linalg.norm(point - target_center)
    b_risk = boundary_risk(point, centroids)

    score = 0.45 * b_risk + 0.35 * own_dist + 0.20 * tgt_dist
    return float(score), float(b_risk), float(own_dist), float(tgt_dist)


def make_spatial_path(cluster_path, centroids, jitter=0.14):
    pts = []
    for c in cluster_path:
        pts.append(centroids[c] + np.random.normal(scale=jitter, size=2))
    return np.array(pts)


# ============================================================
# 8. SIMULATION
# ============================================================

def simulate_with_policy(prob_adj, policy, start=0, steps=220):
    current = start
    path = [current]
    events = []

    for _ in range(steps):
        choices = prob_adj[current]
        dsts = [d for d, _ in choices]
        probs = [p for _, p in choices]

        actual = random.choices(dsts, weights=probs)[0]
        intended = policy[current]

        if actual == intended:
            events.append("policy_match")
        else:
            events.append("deviation")

        current = actual
        path.append(current)

    return path, events


# ============================================================
# 9. BOUNDARY MAP
# ============================================================

def compute_boundary_map(xlim, ylim, centroids, resolution=240):
    xs = np.linspace(xlim[0], xlim[1], resolution)
    ys = np.linspace(ylim[0], ylim[1], resolution)

    M = np.zeros((resolution, resolution))
    cluster_map = np.zeros((resolution, resolution), dtype=int)

    for i, x in enumerate(xs):
        for j, y in enumerate(ys):
            p = np.array([x, y])
            c, _ = assign_cluster(p, centroids)
            cluster_map[j, i] = c
            M[j, i] = boundary_risk(p, centroids)

    return xs, ys, M, cluster_map


# ============================================================
# 10. PLOT
# ============================================================

def plot_observer(H, xedges, yedges, nodes, groups, centroids,
                  cluster_path, pts, events,
                  scores, boundary_scores, own_dists, tgt_dists,
                  target_cluster=2):
    cluster_colors = {
        0: "#1f77b4",
        1: "#d62728",
        2: "#e377c2",
        3: "#17becf",
    }

    xlim = (6.0, 16.5)
    ylim = (21.0, 30.8)
    xs, ys, B, cluster_map = compute_boundary_map(xlim, ylim, centroids)

    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    ax1, ax2, ax3, ax4 = axes.flatten()

    # -------------------------
    # Q1 — path + observer highlights
    # -------------------------
    ax1.imshow(
        H.T, origin="lower",
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
        aspect="auto", cmap="viridis"
    )

    for c_idx, node_list in groups.items():
        arr = np.array(node_list)
        ax1.scatter(arr[:, 0], arr[:, 1], s=240, c=cluster_colors[c_idx],
                    edgecolor="black", zorder=5)

    for i, (x, y) in enumerate(nodes):
        ax1.text(x, y, f"N{i}", fontsize=9, ha="center", va="center", zorder=6)

    for c_idx, center in centroids.items():
        ax1.scatter(center[0], center[1], s=420, c=cluster_colors[c_idx],
                    marker="X", edgecolor="white", linewidth=1.8, zorder=7)
        ax1.text(center[0], center[1] + 0.35, f"C{c_idx}",
                 color="white", fontsize=11, ha="center", va="bottom", zorder=8)

    tgt = centroids[target_cluster]
    ax1.scatter(tgt[0], tgt[1], s=760, facecolors="none",
                edgecolors="yellow", linewidths=2.5, zorder=9)

    ax1.plot(pts[:, 0], pts[:, 1], color="white", linewidth=1.0, alpha=0.45, zorder=4)
    ax1.scatter(pts[:, 0], pts[:, 1],
                c=[cluster_colors[c] for c in cluster_path],
                s=16, alpha=0.9, zorder=6)

    high_idx = np.where(np.array(boundary_scores) > np.quantile(boundary_scores, 0.9))[0]
    if len(high_idx) > 0:
        ax1.scatter(pts[high_idx, 0], pts[high_idx, 1],
                    c="red", s=42, alpha=0.95, label="high boundary risk", zorder=10)

    ax1.set_title("Q1 — Observer Overlay in Field")
    ax1.set_xlabel("α")
    ax1.set_ylabel("β")
    ax1.set_xlim(*xlim)
    ax1.set_ylim(*ylim)
    ax1.legend(loc="lower left")

    # -------------------------
    # Q2 — boundary risk map
    # -------------------------
    im2 = ax2.imshow(
        B, origin="lower",
        extent=[xlim[0], xlim[1], ylim[0], ylim[1]],
        aspect="auto", cmap="magma"
    )

    for c_idx, center in centroids.items():
        ax2.scatter(center[0], center[1], s=340, c=cluster_colors[c_idx],
                    marker="X", edgecolor="white", linewidth=1.6, zorder=7)

    ax2.set_title("Q2 — Boundary Risk Map")
    ax2.set_xlabel("α")
    ax2.set_ylabel("β")
    fig.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)

    # -------------------------
    # Q3 — observer time series
    # -------------------------
    ax3.plot(scores, label="instability_score", linewidth=1.5)
    ax3.plot(boundary_scores, label="boundary_risk", linewidth=1.2)
    ax3.plot(own_dists, label="dist_to_own_cluster", linewidth=1.2)
    ax3.set_title("Q3 — Observer Signals")
    ax3.set_xlabel("step")
    ax3.set_ylabel("value")
    ax3.grid(True, alpha=0.3)
    ax3.legend()

    # -------------------------
    # Q4 — cluster id + warnings
    # -------------------------
    traj_numeric = cluster_path
    ax4.plot(traj_numeric, linewidth=1.2)
    ax4.set_yticks([0, 1, 2, 3])
    ax4.set_yticklabels(["C0", "C1", "C2", "C3"])
    ax4.set_title("Q4 — State Trace with Warning Events")
    ax4.set_xlabel("step")
    ax4.set_ylabel("cluster")
    ax4.grid(True, alpha=0.3)

    warn_idx = np.where(np.array(scores) > np.quantile(scores, 0.9))[0]
    if len(warn_idx) > 0:
        ax4.scatter(warn_idx, np.array(traj_numeric)[warn_idx],
                    c="red", s=22, label="warning")
        ax4.legend()

    out = os.path.join(OUTPUT_DIR, "v18_observer_layer.png")
    plt.tight_layout()
    plt.savefig(out, dpi=200, bbox_inches="tight")
    plt.close()

    print(f"Saved: {out}")


# ============================================================
# 11. MAIN
# ============================================================

def main():
    print("Running V18 Observer Layer...")

    X = generate_lorenz()
    e1, e2, _ = compute_basis(X)
    alpha, beta = project(X, e1, e2)
    H, xedges, yedges = density_field(alpha, beta)

    nodes = get_nodes()
    centroids, groups = build_cluster_centroids(nodes, node_to_cluster)
    prob_adj = build_probabilities(cluster_edges)

    target_cluster = 2
    policy = compute_policy(prob_adj, centroids, target_cluster)

    cluster_path, events = simulate_with_policy(prob_adj, policy, start=0, steps=220)
    pts = make_spatial_path(cluster_path, centroids)

    scores = []
    boundary_scores = []
    own_dists = []
    tgt_dists = []

    for p, c in zip(pts, cluster_path):
        s, br, od, td = instability_score(p, c, centroids, target_cluster)
        scores.append(s)
        boundary_scores.append(br)
        own_dists.append(od)
        tgt_dists.append(td)

    print("\nVisit Counts:")
    counts = Counter(cluster_path)
    for k in sorted(counts):
        print(f"  C{k}: {counts[k]}")

    print("\nEvent Counts:")
    ec = Counter(events)
    for k in sorted(ec):
        print(f"  {k}: {ec[k]}")

    print(f"\nMean instability score: {np.mean(scores):.4f}")
    print(f"Max instability score: {np.max(scores):.4f}")

    plot_observer(
        H, xedges, yedges,
        nodes, groups, centroids,
        cluster_path, pts, events,
        scores, boundary_scores, own_dists, tgt_dists,
        target_cluster=target_cluster
    )


if __name__ == "__main__":
    main()
