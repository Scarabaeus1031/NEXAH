# cycle_core_embedding.py

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from sympy import primerange
import os

# =========================
# CONFIG
# =========================

MOD = 23
N_PRIMES = 20000
TOP_EDGES = 2
MAX_CYCLE_LEN = 8
MAX_CYCLES = 200

OUTPUT_PATH = "output/plots"
DATA_PATH = "output/data"

os.makedirs(OUTPUT_PATH, exist_ok=True)
os.makedirs(DATA_PATH, exist_ok=True)

# =========================
# PRIME RESIDUES
# =========================

primes = np.array(list(primerange(2, 300000)))[:N_PRIMES]
res = primes % MOD

# =========================
# TRANSITION MATRIX
# =========================

T = np.zeros((MOD, MOD))

for i in range(len(res) - 1):
    T[res[i], res[i + 1]] += 1

row_sums = T.sum(axis=1, keepdims=True)
row_sums[row_sums == 0] = 1
P = T / row_sums

# =========================
# SPARSE GRAPH
# =========================

G = nx.DiGraph()

for i in range(MOD):
    top_idx = np.argsort(P[i])[-TOP_EDGES:]
    for j in top_idx:
        if P[i, j] > 0:
            G.add_edge(i, j, weight=float(P[i, j]))

# =========================
# FIND CYCLES
# =========================

cycles = []

for c in nx.simple_cycles(G):
    if 2 <= len(c) <= MAX_CYCLE_LEN:
        cycles.append(c)

cycles = cycles[:MAX_CYCLES]

print(f"\n=== CYCLE CORE EMBEDDING — mod {MOD} ===")
print(f"cycles used: {len(cycles)}")

# =========================
# BUILD CYCLE CORE MATRIX
# =========================

C = np.zeros_like(P)

for cycle in cycles:
    for i in range(len(cycle)):
        a = cycle[i]
        b = cycle[(i + 1) % len(cycle)]
        if P[a, b] > 0:
            C[a, b] += P[a, b]

# Normalize for visualization
if C.max() > 0:
    C_vis = C / C.max()
else:
    C_vis = C.copy()

# =========================
# CORE GRAPH
# =========================

Core = nx.DiGraph()

for i in range(MOD):
    for j in range(MOD):
        if C[i, j] > 0:
            Core.add_edge(i, j, weight=float(C[i, j]))

core_nodes = sorted(Core.nodes())

print(f"core nodes: {len(core_nodes)} / {MOD}")
print(f"core node list: {core_nodes}")

# =========================
# SPECTRAL EMBEDDING
# =========================

# use undirected weighted graph for embedding
U = Core.to_undirected()

if len(U.nodes) >= 3:
    L = nx.normalized_laplacian_matrix(U, nodelist=core_nodes).toarray()
    eigvals, eigvecs = np.linalg.eigh(L)

    x = eigvecs[:, 1]
    y = eigvecs[:, 2]

    coords = {node: (x[k], y[k]) for k, node in enumerate(core_nodes)}
else:
    coords = nx.circular_layout(Core)

# =========================
# PLOT 1 — CORE EMBEDDING
# =========================

plt.figure(figsize=(8, 8))

weights = [Core[u][v]["weight"] / C.max() * 4 for u, v in Core.edges]

nx.draw_networkx_nodes(
    Core,
    coords,
    node_size=700,
    node_color="lightblue"
)

nx.draw_networkx_labels(
    Core,
    coords,
    font_size=10
)

nx.draw_networkx_edges(
    Core,
    coords,
    width=weights,
    edge_color="gray",
    alpha=0.7,
    arrows=True
)

plt.title(f"Cycle-Core Spectral Embedding — mod {MOD}")
plt.axis("off")

out = f"{OUTPUT_PATH}/cycle_core_embedding_mod{MOD}.png"
plt.savefig(out, dpi=300)
plt.close()

print(f"[OK] saved → {out}")

# =========================
# PLOT 2 — CORE MATRIX
# =========================

plt.figure(figsize=(7, 6))
plt.imshow(C_vis, cmap="viridis")
plt.colorbar(label="normalized cycle-core weight")
plt.title(f"Cycle-Core Matrix — mod {MOD}")
plt.xlabel("to state")
plt.ylabel("from state")

out = f"{OUTPUT_PATH}/cycle_core_matrix_mod{MOD}.png"
plt.savefig(out, dpi=300)
plt.close()

print(f"[OK] saved → {out}")

# =========================
# PLOT 3 — CORE VS FULL RING
# =========================

pos_ring = nx.circular_layout(G)

plt.figure(figsize=(8, 8))

nx.draw_networkx_nodes(
    G,
    pos_ring,
    node_size=400,
    node_color="lightgray"
)

nx.draw_networkx_labels(
    G,
    pos_ring,
    font_size=9
)

nx.draw_networkx_edges(
    G,
    pos_ring,
    alpha=0.15,
    arrows=True
)

nx.draw_networkx_nodes(
    G,
    pos_ring,
    nodelist=core_nodes,
    node_color="red",
    node_size=600
)

core_edges = list(Core.edges)

nx.draw_networkx_edges(
    G,
    pos_ring,
    edgelist=core_edges,
    edge_color="red",
    width=3,
    arrows=True
)

plt.title(f"Cycle-Core on Residue Ring — mod {MOD}")
plt.axis("off")

out = f"{OUTPUT_PATH}/cycle_core_ring_mod{MOD}.png"
plt.savefig(out, dpi=300)
plt.close()

print(f"[OK] saved → {out}")

# =========================
# SAVE SUMMARY
# =========================

summary_path = f"{DATA_PATH}/cycle_core_embedding_mod{MOD}.txt"

with open(summary_path, "w", encoding="utf-8") as f:
    f.write(f"CYCLE CORE EMBEDDING — mod {MOD}\n\n")
    f.write(f"cycles used: {len(cycles)}\n")
    f.write(f"core nodes: {len(core_nodes)} / {MOD}\n")
    f.write(f"core node list: {core_nodes}\n\n")
    f.write("core edges:\n")
    for u, v in Core.edges:
        f.write(f"{u} -> {v} weight={Core[u][v]['weight']:.6f}\n")

print(f"[OK] saved → {summary_path}")

print("\n=== INTERPRETATION ===")
print("""
Cycle-core embedding extracts the recurrent backbone of the transition system.

If the embedding forms a ring:
→ cycle core behaves like a circular / phase structure.

If it splits into lobes:
→ multiple recurrent substructures exist.

If core nodes exclude states such as 0:
→ those states are transient or peripheral relative to the recurrence core.
""")
