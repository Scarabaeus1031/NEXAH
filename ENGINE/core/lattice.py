from __future__ import annotations

from typing import Generic, Iterable, Optional, Set, TypeVar

from ENGINE.core.poset import FinitePoset

T = TypeVar("T")


class LatticeOps(Generic[T]):
    """
    Finite lattice utilities over a FinitePoset.
    """

    def __init__(self, poset: FinitePoset[T]) -> None:
        self.poset = poset

    # -------------------------------------------------
    # Bounds
    # -------------------------------------------------

    def upper_bounds(self, subset: Iterable[T]) -> Set[T]:
        return self.poset.upper_bounds(subset)

    def lower_bounds(self, subset: Iterable[T]) -> Set[T]:
        return self.poset.lower_bounds(subset)

    # -------------------------------------------------
    # Join / Meet
    # -------------------------------------------------

    def join(self, a: T, b: T) -> T:
        ubs = self.upper_bounds([a, b])
        mins = self._minimal(ubs)
        if len(mins) != 1:
            raise ValueError("Join not unique.")
        return next(iter(mins))

    def meet(self, a: T, b: T) -> T:
        lbs = self.lower_bounds([a, b])
        maxs = self._maximal(lbs)
        if len(maxs) != 1:
            raise ValueError("Meet not unique.")
        return next(iter(maxs))

    # -------------------------------------------------
    # Structure Checks
    # -------------------------------------------------

    def is_lattice(self) -> bool:
        for a in self.poset.elements:
            for b in self.poset.elements:
                try:
                    self.join(a, b)
                    self.meet(a, b)
                except ValueError:
                    return False
        return True

    def is_distributive(self) -> bool:
        for a in self.poset.elements:
            for b in self.poset.elements:
                for c in self.poset.elements:
                    left = self.meet(a, self.join(b, c))
                    right = self.join(self.meet(a, b), self.meet(a, c))
                    if left != right:
                        return False
        return True

    # -------------------------------------------------
    # Extremal Elements
    # -------------------------------------------------

    def top(self) -> Optional[T]:
        return self.poset.top()

    def bottom(self) -> Optional[T]:
        return self.poset.bottom()

    # -------------------------------------------------
    # Helpers
    # -------------------------------------------------

    def _minimal(self, subset: Iterable[T]) -> Set[T]:
        mins: Set[T] = set()
        for x in subset:
            is_min = True
            for y in subset:
                if x != y and self.poset.is_leq(y, x):
                    is_min = False
                    break
            if is_min:
                mins.add(x)
        return mins

    def _maximal(self, subset: Iterable[T]) -> Set[T]:
        maxs: Set[T] = set()
        for x in subset:
            is_max = True
            for y in subset:
                if x != y and self.poset.is_leq(x, y):
                    is_max = False
                    break
            if is_max:
                maxs.add(x)
        return maxs
