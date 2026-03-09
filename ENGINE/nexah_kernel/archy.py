ENGINE/nexah_kernel/archy.py

import networkx as nx

def build_structural_graph(architecture):
“””
Build the structural graph used by the NEXAH engine.

Accepts:
- architecture dict
- networkx graph
- architecture object
"""

# Case 1: architecture already contains graph
if isinstance(architecture, dict) and "graph" in architecture:
    return architecture["graph"]

# Case 2: architecture itself is a graph
if isinstance(architecture, nx.Graph) or isinstance(architecture, nx.DiGraph):
    return architecture

# Case 3: architecture object with nodes/edges
if hasattr(architecture, "nodes") and hasattr(architecture, "edges"):
    graph = nx.DiGraph()

    graph.add_nodes_from(architecture.nodes)
    graph.add_edges_from(architecture.edges)

    return graph

raise ValueError("Unsupported architecture format")
