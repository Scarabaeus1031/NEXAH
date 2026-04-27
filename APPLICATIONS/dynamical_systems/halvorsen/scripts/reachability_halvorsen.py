# ============================================================
# NEXAH — Reachability Analysis (Halvorsen)
# ============================================================
#
# Purpose:
# Determine reachable regions in coarse transition graph
#
# Input:
# coarse_matrix_*.npy
#
# Output:
# reachable sets + visualization
#
# ============================================================

import numpy as np
import os
from datetime import datetime
import matplotlib.pyplot as plt
from glob import glob

# ============================================================
# LOAD MATRIX
# ============================================================

def load_latest_matrix():
    files = sorted(glob("APPLICATIONS/dynamical_systems/halvorsen/outputs/coarse_matrix_*.npy"))
    if not files:
        raise RuntimeError("❌ No coarse_matrix found")
    path = files[-1]
    print("→ loading:", path)
    return np.load(path)

# ============================================================
# BUILD GRAPH
# ============================================================

def build_graph(M, threshold=0.05):
    n = M.shape[0]
    graph = {i: [] for i in range(n)}

    for i in range(n):
        for j in range(n):
            if M[i, j] > threshold:
                graph[i].append(j)

    return graph

# ============================================================
# REACHABILITY (DFS)
# ============================================================

def reachable_from(graph, start):
    visited = set()
    stack = [start]

    while stack:
        node = stack.pop()

        if node not in visited:
            visited.add(node)
            stack.extend(graph[node])

    return sorted(list(visited))

# ============================================================
# FULL REACHABILITY MAP
# ============================================================

def compute_reachability(graph):
    reach = {}

    for node in graph:
        reach[node] = reachable_from(graph, node)

    return reach

# ============================================================
# SAVE OUTPUT
# ============================================================

def save_outputs(reach):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_path = "APPLICATIONS/dynamical_systems/halvorsen/outputs"
    os.makedirs(base_path, exist_ok=True)

    txt_path = f"{base_path}/reachability_{timestamp}.txt"

    with open(txt_path, "w") as f:
        f.write("NEXAH Reachability Map\n")
        f.write("="*40 + "\n\n")

        for k, v in reach.items():
            f.write(f"{k} -> {v}\n")

    print(f"[✓] Reachability saved: {txt_path}")

# ============================================================
# VISUALIZATION
# ============================================================

def plot_reachability(reach):
    n = len(reach)
    M = np.zeros((n, n))

    for i in reach:
        for j in reach[i]:
            M[i, j] = 1

    plt.figure(figsize=(6,5))
    plt.imshow(M)
    plt.title("Reachability Matrix")
    plt.xlabel("reachable j")
    plt.ylabel("from i")
    plt.colorbar()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"APPLICATIONS/dynamical_systems/halvorsen/outputs/reachability_{timestamp}.png"
    plt.savefig(path)
    plt.close()

    print(f"[✓] Reachability plot saved: {path}")

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("→ load matrix")
    M = load_latest_matrix()

    print("→ build graph")
    graph = build_graph(M)

    print("→ compute reachability")
    reach = compute_reachability(graph)

    for k in reach:
        print(f"{k} -> {reach[k]}")

    print("→ save")
    save_outputs(reach)

    print("→ visualize")
    plot_reachability(reach)

    print("✔ DONE")
