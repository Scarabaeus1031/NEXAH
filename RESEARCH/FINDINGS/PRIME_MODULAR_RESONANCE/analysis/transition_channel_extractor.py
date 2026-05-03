import numpy as np
import matplotlib.pyplot as plt
from sympy import primerange
import networkx as nx
import os

# =========================
# CONFIG
# =========================

MOD = 31
N_PRIMES = 20000
TOP_K = 3          # stärkste Kanten pro Node
THRESHOLD = 0.05   # minimaler Übergang

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
        b = residues[i+1]
        T[a, b] += 1

    # normalize rows
    row_sums = T.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    T = T / row_sums

    return T

# =========================
# CHANNEL EXTRACTION
# =========================

def extract_channels(T, top_k=3, threshold=0.05):
    channels = []

    for i in range(T.shape[0]):
        row = T[i]

        # top-k indices
        idx = np.argsort(row)[::-1][:top_k]

        for j in idx:
            if row[j] > threshold:
                channels.append((i, j, row[j]))

    return channels

# =========================
# GRAPH BUILD
# =========================

def build_graph(channels):
    G = nx.DiGraph()

    for i, j, w in channels:
        G.add_edge(i, j, weight=w)

    return G

# =========================
# MAIN
# =========================

print(f"\n=== TRANSITION CHANNELS (mod {MOD}) ===")

primes = generate_primes(N_PRIMES)
T = transition_matrix(primes, MOD)

channels = extract_channels(T, TOP_K, THRESHOLD)

# sort strongest edges
channels_sorted = sorted(channels, key=lambda x: x[2], reverse=True)

print("\nTop Channels:")
for i, j, w in channels_sorted[:20]:
    print(f"{i} → {j}  weight={w:.4f}")

# =========================
# GRAPH
# =========================

G = build_graph(channels)

# circular layout (clean für mod)
pos = nx.circular_layout(G)

plt.figure(figsize=(8,8))

edges = G.edges(data=True)
weights = [d['weight']*5 for (_,_,d) in edges]

nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=600,
    font_size=8,
    arrows=True,
    width=weights
)

plt.title(f"Transition Channels (mod {MOD})")

save_path = f"{OUTPUT_PATH}/transition_channels_mod{MOD}.png"
plt.savefig(save_path)
plt.close()

print(f"\n[OK] saved → {save_path}")

# =========================
# PATH DETECTION (optional)
# =========================

print("\n=== STRONG PATHS ===")

for node in range(MOD):
    if node in G:
        neighbors = list(G.successors(node))
        if neighbors:
            print(f"{node} → {neighbors}")

print("\n=== DONE ===")
