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
# 4. CLUSTERS
# ============================================================

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


def build_cluster_centroids(nodes, node_to_cluster):
    groups = defaultdict(list)
    for n_idx, c_idx in node_to_cluster.items():
        groups[c_idx].append(nodes[n_idx])

    centroids = {}
    for c_idx, pts in groups.items():
        centroids[c_idx] = np.mean(np.array(pts), axis=0)

    return centroids, groups


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
# 5. ENERGY + POLICY
# ============================================================

def transition_control_energy(src, dst, base_p, target, centroids, eps=1e-9):
    src_center = centroids[src]
    dst_center = centroids[dst]
    tgt_center = centroids[target]

    d_src = np.linalg.norm(src_center - tgt_center)
    d_dst = np.linalg.norm(dst_center - tgt_center)

    improvement = d_src - d_dst
    native_cost = -math.log(base_p + eps)
    geom_cost = max(0.0, -improvement) + 0.25 * max(0.0, d_dst)
    return native_cost + geom_cost


def build_energy_table(prob_adj, centroids, target):
    table = {}
    for src, choices in prob_adj.items():
        for dst, base_p in choices:
            table[(src, dst)] = transition_control_energy(src, dst, base_p, target, centroids)
    return table


def reverse_graph_from_energy(energy_table):
    rev = defaultdict(list)
    for (src, dst), e in energy_table.items():
        rev[dst].append((src, e))
    return rev


def shortest_costs_to_target(energy_table, target, clusters):
    import heapq
    rev = reverse_graph_from_energy(energy_table)

    cost = {c: float("inf") for c in clusters}
    parent = {c: None for c in clusters}
    cost[target] = 0.0

    heap = [(0.0, target)]
    while heap:
        curr_cost, node = heapq.heappop(heap)
        if curr_cost > cost[node]:
            continue

        for prev, edge_cost in rev[node]:
            new_cost = curr_cost + edge_cost
            if new_cost < cost[prev]:
                cost[prev] = new_cost
                parent[prev] = node
                heapq.heappush(heap, (new_cost, prev))
    return cost, parent


def derive_policy(parent, target, clusters):
    policy = {}
    for c in clusters:
        policy[c] = target if c == target else parent[c]
    return policy


# ============================================================
# 6. ROBUST SIMULATION
# ============================================================

def simulate_robust_policy(policy, prob_adj, start=0, steps=120,
                           failure_prob=0.18, policy_dropout_prob=0.08):
    """
    failure_prob: chance that intended control fails and natural dynamics is used
    policy_dropout_prob: chance that policy is ignored and a random reachable edge is taken
    """
    path = [start]
    events = []
    current = start

    for _ in range(steps):
        choices = prob_adj.get(current, [])
        natural_dsts = [d for d, _ in choices]
        natural_probs = [p for _, p in choices]

        intended = policy.get(current, current)

        r = random.random()

        if len(choices) == 0:
            path.append(current)
            events.append("stuck")
            continue

        if r < policy_dropout_prob:
            nxt = random.choice(natural_dsts)
            events.append("dropout")
        elif r < policy_dropout_prob + failure_prob:
            nxt = random.choices(natural_dsts, weights=natural_probs)[0]
            events.append("failure")
        else:
            if intended in natural_dsts:
                nxt = intended
            else:
                nxt = random.choices(natural_dsts, weights=natural_probs)[0]
            events.append("policy")

        current = nxt
        path.append(current)

    return path, events


def simulate_natural(prob_adj, start=0, steps=120):
    path = [start]
    current = start
    for _ in range(steps):
        choices = prob_adj.get(current, [])
        if not choices:
            break
        dsts = [d for d, _ in choices]
        probs = [p for _, p in choices]
        current = random.choices(dsts, weights=probs)[0]
        path.append(current)
    return path


def make_spatial_path(cluster_path, centroids, jitter=0.14):
    pts = []
    for c in cluster_path:
        pts.append(centroids[c] + np.random.normal(scale=jitter, size=2))
    return np.array(pts)


# ============================================================
# 7. PLOT
# ============================================================

def plot_robust(H, xedges, yedges, nodes, groups, centroids,
                natural_path, natural_pts, robust_path, robust_pts,
                events, target):
    cluster_colors = {0: "#1f77b4", 1: "#d62728", 2: "#e377c2", 3: "#17becf"}

    fig, axes = plt.subplots(1, 2, figsize=(16, 7), sharex=True, sharey=True)
    panels = [
        ("Natural Dynamics", natural_path, natural_pts, None),
        (f"Robust Policy (target = C{target})", robust_path, robust_pts, events),
    ]

    for ax, (title, path, pts, ev) in zip(axes, panels):
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
            ax.text(center[0], center[1] + 0.35, f"C{c_idx}", color="white",
                    fontsize=11, ha="center", va="bottom", zorder=8)

        tgt = centroids[target]
        ax.scatter(tgt[0], tgt[1], s=760, facecolors="none", edgecolors="yellow",
                   linewidths=2.5, zorder=9)

        ax.plot(pts[:, 0], pts[:, 1], color="white", linewidth=1.4, alpha=0.55, zorder=4)
        ax.scatter(pts[:, 0], pts[:, 1], c=[cluster_colors[c] for c in path],
                   s=18, alpha=0.95, zorder=6)

        ax.scatter(pts[0, 0], pts[0, 1], s=220, c="lime", edgecolor="black", zorder=10)
        ax.scatter(pts[-1, 0], pts[-1, 1], s=220, c="yellow", edgecolor="black", zorder=10)

        txt = "\n".join([f"C{k}: {Counter(path)[k]}" for k in sorted(set(path))])
        if ev is not None:
            ec = Counter(ev)
            txt += f"\npolicy: {ec['policy']}"
            txt += f"\nfailure: {ec['failure']}"
            txt += f"\ndropout: {ec['dropout']}"
        ax.text(
            0.02, 0.98, txt,
            transform=ax.transAxes,
            ha="left", va="top",
            fontsize=10, color="white",
            bbox=dict(facecolor="black", alpha=0.45, edgecolor="white")
        )

        ax.set_title(title)
        ax.set_xlabel("α")
        ax.set_xlim(6.0, 16.5)
        ax.set_ylim(21.0, 30.8)

    axes[0].set_ylabel("β")

    out = os.path.join(OUTPUT_DIR, "v16_1_robust_policy.png")
    plt.savefig(out, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out}")


# ============================================================
# 8. MAIN
# ============================================================

def main():
    print("Running V16.1 Robust Policy...")

    X = generate_lorenz()
    e1, e2, _ = compute_basis(X)
    alpha, beta = project(X, e1, e2)
    H, xedges, yedges = density_field(alpha, beta)

    nodes = get_nodes()
    centroids, groups = build_cluster_centroids(nodes, node_to_cluster)
    prob_adj = build_probabilities(cluster_edges)

    clusters = sorted(set(node_to_cluster.values()))
    start_cluster = 0
    target_cluster = 2

    energy_table = build_energy_table(prob_adj, centroids, target_cluster)
    _, parent = shortest_costs_to_target(energy_table, target_cluster, clusters)
    policy = derive_policy(parent, target_cluster, clusters)

    natural_path = simulate_natural(prob_adj, start=start_cluster, steps=120)
    robust_path, events = simulate_robust_policy(
        policy, prob_adj,
        start=start_cluster,
        steps=120,
        failure_prob=0.18,
        policy_dropout_prob=0.08
    )

    natural_pts = make_spatial_path(natural_path, centroids)
    robust_pts = make_spatial_path(robust_path, centroids)

    print("\nRobust policy:")
    for c in clusters:
        print(f"  C{c} -> C{policy[c]}")

    print("\nRobust visit counts:")
    rc = Counter(robust_path)
    for c in clusters:
        print(f"  C{c}: {rc[c]}")

    print("\nEvent counts:")
    ec = Counter(events)
    for k in ["policy", "failure", "dropout"]:
        print(f"  {k}: {ec[k]}")

    plot_robust(
        H, xedges, yedges, nodes, groups, centroids,
        natural_path, natural_pts, robust_path, robust_pts,
        events, target_cluster
    )


if __name__ == "__main__":
    main()
