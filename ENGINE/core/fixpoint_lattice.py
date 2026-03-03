from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, Set, TypeVar

from ENGINE.core.poset import FinitePoset
from ENGINE.core.lattice import LatticeOps

T = TypeVar("T")


# -------------------------------------------------
# Build Fixpoint Poset
# -------------------------------------------------

def build_fixpoint_poset(
    poset: FinitePoset[T],
    f: Callable[[T], T],
) -> FinitePoset[T]:
    """
    Build induced poset of fixpoints Fix(f) = { x in P | f(x)=x }.
    """
    fps: Set[T] = {x for x in poset.elements if f(x) == x}

    def leq_fp(x: T, y: T) -> bool:
        return poset.is_leq(x, y)

    return FinitePoset(elements=fps, leq=leq_fp)


# -------------------------------------------------
# Structure expected by tests
# -------------------------------------------------

@dataclass(frozen=True)
class FixpointLatticeStructure(Generic[T]):
    poset: FinitePoset[T]
    lattice: LatticeOps[T]

    def is_lattice(self) -> bool:
        return self.lattice.is_lattice()


# -------------------------------------------------
# Legacy compatibility function (tests expect this)
# -------------------------------------------------

def build_fixpoint_structure(
    poset: FinitePoset[T],
    f: Callable[[T], T],
) -> FixpointLatticeStructure[T]:
    """
    Backward-compatible builder used by tests.
    """
    fp_poset = build_fixpoint_poset(poset, f)
    lat = LatticeOps(fp_poset)
    return FixpointLatticeStructure(poset=fp_poset, lattice=lat)
