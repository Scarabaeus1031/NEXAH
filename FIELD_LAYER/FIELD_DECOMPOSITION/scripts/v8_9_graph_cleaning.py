# FIELD_LAYER/field_decomposition/scripts/v8_9_graph_cleaning.py

"""
NEXAH V8.9 — Graph Cleaning

Goal:
→ reduce noisy graph
→ cluster nodes
→ keep only meaningful edges
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PATHS
# ============================================================

BASE = "FIELD_LAYER/field_decomposition/outputs"
OUTDIR = os.path.join(BASE, "v8_9")
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# LOAD
# ============================================================

nodes = np.load(os.path.join(BASE, "v8_8", "nodes.npy"))
edges = np.load(os.path.join(BASE, "v8_8", "edges.npy"), allow_pickle=True)

print("original nodes:", len(nodes))
print("original edges:", len(edges))

# ============================================================
# NODE CLUSTERING (simple)
# ============================================================

cluster_radius = 3  # pixels

clusters = []
used = np.zeros(len(nodes), dtype=bool)

for i in range(len(nodes)):
    if used[i]:
        continue

    cluster = [nodes[i]]
    used[i] = True

    for j in range(i+1, len(nodes)):
        if used[j]:
            continue

        dist = np.linalg.norm(nodes[i] - nodes[j])
        if dist < cluster_radius:
            cluster.append(nodes[j])
            used[j] = True

    cluster = np.array(cluster)
    center = np.mean(cluster, axis=0).astype(int)
    clusters.append(center)

clusters = np.array(clusters)

print("reduced nodes:", len(clusters))

# ============================================================
# EDGE FILTERING
# ============================================================

min_length = 20  # remove short junk

clean_edges = []

for edge in edges:
    if len(edge) >= min_length:
        clean_edges.append(edge)

print("filtered edges:", len(clean_edges))

# ============================================================
# GRID
# ============================================================

ny, nx = 200, 200  # same as before
x = np.linspace(6, 17, nx)
y = np.linspace(22, 31, ny)

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(10, 7))

# edges
for edge in clean_edges:
    pts = np.array(edge)
    plt.plot(x[pts[:,1]], y[pts[:,0]], color="cyan", linewidth=2)

# nodes
if len(clusters) > 0:
    plt.scatter(
        x[clusters[:,1]],
        y[clusters[:,0]],
        color="red",
        s=40,
        label="nodes"
    )

plt.title("NEXAH V8.9 — Cleaned Decision Graph")
plt.legend()

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v8_9_clean_graph.png"), dpi=150)
plt.close()

# ============================================================
# SAVE
# ============================================================

np.save(os.path.join(OUTDIR, "clean_nodes.npy"), clusters)
np.save(os.path.join(OUTDIR, "clean_edges.npy"), np.array(clean_edges, dtype=object))

print("✓ V8.9 done →", OUTDIR)
