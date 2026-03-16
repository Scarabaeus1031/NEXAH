from __future__ import annotations

from typing import Callable, Iterable, List, Tuple, TypeVar
from collections.abc import Hashable

from ENGINE.core.poset import FinitePoset
from ENGINE.core.hasse import HasseDiagram

T = TypeVar("T", bound=Hashable)


def _label(x: object) -> str:
    """
    Escape labels for DOT output.
    """
    s = str(x)
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    return s


# -----------------------------------------------------------
# Hasse Diagram Export
# -----------------------------------------------------------

def export_hasse_to_dot(
    poset: FinitePoset[T],
    *,
    name: str = "Hasse",
    node_label: Callable[[T], str] | None = None,
) -> str:
    """
    Export the Hasse cover graph of a poset as Graphviz DOT.

    Edges represent cover relations:
    x -> y where y covers x.
    """

    lab = node_label or (lambda x: _label(x))

    hasse = HasseDiagram(poset)
    edges: List[Tuple[T, T]] = list(hasse.covers())

    lines: List[str] = []

    lines.append(f'digraph "{_label(name)}" {{')
    lines.append("  rankdir=BT;")
    lines.append("  node [shape=ellipse];")

    # Nodes
    for x in sorted(poset.elements, key=lambda z: str(z)):
        lines.append(f'  "{lab(x)}";')

    # Edges
    for a, b in edges:
        lines.append(f'  "{lab(a)}" -> "{lab(b)}";')

    lines.append("}")

    return "\n".join(lines)


# -----------------------------------------------------------
# CFG / Generic Graph Export
# -----------------------------------------------------------

def export_cfg_to_dot(
    nodes: Iterable[Hashable],
    edges: Iterable[tuple[Hashable, Hashable]],
    *,
    name: str = "CFG",
) -> str:
    """
    Export a directed graph (CFG, dependency graph, etc.)
    to Graphviz DOT format.
    """

    node_list = list(nodes)
    edge_list = list(edges)

    lines: List[str] = []

    lines.append(f'digraph "{_label(name)}" {{')
    lines.append("  rankdir=TB;")
    lines.append("  node [shape=box];")

    # Nodes
    for n in sorted(node_list, key=lambda z: str(z)):
        lines.append(f'  "{_label(n)}";')

    # Edges
    for u, v in edge_list:
        lines.append(f'  "{_label(u)}" -> "{_label(v)}";')

    lines.append("}")

    return "\n".join(lines)


# -----------------------------------------------------------
# Generic Graph Export (fallback)
# -----------------------------------------------------------

def export_graph_to_dot(
    nodes: Iterable[Hashable],
    edges: Iterable[tuple[Hashable, Hashable]],
    *,
    name: str = "Graph",
) -> str:
    """
    Generic directed graph exporter.
    Useful for fixpoint graphs, dependency graphs,
    resonance graphs, etc.
    """

    node_list = list(nodes)
    edge_list = list(edges)

    lines: List[str] = []

    lines.append(f'digraph "{_label(name)}" {{')

    for n in node_list:
        lines.append(f'  "{_label(n)}";')

    for u, v in edge_list:
        lines.append(f'  "{_label(u)}" -> "{_label(v)}";')

    lines.append("}")

    return "\n".join(lines)
