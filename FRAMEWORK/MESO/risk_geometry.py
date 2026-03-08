import networkx as nx


def compute_risk_distance(graph, risk_target):
    """
    Compute distance of every node to the collapse state.
    """

    reversed_graph = graph.reverse()

    distances = nx.single_source_shortest_path_length(
        reversed_graph,
        risk_target
    )

    return distances


def compute_risk_gradient(distances):
    """
    Normalize distance into safety gradient.
    Higher value = safer
    """

    if not distances:
        return {}

    max_distance = max(distances.values())

    gradient = {}

    for node, distance in distances.items():

        if max_distance == 0:
            gradient[node] = 0
        else:
            gradient[node] = distance / max_distance

    return gradient


def compute_risk_geometry(regime_map):
    """
    Full MESO risk geometry pipeline.
    """

    graph = regime_map["graph"]
    collapse_states = regime_map["collapse_states"]

    # -----------------------------
    # SAFETY CHECK
    # -----------------------------

    if not collapse_states:

        raise ValueError(
            "No collapse states defined in regime_map. "
            "Check system.regimes for COLLAPSE states."
        )

    collapse = list(collapse_states)[0]

    distances = compute_risk_distance(graph, collapse)

    gradient = compute_risk_gradient(distances)

    return {
        "risk_distance": distances,
        "risk_gradient": gradient
    }
