# ============================================================
# NEXAH — Global Policy (Halvorsen)
# ============================================================
#
# Purpose:
# Compute a global navigation policy on the connected
# Halvorsen transition system.
#
# Concept:
# - nodes = coarse clusters
# - edges = transition probabilities
# - policy chooses best next node toward a target
# - cost = -log(P)
#
# Input:
# - latest connected_matrix_*.npy
#   fallback: latest coarse_matrix_*.npy
#
# Output:
# - global_policy_*.txt
# - global_policy_*.png
#
# ============================================================

import os
import glob
import heapq
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# LOAD MATRIX
# ============================================================

def load_latest_matrix():
    connected = sorted(glob.glob(
        "APPLICATIONS/dynamical_systems/halvorsen/outputs/connected_matrix_*.npy"
    ))

    coarse = sorted(glob.glob(
        "APPLICATIONS/dynamical_systems/halvorsen/outputs/coarse_matrix_*.npy"
    ))

    if connected:
        path = connected[-1]
        print(f"→ loading connected matrix: {path}")
        return np.load(path), path, "connected"

    if coarse:
        path = coarse[-1]
        print(f"→ loading coarse matrix: {path}")
        return np.load(path), path, "coarse"

    raise RuntimeError("No matrix found. Run coarse_grain_halvorsen.py first.")


# ============================================================
# BUILD WEIGHTED GRAPH
# ============================================================

def build_graph(M, threshold=0.001):
    graph = {}
    n = M.shape[0]

    for i in range(n):
        graph[i] = []

        for j in range(n):
            if i == j:
                continue

            p = M[i, j]

            if p > threshold:
                cost = -np.log(p)
                graph[i].append((j, cost, p))

    return graph


# ============================================================
# DIJKSTRA TO TARGET
# ============================================================

def shortest_path(graph, start, target):
    queue = [(0.0, start, [])]
    visited = set()

    while queue:
        cost, node, path = heapq.heappop(queue)

        if node in visited:
            continue

        path = path + [node]
        visited.add(node)

        if node == target:
            return cost, path

        for neighbor, edge_cost, probability in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(
                    queue,
                    (cost + edge_cost, neighbor, path)
                )

    return None, None


# ============================================================
# COMPUTE GLOBAL POLICY
# ============================================================

def compute_policy(graph, target):
    policy = {}
    paths = {}

    for start in graph.keys():
        cost, path = shortest_path(graph, start, target)

        if path is None or len(path) < 2:
            policy[start] = None
            paths[start] = {
                "path": path,
                "cost": cost
            }
        else:
            policy[start] = path[1]
            paths[start] = {
                "path": path,
                "cost": cost
            }

    return policy, paths


# ============================================================
# SAVE POLICY TXT
# ============================================================

def save_policy_txt(policy, paths, target, source_matrix, matrix_type, base):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    txt_path = f"{base}/global_policy_{timestamp}.txt"

    with open(txt_path, "w") as f:
        f.write("NEXAH — Halvorsen Global Policy\n")
        f.write("=" * 60 + "\n\n")

        f.write(f"Target cluster: {target}\n")
        f.write(f"Source matrix: {source_matrix}\n")
        f.write(f"Matrix type: {matrix_type}\n\n")

        f.write("POLICY\n")
        f.write("-" * 60 + "\n")
        for node in sorted(policy.keys()):
            action = policy[node]
            if action is None:
                f.write(f"{node} -> STOP / UNREACHABLE\n")
            else:
                f.write(f"{node} -> {action}\n")

        f.write("\nPATHS\n")
        f.write("-" * 60 + "\n")
        for node in sorted(paths.keys()):
            path = paths[node]["path"]
            cost = paths[node]["cost"]

            if path is None:
                f.write(f"{node}: NO PATH\n")
            elif cost is None:
                f.write(f"{node}: path={path} | cost=None\n")
            else:
                f.write(f"{node}: path={path} | cost={cost:.4f}\n")

    print(f"[✓] Policy TXT saved: {txt_path}")
    return txt_path


# ============================================================
# PLOT POLICY
# ============================================================

def plot_policy(policy, target, base):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    png_path = f"{base}/global_policy_{timestamp}.png"

    nodes = sorted(policy.keys())
    n = len(nodes)

    x = np.arange(n)
    y = np.sin(np.linspace(0, 2 * np.pi, n)) * 0.25

    fig, ax = plt.subplots(figsize=(12, 4))

    # nodes
    ax.scatter(x, y, s=260, zorder=3)

    for node in nodes:
        ax.text(
            x[node],
            y[node],
            str(node),
            ha="center",
            va="center",
            fontsize=9,
            zorder=4
        )

    # target marker
    ax.scatter(
        x[target],
        y[target],
        s=500,
        facecolors="none",
        edgecolors="red",
        linewidths=2.5,
        zorder=5
    )

    # policy arrows
    for node, action in policy.items():
        if action is None:
            continue

        dx = x[action] - x[node]
        dy = y[action] - y[node]

        ax.arrow(
            x[node],
            y[node],
            dx * 0.82,
            dy * 0.82,
            length_includes_head=True,
            head_width=0.06,
            head_length=0.18,
            linewidth=2,
            alpha=0.8,
            zorder=2
        )

    ax.set_title(f"NEXAH — Global Policy Toward Cluster {target}")
    ax.set_xlabel("coarse cluster order")
    ax.set_yticks([])
    ax.grid(axis="x", alpha=0.2)

    plt.tight_layout()
    fig.savefig(png_path, dpi=300)
    plt.close(fig)

    print(f"[✓] Policy PNG saved: {png_path}")
    return png_path


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    base = "APPLICATIONS/dynamical_systems/halvorsen/outputs"
    os.makedirs(base, exist_ok=True)

    print("→ load matrix")
    M, source_matrix, matrix_type = load_latest_matrix()

    print("→ build graph")
    graph = build_graph(M, threshold=0.001)

    # Change this target to test other policies.
    target = 15

    print(f"→ compute global policy toward target {target}")
    policy, paths = compute_policy(graph, target)

    reachable = sum(1 for p in paths.values() if p["path"] is not None)
    print(f"reachable nodes: {reachable}/{len(paths)}")

    for node in sorted(policy.keys()):
        action = policy[node]
        if action is None:
            print(f"{node} -> STOP / UNREACHABLE")
        else:
            print(f"{node} -> {action}")

    print("→ save")
    save_policy_txt(policy, paths, target, source_matrix, matrix_type, base)
    plot_policy(policy, target, base)

    print("✔ DONE")
