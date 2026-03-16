from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, Set, TypeVar, Optional

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

    # ---- Delegations ----

    def is_lattice(self) -> bool:
        return self.lattice.is_lattice()

    def is_distributive(self) -> bool:
        return self.lattice.is_distributive()

    def top(self) -> Optional[T]:
        return self.lattice.top()

    def bottom(self) -> Optional[T]:
        return self.lattice.bottom()

    def join(self, x: T, y: T) -> T:
        return self.lattice.join(x, y)

    def meet(self, x: T, y: T) -> T:
        return self.lattice.meet(x, y)


# -------------------------------------------------
# Legacy compatibility function
# -------------------------------------------------

def build_fixpoint_structure(
    poset: FinitePoset[T],
    f: Callable[[T], T],
) -> FixpointLatticeStructure[T]:
    fp_poset = build_fixpoint_poset(poset, f)
    lat = LatticeOps(fp_poset)
    return FixpointLatticeStructure(poset=fp_poset, lattice=lat)
