# cycle_overlap_graph.py

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
MAX_CYCLES = 200   # 🔥 Begrenzung für Übersicht

OUTPUT_PATH = "output/plots"
os.makedirs(OUTPUT_PATH, exist_ok=True)

# =========================
# PRIMES
# =========================

primes = np.array(list(primerange(2, 300000)))[:N_PRIMES]
res = primes % MOD

# =========================
# TRANSITION MATRIX
# =========================

T = np.zeros((MOD, MOD))

for i in range(len(res)-1):
    T[res[i], res[i+1]] += 1

row_sums = T.sum(axis=1, keepdims=True)
row_sums[row_sums == 0] = 1
T = T / row_sums

# =========================
# BUILD SPARSE GRAPH
# =========================

G = nx.DiGraph()

for i in range(MOD):
    top_idx = np.argsort(T[i])[-TOP_EDGES:]
    for j in top_idx:
        if T[i, j] > 0:
            G.add_edge(i, j, weight=T[i, j])

# =========================
# FIND CYCLES
# =========================

cycles = []

for c in nx.simple_cycles(G):
    if len(c) <= MAX_CYCLE_LEN:
        cycles.append(tuple(sorted(c)))  # 🔥 canonical form

# unique cycles
cycles = list(set(cycles))

# limit size
cycles = cycles[:MAX_CYCLES]

print(f"\nUsing {len(cycles)} cycles")

# =========================
# BUILD OVERLAP GRAPH
# =========================

OG = nx.Graph()

# add cycle nodes
for i, c in enumerate(cycles):
    OG.add_node(i, size=len(c), nodes=c)

# connect if overlap
for i in range(len(cycles)):
    for j in range(i+1, len(cycles)):
        overlap = set(cycles[i]).intersection(set(cycles[j]))
        if len(overlap) >= 2:  # 🔥 threshold (shared nodes)
            OG.add_edge(i, j, weight=len(overlap))

# =========================
# ANALYSIS
# =========================

components = list(nx.connected_components(OG))

print("\n=== COMPONENTS ===")
for idx, comp in enumerate(components):
    print(f"Component {idx}: size={len(comp)}")

# =========================
# VISUALIZATION
# =========================

plt.figure(figsize=(8,8))

pos = nx.spring_layout(OG, seed=42)

# node sizes ~ cycle length
sizes = [OG.nodes[n]['size'] * 100 for n in OG.nodes]

nx.draw(
    OG,
    pos,
    node_size=sizes,
    node_color='lightblue',
    edge_color='gray',
    alpha=0.7
)

# highlight largest component
largest = max(components, key=len)

nx.draw_networkx_nodes(
    OG,
    pos,
    nodelist=list(largest),
    node_color='red'
)

plt.title(f"Cycle Overlap Graph (mod {MOD})")

save_path = f"{OUTPUT_PATH}/cycle_overlap_mod{MOD}.png"
plt.savefig(save_path)
print(f"[OK] saved → {save_path}")

plt.show()
