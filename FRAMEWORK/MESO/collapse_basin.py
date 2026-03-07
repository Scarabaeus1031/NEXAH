import networkx as nx


def compute_collapse_basin(regime_map):
    """
    Compute the collapse basin of the system.

    The collapse basin contains all states from which
    collapse states are reachable.
    """

    graph = regime_map["graph"]
    collapse_states = regime_map["collapse_states"]

    reversed_graph = graph.reverse()

    basin = set()

    for collapse in collapse_states:

        reachable = nx.single_source_shortest_path_length(
            reversed_graph,
            collapse
        )

        basin.update(reachable.keys())

    return basin
