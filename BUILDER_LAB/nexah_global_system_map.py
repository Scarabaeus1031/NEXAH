# ==========================================================
# NEXAH GLOBAL SYSTEM MAP
# Visualize global system interdependencies
# ==========================================================

import os
import json
import networkx as nx
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MAP_FILE = os.path.join(BASE_DIR, "global_systems", "global_system_map.json")

with open(MAP_FILE) as f:
    data = json.load(f)

systems = data["systems"]
couplings = data["couplings"]

G = nx.DiGraph()

for s in systems:
    G.add_node(s)

for src, tgt in couplings:
    G.add_edge(src, tgt)

plt.figure(figsize=(10,8))

pos = nx.spring_layout(G, seed=42)

nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=3000,
    node_color="lightblue",
    arrows=True
)

plt.title("NEXAH Global System Network")

plt.show()
