"""
NEXAH Engine — Hasse diagram utilities for finite posets.

Extracts cover relations.
"""

from __future__ import annotations

from typing import Generic, Set, Tuple, TypeVar
from collections.abc import Hashable

from ENGINE.core.poset import FinitePoset

T = TypeVar("T", bound=Hashable)


class HasseDiagram(Generic[T]):
    def __init__(self, poset: FinitePoset[T]) -> None:
        self.poset: FinitePoset[T] = poset

    def covers(self) -> Set[Tuple[T, T]]:
        result: Set[Tuple[T, T]] = set()

        elems = list(self.poset.elements)

        for a in elems:
            for b in elems:
                if a == b:
                    continue

                if not self.poset.is_leq(a, b):
                    continue

                # Strict: a < b
                if self.poset.is_leq(b, a):
                    continue

                # Minimality: no c with a < c < b
                is_cover = True
                for c in elems:
                    if c == a or c == b:
                        continue

                    if (
                        self.poset.is_leq(a, c)
                        and self.poset.is_leq(c, b)
                        and not self.poset.is_leq(c, a)
                        and not self.poset.is_leq(b, c)
                    ):
                        is_cover = False
                        break

                if is_cover:
                    result.add((a, b))

        return result
