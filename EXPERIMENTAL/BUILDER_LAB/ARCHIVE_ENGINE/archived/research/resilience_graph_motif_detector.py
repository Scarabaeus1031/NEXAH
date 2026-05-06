"""
NEXAH Resilience Graph Motif Detector

Detects structural motifs in architecture graphs and compares them
to resilience values.

Motifs analyzed:

- triangles
- bidirectional edges
- simple directed cycles
- strongly connected core size
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


def count_triangles(G):

    UG = G.to_undirected()
    triangles = sum(nx.triangles(UG).values()) / 3
    return triangles


def count_bidirectional_edges(G):

    count = 0

    for u, v in G.edges():

        if G.has_edge(v, u):
            count += 1

    return count / 2


def count_cycles(G, limit=100):

    cycles = list(nx.simple_cycles(G))

    if len(cycles) > limit:
        return limit

    return len(cycles)


def largest_scc_size(G):

    scc = list(nx.strongly_connected_components(G))

    if not scc:
        return 0

    return max(len(c) for c in scc)


def analyze_graph(G):

    return {
        "triangles": count_triangles(G),
        "bidirectional": count_bidirectional_edges(G),
        "cycles": count_cycles(G),
        "largest_scc": largest_scc_size(G)
    }


def run():

    print("\nNEXAH Graph Motif Detector")
    print("--------------------------")

    graphs = load_graphs()

    if len(graphs) < 3:
        print("Not enough graphs.")
        return

    high = []
    low = []

    for G, res in graphs:

        motifs = analyze_graph(G)

        motifs["resilience"] = res

        if res > 0.8:
            high.append(motifs)
        else:
            low.append(motifs)

    def summarize(group):

        if not group:
            return None

        return {
            "triangles": statistics.mean([g["triangles"] for g in group]),
            "bidirectional": statistics.mean([g["bidirectional"] for g in group]),
            "cycles": statistics.mean([g["cycles"] for g in group]),
            "largest_scc": statistics.mean([g["largest_scc"] for g in group])
        }

    high_stats = summarize(high)
    low_stats = summarize(low)

    print("\nHigh Resilience Motifs")
    print("----------------------")

    if high_stats:
        for k, v in high_stats.items():
            print(f"{k:15s} ≈ {round(v,3)}")

    print("\nLow Resilience Motifs")
    print("---------------------")

    if low_stats:
        for k, v in low_stats.items():
            print(f"{k:15s} ≈ {round(v,3)}")


if __name__ == "__main__":

    run()
