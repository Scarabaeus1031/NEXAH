"""
NEXAH Engine – Regime Operator Δ

Δ is a structural restriction operator over a finite poset.

Given:
    P = (elements, ≤)

Δ_φ(P) = induced sub-poset on elements satisfying predicate φ.

Δ does NOT guarantee:
    - closure properties
    - lattice preservation
    - completeness

It is purely a structural restriction.
"""

from __future__ import annotations

from typing import Callable, Generic, TypeVar
from collections.abc import Hashable

from ENGINE.core.poset import FinitePoset

T = TypeVar("T", bound=Hashable)


class RegimeOperator(Generic[T]):
    def __init__(self, poset: FinitePoset[T]) -> None:
        self.poset: FinitePoset[T] = poset

    def restrict(self, predicate: Callable[[T], bool]) -> FinitePoset[T]:
        """
        Returns induced sub-poset of elements satisfying predicate.

        Raises ValueError if restriction yields empty set.
        """

        new_elements = {
            x for x in self.poset.elements if predicate(x)
        }

        if not new_elements:
            raise ValueError("Δ restriction produced empty regime.")

        # Induced order
        def induced_leq(x: T, y: T) -> bool:
            return self.poset.is_leq(x, y)

        return FinitePoset(new_elements, induced_leq)
