from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, Iterable, Iterator, Optional, Set, TypeVar
from collections.abc import Hashable

T = TypeVar("T", bound=Hashable)


@dataclass(frozen=True)
class FinitePoset(Generic[T]):
    """
    Finite partially ordered set P = (elements, ≤)
    """

    elements: Set[T]
    leq: Callable[[T, T], bool]

    def __init__(self, elements: Iterable[T], leq: Callable[[T, T], bool]) -> None:
        object.__setattr__(self, "elements", set(elements))
        object.__setattr__(self, "leq", leq)
        self._validate_partial_order()

    # -------------------------------------------------
    # Core API
    # -------------------------------------------------

    def is_leq(self, x: T, y: T) -> bool:
        if x not in self.elements or y not in self.elements:
            raise ValueError("is_leq called with element(s) not in carrier.")
        return bool(self.leq(x, y))

    def __contains__(self, x: object) -> bool:
        return x in self.elements

    def __iter__(self) -> Iterator[T]:
        return iter(self.elements)

    # -------------------------------------------------
    # Validation
    # -------------------------------------------------

    def _validate_partial_order(self) -> None:
        # Empty poset allowed (degenerate case)
        if not self.elements:
            return
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

    # -------------------------------------------------
    # Iteration
    # -------------------------------------------------

    def iterate_until_fixpoint(self, f: Callable[[T], T], start: T) -> T:
        """
        Iterate f until a fixpoint is reached.
        Raises RuntimeError if cycle detected.
        """
        seen: Set[T] = set()
        current = start

        while True:
            if current in seen:
                raise RuntimeError("Iteration did not converge.")
            seen.add(current)

            nxt = f(current)
            if nxt == current:
                return current
            current = nxt

    # -------------------------------------------------
    # Extremal elements
    # -------------------------------------------------

    def minimal_elements(self) -> Set[T]:
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
        mins = self.minimal_elements()
        if len(mins) == 1:
            return next(iter(mins))
        return None

    def top(self) -> Optional[T]:
        maxs = self.maximal_elements()
        if len(maxs) == 1:
            return next(iter(maxs))
        return None

    # -------------------------------------------------
    # Bounds
    # -------------------------------------------------

    def upper_bounds(self, subset: Iterable[T]) -> Set[T]:
        subset_list = list(subset)
        if not subset_list:
            raise ValueError("Subset must be non-empty.")

        result: Set[T] = set()

        for candidate in self.elements:
            if all(self.is_leq(x, candidate) for x in subset_list):
                result.add(candidate)

        return result

    def lower_bounds(self, subset: Iterable[T]) -> Set[T]:
        subset_list = list(subset)
        if not subset_list:
            raise ValueError("Subset must be non-empty.")

        result: Set[T] = set()

        for candidate in self.elements:
            if all(self.is_leq(candidate, x) for x in subset_list):
                result.add(candidate)

        return result
