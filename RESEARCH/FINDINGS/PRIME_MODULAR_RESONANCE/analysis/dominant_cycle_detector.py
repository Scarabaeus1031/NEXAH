# dominant_cycle_detector.py

import numpy as np
import matplotlib.pyplot as plt
from sympy import primerange
import networkx as nx
import os

# =========================
# CONFIG
# =========================

MODS = [7, 11, 13, 17, 19, 23, 29, 31]
N_PRIMES = 20000
TOP_K = 5
THRESHOLD = 0.03

OUTPUT_PATH = "output/plots"
os.makedirs(OUTPUT_PATH, exist_ok=True)

# =========================
# PRIME GENERATOR
# =========================

def generate_primes(n):
    primes = list(primerange(2, 300000))
    return np.array(primes[:n])

# =========================
# TRANSITION MATRIX
# =========================

def transition_matrix(sequence, mod):
    residues = sequence % mod
    T = np.zeros((mod, mod))

    for i in range(len(residues) - 1):
        a = residues[i]
        b = residues[i + 1]
        T[a, b] += 1

    row_sums = T.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    return T / row_sums

# =========================
# GRAPH EXTRACTION
# =========================

def extract_graph(T, top_k=5, threshold=0.03):
    G = nx.DiGraph()

    for i in range(T.shape[0]):
        row = T[i]
        top_targets = np.argsort(row)[::-1][:top_k]

        for j in top_targets:
            w = row[j]
            if w >= threshold:
                G.add_edge(i, j, weight=float(w))

    return G

# =========================
# CYCLE SCORING
# =========================

def cycle_weight(G, cycle):
    weights = []

    for i in range(len(cycle)):
        a = cycle[i]
        b = cycle[(i + 1) % len(cycle)]

        if G.has_edge(a, b):
            weights.append(G[a][b]["weight"])
        else:
            return 0.0

    return float(np.mean(weights))

# =========================
# FIND CYCLES
# =========================

def find_dominant_cycles(G, max_cycles=10):
    cycles = list(nx.simple_cycles(G))

    scored = []
    for c in cycles:
        if len(c) < 2:
            continue
        w = cycle_weight(G, c)
        scored.append((c, w, len(c)))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:max_cycles]

# =========================
# PLOT
# =========================

def plot_dominant_cycle(G, cycle, mod, weight):
    pos = nx.circular_layout(G)

    plt.figure(figsize=(6, 6))

    nx.draw_networkx_nodes(G, pos, node_size=400, node_color="lightgray")
    nx.draw_networkx_labels(G, pos, font_size=8)

    # faint edges
    nx.draw_networkx_edges(G, pos, alpha=0.2)

    # highlight cycle
    edges = [(cycle[i], cycle[(i + 1) % len(cycle)]) for i in range(len(cycle))]

    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=edges,
        edge_color="red",
        width=3
    )

    nx.draw_networkx_nodes(G, pos, nodelist=cycle, node_color="red", node_size=600)

    plt.title(f"Dominant Cycle (mod {mod})\nlen={len(cycle)} weight={weight:.3f}")
    plt.axis("off")

    path = f"{OUTPUT_PATH}/dominant_cycle_mod{mod}.png"
    plt.savefig(path, dpi=200)
    plt.close()

    print(f"[OK] saved → {path}")

# =========================
# MAIN
# =========================

def main():
    print("\n=== DOMINANT CYCLE DETECTOR ===")

    primes = generate_primes(N_PRIMES)

    for mod in MODS:
        print(f"\n--- mod {mod} ---")

        T = transition_matrix(primes, mod)
        G = extract_graph(T, TOP_K, THRESHOLD)

        cycles = find_dominant_cycles(G)

        if not cycles:
            print("No cycles found.")
            continue

        print("Top cycles:")

        for i, (cycle, w, length) in enumerate(cycles, start=1):
            print(f"{i:02d}. len={length} | weight={w:.4f} | {cycle}")

        # dominant
        best_cycle, best_weight, _ = cycles[0]

        plot_dominant_cycle(G, best_cycle, mod, best_weight)

    print("\n=== DONE ===")

# =========================
# RUN
# =========================

if __name__ == "__main__":
    main()
