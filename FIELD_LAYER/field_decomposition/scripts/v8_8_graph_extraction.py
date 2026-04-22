# FIELD_LAYER/field_decomposition/scripts/v8_8_graph_extraction.py

"""
NEXAH V8.8 — Decision Graph Extraction

Goal:
→ convert skeleton into graph
→ extract nodes and edges
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PATHS
# ============================================================

BASE = "FIELD_LAYER/field_decomposition/outputs"
OUTDIR = os.path.join(BASE, "v8_8")
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# LOAD
# ============================================================

skeleton = np.load(os.path.join(BASE, "v8_7", "decision_skeleton.npy"))

ny, nx = skeleton.shape

# ============================================================
# HELPERS
# ============================================================

def neighbors(i, j):
    coords = []
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            ni = i + di
            nj = j + dj
            if 0 <= ni < ny and 0 <= nj < nx:
                coords.append((ni, nj))
    return coords

# ============================================================
# NODE DETECTION
# ============================================================

nodes = []

for i in range(ny):
    for j in range(nx):
        if not skeleton[i, j]:
            continue

        count = 0
        for ni, nj in neighbors(i, j):
            if skeleton[ni, nj]:
                count += 1

        # node criteria:
        # endpoint (1 neighbor) or junction (>2)
        if count == 1 or count > 2:
            nodes.append((i, j))

nodes = np.array(nodes)

print("✓ nodes:", len(nodes))

# ============================================================
# EDGE DETECTION (simple tracing)
# ============================================================

visited = np.zeros_like(skeleton, dtype=bool)
edges = []

for node in nodes:
    i, j = node

    for ni, nj in neighbors(i, j):

        if not skeleton[ni, nj]:
            continue
        if visited[ni, nj]:
            continue

        path = [(i, j)]
        ci, cj = ni, nj

        while True:
            path.append((ci, cj))
            visited[ci, cj] = True

            next_pts = []
            for xi, xj in neighbors(ci, cj):
                if skeleton[xi, xj] and not visited[xi, xj]:
                    next_pts.append((xi, xj))

            if len(next_pts) == 0:
                break

            if len(next_pts) > 1:
                break

            ci, cj = next_pts[0]

        if len(path) > 5:
            edges.append(path)

print("✓ edges:", len(edges))

# ============================================================
# GRID
# ============================================================

x = np.linspace(6, 17, nx)
y = np.linspace(22, 31, ny)

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(10, 7))

# skeleton background
plt.imshow(
    skeleton,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin="lower",
    cmap="gray",
    alpha=0.2
)

# edges
for edge in edges:
    pts = np.array(edge)
    plt.plot(x[pts[:,1]], y[pts[:,0]], color="cyan", linewidth=1.5)

# nodes
if len(nodes) > 0:
    nodes_arr = np.array(nodes)
    plt.scatter(
        x[nodes_arr[:,1]],
        y[nodes_arr[:,0]],
        color="red",
        s=20,
        label="nodes"
    )

plt.title("NEXAH V8.8 — Decision Graph")
plt.legend()

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v8_8_graph.png"), dpi=150)
plt.close()

# ============================================================
# SAVE
# ============================================================

np.save(os.path.join(OUTDIR, "nodes.npy"), nodes)
np.save(os.path.join(OUTDIR, "edges.npy"), np.array(edges, dtype=object))

print("✓ V8.8 done →", OUTDIR)
