"""
NEXAH Engine – Worklist Fixpoint Solver (finite)

Forward dataflow with explicit IN/OUT semantics.

We maintain:
  IN[n]  : value entering node n
  OUT[n] : value leaving node n

Rules:
  OUT[n] = transfer(n, IN[n])
  IN[v]  = join(IN[v], OUT[u])   for each edge u -> v

Requires:
  - finite carrier (FinitePoset)
  - join via LatticeOps
  - strict carrier validation (type + equality)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Generic, Iterable, List, Tuple, TypeVar
from collections.abc import Hashable

from ENGINE.core.poset import FinitePoset
from ENGINE.core.lattice import LatticeOps


N = TypeVar("N", bound=Hashable)
V = TypeVar("V", bound=Hashable)


@dataclass(frozen=True)
class WorklistResult(Generic[N, V]):
    in_values: Dict[N, V]
    out_values: Dict[N, V]
    iterations: int
    pops: int


def _require_in_carrier(value: V, carrier: Iterable[V], *, where: str) -> None:
    for e in carrier:
        if type(value) is type(e) and value == e:
            return
    raise ValueError(f"{where}: value not in lattice carrier: {value!r}")


def solve_worklist(
    nodes: Iterable[N],
    edges: Iterable[Tuple[N, N]],
    value_poset: FinitePoset[V],
    initial_in: Dict[N, V],
    transfer: Callable[[N, V], V],
    strict: bool = True,
    max_pops: int = 100_000,
) -> WorklistResult[N, V]:

    nodes_list: List[N] = list(nodes)
    node_set = set(nodes_list)

    # Build successor map
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

    # Validate initial IN mapping
    for n in node_set:
        if n not in initial_in:
            raise ValueError(f"Missing initial value for node {n!r}.")
        _require_in_carrier(initial_in[n], carrier, where=f"initial_in[{n!r}]")

    in_values: Dict[N, V] = dict(initial_in)

    # Initialize OUT as transfer(IN) once (validated)
    out_values: Dict[N, V] = {}
    for n in node_set:
        out_n = transfer(n, in_values[n])
        _require_in_carrier(out_n, carrier, where="transfer(init)")
        out_values[n] = out_n

    worklist: List[N] = list(nodes_list)
    pops = 0
    iters = 0

    while worklist:
        pops += 1
        if pops > max_pops:
            raise RuntimeError("Worklist exceeded max_pops.")

        u = worklist.pop(0)
        iters += 1

        # Recompute OUT[u] from current IN[u]
        new_out_u = transfer(u, in_values[u])
        _require_in_carrier(new_out_u, carrier, where="transfer(...)")

        if new_out_u != out_values[u]:
            out_values[u] = new_out_u

        # Propagate OUT[u] to successors' IN
        for v in succ[u]:
            new_in_v = lat.join(in_values[v], out_values[u])
            if new_in_v != in_values[v]:
                in_values[v] = new_in_v
                if v not in worklist:
                    worklist.append(v)

    return WorklistResult(
        in_values=in_values,
        out_values=out_values,
        iterations=iters,
        pops=pops,
    )
