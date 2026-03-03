"""
NEXAH Engine – Worklist Fixpoint Solver (finite)

Computes least fixpoint over a directed graph using:
- a join-semilattice (via LatticeOps)
- transfer functions (monotone in typical use)
- classic worklist propagation

Typical use: abstract interpretation / dataflow analysis.

We assume:
- finite set of nodes
- finite lattice carrier (FinitePoset.elements must be hashable)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Generic, Iterable, List, Tuple, TypeVar
from collections import deque
from collections.abc import Hashable

from ENGINE.core.poset import FinitePoset
from ENGINE.core.lattice import LatticeOps


# ---------------------------------------------------------
# Type variables
# ---------------------------------------------------------

N = TypeVar("N", bound=Hashable)  # node type
V = TypeVar("V", bound=Hashable)  # lattice value type


# ---------------------------------------------------------
# Result container
# ---------------------------------------------------------

@dataclass(frozen=True)
class WorklistResult(Generic[N, V]):
    values: Dict[N, V]
    iterations: int
    pops: int


# ---------------------------------------------------------
# Internal helper
# ---------------------------------------------------------

def _require_in_carrier(value: V, carrier: Iterable[V], *, where: str) -> None:
    """
    Strict carrier check:
    - same type
    - same value
    - no equality-only matches across different types
    """
    for e in carrier:
        if type(value) is type(e) and value == e:
            return
    raise ValueError(f"{where}: value not in lattice carrier: {value!r}")


# ---------------------------------------------------------
# Main solver
# ---------------------------------------------------------

def solve_worklist(
    nodes: Iterable[N],
    edges: Iterable[Tuple[N, N]],
    value_poset: FinitePoset[V],
    initial: Dict[N, V],
    transfer: Callable[[N, V], V],
    strict: bool = True,
    max_pops: int = 100_000,
) -> WorklistResult[N, V]:
    """
    Least fixpoint solver.

    For each edge u -> v:
        new_v = join(old_v, transfer(v, old_u))

    - value_poset: lattice carrier for values
    - initial: initial state (must provide each node)
    - transfer: node-local transformer
    - strict: require value_poset to be a lattice
    """

    nodes_list: List[N] = list(nodes)
    node_set = set(nodes_list)

    # -----------------------------------------------------
    # Build successor map
    # -----------------------------------------------------

    succ: Dict[N, List[N]] = {n: [] for n in node_set}

    for u, v in edges:
        if u not in node_set or v not in node_set:
            raise ValueError("Edges refer to nodes not in `nodes`.")
        succ[u].append(v)

    # -----------------------------------------------------
    # Lattice validation
    # -----------------------------------------------------

    lat = LatticeOps(value_poset)

    if strict and not lat.is_lattice():
        raise ValueError("value_poset must be a lattice (strict=True).")

    # -----------------------------------------------------
    # Validate initial mapping
    # -----------------------------------------------------

    carrier = value_poset.elements

    for n in node_set:
        if n not in initial:
            raise ValueError(f"Missing initial value for node {n!r}.")
        _require_in_carrier(initial[n], carrier, where=f"initial[{n!r}]")

    values: Dict[N, V] = dict(initial)

    # -----------------------------------------------------
    # Worklist algorithm (FIFO via deque)
    # -----------------------------------------------------

    worklist = deque(nodes_list)
    pops = 0
    iters = 0

    while worklist:
        pops += 1

        if pops > max_pops:
            raise RuntimeError(
                f"Worklist exceeded max_pops={max_pops}. "
                "Possible non-termination or exploding state space."
            )

        u = worklist.popleft()
        iters += 1

        u_val = values[u]

        for v in succ[u]:
            cand = transfer(v, u_val)

            # Validate transfer result BEFORE lattice ops
            _require_in_carrier(cand, carrier, where="transfer(...)")

            new_v = lat.join(values[v], cand)

            if new_v != values[v]:
                values[v] = new_v
                if v not in worklist:
                    worklist.append(v)

    return WorklistResult(values=values, iterations=iters, pops=pops)    """
    Least fixpoint solver.

    For each edge u -> v:
        new_v = join(old_v, transfer(v, old_u))

    - value_poset: lattice carrier for values
    - initial: initial state (must provide each node)
    - transfer: node-local transformer
    - strict: require value_poset to be a lattice
    """

    nodes_list: List[N] = list(nodes)
    node_set = set(nodes_list)

    # -----------------------------------------------------
    # Build successor map
    # -----------------------------------------------------

    succ: Dict[N, List[N]] = {n: [] for n in node_set}

    for u, v in edges:
        if u not in node_set or v not in node_set:
            raise ValueError("Edges refer to nodes not in `nodes`.")
        succ[u].append(v)

    # -----------------------------------------------------
    # Lattice validation
    # -----------------------------------------------------

    lat = LatticeOps(value_poset)

    if strict and not lat.is_lattice():
        raise ValueError("value_poset must be a lattice (strict=True).")

    # -----------------------------------------------------
    # Validate initial mapping
    # -----------------------------------------------------

    carrier = value_poset.elements

    for n in node_set:
        if n not in initial:
            raise ValueError(f"Missing initial value for node {n!r}.")
        _require_in_carrier(initial[n], carrier, where=f"initial[{n!r}]")

    values: Dict[N, V] = dict(initial)

    # -----------------------------------------------------
    # Worklist algorithm
    # -----------------------------------------------------

    worklist: List[N] = list(nodes_list)
    pops = 0
    iters = 0

    while worklist:
        pops += 1

        if pops > max_pops:
            raise RuntimeError(
                f"Worklist exceeded max_pops={max_pops}. "
                "Possible non-termination or exploding state space."
            )

        u = worklist.pop(0)  # FIFO
        iters += 1

        u_val = values[u]

        for v in succ[u]:
            cand = transfer(v, u_val)

            # Validate transfer result BEFORE lattice ops
            _require_in_carrier(cand, carrier, where="transfer(...)")

            new_v = lat.join(values[v], cand)

            if new_v != values[v]:
                values[v] = new_v
                if v not in worklist:
                    worklist.append(v)

    return WorklistResult(values=values, iterations=iters, pops=pops)
