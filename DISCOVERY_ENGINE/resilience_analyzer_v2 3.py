"""
NEXAH Resilience Analyzer v2

Improved resilience scoring based on structural properties
of the system graph.
"""

import networkx as nx


def compute_resilience_score(graph):
    """
    Compute structural resilience score based on
    graph topology metrics.
    """

    if graph.number_of_nodes() == 0:
        return 0.0

    n = graph.number_of_nodes()
    e = graph.number_of_edges()

    # -------------------------
    # Connectivity
    # -------------------------

    try:
        connectivity = nx.node_connectivity(graph)
    except:
        connectivity = 0

    connectivity_score = connectivity / max(1, n)

    # -------------------------
    # Path redundancy
    # -------------------------

    try:
        avg_clustering = nx.average_clustering(graph.to_undirected())
    except:
        avg_clustering = 0

    redundancy_score = avg_clustering

    # -------------------------
    # Cycle structure
    # -------------------------

    try:
        cycles = len(list(nx.simple_cycles(graph)))
    except:
        cycles = 0

    cycle_score = min(1.0, cycles / max(1, n))

    # -------------------------
    # Diameter penalty
    # -------------------------

    try:
        diameter = nx.diameter(graph.to_undirected())
        diameter_penalty = diameter / max(1, n)
    except:
        diameter_penalty = 0.5

    # -------------------------
    # Combine metrics
    # -------------------------

    score = (
        0.35 * connectivity_score +
        0.30 * redundancy_score +
        0.25 * cycle_score +
        0.10 * (1 - diameter_penalty)
    )

    score = max(0.0, min(1.0, score))

    return score


def analyze_resilience(graph):
    """
    Return resilience report compatible with NEXAH engine.
    """

    resilience_score = compute_resilience_score(graph)

    report = {
        "resilience_score": round(resilience_score, 3),
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges()
    }

    return report
