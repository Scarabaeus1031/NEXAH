from .models import StructuralGraph


def build_structural_graph(architecture):

    nodes = {}
    edges = []
    weights = {}

    for node in architecture.nodes:
        nodes[str(node)] = node

    for edge in architecture.edges:
        edges.append(edge)

    return StructuralGraph(
        nodes=nodes,
        edges=edges,
        weights=weights,
    )
