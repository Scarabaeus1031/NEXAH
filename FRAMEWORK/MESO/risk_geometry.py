import networkx as nx


def compute_risk_distance(graph, risk_target):
    """
    Compute distance of every node to the collapse state.

    This produces the MESO risk geometry:
    distance_to_collapse
    """

    reversed_graph = graph.reverse()

    distances = nx.single_source_shortest_path_length(
        reversed_graph,
        risk_target
    )

    return distances


def compute_risk_gradient(distances):
    """
    Convert risk distance into normalized gradient.

    Higher value = safer state
    Lower value = higher collapse risk
    """

    if not distances:
        return {}

    max_distance = max(distances.values())

    gradient = {}

    for node, distance in distances.items():

        gradient[node] = distance / max_distance

    return gradient


def compute_risk_geometry(regime_map):
    """
    Full MESO pipeline.

    Produces risk distance and gradient over the regime graph.
    """

    graph = regime_map["graph"]
    collapse_states = regime_map["collapse_states"]

    collapse = list(collapse_states)[0]

    distances = compute_risk_distance(graph, collapse)

    gradient = compute_risk_gradient(distances)

    return {
        "risk_distance": distances,
        "risk_gradient": gradient
    }
