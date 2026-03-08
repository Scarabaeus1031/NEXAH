import networkx as nx


def compute_risk_distance(graph, collapse_state):

    reversed_graph = graph.reverse()

    distances = nx.single_source_shortest_path_length(
        reversed_graph,
        collapse_state
    )

    return distances


def compute_risk_gradient(distances):

    if not distances:
        return {}

    max_distance = max(distances.values())

    gradient = {}

    for node, distance in distances.items():

        gradient[node] = distance / max_distance

    return gradient


def compute_collapse_basin(graph, collapse_state):

    basin = set()

    for node in graph.nodes:

        try:

            path = nx.shortest_path(graph, node, collapse_state)

            if path:
                basin.add(node)

        except nx.NetworkXNoPath:

            continue

    return basin


def compute_risk_geometry(regime_map):

    graph = regime_map["graph"]
    collapse_states = regime_map["collapse_states"]

    if not collapse_states:

        raise ValueError(
            "No collapse states defined in regime_map. "
            "Check system.regimes for COLLAPSE states."
        )

    collapse = list(collapse_states)[0]

    distances = compute_risk_distance(graph, collapse)

    gradient = compute_risk_gradient(distances)

    basin = compute_collapse_basin(graph, collapse)

    return {
        "risk_distance": distances,
        "risk_gradient": gradient,
        "collapse_basin": basin
    }
