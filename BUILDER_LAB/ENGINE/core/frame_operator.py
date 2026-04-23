"""
NEXAH Engine – Frame Operator F

F is a projection / framing operator.

Given a finite poset P = (X, ≤) and a mapping F: X → Y,
we construct the projected poset F(P) on Y with the induced order:

    a ≤_F b    iff    for every x in X with F(x)=a,
                      there exists y in X with F(y)=b
                      such that x ≤ y.
"""

from __future__ import annotations

from typing import Callable, Dict, Generic, Iterable, Set, TypeVar
from collections.abc import Hashable

from ENGINE.core.poset import FinitePoset

X = TypeVar("X", bound=Hashable)  # original carrier type
Y = TypeVar("Y", bound=Hashable)  # projected carrier type


class FrameOperator(Generic[X, Y]):
    def __init__(self, mapping: Callable[[X], Y]) -> None:
        if not callable(mapping):
            raise TypeError("FrameOperator requires a callable mapping.")
        self.mapping: Callable[[X], Y] = mapping

    def apply(self, x: X) -> Y:
        return self.mapping(x)

    def project_set(self, elements: Iterable[X]) -> Set[Y]:
        return {self.mapping(x) for x in elements}

    def on_poset(self, poset: FinitePoset[X]) -> FinitePoset[Y]:
        image: Set[Y] = self.project_set(poset.elements)

        # Preimages: a -> { x in X | F(x)=a }
        pre: Dict[Y, Set[X]] = {a: set() for a in image}
        for x in poset.elements:
            pre[self.mapping(x)].add(x)

        def induced_leq(a: Y, b: Y) -> bool:
            # a,b are in the image; pre[a], pre[b] are defined
            for x in pre[a]:
                ok = False
                for y in pre[b]:
                    if poset.is_leq(x, y):
                        ok = True
                        break
                if not ok:
                    return False
            return True

        return FinitePoset(image, induced_leq)
