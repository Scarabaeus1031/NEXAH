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
# 6. ENERGY / POLICY
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
# 7. OBSERVER
# ============================================================

def boundary_risk(point, centroids):
    keys = sorted(centroids.keys())
    dists = np.array([np.linalg.norm(point - centroids[k]) for k in keys])
    order = np.sort(dists)
    d1, d2 = order[0], order[1]
    risk = math.exp(-(d2 - d1))
    return float(risk)


def instability_score(point, current_cluster, centroids, target_cluster):
    own_center = centroids[current_cluster]
    target_center = centroids[target_cluster]

    own_dist = np.linalg.norm(point - own_center)
    tgt_dist = np.linalg.norm(point - target_center)
    b_risk = boundary_risk(point, centroids)

    score = 0.45 * b_risk + 0.35 * own_dist + 0.20 * tgt_dist
    return float(score), float(b_risk), float(own_dist), float(tgt_dist)


def make_spatial_point(cluster_id, centroids, jitter=0.14):
    return centroids[cluster_id] + np.random.normal(scale=jitter, size=2)


# ============================================================
# 8. OBSERVER-GUIDED CONTROL
# ============================================================

def sample_natural_transition(current, prob_adj):
    choices = prob_adj[current]
    dsts = [d for d, _ in choices]
    probs = [p for _, p in choices]
    return random.choices(dsts, weights=probs)[0]


def run_observer_guided_control(prob_adj, centroids,
                                start=0,
                                target_cluster=2,
                                safe_cluster=1,
                                steps=220,
                                instability_threshold=0.72,
                                boundary_threshold=0.19):
    """
    Normal mode: guide toward target_cluster
    Warning mode: switch temporarily to safe_cluster
    """
    cluster_path = [start]
    points = [make_spatial_point(start, centroids)]
    control_mode = []
    observer_scores = []
    boundary_scores = []
    own_dists = []
    tgt_dists = []
    event_types = []

    current = start

    for _ in range(steps):
        p = points[-1]

        score, br, od, td = instability_score(p, current, centroids, target_cluster)
        observer_scores.append(score)
        boundary_scores.append(br)
        own_dists.append(od)
        tgt_dists.append(td)

        warning = (score > instability_threshold) or (br > boundary_threshold)

        if warning:
            active_target = safe_cluster
            mode = "stabilize"
        else:
            active_target = target_cluster
            mode = "target"

        control_mode.append(mode)

        policy = compute_policy(prob_adj, centroids, active_target)
        intended = policy[current]
        actual = sample_natural_transition(current, prob_adj)

        if actual == intended:
            event_types.append("policy_match")
        else:
            event_types.append("deviation")

        current = actual
        cluster_path.append(current)
        points.append(make_spatial_point(current, centroids))

    return {
        "cluster_path": cluster_path,
        "points": np.array(points),
        "control_mode": control_mode,
        "observer_scores": observer_scores,
        "boundary_scores": boundary_scores,
        "own_dists": own_dists,
        "tgt_dists": tgt_dists,
        "event_types": event_types,
    }


# ============================================================
# 9. PLOTTING
# ============================================================

def plot_v19(H, xedges, yedges, nodes, groups, centroids, result,
             target_cluster=2, safe_cluster=1):
    cluster_colors = {
        0: "#1f77b4",
        1: "#d62728",
        2: "#e377c2",
        3: "#17becf",
    }

    cluster_path = result["cluster_path"]
    pts = result["points"]
    control_mode = result["control_mode"]
    observer_scores = result["observer_scores"]
    boundary_scores = result["boundary_scores"]
    own_dists = result["own_dists"]
    event_types = result["event_types"]

    xlim = (6.0, 16.5)
    ylim = (21.0, 30.8)

    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    ax1, ax2, ax3, ax4 = axes.flatten()

    # -------------------------
    # Q1 — path + mode overlay
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
    safe = centroids[safe_cluster]
    ax1.scatter(tgt[0], tgt[1], s=760, facecolors="none",
                edgecolors="yellow", linewidths=2.5, zorder=9, label="target")
    ax1.scatter(safe[0], safe[1], s=700, facecolors="none",
                edgecolors="lime", linewidths=2.2, zorder=9, label="safe")

    ax1.plot(pts[:, 0], pts[:, 1], color="white", linewidth=1.0, alpha=0.45, zorder=4)
    ax1.scatter(pts[:, 0], pts[:, 1],
                c=[cluster_colors[c] for c in cluster_path],
                s=16, alpha=0.9, zorder=6)

    stabilize_idx = [i for i, m in enumerate(control_mode) if m == "stabilize"]
    if stabilize_idx:
        stab_pts = pts[np.array(stabilize_idx)]
        ax1.scatter(stab_pts[:, 0], stab_pts[:, 1],
                    c="red", s=32, alpha=0.9, label="stabilize mode", zorder=10)

    ax1.set_title("Q1 — Observer-Guided Control in Field")
    ax1.set_xlabel("α")
    ax1.set_ylabel("β")
    ax1.set_xlim(*xlim)
    ax1.set_ylim(*ylim)
    ax1.legend(loc="lower left")

    # -------------------------
    # Q2 — mode over time
    # -------------------------
    mode_numeric = [1 if m == "stabilize" else 0 for m in control_mode]
    ax2.plot(mode_numeric, linewidth=1.6, color="red", label="stabilize_mode")
    ax2.plot(observer_scores, linewidth=1.2, color="blue", label="instability_score")
    ax2.plot(boundary_scores, linewidth=1.2, color="orange", label="boundary_risk")
    ax2.set_title("Q2 — Control Mode Switches")
    ax2.set_xlabel("step")
    ax2.set_ylabel("value")
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    # -------------------------
    # Q3 — state trace + warnings
    # -------------------------
    ax3.plot(cluster_path, linewidth=1.2)
    ax3.set_yticks([0, 1, 2, 3])
    ax3.set_yticklabels(["C0", "C1", "C2", "C3"])
    ax3.set_title("Q3 — State Trace")
    ax3.set_xlabel("step")
    ax3.set_ylabel("cluster")
    ax3.grid(True, alpha=0.3)

    if stabilize_idx:
        ax3.scatter(stabilize_idx, np.array(cluster_path)[stabilize_idx],
                    c="red", s=22, label="stabilize mode")
        ax3.legend()

    # -------------------------
    # Q4 — transition usage
    # -------------------------
    trans_counts = defaultdict(int)
    for i in range(len(cluster_path) - 1):
        trans_counts[(cluster_path[i], cluster_path[i+1])] += 1

    M = np.zeros((4, 4))
    for (src, dst), count in trans_counts.items():
        M[src, dst] = count

    im4 = ax4.imshow(M, cmap="magma")
    for i in range(4):
        for j in range(4):
            if M[i, j] > 0:
                ax4.text(j, i, f"{int(M[i,j])}", ha="center", va="center",
                         color="white", fontsize=11)

    ax4.set_title("Q4 — Observer-Guided Transition Usage")
    ax4.set_xlabel("to cluster")
    ax4.set_ylabel("from cluster")
    ax4.set_xticks(range(4))
    ax4.set_xticklabels(["C0", "C1", "C2", "C3"])
    ax4.set_yticks(range(4))
    ax4.set_yticklabels(["C0", "C1", "C2", "C3"])
    fig.colorbar(im4, ax=ax4, fraction=0.046, pad=0.04)

    out = os.path.join(OUTPUT_DIR, "v19_observer_guided_control.png")
    plt.tight_layout()
    plt.savefig(out, dpi=200, bbox_inches="tight")
    plt.close()

    print(f"Saved: {out}")


# ============================================================
# 10. MAIN
# ============================================================

def main():
    print("Running V19 Observer-Guided Control...")

    X = generate_lorenz()
    e1, e2, _ = compute_basis(X)
    alpha, beta = project(X, e1, e2)
    H, xedges, yedges = density_field(alpha, beta)

    nodes = get_nodes()
    centroids, groups = build_cluster_centroids(nodes, node_to_cluster)
    prob_adj = build_probabilities(cluster_edges)

    result = run_observer_guided_control(
        prob_adj, centroids,
        start=0,
        target_cluster=2,
        safe_cluster=1,
        steps=220,
        instability_threshold=0.72,
        boundary_threshold=0.19
    )

    counts = Counter(result["cluster_path"])
    print("\nVisit Counts:")
    for k in sorted(counts):
        print(f"  C{k}: {counts[k]}")

    ec = Counter(result["event_types"])
    print("\nEvent Counts:")
    for k in sorted(ec):
        print(f"  {k}: {ec[k]}")

    mode_counts = Counter(result["control_mode"])
    print("\nControl Mode Counts:")
    for k in sorted(mode_counts):
        print(f"  {k}: {mode_counts[k]}")

    print(f"\nMean instability score: {np.mean(result['observer_scores']):.4f}")
    print(f"Max instability score: {np.max(result['observer_scores']):.4f}")

    plot_v19(
        H, xedges, yedges,
        nodes, groups, centroids,
        result,
        target_cluster=2,
        safe_cluster=1
    )


if __name__ == "__main__":
    main()
