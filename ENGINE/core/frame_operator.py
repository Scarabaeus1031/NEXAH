"""
NEXAH Engine – Frame Operator F

F is a projection / framing operator.

Given a finite poset P = (X, ≤) and a mapping F: X → Y,
we construct the projected poset F(P) on Y with the induced order:

    a ≤_F b    iff    for every x in X with F(x)=a,
                      there exists y in X with F(y)=b
                      such that x ≤ y.

This guarantees reflexivity on the image, and tends to preserve antisymmetry
better than naive existential lifting (which usually collapses too much).
"""

from __future__ import annotations

from typing import Callable, Any, Dict, Set, Iterable

from ENGINE.core.poset import FinitePoset


class FrameOperator:
    def __init__(self, mapping: Callable[[Any], Any]):
        if not callable(mapping):
            raise TypeError("FrameOperator requires a callable mapping.")
        self.mapping = mapping

    def apply(self, x: Any) -> Any:
        return self.mapping(x)

    def project_set(self, elements: Iterable[Any]) -> Set[Any]:
        return {self.mapping(x) for x in elements}

    def on_poset(self, poset: FinitePoset) -> FinitePoset:
        image = self.project_set(poset.elements)

        # Preimages: a -> { x in X | F(x)=a }
        pre: Dict[Any, Set[Any]] = {a: set() for a in image}
        for x in poset.elements:
            pre[self.mapping(x)].add(x)

        def induced_leq(a, b) -> bool:
            # a,b are in the image, hence pre[a], pre[b] non-empty
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
