import networkx as nx
from FRAMEWORK.MESO.attractor_detection import detect_attractors


def compute_attractor_basins(regime_map):
    """
    Compute the basin of attraction for each attractor.

    Returns a dictionary:

    {
        attractor_state : [states that flow to it]
    }
    """

    graph = regime_map["graph"]

    attractor_data = detect_attractors(regime_map)

    attractors = attractor_data["terminal_states"]

    reversed_graph = graph.reverse()

    basins = {}

    for attractor in attractors:

        reachable = nx.single_source_shortest_path_length(
            reversed_graph,
            attractor
        )

        basins[attractor] = list(reachable.keys())

    return basins
