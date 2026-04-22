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
# 5. CLUSTER TRANSITION GRAPH
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
# 6. CONTROL ENERGY MODEL
# ============================================================

def transition_control_energy(src, dst, base_p, target, centroids, eps=1e-9):
    """
    Heuristic control energy:
    - lower if a transition already has high base probability
    - lower if it moves closer to the target
    - higher if it fights the native flow
    """
    src_center = centroids[src]
    dst_center = centroids[dst]
    tgt_center = centroids[target]

    d_src = np.linalg.norm(src_center - tgt_center)
    d_dst = np.linalg.norm(dst_center - tgt_center)

    improvement = d_src - d_dst  # positive if dst is closer to target

    # Native resistance: unlikely transitions are harder to enforce
    native_cost = -math.log(base_p + eps)

    # Geometric penalty/reward:
    # if improvement is positive, control is easier
    # if negative, harder
    geom_cost = max(0.0, -improvement) + 0.25 * max(0.0, d_dst)

    return native_cost + geom_cost


def build_energy_table(prob_adj, centroids, target):
    table = {}
    for src, choices in prob_adj.items():
        for dst, base_p in choices:
            e = transition_control_energy(src, dst, base_p, target, centroids)
            table[(src, dst)] = {
                "base_p": base_p,
                "energy": e
            }
    return table


def controlled_step_min_energy(current, prob_adj, energy_table, bias_strength=2.0):
    """
    Prefer low-energy outgoing transitions.
    """
    if current not in prob_adj:
        return current, 0.0

    choices = prob_adj[current]
    dsts = []
    weights = []
    energies = []

    for dst, _ in choices:
        e = energy_table[(current, dst)]["energy"]
        w = math.exp(-bias_strength * e)
        dsts.append(dst)
        weights.append(w)
        energies.append(e)

    if sum(weights) <= 0:
        weights = [1.0] * len(dsts)

    chosen = random.choices(range(len(dsts)), weights=weights)[0]
    return dsts[chosen], energies[chosen]


def simulate_min_energy_control(prob_adj, energy_table, start=0, steps=120, bias_strength=2.0):
    path = [start]
    energies = []
    current = start

    for _ in range(steps):
        nxt, e = controlled_step_min_energy(current, prob_adj, energy_table, bias_strength=bias_strength)
        path.append(nxt)
        energies.append(e)
        current = nxt

    return path, energies


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


# ============================================================
# 7. BACKPROJECTION
# ============================================================

def make_spatial_path(cluster_path, centroids, jitter=0.16):
    pts = []
    for c in cluster_path:
        center = centroids[c].copy()
        noise = np.random.normal(scale=jitter, size=2)
        pts.append(center + noise)
    return np.array(pts)


# ============================================================
# 8. PLOTS
# ============================================================

def plot_energy_graph(energy_table, target):
    clusters = sorted(set([a for a, _ in energy_table] + [b for _, b in energy_table]))
    n = max(clusters) + 1
    M = np.full((n, n), np.nan)

    for (src, dst), info in energy_table.items():
        M[src, dst] = info["energy"]

    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(M, cmap="magma")

    for i in range(n):
        for j in range(n):
            if not np.isnan(M[i, j]):
                ax.text(j, i, f"{M[i, j]:.2f}", ha="center", va="center", color="white", fontsize=10)

    ax.set_title(f"V14 Control Energy Matrix (target = C{target})")
    ax.set_xlabel("to cluster")
    ax.set_ylabel("from cluster")
    ax.set_xticks(range(n))
    ax.set_xticklabels([f"C{i}" for i in range(n)])
    ax.set_yticks(range(n))
    ax.set_yticklabels([f"C{i}" for i in range(n)])
    fig.colorbar(im, ax=ax, label="control energy")

    out = os.path.join(OUTPUT_DIR, "v14_control_energy_matrix.png")
    plt.savefig(out, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out}")


def plot_control_comparison(H, xedges, yedges, nodes, groups, centroids,
                            uncontrolled_path, uncontrolled_pts,
                            controlled_path, controlled_pts,
                            energies, target):
    cluster_colors = {
        0: "#1f77b4",  # blue
        1: "#d62728",  # red
        2: "#e377c2",  # magenta
        3: "#17becf",  # cyan
    }

    fig, axes = plt.subplots(1, 2, figsize=(16, 7), sharex=True, sharey=True)

    panels = [
        ("Natural Dynamics", uncontrolled_path, uncontrolled_pts, None),
        (f"Minimal-Energy Controlled Dynamics (target = C{target})", controlled_path, controlled_pts, energies),
    ]

    for ax, (title, path, pts, e_series) in zip(axes, panels):
        ax.imshow(
            H.T,
            origin="lower",
            extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
            aspect="auto",
            cmap="viridis"
        )

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

        for i, (x, y) in enumerate(nodes):
            ax.text(x, y, f"N{i}", fontsize=9, ha="center", va="center", zorder=6)

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
            ax.text(center[0], center[1] + 0.35, f"C{c_idx}",
                    color="white", fontsize=11, ha="center", va="bottom", zorder=8)

        tgt = centroids[target]
        ax.scatter(
            tgt[0], tgt[1],
            s=760, facecolors="none", edgecolors="yellow",
            linewidths=2.5, zorder=9
        )

        ax.plot(pts[:, 0], pts[:, 1], color="white", linewidth=1.2, alpha=0.55, zorder=4)
        ax.scatter(pts[:, 0], pts[:, 1], c=[cluster_colors[c] for c in path], s=18, alpha=0.95, zorder=6)

        ax.scatter(pts[0, 0], pts[0, 1], s=220, c="lime", edgecolor="black", zorder=10)
        ax.scatter(pts[-1, 0], pts[-1, 1], s=220, c="yellow", edgecolor="black", zorder=10)

        counts = Counter(path)
        txt = "\n".join([f"C{k}: {counts[k]}" for k in sorted(counts)])
        if e_series is not None and len(e_series) > 0:
            txt += f"\nmean E: {np.mean(e_series):.2f}"
            txt += f"\nmax E: {np.max(e_series):.2f}"

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

    out = os.path.join(OUTPUT_DIR, "v14_minimal_control_energy.png")
    plt.savefig(out, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out}")


def plot_energy_series(energies):
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(energies, linewidth=1.5)
    ax.set_title("V14 Control Energy per Step")
    ax.set_xlabel("step")
    ax.set_ylabel("energy")

    out = os.path.join(OUTPUT_DIR, "v14_control_energy_series.png")
    plt.savefig(out, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out}")


# ============================================================
# 9. MAIN
# ============================================================

def main():
    print("Running V14 Minimal Control Energy...")

    X = generate_lorenz()
    e1, e2, _ = compute_basis(X)
    alpha, beta = project(X, e1, e2)
    H, xedges, yedges = density_field(alpha, beta, bins=180, sigma=2.0)

    nodes = get_nodes()
    centroids, groups = build_cluster_centroids(nodes, node_to_cluster)

    prob_adj = build_probabilities(cluster_edges)

    start_cluster = 0
    target_cluster = 2
    n_steps = 140
    bias_strength = 2.2

    energy_table = build_energy_table(prob_adj, centroids, target_cluster)

    uncontrolled = simulate_uncontrolled(prob_adj, start=start_cluster, steps=n_steps)
    controlled, energies = simulate_min_energy_control(
        prob_adj, energy_table,
        start=start_cluster,
        steps=n_steps,
        bias_strength=bias_strength
    )

    uncontrolled_pts = make_spatial_path(uncontrolled, centroids, jitter=0.16)
    controlled_pts = make_spatial_path(controlled, centroids, jitter=0.16)

    print("\nUncontrolled Visit Counts:")
    uc = Counter(uncontrolled)
    for k in sorted(uc):
        print(f"  C{k}: {uc[k]}")

    print("\nControlled Visit Counts:")
    cc = Counter(controlled)
    for k in sorted(cc):
        print(f"  C{k}: {cc[k]}")

    print(f"\nTarget cluster: C{target_cluster}")
    print(f"Mean control energy: {np.mean(energies):.4f}")
    print(f"Max control energy: {np.max(energies):.4f}")

    print("\nTransition energies:")
    for (src, dst), info in sorted(energy_table.items(), key=lambda x: (x[0][0], x[0][1])):
        print(f"  C{src} -> C{dst}: p={info['base_p']:.3f}, E={info['energy']:.3f}")

    plot_energy_graph(energy_table, target_cluster)
    plot_control_comparison(
        H, xedges, yedges, nodes, groups, centroids,
        uncontrolled, uncontrolled_pts,
        controlled, controlled_pts,
        energies, target_cluster
    )
    plot_energy_series(energies)


if __name__ == "__main__":
    main()
