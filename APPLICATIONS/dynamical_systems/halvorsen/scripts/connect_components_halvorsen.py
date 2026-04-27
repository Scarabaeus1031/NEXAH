# ============================================================
# NEXAH — Connect Components (Halvorsen)
# ============================================================
#
# Purpose:
# Add minimal synthetic bridge edges between disconnected
# reachability components to create a closed navigable graph.
#
# Input:
# - latest coarse_matrix_*.npy
#
# Output:
# - connected_matrix_*.npy
# - connected_matrix_*.png
# - component_bridges_*.txt
#
# ============================================================

import numpy as np
import os
import glob
from datetime import datetime
import matplotlib.pyplot as plt


# ============================================================
# LOAD MATRIX
# ============================================================

def load_latest_matrix():
    files = sorted(glob.glob(
        "APPLICATIONS/dynamical_systems/halvorsen/outputs/coarse_matrix_*.npy"
    ))

    if not files:
        raise RuntimeError("No coarse_matrix_*.npy found.")

    path = files[-1]
    print(f"→ loading: {path}")
    return np.load(path), path


# ============================================================
# BUILD GRAPH
# ============================================================

def build_graph(M, threshold=0.05):
    n = M.shape[0]
    graph = {i: [] for i in range(n)}

    for i in range(n):
        for j in range(n):
            if i != j and M[i, j] > threshold:
                graph[i].append(j)

    return graph


# ============================================================
# REACHABILITY
# ============================================================

def reachable_from(graph, start):
    visited = set()
    stack = [start]

    while stack:
        node = stack.pop()

        if node not in visited:
            visited.add(node)
            stack.extend(graph[node])

    return visited


# ============================================================
# COMPONENT EXTRACTION
# ============================================================

def weak_components(graph):
    undirected = {k: set() for k in graph}

    for i, targets in graph.items():
        for j in targets:
            undirected[i].add(j)
            undirected[j].add(i)

    components = []
    seen = set()

    for node in undirected:
        if node in seen:
            continue

        stack = [node]
        comp = set()

        while stack:
            n = stack.pop()
            if n in comp:
                continue
            comp.add(n)
            stack.extend(undirected[n] - comp)

        seen |= comp
        components.append(sorted(comp))

    return components


# ============================================================
# CONNECT COMPONENTS
# ============================================================

def connect_components(M, components, bridge_weight=0.05):
    """
    Adds minimal forward bridge edges between component sinks
    and next component starts.
    """

    connected = M.copy()
    bridges = []

    for idx in range(len(components) - 1):
        current = components[idx]
        nxt = components[idx + 1]

        source = max(current)
        target = min(nxt)

        connected[source, target] += bridge_weight
        bridges.append((source, target, bridge_weight))

    # renormalize rows
    for i in range(connected.shape[0]):
        row_sum = connected[i].sum()
        if row_sum > 0:
            connected[i] /= row_sum

    return connected, bridges


# ============================================================
# SAVE OUTPUTS
# ============================================================

def save_outputs(M_original, M_connected, components, bridges, source_matrix):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = "APPLICATIONS/dynamical_systems/halvorsen/outputs"
    os.makedirs(base, exist_ok=True)

    txt_path = f"{base}/component_bridges_{timestamp}.txt"

    with open(txt_path, "w") as f:
        f.write("NEXAH — Halvorsen Component Connection Report\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Source matrix: {source_matrix}\n\n")

        f.write("WEAK COMPONENTS\n")
        f.write("-" * 60 + "\n")
        for idx, comp in enumerate(components):
            f.write(f"Component {idx}: {comp}\n")

        f.write("\nBRIDGES ADDED\n")
        f.write("-" * 60 + "\n")
        for s, t, w in bridges:
            f.write(f"{s} -> {t} | bridge_weight={w:.4f}\n")

        f.write("\nNOTE\n")
        f.write("-" * 60 + "\n")
        f.write("Bridge edges are synthetic control candidates, not observed transitions.\n")
        f.write("They represent minimal interventions required for global navigability.\n")

    npy_path = f"{base}/connected_matrix_{timestamp}.npy"
    np.save(npy_path, M_connected)

    png_path = f"{base}/connected_matrix_{timestamp}.png"

    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(M_connected)
    plt.colorbar(im)

    for s, t, _ in bridges:
        ax.scatter(t, s, s=120, facecolors="none", edgecolors="red", linewidths=2)

    ax.set_title("Connected Transition Matrix")
    ax.set_xlabel("to cluster")
    ax.set_ylabel("from cluster")

    plt.tight_layout()
    fig.savefig(png_path, dpi=300)
    plt.close(fig)

    print(f"[✓] Report saved: {txt_path}")
    print(f"[✓] Connected matrix NPY saved: {npy_path}")
    print(f"[✓] Connected matrix PNG saved: {png_path}")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("→ load matrix")
    M, source_matrix = load_latest_matrix()

    print("→ build graph")
    graph = build_graph(M, threshold=0.05)

    print("→ find components")
    components = weak_components(graph)

    print(f"components found: {len(components)}")
    for i, comp in enumerate(components):
        print(f"component {i}: {comp}")

    print("→ connect components")
    connected, bridges = connect_components(
        M,
        components,
        bridge_weight=0.05
    )

    print("bridges added:")
    for b in bridges:
        print(f"{b[0]} -> {b[1]} | w={b[2]}")

    print("→ save")
    save_outputs(M, connected, components, bridges, source_matrix)

    print("✔ DONE")
