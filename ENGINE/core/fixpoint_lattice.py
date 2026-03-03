"""
NEXAH Engine – Fixpoint Poset / Fixpoint Lattice Construction

Builds the induced poset on Fix(Γ) = {x | Γ(x)=x} and exposes lattice utilities
on that induced structure.

Note:
- We do NOT assume completeness.
- Lattice properties can be tested via LatticeOps on the induced poset.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Set

from ENGINE.core.poset import FinitePoset


@dataclass(frozen=True)
class FixpointStructure:
    """
    Container for the induced structure on fixpoints of a closure operator.
    """
    poset: FinitePoset
    lattice: Any  # Avoid top-level LatticeOps import (prevents circular import)


def build_fixpoint_poset(
    base_poset: FinitePoset,
    operator: Callable[[Any], Any],
) -> FinitePoset:
    """
    Returns the induced poset on fixpoints Fix(Γ), with the inherited order ≤.
    """
    fps: Set[Any] = {
        x for x in base_poset.elements
        if operator(x) == x
    }

    def leq_fp(x: Any, y: Any) -> bool:
        return base_poset.is_leq(x, y)

    return FinitePoset(elements=fps, leq=leq_fp)


def build_fixpoint_structure(
    base_poset: FinitePoset,
    operator: Callable[[Any], Any],
) -> FixpointStructure:
    """
    Convenience: returns FixpointStructure(poset, latticeOps).
    """
    # LAZY IMPORT to avoid circular dependency
    from ENGINE.core.lattice import LatticeOps

    fp_poset = build_fixpoint_poset(base_poset, operator)

    return FixpointStructure(
        poset=fp_poset,
        lattice=LatticeOps(fp_poset),
    )
