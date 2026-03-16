"""
NEXAH Resilience Graph Topology Analyzer

Analyzes graph topology features of architectures and compares
them with measured resilience values.

Topology metrics computed:

- average degree
- clustering coefficient
- average shortest path length
- density
- number of strongly connected components

Goal:
identify structural patterns that correlate with high resilience.
"""

import os
import json
import networkx as nx
import statistics

RESULT_DIR = "results"


def load_graphs():

    graphs = []

    if not os.path.exists(RESULT_DIR):
        return graphs

    for f in os.listdir(RESULT_DIR):

        if not f.endswith(".json"):
            continue

        path = os.path.join(RESULT_DIR, f)

        try:
            with open(path) as file:
                r = json.load(file)

            if "nodes" not in r:
                continue

            nodes = r["nodes"]
            edges = r["edges"]
            resilience = r["resilience_score"]

            G = nx.gnm_random_graph(nodes, edges, directed=True)

            graphs.append((G, resilience))

        except Exception:
            continue

    return graphs


def analyze_graph(G):

    nodes = G.number_of_nodes()
    edges = G.number_of_edges()

    if nodes == 0:
        return None

    degree = edges / nodes
    density = nx.density(G)

    try:
        clustering = nx.average_clustering(G.to_undirected())
    except Exception:
        clustering = 0

    try:
        if nx.is_connected(G.to_undirected()):
            path_length = nx.average_shortest_path_length(G.to_undirected())
        else:
            path_length = None
    except Exception:
        path_length = None

    scc = nx.number_strongly_connected_components(G)

    return {
        "nodes": nodes,
        "edges": edges,
        "degree": degree,
        "density": density,
        "clustering": clustering,
        "path_length": path_length,
        "scc": scc
    }


def run():

    print("\nNEXAH Graph Topology Analyzer")
    print("-----------------------------")

    graphs = load_graphs()

    if len(graphs) < 3:
        print("Not enough graphs.")
        return

    high_resilience = []
    low_resilience = []

    for G, res in graphs:

        topo = analyze_graph(G)

        if topo is None:
            continue

        topo["resilience"] = res

        if res > 0.8:
            high_resilience.append(topo)
        else:
            low_resilience.append(topo)

    def summarize(group):

        if not group:
            return None

        return {
            "degree": statistics.mean([g["degree"] for g in group]),
            "density": statistics.mean([g["density"] for g in group]),
            "clustering": statistics.mean([g["clustering"] for g in group]),
            "scc": statistics.mean([g["scc"] for g in group])
        }

    high_stats = summarize(high_resilience)
    low_stats = summarize(low_resilience)

    print("\nHigh Resilience Architectures")
    print("-----------------------------")

    if high_stats:
        for k, v in high_stats.items():
            print(f"{k:12s} ≈ {round(v,3)}")

    print("\nLow Resilience Architectures")
    print("----------------------------")

    if low_stats:
        for k, v in low_stats.items():
            print(f"{k:12s} ≈ {round(v,3)}")


if __name__ == "__main__":
    run()
