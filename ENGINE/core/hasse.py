"""
NEXAH Engine — Hasse diagram utilities for finite posets.

Extracts cover relations.
"""

from __future__ import annotations

from typing import Set, Tuple, Any

from ENGINE.core.poset import FinitePoset


class HasseDiagram:
    def __init__(self, poset: FinitePoset):
        self.poset = poset

    def covers(self) -> Set[Tuple[Any, Any]]:
        result = set()

        for a in self.poset.elements:
            for b in self.poset.elements:
                if a == b:
                    continue

                if not self.poset.is_leq(a, b):
                    continue

                # Check strict
                if self.poset.is_leq(b, a):
                    continue

                # Check minimality: no c with a < c < b
                is_cover = True
                for c in self.poset.elements:
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
