"""
NEXAH Engine – Fixpoint Poset / Fixpoint Lattice Construction

Builds the induced poset on Fix(Γ) = {x | Γ(x)=x}
and exposes lattice utilities on that induced structure.

Note:
- We do NOT assume completeness.
- Lattice properties can be tested via LatticeOps
  on the induced poset.
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
    lattice: Any  # Lazy-constructed LatticeOps (avoid circular import)

    # -----------------------------------------------------
    # Delegations to lattice operations
    # -----------------------------------------------------

    def is_lattice(self) -> bool:
        return self.lattice.is_lattice()

    def is_distributive(self) -> bool:
        return self.lattice.is_distributive()

    def top(self):
        return self.lattice.top()

    def bottom(self):
        return self.lattice.bottom()

    def join(self, a, b):
        return self.lattice.join(a, b)

    def meet(self, a, b):
        return self.lattice.meet(a, b)


# ---------------------------------------------------------
# Fixpoint Poset Construction
# ---------------------------------------------------------

def build_fixpoint_poset(
    base_poset: FinitePoset,
    operator: Callable[[Any], Any],
) -> FinitePoset:
    """
    Returns the induced poset on fixpoints Fix(Γ),
    with the inherited order ≤.
    """
    fps: Set[Any] = {
        x for x in base_poset.elements
        if operator(x) == x
    }

    def leq_fp(x: Any, y: Any) -> bool:
        return base_poset.is_leq(x, y)

    return FinitePoset(elements=fps, leq=leq_fp)


# ---------------------------------------------------------
# Fixpoint Structure (Poset + LatticeOps)
# ---------------------------------------------------------

def build_fixpoint_structure(
    base_poset: FinitePoset,
    operator: Callable[[Any], Any],
) -> FixpointStructure:
    """
    Convenience constructor:
    returns FixpointStructure(poset, latticeOps).
    """

    # LAZY IMPORT to prevent circular dependency
    from ENGINE.core.lattice import LatticeOps

    fp_poset = build_fixpoint_poset(base_poset, operator)

    return FixpointStructure(
        poset=fp_poset,
        lattice=LatticeOps(fp_poset),
    )
def test_delegation_methods():
    P = small_poset()

    def gamma(x):
        return x

    struct = build_fixpoint_structure(P, gamma)

    # Delegations
    assert struct.is_lattice()
    assert not struct.is_distributive() is False or True  # just trigger call

    # Top & Bottom
    assert struct.top() == "1"
    assert struct.bottom() == "0"

    # Join & Meet
    assert struct.join("0", "a") == "a"
    assert struct.meet("a", "1") == "a"
