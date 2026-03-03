"""
NEXAH Engine – Worklist Fixpoint Solver (finite)

Computes least fixpoint over a directed graph using:
- a join-semilattice (via LatticeOps)
- transfer functions (monotone in typical use)
- classic worklist propagation

Typical use: abstract interpretation / dataflow analysis.

We assume:
- finite set of nodes
- finite lattice carrier
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


def _in_carrier_hashsafe(value: Any, carrier: Iterable[Any]) -> bool:
    """
    Hash-safe membership test for carrier sets that may contain unhashable values
    or when `value` itself may be unhashable (e.g. `set`).

    We avoid: value in carrier_set  (would hash `value`)
    """
    for elem in carrier:
        if value == elem:
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
    """
    Least fixpoint solver.

    For each edge u -> v:
        new_v = join(old_v, transfer(v, old_u))

    - value_poset: lattice carrier for values
    - initial: initial state (must provide each node)
    - transfer: node-local transformer
    - strict: require value_poset to be a lattice
    """

    nodes_list = list(nodes)
    node_set = set(nodes_list)

    # -----------------------------------------------------
    # Build successor map
    # -----------------------------------------------------
    succ: Dict[Node, List[Node]] = {n: [] for n in node_set}
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
    # Validate initial mapping (hash-safe)
    # -----------------------------------------------------
    for n in node_set:
        if n not in initial:
            raise ValueError(f"Missing initial value for node {n!r}.")
        if not _in_carrier_hashsafe(initial[n], value_poset.elements):
            raise ValueError(
                f"Initial value for {n!r} not in lattice carrier: {initial[n]!r}"
            )

    values: Dict[Node, Value] = dict(initial)

    # -----------------------------------------------------
    # Worklist algorithm
    # -----------------------------------------------------
    worklist: List[Node] = list(nodes_list)
    pops = 0
    iters = 0

    while worklist:
        pops += 1
        if pops > max_pops:
            raise RuntimeError(
                f"Worklist exceeded max_pops={max_pops}. "
                "Possible non-termination or exploding state space."
            )

        u = worklist.pop(0)
        iters += 1

        u_val = values[u]

        for v in succ[u]:
            cand = transfer(v, u_val)

            # -------------------------------------------------
            # Validate transfer result BEFORE lattice ops
            # (hash-safe membership check)
            # -------------------------------------------------
            if not _in_carrier_hashsafe(cand, value_poset.elements):
                raise ValueError(
                    f"transfer produced value not in lattice carrier: {cand!r}"
                )

            # -------------------------------------------------
            # Lattice join
            # -------------------------------------------------
            new_v = lat.join(values[v], cand)

            if new_v != values[v]:
                values[v] = new_v
                if v not in worklist:
                    worklist.append(v)

    return WorklistResult(values=values, iterations=iters, pops=pops)
