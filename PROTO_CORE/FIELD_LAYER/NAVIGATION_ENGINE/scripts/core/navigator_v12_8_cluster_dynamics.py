import numpy as np
import matplotlib.pyplot as plt
import random
from collections import defaultdict, Counter

# --- Cluster Transition Weights (aus V12.7) ---
cluster_edges = {
    (2, 1): 23,
    (0, 2): 16,
    (1, 0): 15,
    (3, 0): 15,
    (0, 1): 14,
    (1, 2): 12,
    (0, 0): 12,
    (1, 3): 9,
    (3, 3): 7
}

# --- Build adjacency list ---
adj = defaultdict(list)

for (src, dst), w in cluster_edges.items():
    adj[src].append((dst, w))

# --- Convert to probabilities ---
prob_adj = {}

for src, edges in adj.items():
    total = sum(w for _, w in edges)
    prob_adj[src] = [(dst, w / total) for dst, w in edges]

# --- Simulation ---
def simulate(start=0, steps=200):
    path = [start]
    current = start

    for _ in range(steps):
        if current not in prob_adj:
            break

        choices = prob_adj[current]
        nodes = [dst for dst, _ in choices]
        probs = [p for _, p in choices]

        current = random.choices(nodes, weights=probs)[0]
        path.append(current)

    return path

# --- Run simulation ---
path = simulate(start=0, steps=300)

# --- Count visits ---
counts = Counter(path)

print("\nCluster Visit Counts:")
for k, v in sorted(counts.items()):
    print(f"  C{k}: {v}")

# --- Plot trajectory ---
plt.figure(figsize=(10,3))
plt.plot(path, marker='o', markersize=3)
plt.title("V12.8 Cluster State Trajectory")
plt.xlabel("step")
plt.ylabel("cluster state")
plt.yticks([0,1,2,3], ["C0","C1","C2","C3"])

plt.grid(alpha=0.3)

# Save
out_path = "FIELD_LAYER/outputs/plots/v12_8_cluster_dynamics.png"
plt.savefig(out_path, dpi=150)
plt.close()

print(f"\nSaved: {out_path}")
