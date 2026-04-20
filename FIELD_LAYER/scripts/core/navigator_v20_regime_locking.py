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
# 6. OBSERVER
# ============================================================

def boundary_risk(point, centroids):
    keys = sorted(centroids.keys())
    dists = np.array([np.linalg.norm(point - centroids[k]) for k in keys])
    d1, d2 = np.sort(dists)[:2]
    return float(math.exp(-(d2 - d1)))


def instability_score(point, current_cluster, centroids, regime_center_cluster):
    own_center = centroids[current_cluster]
    reg_center = centroids[regime_center_cluster]

    own_dist = np.linalg.norm(point - own_center)
    reg_dist = np.linalg.norm(point - reg_center)
    br = boundary_risk(point, centroids)

    score = 0.45 * br + 0.35 * own_dist + 0.20 * reg_dist
    return float(score), float(br), float(own_dist), float(reg_dist)


def make_spatial_point(cluster_id, centroids, jitter=0.14):
    return centroids[cluster_id] + np.random.normal(scale=jitter, size=2)


# ============================================================
# 7. REGIME POLICY
# ============================================================

def regime_transition_cost(src, dst, base_p, regime_good, fallback, bad, centroids, eps=1e-9):
    """
    Low cost if destination stays in the desired regime.
    Higher cost if it falls into fallback.
    Strong penalty if it goes to bad / overshoot zone.
    """
    dst_center = centroids[dst]

    # distance to regime manifold approximated by nearest regime-good center
    reg_d = min(np.linalg.norm(dst_center - centroids[g]) for g in regime_good)
    fb_d = np.linalg.norm(dst_center - centroids[fallback])
    bad_d = np.linalg.norm(dst_center - centroids[bad])

    native_cost = -math.log(base_p + eps)

    regime_penalty = 0.0
    if dst in regime_good:
        regime_penalty -= 0.55
    elif dst == fallback:
        regime_penalty += 0.35
    elif dst == bad:
        regime_penalty += 1.25

    geom_term = 0.35 * reg_d + 0.15 * fb_d - 0.10 * bad_d

    return native_cost + regime_penalty + geom_term


def compute_regime_policy(prob_adj, centroids, regime_good=(1, 2), fallback=0, bad=3):
    policy = {}
    for src, choices in prob_adj.items():
        best_dst = None
        best_cost = float("inf")

        for dst, base_p in choices:
            cost = regime_transition_cost(
                src, dst, base_p,
                regime_good=regime_good,
                fallback=fallback,
                bad=bad,
                centroids=centroids
            )
            if cost < best_cost:
                best_cost = cost
                best_dst = dst

        policy[src] = best_dst
    return policy


# ============================================================
# 8. REGIME LOCK CONTROLLER
# ============================================================

def sample_natural_transition(current, prob_adj):
    choices = prob_adj[current]
    dsts = [d for d, _ in choices]
    probs = [p for _, p in choices]
    return random.choices(dsts, weights=probs)[0]


def run_regime_lock(prob_adj, centroids,
                    start=0,
                    regime_good=(1, 2),
                    fallback=0,
                    bad=3,
                    steps=240,
                    instability_threshold=0.72,
                    boundary_threshold=0.19):
    """
    Controller modes:
    - lock: keep inside regime_good
    - recover: if in bad or high observer risk, aim for fallback/regime return
    """
    cluster_path = [start]
    points = [make_spatial_point(start, centroids)]
    mode_trace = []
    event_types = []
    observer_scores = []
    boundary_scores = []
    own_dists = []
    regime_dists = []

    regime_center = 1  # use C1 as center of stable corridor
    current = start

    for _ in range(steps):
        p = points[-1]
        score, br, od, rd = instability_score(p, current, centroids, regime_center)

        observer_scores.append(score)
        boundary_scores.append(br)
        own_dists.append(od)
        regime_dists.append(rd)

        # mode logic
        if current == bad:
            mode = "recover"
        elif (score > instability_threshold) or (br > boundary_threshold):
            mode = "stabilize"
        else:
            mode = "lock"

        mode_trace.append(mode)

        if mode == "lock":
            policy = compute_regime_policy(
                prob_adj, centroids,
                regime_good=regime_good,
                fallback=fallback,
                bad=bad
            )
        elif mode == "stabilize":
            policy = compute_regime_policy(
                prob_adj, centroids,
                regime_good=(1,),   # pull tighter to C1
                fallback=fallback,
                bad=bad
            )
        else:  # recover
            policy = compute_regime_policy(
                prob_adj, centroids,
                regime_good=(1,),
                fallback=0,
                bad=3
            )

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
        "mode_trace": mode_trace,
        "event_types": event_types,
        "observer_scores": observer_scores,
        "boundary_scores": boundary_scores,
        "own_dists": own_dists,
        "regime_dists": regime_dists,
    }


# ============================================================
# 9. PLOTTING
# ============================================================

def plot_v20(H, xedges, yedges, nodes, groups, centroids, result,
             regime_good=(1, 2), fallback=0, bad=3):
    cluster_colors = {
        0: "#1f77b4",
        1: "#d62728",
        2: "#e377c2",
        3: "#17becf",
    }

    cluster_path = result["cluster_path"]
    pts = result["points"]
    mode_trace = result["mode_trace"]
    observer_scores = result["observer_scores"]
    boundary_scores = result["boundary_scores"]
    event_types = result["event_types"]

    xlim = (6.0, 16.5)
    ylim = (21.0, 30.8)

    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    ax1, ax2, ax3, ax4 = axes.flatten()

    # -------------------------
    # Q1 — field + regime lock path
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

    # regime rings
    for g in regime_good:
        ax1.scatter(*centroids[g], s=760, facecolors="none",
                    edgecolors="yellow", linewidths=2.5, zorder=9)
    ax1.scatter(*centroids[fallback], s=700, facecolors="none",
                edgecolors="lime", linewidths=2.2, zorder=9)
    ax1.scatter(*centroids[bad], s=700, facecolors="none",
                edgecolors="red", linewidths=2.2, zorder=9)

    ax1.plot(pts[:, 0], pts[:, 1], color="white", linewidth=1.0, alpha=0.45, zorder=4)
    ax1.scatter(pts[:, 0], pts[:, 1],
                c=[cluster_colors[c] for c in cluster_path],
                s=16, alpha=0.9, zorder=6)

    recover_idx = [i for i, m in enumerate(mode_trace) if m == "recover"]
    stab_idx = [i for i, m in enumerate(mode_trace) if m == "stabilize"]

    if stab_idx:
        spts = pts[np.array(stab_idx)]
        ax1.scatter(spts[:, 0], spts[:, 1], c="orange", s=32, alpha=0.9,
                    label="stabilize", zorder=10)
    if recover_idx:
        rpts = pts[np.array(recover_idx)]
        ax1.scatter(rpts[:, 0], rpts[:, 1], c="red", s=36, alpha=0.95,
                    label="recover", zorder=10)

    ax1.set_title("Q1 — Regime Locking in Field")
    ax1.set_xlabel("α")
    ax1.set_ylabel("β")
    ax1.set_xlim(*xlim)
    ax1.set_ylim(*ylim)
    ax1.legend(loc="lower left")

    # -------------------------
    # Q2 — mode trace
    # -------------------------
    mode_numeric = []
    for m in mode_trace:
        if m == "lock":
            mode_numeric.append(0)
        elif m == "stabilize":
            mode_numeric.append(1)
        else:
            mode_numeric.append(2)

    ax2.plot(mode_numeric, linewidth=1.6, color="red", label="mode")
    ax2.plot(observer_scores, linewidth=1.2, color="blue", label="instability")
    ax2.plot(boundary_scores, linewidth=1.2, color="orange", label="boundary_risk")
    ax2.set_title("Q2 — Regime Lock Modes")
    ax2.set_xlabel("step")
    ax2.set_ylabel("value / mode")
    ax2.set_yticks([0, 1, 2])
    ax2.set_yticklabels(["lock", "stabilize", "recover"])
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    # -------------------------
    # Q3 — state trace
    # -------------------------
    ax3.plot(cluster_path, linewidth=1.2)
    ax3.set_yticks([0, 1, 2, 3])
    ax3.set_yticklabels(["C0", "C1", "C2", "C3"])
    ax3.set_title("Q3 — State Trace under Regime Lock")
    ax3.set_xlabel("step")
    ax3.set_ylabel("cluster")
    ax3.grid(True, alpha=0.3)

    if recover_idx:
        ax3.scatter(recover_idx, np.array(cluster_path)[recover_idx],
                    c="red", s=22, label="recover")
    if stab_idx:
        ax3.scatter(stab_idx, np.array(cluster_path)[stab_idx],
                    c="orange", s=18, label="stabilize")
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

    ax4.set_title("Q4 — Regime-Locked Transition Usage")
    ax4.set_xlabel("to cluster")
    ax4.set_ylabel("from cluster")
    ax4.set_xticks(range(4))
    ax4.set_xticklabels(["C0", "C1", "C2", "C3"])
    ax4.set_yticks(range(4))
    ax4.set_yticklabels(["C0", "C1", "C2", "C3"])
    fig.colorbar(im4, ax=ax4, fraction=0.046, pad=0.04)

    out = os.path.join(OUTPUT_DIR, "v20_regime_locking.png")
    plt.tight_layout()
    plt.savefig(out, dpi=200, bbox_inches="tight")
    plt.close()

    print(f"Saved: {out}")


# ============================================================
# 10. MAIN
# ============================================================

def main():
    print("Running V20 Regime Locking...")

    X = generate_lorenz()
    e1, e2, _ = compute_basis(X)
    alpha, beta = project(X, e1, e2)
    H, xedges, yedges = density_field(alpha, beta)

    nodes = get_nodes()
    centroids, groups = build_cluster_centroids(nodes, node_to_cluster)
    prob_adj = build_probabilities(cluster_edges)

    result = run_regime_lock(
        prob_adj, centroids,
        start=0,
        regime_good=(1, 2),
        fallback=0,
        bad=3,
        steps=240,
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

    mc = Counter(result["mode_trace"])
    print("\nMode Counts:")
    for k in sorted(mc):
        print(f"  {k}: {mc[k]}")

    print(f"\nMean instability score: {np.mean(result['observer_scores']):.4f}")
    print(f"Max instability score: {np.max(result['observer_scores']):.4f}")

    plot_v20(
        H, xedges, yedges,
        nodes, groups, centroids,
        result,
        regime_good=(1, 2),
        fallback=0,
        bad=3
    )


if __name__ == "__main__":
    main()
