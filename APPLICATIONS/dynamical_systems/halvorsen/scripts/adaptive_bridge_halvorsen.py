# ============================================================
# NEXAH — Adaptive Bridge Injection (Halvorsen)
# ============================================================
#
# Purpose:
# Replace fixed bridge weights with adaptive, data-driven weights
#
# Idea:
# bridge_weight = alpha * max_outgoing_probability(source)
#
# This enables:
# - functional connectivity
# - usable transitions for policy
# - minimal intervention principle
#
# Outputs:
# - connected matrix (npy, png)
# - report (txt)
#
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

# ============================================================
# 🔹 LOAD MATRIX
# ============================================================

def load_latest_matrix():
    base = "APPLICATIONS/dynamical_systems/halvorsen/outputs"
    files = [f for f in os.listdir(base) if f.startswith("coarse_matrix") and f.endswith(".npy")]
    files.sort()
    path = os.path.join(base, files[-1])
    print(f"→ loading: {path}")
    return np.load(path), path

# ============================================================
# 🔹 BUILD GRAPH
# ============================================================

def build_graph(M, threshold=1e-6):
    graph = {}
    n = M.shape[0]

    for i in range(n):
        neighbors = []
        for j in range(n):
            if M[i, j] > threshold:
                neighbors.append(j)
        graph[i] = neighbors

    return graph

# ============================================================
# 🔹 FIND COMPONENTS
# ============================================================

def find_components(graph):
    visited = set()
    components = []

    def dfs(start):
        stack = [start]
        comp = []

        while stack:
            node = stack.pop()
            if node in visited:
                continue

            visited.add(node)
            comp.append(node)

            for nbr in graph[node]:
                if nbr not in visited:
                    stack.append(nbr)

        return comp

    for node in graph:
        if node not in visited:
            components.append(dfs(node))

    return components

# ============================================================
# 🔹 ADAPTIVE BRIDGES
# ============================================================

def compute_max_outgoing(M):
    max_out = {}
    for i in range(M.shape[0]):
        max_out[i] = np.max(M[i])
    return max_out

def add_adaptive_bridges(M, components, alpha=0.5):
    M_new = M.copy()
    max_out = compute_max_outgoing(M)

    bridges = []

    # connect components sequentially
    for k in range(len(components) - 1):
        src_comp = components[k]
        dst_comp = components[k+1]

        i = src_comp[-1]   # last node of comp
        j = dst_comp[0]    # first node of next comp

        base_weight = max_out[i]
        w = alpha * base_weight

        M_new[i, j] = w

        bridges.append((i, j, w))

    # normalize rows
    for i in range(M_new.shape[0]):
        s = M_new[i].sum()
        if s > 0:
            M_new[i] /= s

    return M_new, bridges

# ============================================================
# 🔹 SAVE OUTPUT
# ============================================================

def save_outputs(M, bridges, source_path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = "APPLICATIONS/dynamical_systems/halvorsen/outputs"
    os.makedirs(base, exist_ok=True)

    # TXT
    txt_path = f"{base}/adaptive_bridges_{timestamp}.txt"
    with open(txt_path, "w") as f:
        f.write("NEXAH — Adaptive Bridge Report\n")
        f.write("="*50 + "\n\n")
        f.write(f"Source matrix: {source_path}\n\n")

        for i, j, w in bridges:
            f.write(f"{i} -> {j} | weight={w:.4f}\n")

    # NPY
    npy_path = f"{base}/adaptive_matrix_{timestamp}.npy"
    np.save(npy_path, M)

    # PNG
    plt.figure(figsize=(6,5))
    plt.imshow(M)
    plt.title("Adaptive Connected Matrix")
    plt.colorbar()
    plt.xlabel("to")
    plt.ylabel("from")
    plt.tight_layout()

    png_path = f"{base}/adaptive_matrix_{timestamp}.png"
    plt.savefig(png_path)
    plt.close()

    print(f"[✓] TXT saved: {txt_path}")
    print(f"[✓] NPY saved: {npy_path}")
    print(f"[✓] PNG saved: {png_path}")

# ============================================================
# 🔹 MAIN
# ============================================================

if __name__ == "__main__":

    print("→ load matrix")
    M, path = load_latest_matrix()

    print("→ build graph")
    graph = build_graph(M)

    print("→ find components")
    components = find_components(graph)

    print(f"components: {len(components)}")
    for i, c in enumerate(components):
        print(f"{i}: {c}")

    print("→ adaptive bridging")
    M_new, bridges = add_adaptive_bridges(M, components, alpha=0.5)

    print("bridges:")
    for b in bridges:
        print(b)

    print("→ save")
    save_outputs(M_new, bridges, path)

    print("✔ DONE")
