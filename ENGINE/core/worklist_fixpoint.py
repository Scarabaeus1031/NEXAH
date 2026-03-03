"""
NEXAH Engine – Worklist Fixpoint Solver (Forward OUT Semantics)

We store OUT[u] in values[u].

Algorithm:

Initialize:
    values[u] = initial[u]

Loop:
    out_u = transfer(u, values[u])

    values[u] = join(values[u], out_u)

    For each successor v:
        values[v] = join(values[v], values[u])

Until stabilization.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Generic, Iterable, List, Tuple, TypeVar
from collections.abc import Hashable

from ENGINE.core.poset import FinitePoset
from ENGINE.core.lattice import LatticeOps


# ---------------------------------------------------------
# Type variables
# ---------------------------------------------------------

N = TypeVar("N", bound=Hashable)
V = TypeVar("V", bound=Hashable)


# ---------------------------------------------------------
# Result container
# ---------------------------------------------------------

@dataclass(frozen=True)
class WorklistResult(Generic[N, V]):
    values: Dict[N, V]
    iterations: int
    pops: int


# ---------------------------------------------------------
# Carrier validation
# ---------------------------------------------------------

def _require_in_carrier(value: V, carrier: Iterable[V], *, where: str) -> None:
    for e in carrier:
        if type(value) is type(e) and value == e:
            return
    raise ValueError(f"{where}: value not in lattice carrier: {value!r}")


# ---------------------------------------------------------
# Solver
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

    nodes_list: List[N] = list(nodes)
    node_set = set(nodes_list)

    # Successor map
    succ: Dict[N, List[N]] = {n: [] for n in node_set}
    for u, v in edges:
        if u not in node_set or v not in node_set:
            raise ValueError("Edges refer to nodes not in `nodes`.")
        succ[u].append(v)

    # Lattice validation
    lat = LatticeOps(value_poset)
    if strict and not lat.is_lattice():
        raise ValueError("value_poset must be a lattice (strict=True).")

    carrier = value_poset.elements

    # Validate initial values
    for n in node_set:
        if n not in initial:
            raise ValueError(f"Missing initial value for node {n!r}.")
        _require_in_carrier(initial[n], carrier, where=f"initial[{n!r}]")

    values: Dict[N, V] = dict(initial)

    worklist: List[N] = list(nodes_list)
    pops = 0
    iters = 0

    while worklist:
        pops += 1
        if pops > max_pops:
            raise RuntimeError("Worklist exceeded max_pops.")

        u = worklist.pop(0)
        iters += 1

        # Apply transfer
        out_u = transfer(u, values[u])
        _require_in_carrier(out_u, carrier, where="transfer(...)")

        # Self-update (OUT semantics)
        new_u = lat.join(values[u], out_u)
        if new_u != values[u]:
            values[u] = new_u
            for v in succ[u]:
                if v not in worklist:
                    worklist.append(v)

        # Propagate to successors
        for v in succ[u]:
            new_v = lat.join(values[v], values[u])
            if new_v != values[v]:
                values[v] = new_v
                if v not in worklist:
                    worklist.append(v)

    return WorklistResult(values=values, iterations=iters, pops=pops)
