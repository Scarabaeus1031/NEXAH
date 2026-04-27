# ============================================================
# NEXAH — Path Planning on Gate Graph (Halvorsen)
# ============================================================
#
# Purpose:
# Compute optimal path through gate graph using transition costs.
#
# Concept:
# - nodes = clusters
# - edges = gates
# - weight = -log(p)  (high probability = low cost)
#
# Output:
# - best path
# - path visualization
#
# ============================================================

import numpy as np
import os
import glob
from datetime import datetime
import matplotlib.pyplot as plt
import heapq


# ============================================================
# LOAD MATRIX
# ============================================================

def load_latest_matrix():
    files = sorted(glob.glob(
        "APPLICATIONS/dynamical_systems/halvorsen/outputs/coarse_matrix_*.npy"
    ))

    if not files:
        raise RuntimeError("No coarse matrix found.")

    latest = files[-1]
    print(f"→ loading: {latest}")

    return np.load(latest)


# ============================================================
# BUILD GRAPH (from matrix)
# ============================================================

def build_graph(M, threshold=0.05):
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
# DIJKSTRA PATH
# ============================================================

def shortest_path(graph, start, target):
    queue = [(0, start, [])]
    visited = set()

    while queue:
        cost, node, path = heapq.heappop(queue)

        if node in visited:
            continue

        path = path + [node]
        visited.add(node)

        if node == target:
            return cost, path

        for neighbor, edge_cost, p in graph[node]:
            heapq.heappush(queue, (cost + edge_cost, neighbor, path))

    return None, None


# ============================================================
# VISUALIZE PATH
# ============================================================

def plot_path(graph, path, base_path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    png_path = f"{base_path}/planned_path_{timestamp}.png"

    nodes = list(graph.keys())
    n = len(nodes)

    x = np.arange(n)
    y = np.sin(np.linspace(0, 2*np.pi, n)) * 0.25

    fig, ax = plt.subplots(figsize=(12,4))

    # draw nodes
    ax.scatter(x, y, s=200)

    for node in nodes:
        ax.text(x[node], y[node], str(node), ha="center", va="center")

    # draw all edges faint
    for i in graph:
        for j, _, _ in graph[i]:
            ax.plot([x[i], x[j]], [y[i], y[j]], alpha=0.1, color="gray")

    # highlight path
    for i in range(len(path)-1):
        a = path[i]
        b = path[i+1]

        ax.plot(
            [x[a], x[b]],
            [y[a], y[b]],
            linewidth=3,
            color="red"
        )

    ax.set_title("NEXAH — Planned Path")
    ax.set_yticks([])
    ax.grid(axis="x", alpha=0.2)

    plt.tight_layout()
    plt.savefig(png_path)
    plt.close()

    print(f"[✓] Path plot saved: {png_path}")


# ============================================================
# SAVE TXT (FIXED)
# ============================================================

def save_path(path, cost, base_path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    txt_path = f"{base_path}/planned_path_{timestamp}.txt"

    with open(txt_path, "w") as f:
        f.write("NEXAH Path Planning\n")
        f.write("="*40 + "\n\n")

        if path is None:
            f.write("NO PATH FOUND\n")
        else:
            f.write(f"path: {path}\n")
            f.write(f"cost: {cost:.4f}\n")

    print(f"[✓] Path TXT saved: {txt_path}")


# ============================================================
# DEBUG: SHOW GRAPH CONNECTIONS
# ============================================================

def debug_graph(graph):
    print("\n--- GRAPH STRUCTURE ---")
    for node in graph:
        neighbors = [n for (n, _, _) in graph[node]]
        print(f"{node} -> {neighbors}")
    print("------------------------\n")


# ============================================================
# MAIN (FIXED)
# ============================================================

if __name__ == "__main__":

    base_path = "APPLICATIONS/dynamical_systems/halvorsen/outputs"
    os.makedirs(base_path, exist_ok=True)

    print("→ load matrix")
    M = load_latest_matrix()

    print("→ build graph")
    graph = build_graph(M, threshold=0.05)

    # 🔍 DEBUG (WICHTIG!)
    debug_graph(graph)

    # 🔥 SPIEL HIERMIT
    start = 6
    target = 15

    print(f"→ plan path: {start} → {target}")
    cost, path = shortest_path(graph, start, target)

    if path is None:
        print("❌ NO PATH FOUND")
    else:
        print("PATH:", path)
        print("COST:", cost)

    print("→ save")
    save_path(path, cost, base_path)

    if path is not None:
        plot_path(graph, path, base_path)

    print("✔ DONE")
