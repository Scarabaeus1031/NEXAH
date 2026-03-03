"""
NEXAH Engine – Frame Operator F

F is a projection operator.

On posets:
    F(P) = projected poset with induced order:
        a ≤_F b  iff  ∃ x,y ∈ P:
            F(x)=a, F(y)=b, and x ≤ y
"""

from __future__ import annotations

from typing import Callable, Any, Iterable, Set

from ENGINE.core.poset import FinitePoset


class FrameOperator:
    def __init__(self, mapping: Callable[[Any], Any]):
        if not callable(mapping):
            raise TypeError("FrameOperator requires a callable mapping.")
        self.mapping = mapping

    # ------------------------
    # Value-level projection
    # ------------------------

    def apply(self, x: Any) -> Any:
        return self.mapping(x)

    def project_set(self, elements: Iterable[Any]) -> Set[Any]:
        return {self.mapping(x) for x in elements}

    # ------------------------
    # Poset-level projection
    # ------------------------

    def on_poset(self, poset: FinitePoset) -> FinitePoset:
        new_elements = self.project_set(poset.elements)

        def induced_leq(a, b):
            for x in poset.elements:
                if self.mapping(x) != a:
                    continue
                for y in poset.elements:
                    if self.mapping(y) != b:
                        continue
                    if poset.is_leq(x, y):
                        return True
            return False

        return FinitePoset(new_elements, induced_leq)
