import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# --- Node → Cluster mapping (aus V12.6) ---
node_to_cluster = {
    0: 0, 1: 0, 7: 0, 10: 0,   # Cluster 0
    2: 1, 4: 1, 5: 1,          # Cluster 1 (CORE)
    3: 2, 8: 2,                # Cluster 2
    6: 3, 9: 3                 # Cluster 3
}

# --- Transition edges (aus V12) ---
edges = [
    (3, 4, 15),
    (5, 3, 12),
    (7, 8, 12),
    (4, 6, 9),
    (2, 1, 8),
    (8, 5, 8),
    (9, 10, 8),
    (10, 7, 8),
    (6, 9, 7),
    (0, 2, 6),
    (0, 10, 4),
    (1, 3, 4),
    (1, 5, 4),
    (2, 7, 4),
    (9, 0, 4),
    (10, 2, 4),
    (4, 0, 3),
    (6, 0, 3)
]

# --- Cluster Transition Aggregation ---
cluster_edges = {}

for src, dst, w in edges:
    c_src = node_to_cluster[src]
    c_dst = node_to_cluster[dst]

    key = (c_src, c_dst)
    cluster_edges[key] = cluster_edges.get(key, 0) + w

# --- Graph erstellen ---
G = nx.DiGraph()

for (c_src, c_dst), w in cluster_edges.items():
    G.add_edge(c_src, c_dst, weight=w)

# --- Layout ---
pos = nx.circular_layout(G)

# --- Plot ---
plt.figure(figsize=(6,6))

nx.draw_networkx_nodes(G, pos, node_size=1200, node_color='yellow', edgecolors='black')
nx.draw_networkx_labels(G, pos, labels={i: f"C{i}" for i in G.nodes}, font_size=12)

# Edges
edges_drawn = nx.draw_networkx_edges(
    G,
    pos,
    arrowstyle='->',
    arrowsize=20,
    width=[G[u][v]['weight']*0.2 for u,v in G.edges()]
)

# Edge Labels
edge_labels = {(u,v): G[u][v]['weight'] for u,v in G.edges()}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

plt.title("V12.7 Cluster Transition Graph")
plt.axis('off')

# --- Save ---
output_path = "FIELD_LAYER/outputs/plots/v12_7_cluster_transition_graph.png"
plt.savefig(output_path, dpi=150)
plt.close()

# --- Print Output ---
print("\nCluster → Cluster Transitions:")
for (c_src, c_dst), w in sorted(cluster_edges.items(), key=lambda x: -x[1]):
    print(f"  C{c_src} -> C{c_dst}: {w}")

print(f"\nSaved: {output_path}")
