from __future__ import annotations

from typing import TypeVar, Generic, Callable, Set, Iterable

T = TypeVar("T")


class FinitePoset(Generic[T]):

    def __init__(
        self,
        elements: Iterable[T],
        leq: Callable[[T, T], bool],
    ) -> None:
        self.elements: Set[T] = set(elements)
        self.leq: Callable[[T, T], bool] = leq
        self._validate_partial_order()

    # -------------------------
    # Public API
    # -------------------------

    def is_leq(self, x: T, y: T) -> bool:
        return self.leq(x, y)

    def minimal_elements(self) -> Set[T]:
        return {
            x for x in self.elements
            if not any(
                self.is_leq(y, x) and y != x
                for y in self.elements
            )
        }

    def maximal_elements(self) -> Set[T]:
        return {
            x for x in self.elements
            if not any(
                self.is_leq(x, y) and y != x
                for y in self.elements
            )
        }

    # -------------------------
    # Validation
    # -------------------------

    def _validate_partial_order(self) -> None:
        self._check_reflexive()
        self._check_antisymmetric()
        self._check_transitive()

    def _check_reflexive(self) -> None:
        for x in self.elements:
            if not self.is_leq(x, x):
                raise ValueError("Relation is not reflexive.")

    def _check_antisymmetric(self) -> None:
        for x in self.elements:
            for y in self.elements:
                if (
                    self.is_leq(x, y)
                    and self.is_leq(y, x)
                    and x != y
                ):
                    raise ValueError("Relation is not antisymmetric.")

    def _check_transitive(self) -> None:
        for x in self.elements:
            for y in self.elements:
                for z in self.elements:
                    if (
                        self.is_leq(x, y)
                        and self.is_leq(y, z)
                        and not self.is_leq(x, z)
                    ):
                        raise ValueError("Relation is not transitive.")
