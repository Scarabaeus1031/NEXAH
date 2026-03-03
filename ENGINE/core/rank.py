"""
NEXAH Engine — Rank / Height utilities for finite posets.

Height(x) = length of longest chain from a minimal element to x.
"""

from __future__ import annotations

from typing import Dict, Any

from ENGINE.core.poset import FinitePoset


class RankStructure:
    def __init__(self, poset: FinitePoset):
        self.poset = poset
        self._cache: Dict[Any, int] = {}

    # -----------------
    # Public API
    # -----------------

    def height(self, x: Any) -> int:
        if x not in self.poset.elements:
            raise ValueError(f"{x!r} not in poset.")

        return self._height_recursive(x)

    def rank(self, x: Any) -> int:
        return self.height(x)

    def max_height(self) -> int:
        return max(self.height(x) for x in self.poset.elements)

    # -----------------
    # Internal
    # -----------------

    def _height_recursive(self, x: Any) -> int:
        if x in self._cache:
            return self._cache[x]

        # predecessors strictly below x
        preds = [
            y for y in self.poset.elements
            if y != x and self.poset.is_leq(y, x)
        ]

        if not preds:
            self._cache[x] = 0
            return 0

        value = 1 + max(self._height_recursive(p) for p in preds)
        self._cache[x] = value
        return value
