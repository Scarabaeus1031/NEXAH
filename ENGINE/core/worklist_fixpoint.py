"""
NEXAH Engine – Worklist Fixpoint Solver (finite)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Hashable, Iterable, List, Tuple

from ENGINE.core.poset import FinitePoset
from ENGINE.core.lattice import LatticeOps


Node = Hashable
Value = Any
Transfer = Callable[[Node, Value], Value]


@dataclass(frozen=True)
class WorklistResult:
    values: Dict[Node, Value]
    iterations: int
    pops: int


def _in_carrier_strict(value: Any, carrier) -> bool:
    """
    Strict carrier membership:
    - same value
    - same type
    """
    for e in carrier:
        if value == e and type(value) is type(e):
            return True
    return False


def solve_worklist(
    nodes: Iterable[Node],
    edges: Iterable[Tuple[Node, Node]],
    value_poset: FinitePoset,
    initial: Dict[Node, Value],
    transfer: Transfer,
    strict: bool = True,
    max_pops: int = 100_000,
) -> WorklistResult:

    nodes_list = list(nodes)
    node_set = set(nodes_list)

    # -----------------------------------------------------
    # Build successor map
    # -----------------------------------------------------
    succ: Dict[Node, List[Node]] = {n: [] for n in node_set}
    for u, v in edges:
        if u not in node_set or v not in node_set:
            raise ValueError("Edges refer to unknown nodes.")
        succ[u].append(v)

    # -----------------------------------------------------
    # Lattice validation
    # -----------------------------------------------------
    lat = LatticeOps(value_poset)
    if strict and not lat.is_lattice():
        raise ValueError("value_poset must be a lattice (strict=True).")

    # -----------------------------------------------------
    # Validate initial values
    # -----------------------------------------------------
    for n in node_set:
        if n not in initial:
            raise ValueError(f"Missing initial value for node {n!r}.")
        if not _in_carrier_strict(initial[n], value_poset.elements):
            raise ValueError(
                f"Initial value for {n!r} not in lattice carrier: {initial[n]!r}"
            )

    values: Dict[Node, Value] = dict(initial)

    worklist: List[Node] = list(nodes_list)
    pops = 0
    iters = 0

    while worklist:
        pops += 1
        if pops > max_pops:
            raise RuntimeError("Worklist exceeded max_pops.")

        u = worklist.pop(0)
        iters += 1

        u_val = values[u]

        for v in succ[u]:
            cand = transfer(v, u_val)

            # 🔥 STRICT validation BEFORE join
            if not _in_carrier_strict(cand, value_poset.elements):
                raise ValueError(
                    f"transfer produced value not in lattice carrier: {cand!r}"
                )

            new_v = lat.join(values[v], cand)

            if new_v != values[v]:
                values[v] = new_v
                if v not in worklist:
                    worklist.append(v)

    return WorklistResult(values=values, iterations=iters, pops=pops)
