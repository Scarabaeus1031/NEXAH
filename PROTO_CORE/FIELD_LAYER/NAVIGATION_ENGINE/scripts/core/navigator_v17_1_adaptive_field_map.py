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
# 6. ADAPTIVE POLICY CORE
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


def compute_policy(prob_adj, centroids, target, memory, penalty_weight=2.0):
    policy = {}

    for src, choices in prob_adj.items():
        best_dst = None
        best_cost = float("inf")

        for dst, base_p in choices:
            base_energy = transition_energy(src, dst, base_p, target, centroids)

            mem = memory[(src, dst)]
            fail_rate = mem["fail"] / (mem["fail"] + mem["success"])
            adaptive_cost = base_energy + penalty_weight * fail_rate

            if adaptive_cost < best_cost:
                best_cost = adaptive_cost
                best_dst = dst

        policy[src] = best_dst

    return policy


def sample_natural_transition(current, prob_adj):
    choices = prob_adj[current]
    dsts = [d for d, _ in choices]
    probs = [p for _, p in choices]
    return random.choices(dsts, weights=probs)[0]


def run_adaptive_sim(prob_adj, centroids, target=2, start=0,
                     steps=220, adapt_interval=20, penalty_weight=2.0):
    memory = defaultdict(lambda: {"success": 1, "fail": 1})

    current = start
    cluster_path = [current]
    event_types = []
    policy_history = []

    policy = compute_policy(prob_adj, centroids, target, memory, penalty_weight=penalty_weight)

    for t in range(steps):
        if current in policy:
            intended = policy[current]
        else:
            intended = sample_natural_transition(current, prob_adj)

        actual = sample_natural_transition(current, prob_adj)

        if actual == intended:
            memory[(current, intended)]["success"] += 1
            event_types.append("policy_match")
        else:
            memory[(current, intended)]["fail"] += 1
            event_types.append("overshoot")

        current = actual
        cluster_path.append(current)
        policy_history.append(dict(policy))

        if (t + 1) % adapt_interval == 0:
            policy = compute_policy(prob_adj, centroids, target, memory, penalty_weight=penalty_weight)

    return cluster_path, event_types, memory, policy_history


# ============================================================
# 7. SPATIAL BACKPROJECTION
# ============================================================

def make_spatial_path(cluster_path, centroids, jitter=0.14):
    pts = []
    for c in cluster_path:
        pts.append(centroids[c] + np.random.normal(scale=jitter, size=2))
    return np.array(pts)


# ============================================================
# 8. PLOT
# ============================================================

def plot_adaptive_field_map(H, xedges, yedges, nodes, groups, centroids,
                            cluster_path, pts, event_types, target=2):
    cluster_colors = {
        0: "#1f77b4",  # blue
        1: "#d62728",  # red
        2: "#e377c2",  # magenta
        3: "#17becf",  # cyan
    }

    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    ax1, ax2, ax3, ax4 = axes.flatten()

    # -------------------------
    # Q1 — full adaptive path
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

    tgt = centroids[target]
    ax1.scatter(tgt[0], tgt[1], s=760, facecolors="none",
                edgecolors="yellow", linewidths=2.5, zorder=9)

    ax1.plot(pts[:, 0], pts[:, 1], color="white", linewidth=1.0, alpha=0.45, zorder=4)
    ax1.scatter(pts[:, 0], pts[:, 1],
                c=[cluster_colors[c] for c in cluster_path],
                s=16, alpha=0.9, zorder=6)

    ax1.scatter(pts[0, 0], pts[0, 1], s=220, c="lime", edgecolor="black", zorder=10)
    ax1.scatter(pts[-1, 0], pts[-1, 1], s=220, c="yellow", edgecolor="black", zorder=10)

    counts = Counter(cluster_path)
    txt = "\n".join([f"C{k}: {counts[k]}" for k in sorted(counts)])
    ax1.text(
        0.02, 0.98, txt,
        transform=ax1.transAxes,
        ha="left", va="top",
        fontsize=10, color="white",
        bbox=dict(facecolor="black", alpha=0.45, edgecolor="white")
    )

    ax1.set_title("Q1 — Adaptive Path in Field")
    ax1.set_xlabel("α")
    ax1.set_ylabel("β")
    ax1.set_xlim(6.0, 16.5)
    ax1.set_ylim(21.0, 30.8)

    # -------------------------
    # Q2 — Overshoot points
    # -------------------------
    ax2.imshow(
        H.T, origin="lower",
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
        aspect="auto", cmap="viridis"
    )

    overs_idx = [i for i, ev in enumerate(event_types) if ev == "overshoot"]
    match_idx = [i for i, ev in enumerate(event_types) if ev == "policy_match"]

    if match_idx:
        match_pts = pts[np.array(match_idx)]
        ax2.scatter(match_pts[:, 0], match_pts[:, 1],
                    c="white", s=25, alpha=0.35, label="policy match")

    if overs_idx:
        over_pts = pts[np.array(overs_idx)]
        ax2.scatter(over_pts[:, 0], over_pts[:, 1],
                    c="red", s=45, alpha=0.9, label="overshoot")

    for c_idx, center in centroids.items():
        ax2.scatter(center[0], center[1], s=320, c=cluster_colors[c_idx],
                    marker="X", edgecolor="white", linewidth=1.6, zorder=7)

    ax2.scatter(tgt[0], tgt[1], s=700, facecolors="none",
                edgecolors="yellow", linewidths=2.3, zorder=9)

    ax2.set_title("Q2 — Overshoot / Recovery Events")
    ax2.set_xlabel("α")
    ax2.set_ylabel("β")
    ax2.set_xlim(6.0, 16.5)
    ax2.set_ylim(21.0, 30.8)
    ax2.legend(loc="lower left")

    # -------------------------
    # Q3 — time trajectory
    # -------------------------
    mapping = {0: 0, 1: 1, 2: 2, 3: 3}
    traj_numeric = [mapping[c] for c in cluster_path]

    ax3.plot(traj_numeric, linewidth=1.2)
    ax3.set_yticks([0, 1, 2, 3])
    ax3.set_yticklabels(["C0", "C1", "C2", "C3"])
    ax3.set_title("Q3 — Adaptive Policy Trajectory")
    ax3.set_xlabel("step")
    ax3.set_ylabel("cluster")
    ax3.grid(True, alpha=0.3)

    # mark overshoots
    if overs_idx:
        ax3.scatter(overs_idx, [traj_numeric[i] for i in overs_idx],
                    c="red", s=20, label="overshoot")
        ax3.legend()

    # -------------------------
    # Q4 — memory heatmap
    # -------------------------
    trans_counts = defaultdict(int)
    for i in range(len(cluster_path) - 1):
        trans_counts[(cluster_path[i], cluster_path[i+1])] += 1

    M = np.zeros((4, 4))
    for (src, dst), count in trans_counts.items():
        M[src, dst] = count

    im = ax4.imshow(M, cmap="magma")
    for i in range(4):
        for j in range(4):
            if M[i, j] > 0:
                ax4.text(j, i, f"{int(M[i,j])}", ha="center", va="center",
                         color="white", fontsize=11)

    ax4.set_title("Q4 — Learned Transition Usage")
    ax4.set_xlabel("to cluster")
    ax4.set_ylabel("from cluster")
    ax4.set_xticks(range(4))
    ax4.set_xticklabels(["C0", "C1", "C2", "C3"])
    ax4.set_yticks(range(4))
    ax4.set_yticklabels(["C0", "C1", "C2", "C3"])
    fig.colorbar(im, ax=ax4, fraction=0.046, pad=0.04)

    out = os.path.join(OUTPUT_DIR, "v17_1_adaptive_field_map.png")
    plt.tight_layout()
    plt.savefig(out, dpi=200, bbox_inches="tight")
    plt.close()

    print(f"Saved: {out}")


# ============================================================
# 9. MAIN
# ============================================================

def main():
    print("Running V17.1 Adaptive Field Map...")

    X = generate_lorenz()
    e1, e2, _ = compute_basis(X)
    alpha, beta = project(X, e1, e2)
    H, xedges, yedges = density_field(alpha, beta)

    nodes = get_nodes()
    centroids, groups = build_cluster_centroids(nodes, node_to_cluster)
    prob_adj = build_probabilities(cluster_edges)

    cluster_path, event_types, memory, policy_history = run_adaptive_sim(
        prob_adj, centroids,
        target=2, start=0,
        steps=220, adapt_interval=20,
        penalty_weight=2.0
    )

    pts = make_spatial_path(cluster_path, centroids)

    print("\nVisit Counts:")
    counts = Counter(cluster_path)
    for k in sorted(counts):
        print(f"  C{k}: {counts[k]}")

    print("\nEvent Counts:")
    ec = Counter(event_types)
    for k in sorted(ec):
        print(f"  {k}: {ec[k]}")

    plot_adaptive_field_map(
        H, xedges, yedges,
        nodes, groups, centroids,
        cluster_path, pts, event_types,
        target=2
    )


if __name__ == "__main__":
    main()
