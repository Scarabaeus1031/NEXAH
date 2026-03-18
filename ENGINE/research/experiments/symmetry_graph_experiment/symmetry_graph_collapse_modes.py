"""
Symmetry Graph Collapse Mode Analysis
-------------------------------------

Identifies which structural mechanism caused graph fragmentation.

Modes:
- HUB failure
- PENTAGON collapse
- HEXAGON collapse
"""

import networkx as nx
import random
from collections import Counter

from .symmetry_graph_3cycle import build_graph


# ---------------------------
# classify edge type
# ---------------------------

def edge_type(edge):

    a, b = edge

    if "center" in edge:
        return "hub"

    # node index
    ia = int(a[1:])
    ib = int(b[1:])

    if ia <= 4 and ib <= 4:
        return "pentagon"

    if 5 <= ia <= 10 and 5 <= ib <= 10:
        return "hexagon_A"

    if 11 <= ia <= 16 and 11 <= ib <= 16:
        return "hexagon_B"

    return "cross"


# ---------------------------
# simulation
# ---------------------------

def run_simulation():

    G = build_graph()

    removed_types = []

    edges = list(G.edges())
    random.shuffle(edges)

    for step, edge in enumerate(edges):

        removed_types.append(edge_type(edge))

        G.remove_edge(*edge)

        if nx.number_connected_components(G) > 1:

            return {
                "step": step + 1,
                "mode": most_common(removed_types)
            }

    return None


# ---------------------------
# helper
# ---------------------------

def most_common(lst):

    c = Counter(lst)
    return c.most_common(1)[0][0]


# ---------------------------
# experiment
# ---------------------------

def collapse_mode_experiment(runs=300):

    results = []

    for _ in range(runs):

        res = run_simulation()

        if res:
            results.append(res["mode"])

    return Counter(results)


# ---------------------------
# run
# ---------------------------

if __name__ == "__main__":

    print("\nRunning Collapse Mode Analysis...\n")

    modes = collapse_mode_experiment(300)

    print("Collapse Modes:\n")

    for mode, count in modes.items():
        print(mode, ":", count)
