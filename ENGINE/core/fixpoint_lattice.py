from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, Set, TypeVar

from ENGINE.core.poset import FinitePoset
from ENGINE.core.lattice import LatticeOps

T = TypeVar("T")


def build_fixpoint_poset(poset: FinitePoset[T], f: Callable[[T], T]) -> FinitePoset[T]:
    """
    Build induced poset of fixpoints Fix(f) = { x in P | f(x)=x }.
    Empty fixpoint set is allowed (degenerate poset).
    """
    fps: Set[T] = {x for x in poset.elements if f(x) == x}

    def leq_fp(x: T, y: T) -> bool:
        return poset.is_leq(x, y)

    return FinitePoset(elements=fps, leq=leq_fp)


@dataclass(frozen=True)
class FixpointLatticeStructure(Generic[T]):
    """
    Convenience structure expected by tests:
      - .poset: the fixpoint poset
      - .lattice: lattice utilities over the fixpoint poset
      - .is_lattice(): convenience delegate
    """

    poset: FinitePoset[T]
    lattice: LatticeOps[T]

    def is_lattice(self) -> bool:
        return self.lattice.is_lattice()
