# ENGINE/core/poset.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, Iterable, Iterator, Optional, Set, TypeVar
from collections.abc import Hashable

T = TypeVar("T", bound=Hashable)


@dataclass(frozen=True)
class FinitePoset(Generic[T]):
    """
    Finite partially ordered set P = (elements, ≤).

    - elements must be finite + hashable (stored as a Python set)
    - leq must define a partial order on elements:
        reflexive, antisymmetric, transitive
    """

    elements: Set[T]
    leq: Callable[[T, T], bool]

    def __init__(self, elements: Iterable[T], leq: Callable[[T, T], bool]) -> None:
        object.__setattr__(self, "elements", set(elements))
        object.__setattr__(self, "leq", leq)
        self._validate_partial_order()

    # -------------------------
    # Core relation API
    # -------------------------

    def is_leq(self, x: T, y: T) -> bool:
        """Return True iff x ≤ y (only defined for x,y in carrier)."""
        if x not in self.elements or y not in self.elements:
            raise ValueError("is_leq called with element(s) not in carrier.")
        return bool(self.leq(x, y))

    def __contains__(self, x: object) -> bool:
        return x in self.elements

    def __iter__(self) -> Iterator[T]:
        return iter(self.elements)

    # -------------------------
    # Validation
    # -------------------------

    def _validate_partial_order(self) -> None:
        if not self.elements:
            raise ValueError("Poset carrier must be non-empty.")
        self._check_reflexive()
        self._check_antisymmetric()
        self._check_transitive()

    def _check_reflexive(self) -> None:
        for x in self.elements:
            if not self.leq(x, x):
                raise ValueError("Relation is not reflexive.")

    def _check_antisymmetric(self) -> None:
        for x in self.elements:
            for y in self.elements:
                if x != y and self.leq(x, y) and self.leq(y, x):
                    raise ValueError("Relation is not antisymmetric.")

    def _check_transitive(self) -> None:
        for x in self.elements:
            for y in self.elements:
                if not self.leq(x, y):
                    continue
                for z in self.elements:
                    if self.leq(y, z) and not self.leq(x, z):
                        raise ValueError("Relation is not transitive.")

    # -------------------------
    # Extremal elements
    # -------------------------

    def minimal_elements(self) -> Set[T]:
        """All minimal elements (no strictly smaller element exists)."""
        mins: Set[T] = set()
        for x in self.elements:
            has_smaller = False
            for y in self.elements:
                if y != x and self.leq(y, x) and not self.leq(x, y):
                    has_smaller = True
                    break
            if not has_smaller:
                mins.add(x)
        return mins

    def maximal_elements(self) -> Set[T]:
        """All maximal elements (no strictly larger element exists)."""
        maxs: Set[T] = set()
        for x in self.elements:
            has_larger = False
            for y in self.elements:
                if y != x and self.leq(x, y) and not self.leq(y, x):
                    has_larger = True
                    break
            if not has_larger:
                maxs.add(x)
        return maxs

    def bottom(self) -> Optional[T]:
        """Return a unique bottom element if it exists, else None."""
        mins = self.minimal_elements()
        if len(mins) == 1:
            return next(iter(mins))
        return None

    def top(self) -> Optional[T]:
        """Return a unique top element if it exists, else None."""
        maxs = self.maximal_elements()
        if len(maxs) == 1:
            return next(iter(maxs))
        return None

    # -------------------------
    # Bounds helpers (often used by lattice ops)
    # -------------------------

    def lower_bounds(self, subset: Iterable[T]) -> Set[T]:
        """{ b in P | b ≤ s for all s in subset }"""
        S = list(subset)
        for s in S:
            if s not in self.elements:
                raise ValueError("lower_bounds: subset contains element not in carrier.")

        lbs: Set[T] = set()
        for b in self.elements:
            ok = True
            for s in S:
                if not self.leq(b, s):
                    ok = False
                    break
            if ok:
                lbs.add(b)
        return lbs

    def upper_bounds(self, subset: Iterable[T]) -> Set[T]:
        """{ b in P | s ≤ b for all s in subset }"""
        S = list(subset)
        for s in S:
            if s not in self.elements:
                raise ValueError("upper_bounds: subset contains element not in carrier.")

        ubs: Set[T] = set()
        for b in self.elements:
            ok = True
            for s in S:
                if not self.leq(s, b):
                    ok = False
                    break
            if ok:
                ubs.add(b)
        return ubs
