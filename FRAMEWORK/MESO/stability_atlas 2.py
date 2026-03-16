import networkx as nx
from FRAMEWORK.MESO.collapse_basin import compute_collapse_basin


def compute_stability_atlas(regime_map, risk_geometry):
    """
    Build a global stability atlas of the system.

    The atlas combines:

    - collapse basin
    - safe states
    - risk gradient
    - risk distance

    Returns a structured map of system stability.
    """

    graph = regime_map["graph"]
    collapse_states = regime_map.get("collapse_states", set())

    risk_distance = risk_geometry["risk_distance"]
    risk_gradient = risk_geometry["risk_gradient"]

    # compute collapse basin
    basin = compute_collapse_basin(regime_map)

    safe_states = []
    basin_states = []
    collapse = []

    for node in graph.nodes():

        if node in collapse_states:
            collapse.append(node)

        elif node in basin:
            basin_states.append(node)

        else:
            safe_states.append(node)

    atlas = {

        "safe_states": safe_states,

        "collapse_basin": basin_states,

        "collapse_states": collapse,

        "risk_distance": risk_distance,

        "risk_gradient": risk_gradient,

        "system_size": len(graph.nodes())

    }

    return atlas
