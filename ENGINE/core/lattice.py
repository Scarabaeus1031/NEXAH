"""
NEXAH Engine – Core Layer
Lattice utilities built on top of FinitePoset.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Optional, Set, List

from ENGINE.core.poset import FinitePoset


@dataclass(frozen=True)
class LatticeOps:
    """
    Utility wrapper: provides lattice operations for a given FinitePoset.
    """

    poset: FinitePoset

    # -------------------------------------------------
    # Internal helpers
    # -------------------------------------------------

    def _safe_contains(self, x: Any) -> bool:
        """
        Safe membership test for poset.elements (a set).
        Returns False if x is unhashable.
        """
        try:
            return x in self.poset.elements
        except TypeError:
            return False

    def _require_in_carrier(self, x: Any, ctx: str = "value") -> None:
        """
        Raise ValueError if x is not a valid carrier element (incl. unhashable).
        """
        try:
            if x not in self.poset.elements:
                raise ValueError(f"{ctx} not in poset carrier: {x!r}")
        except TypeError:
            raise ValueError(f"{ctx} is unhashable and cannot be in poset carrier: {x!r}")

    # -------------------------------------------------
    # Bounds
    # -------------------------------------------------

    def upper_bounds(self, subset: Iterable[Any]) -> Set[Any]:
        """
        Returns {u in P | for all x in subset: x ≤ u}.
        Requires subset elements to be in the carrier.
        """
        S: List[Any] = list(subset)
        if not S:
            raise ValueError("upper_bounds() needs a non-empty subset.")

        for x in S:
            self._require_in_carrier(x, ctx="upper_bounds subset element")

        return {
            u for u in self.poset.elements
            if all(self.poset.is_leq(x, u) for x in S)
        }

    def lower_bounds(self, subset: Iterable[Any]) -> Set[Any]:
        """
        Returns {l in P | for all x in subset: l ≤ x}.
        Requires subset elements to be in the carrier.
        """
        S: List[Any] = list(subset)
        if not S:
            raise ValueError("lower_bounds() needs a non-empty subset.")

        for x in S:
            self._require_in_carrier(x, ctx="lower_bounds subset element")

        return {
            l for l in self.poset.elements
            if all(self.poset.is_leq(l, x) for x in S)
        }

    # -------------------------------------------------
    # Extremal elements in subset
    # -------------------------------------------------

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

    # -------------------------------------------------
    # Join / Meet
    # -------------------------------------------------

    def join(self, a: Any, b: Any) -> Any:
        # Guard early: avoid {a,b} crash if unhashable
        self._require_in_carrier(a, ctx="join arg a")
        self._require_in_carrier(b, ctx="join arg b")

        U = self.upper_bounds([a, b])
        mins = self.minimal_in(U)

        if len(mins) != 1:
            raise ValueError(
                f"join({a!r},{b!r}) not unique / does not exist. Candidates={mins}"
            )
        return next(iter(mins))

    def meet(self, a: Any, b: Any) -> Any:
        # Guard early: avoid {a,b} crash if unhashable
        self._require_in_carrier(a, ctx="meet arg a")
        self._require_in_carrier(b, ctx="meet arg b")

        L = self.lower_bounds([a, b])
        maxs = self.maximal_in(L)

        if len(maxs) != 1:
            raise ValueError(
                f"meet({a!r},{b!r}) not unique / does not exist. Candidates={maxs}"
            )
        return next(iter(maxs))

    # -------------------------------------------------
    # Lattice checks
    # -------------------------------------------------

    def is_lattice(self) -> bool:
        elems = list(self.poset.elements)
        for a in elems:
            for b in elems:
                try:
                    self.join(a, b)
                    self.meet(a, b)
                except ValueError:
                    return False
        return True

    # -------------------------------------------------
    # Full Distributivity Check
    # -------------------------------------------------

    def is_distributive(self) -> bool:
        """
        Full distributivity requires BOTH:

        1) a ∧ (b ∨ c) = (a ∧ b) ∨ (a ∧ c)
        2) a ∨ (b ∧ c) = (a ∨ b) ∧ (a ∨ c)
        """
        elems = list(self.poset.elements)

        for a in elems:
            for b in elems:
                for c in elems:
                    try:
                        left1 = self.meet(a, self.join(b, c))
                        right1 = self.join(self.meet(a, b), self.meet(a, c))
                        if left1 != right1:
                            return False

                        left2 = self.join(a, self.meet(b, c))
                        right2 = self.meet(self.join(a, b), self.join(a, c))
                        if left2 != right2:
                            return False

                    except ValueError:
                        return False

        return True

    # -------------------------------------------------
    # Extremal elements
    # -------------------------------------------------

    def top(self) -> Optional[Any]:
        mx = self.poset.maximal_elements()
        return next(iter(mx)) if len(mx) == 1 else None

    def bottom(self) -> Optional[Any]:
        mn = self.poset.minimal_elements()
        return next(iter(mn)) if len(mn) == 1 else None
