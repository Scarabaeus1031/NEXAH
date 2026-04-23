"""
NEXAH Architecture DNA Extractor

Extracts common structural patterns from high-resilience
network architectures.

Idea:
If several architectures repeatedly produce high resilience,
they likely share a structural "DNA".

Features extracted:

- nodes
- edges
- degree
- density
- clustering
- strongly connected core size
"""

import os
import json
import statistics
import networkx as nx

RESULT_DIR = "results"
RESILIENCE_THRESHOLD = 0.8


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

    degree = edges / nodes if nodes else 0
    density = nx.density(G)

    try:
        clustering = nx.average_clustering(G.to_undirected())
    except Exception:
        clustering = 0

    scc = nx.number_strongly_connected_components(G)

    return {
        "nodes": nodes,
        "edges": edges,
        "degree": degree,
        "density": density,
        "clustering": clustering,
        "scc": scc
    }


def extract_dna(graphs):

    high = []

    for G, res in graphs:

        if res >= RESILIENCE_THRESHOLD:

            topo = analyze_graph(G)
            topo["resilience"] = res

            high.append(topo)

    if not high:
        return None

    dna = {
        "nodes": statistics.mean([g["nodes"] for g in high]),
        "edges": statistics.mean([g["edges"] for g in high]),
        "degree": statistics.mean([g["degree"] for g in high]),
        "density": statistics.mean([g["density"] for g in high]),
        "clustering": statistics.mean([g["clustering"] for g in high]),
        "scc": statistics.mean([g["scc"] for g in high]),
        "resilience": statistics.mean([g["resilience"] for g in high])
    }

    return dna


def run():

    print("\nNEXAH Architecture DNA Extractor")
    print("--------------------------------")

    graphs = load_graphs()

    if len(graphs) < 3:
        print("Not enough data.")
        return

    dna = extract_dna(graphs)

    if dna is None:
        print("No high-resilience architectures found.")
        return

    print("\nExtracted Architecture DNA")
    print("---------------------------")

    for k, v in dna.items():
        print(f"{k:12s} ≈ {round(v,3)}")


if __name__ == "__main__":
    run()
