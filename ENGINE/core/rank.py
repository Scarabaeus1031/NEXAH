"""
NEXAH Engine – Rank / Height utilities for finite posets
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Generic, TypeVar
from collections.abc import Hashable

from ENGINE.core.poset import FinitePoset

T = TypeVar("T", bound=Hashable)


@dataclass(frozen=True)
class RankStructure(Generic[T]):
    poset: FinitePoset[T]

    def rank_map(self) -> Dict[T, int]:
        elems = list(self.poset.elements)

        preds: Dict[T, list[T]] = {}
        for x in elems:
            px: list[T] = []
            for y in elems:
                if y == x:
                    continue
                if self.poset.is_leq(y, x) and not self.poset.is_leq(x, y):
                    px.append(y)
            preds[x] = px

        memo: Dict[T, int] = {}

        def r(x: T) -> int:
            if x in memo:
                return memo[x]
            if not preds[x]:
                memo[x] = 0
                return 0
            memo[x] = 1 + max(r(y) for y in preds[x])
            return memo[x]

        return {x: r(x) for x in elems}

    def height(self, x: T) -> int:
        if x not in self.poset.elements:
            raise ValueError(f"{x} not in poset")

        rm = self.rank_map()
        return rm[x]

    def total_height(self) -> int:
        rm = self.rank_map()
        if not rm:
            raise ValueError("Empty poset")
        return max(rm.values())
