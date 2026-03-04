from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, Iterable, List, Sequence, Tuple, TypeVar
from collections.abc import Hashable

from ENGINE.core.poset import FinitePoset
from ENGINE.core.hasse import HasseDiagram

T = TypeVar("T", bound=Hashable)


def _label(x: object) -> str:
    # DOT needs escaping for quotes/backslashes
    s = str(x)
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    return s


def export_hasse_to_dot(
    poset: FinitePoset[T],
    *,
    name: str = "Hasse",
    node_label: Callable[[T], str] | None = None,
) -> str:
    """
    Export the Hasse cover graph of a poset as Graphviz DOT.

    Renders edges x -> y where y covers x (x < y, no element in between).
    """
    lab = node_label or (lambda x: _label(x))
    hasse = HasseDiagram(poset)
    edges: List[Tuple[T, T]] = list(hasse.covers())  # type: ignore[attr-defined]

    lines: List[str] = []
    lines.append(f'digraph "{_label(name)}" {{')
    lines.append("  rankdir=BT;")  # bottom-to-top like classic Hasse

    # Nodes
    for x in sorted(poset.elements, key=lambda z: str(z)):
        lines.append(f'  "{lab(x)}";')

    # Edges
    for a, b in edges:
        lines.append(f'  "{lab(a)}" -> "{lab(b)}";')

    lines.append("}")
    return "\n".join(lines)


def export_cfg_to_dot(
    nodes: Iterable[Hashable],
    edges: Iterable[tuple[Hashable, Hashable]],
    *,
    name: str = "CFG",
) -> str:
    """
    Export a generic directed graph (e.g. CFG / worklist graph) as DOT.
    """
    node_list = list(nodes)
    edge_list = list(edges)

    lines: List[str] = []
    lines.append(f'digraph "{_label(name)}" {{')
    lines.append("  rankdir=LR;")  # left-to-right reads like flow

    for n in sorted(node_list, key=lambda z: str(z)):
        lines.append(f'  "{_label(n)}";')

    for u, v in edge_list:
        lines.append(f'  "{_label(u)}" -> "{_label(v)}";')

    lines.append("}")
    return "\n".join(lines)
