# cycle_drift_alignment.py

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from sympy import primerange

MOD = 23
N_PRIMES = 20000
TOP_EDGES = 3
MAX_CYCLE_LEN = 10

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

T = T / T.sum(axis=1, keepdims=True)

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

drift = []

for i in range(MOD):
    for j in range(MOD):
        if T[i,j] > 0:
            step = (j - i) % MOD
            drift.append(step * T[i,j])

mean_drift = np.mean(drift)

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

aligned = []

for c in cycles:
    d = cycle_direction(c)
    aligned.append((c, d))

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

best_cycle = aligned[0][0]

pos = nx.circular_layout(G)

plt.figure(figsize=(6,6))
nx.draw(G, pos, node_size=400, alpha=0.3)

edges = [(best_cycle[i], best_cycle[(i+1)%len(best_cycle)]) for i in range(len(best_cycle))]

nx.draw_networkx_nodes(G, pos, nodelist=best_cycle, node_color='red')
nx.draw_networkx_edges(G, pos, edgelist=edges, width=3, edge_color='red')

plt.title(f"Best aligned cycle (mod {MOD})")
plt.show()
