import networkx as nx


def detect_attractors(regime_map):
    """
    Detect attractors in the regime graph.

    An attractor is a strongly connected component (SCC)
    that has no outgoing edges to other components.

    Returns:
        {
            "attractors": [...],
            "terminal_states": [...],
            "cycles": [...]
        }
    """

    graph = regime_map["graph"]

    attractors = []
    terminal_states = []
    cycles = []

    # strongly connected components
    sccs = list(nx.strongly_connected_components(graph))

    for component in sccs:

        component = set(component)

        # check if component has outgoing edges
        outgoing = False

        for node in component:

            for successor in graph.successors(node):

                if successor not in component:
                    outgoing = True
                    break

            if outgoing:
                break

        # if no outgoing edges → attractor
        if not outgoing:

            attractors.append(component)

            if len(component) == 1:
                terminal_states.append(list(component)[0])
            else:
                cycles.append(list(component))

    result = {

        "attractors": attractors,
        "terminal_states": terminal_states,
        "cycles": cycles

    }

    return result
