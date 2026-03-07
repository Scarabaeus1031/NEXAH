import networkx as nx


class RegimeMap:
    """
    Structural representation of a NEXAH system.
    """

    def __init__(self, graph, regimes, collapse_states):
        self.graph = graph
        self.regimes = regimes
        self.collapse_states = collapse_states


def build_state_graph(system):
    """
    Build directed state graph from system definition.
    """

    G = nx.DiGraph()

    for node in system.nodes:
        G.add_node(node)

    for edge in system.edges:
        source, target = edge
        G.add_edge(source, target)

    return G


def detect_collapse_states(system):
    """
    Detect collapse states using risk_target.
    """

    return {system.risk_target}


def compute_basins(graph, collapse_states):
    """
    Compute basin of attraction for collapse states.
    """

    basins = {}

    reversed_graph = graph.reverse()

    for collapse in collapse_states:

        basin_nodes = nx.descendants(reversed_graph, collapse)
        basin_nodes.add(collapse)

        basins[collapse] = basin_nodes

    return basins


def map_regimes(system):
    """
    Full ARCHY regime mapping pipeline.
    """

    graph = build_state_graph(system)

    collapse_states = detect_collapse_states(system)

    basins = compute_basins(graph, collapse_states)

    return {
        "graph": graph,
        "collapse_states": collapse_states,
        "basins": basins,
        "regimes": system.regimes,
    }
