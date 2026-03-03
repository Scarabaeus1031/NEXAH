"""
NEXAH Engine – Core Layer
Lattice utilities built on top of FinitePoset.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Optional, Set

from ENGINE.core.poset import FinitePoset


@dataclass(frozen=True)
class LatticeOps:
    """
    Utility wrapper: provides lattice operations for a given FinitePoset.
    """

    poset: FinitePoset

    # -----------------------------
    # Bounds
    # -----------------------------

    def upper_bounds(self, subset: Iterable[Any]) -> Set[Any]:
        S = set(subset)
        if not S:
            raise ValueError("upper_bounds() needs a non-empty subset.")
        return {
            u for u in self.poset.elements
            if all(self.poset.is_leq(x, u) for x in S)
        }

    def lower_bounds(self, subset: Iterable[Any]) -> Set[Any]:
        S = set(subset)
        if not S:
            raise ValueError("lower_bounds() needs a non-empty subset.")
        return {
            l for l in self.poset.elements
            if all(self.poset.is_leq(l, x) for x in S)
        }

    # -----------------------------
    # Extremal elements
    # -----------------------------

    def minimal_in(self, subset: Iterable[Any]) -> Set[Any]:
        A = set(subset)
        return {
            x for x in A
            if not any(self.poset.is_leq(y, x) and y != x for y in A)
        }

    def maximal_in(self, subset: Iterable[Any]) -> Set[Any]:
        A = set(subset)
        return {
            x for x in A
            if not any(self.poset.is_leq(x, y) and y != x for y in A)
        }

    # -----------------------------
    # Join / Meet
    # -----------------------------

    def join(self, a: Any, b: Any) -> Any:
        U = self.upper_bounds({a, b})
        mins = self.minimal_in(U)
        if len(mins) != 1:
            raise ValueError(
                f"join({a},{b}) not unique / does not exist. Candidates={mins}"
            )
        return next(iter(mins))

    def meet(self, a: Any, b: Any) -> Any:
        L = self.lower_bounds({a, b})
        maxs = self.maximal_in(L)
        if len(maxs) != 1:
            raise ValueError(
                f"meet({a},{b}) not unique / does not exist. Candidates={maxs}"
            )
        return next(iter(maxs))

    # -----------------------------
    # Lattice checks
    # -----------------------------

    def is_lattice(self) -> bool:
        elems = list(self.poset.elements)
        for a in elems:
            for b in elems:
                try:
                    _ = self.join(a, b)
                    _ = self.meet(a, b)
                except ValueError:
                    return False
        return True

    # -----------------------------
    # Distributivity
    # -----------------------------

    def is_distributive(self) -> bool:
        elems = list(self.poset.elements)

        for a in elems:
            for b in elems:
                for c in elems:
                    try:
                        left = self.meet(a, self.join(b, c))
                        right = self.join(
                            self.meet(a, b),
                            self.meet(a, c)
                        )
                        if left != right:
                            return False
                    except ValueError:
                        return False

        return True

    # -----------------------------
    # Extremal elements
    # -----------------------------

    def top(self) -> Optional[Any]:
        mx = self.poset.maximal_elements()
        return next(iter(mx)) if len(mx) == 1 else None

    def bottom(self) -> Optional[Any]:
        mn = self.poset.minimal_elements()
        return next(iter(mn)) if len(mn) == 1 else None
