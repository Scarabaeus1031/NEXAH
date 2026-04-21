# mod7_top_transitions.py

import numpy as np
from sympy import primerange
import matplotlib.pyplot as plt

mod = 7
primes = list(primerange(3, 10000))
seq = [p % mod for p in primes]

# transition matrix
matrix = np.zeros((mod, mod))
for i in range(len(seq)-1):
    matrix[seq[i], seq[i+1]] += 1

matrix /= matrix.sum()

# top edges
edges = []
for i in range(mod):
    for j in range(mod):
        edges.append((i, j, matrix[i, j]))

edges = sorted(edges, key=lambda x: x[2], reverse=True)

print("\nTop Transitions:")
for e in edges[:10]:
    print(f"{e[0]} → {e[1]} : {e[2]:.4f}")

# graph plot
import networkx as nx

G = nx.DiGraph()

for i, j, w in edges[:15]:
    if w > 0:
        G.add_edge(i, j, weight=w)

pos = nx.circular_layout(G)
weights = [G[u][v]['weight']*50 for u,v in G.edges()]

nx.draw(G, pos, with_labels=True, width=weights)
plt.title("Top Prime Transitions (mod 7)")
plt.show()


# ================= AUTO SAVE HOOK =================
import os
import matplotlib.pyplot as plt

if os.environ.get("AUTO_SAVE") == "1":

    figs = list(map(plt.figure, plt.get_fignums()))

    if not figs:
        print("[WARN] No figures to save.")

    for i, fig in enumerate(figs):
        filename = __file__.split("/")[-1].replace(".py", f"_{i}.png")
        fig.savefig(f"output/plots/{filename}", dpi=150, bbox_inches="tight")

    plt.close("all")

else:
    plt.show()

# =================================================
