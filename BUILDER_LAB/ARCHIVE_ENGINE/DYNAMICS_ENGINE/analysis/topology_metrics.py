# DISCOVERY_ENGINE/nexah_dynamics_engine/analysis/topology_metrics.py

import numpy as np


# --------------------------------------------------
# NODE DEGREE ANALYSIS
# --------------------------------------------------

def compute_node_degrees(graph):
    return {node: len(neighbors) for node, neighbors in graph.items()}


def degree_distribution(degrees):
    values = list(degrees.values())
    unique, counts = np.unique(values, return_counts=True)
    return dict(zip(unique, counts))


# --------------------------------------------------
# GRAPH CENTRALITY
# --------------------------------------------------

def find_hubs(degrees, threshold=5):
    return [node for node, deg in degrees.items() if deg >= threshold]


# --------------------------------------------------
# MAIN API FUNCTION (USED BY PIPELINE)
# --------------------------------------------------

def compute_topology_metrics(graph):
    """
    Main metrics function used by pipeline
    """

    degrees = compute_node_degrees(graph)
    degree_dist = degree_distribution(degrees)
    hubs = find_hubs(degrees)

    metrics = {
        "num_nodes": len(graph),
        "num_edges": sum(len(v) for v in graph.values()) // 2,
        "degree_distribution": degree_dist,
        "num_hubs": len(hubs),
        "avg_degree": float(np.mean(list(degrees.values()))) if degrees else 0.0
    }

    return metrics


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":
    print("Topology Metrics Module Ready")
