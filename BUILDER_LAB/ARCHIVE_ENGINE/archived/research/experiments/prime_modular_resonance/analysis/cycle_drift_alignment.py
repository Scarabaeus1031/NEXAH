# cycle_drift_alignment.py

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

TOP_EDGES = 2        # 🔥 reduziert Graph-Dichte (wichtig!)
MAX_CYCLE_LEN = 8    # 🔥 begrenzt Zyklenlänge

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

# normalize
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
# FIND SHORT CYCLES ONLY
# =========================

cycles = []

for c in nx.simple_cycles(G):
    if len(c) <= MAX_CYCLE_LEN:
        cycles.append(c)

print(f"\nFound {len(cycles)} short cycles")

# =========================
# DRIFT VECTOR
# =========================

drift_values = []

for i in range(MOD):
    for j in range(MOD):
        if T[i, j] > 0:
            step = (j - i) % MOD
            drift_values.append(step * T[i, j])

mean_drift = np.mean(drift_values)

print(f"Mean drift: {mean_drift:.3f}")

# =========================
# CYCLE ALIGNMENT
# =========================

def cycle_direction(cycle):
    steps = []
    for i in range(len(cycle)):
        a = cycle[i]
        b = cycle[(i+1) % len(cycle)]
        steps.append((b - a) % MOD)
    return np.mean(steps)

aligned = [(c, cycle_direction(c)) for c in cycles]

# sort by strongest drift alignment
aligned.sort(key=lambda x: -x[1])

# =========================
# OUTPUT
# =========================

print("\nTop aligned cycles:")

for c, d in aligned[:10]:
    print(f"cycle={c}  drift={d:.2f}")

# =========================
# VISUALIZE BEST
# =========================

if len(aligned) == 0:
    print("No cycles found.")
    exit()

best_cycle = aligned[0][0]

pos = nx.circular_layout(G)

plt.figure(figsize=(7,7))

# base graph
nx.draw(
    G,
    pos,
    node_size=600,
    node_color='lightblue',
    edge_color='gray',
    alpha=0.6
)

# labels
nx.draw_networkx_labels(G, pos, font_size=10, font_color='black')

# highlight cycle edges
cycle_edges = [
    (best_cycle[i], best_cycle[(i+1) % len(best_cycle)])
    for i in range(len(best_cycle))
]

nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=best_cycle,
    node_color='red'
)

nx.draw_networkx_edges(
    G,
    pos,
    edgelist=cycle_edges,
    width=3,
    edge_color='red'
)

plt.title(f"Best aligned cycle (mod {MOD})")

# save plot
save_path = f"{OUTPUT_PATH}/cycle_alignment_mod{MOD}.png"
plt.savefig(save_path)
print(f"[OK] saved → {save_path}")

plt.show()
