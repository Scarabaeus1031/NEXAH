"""
NEXAH Engine – Frame Operator F

F is a projection operator.

Given:
    F: X → Y

It maps elements into a new representation space.

F does NOT guarantee:
    - injectivity
    - order preservation
    - lattice preservation

It is purely a projection mechanism.
"""

from __future__ import annotations

from typing import Callable, Any, Iterable, Set


class FrameOperator:
    def __init__(self, mapping: Callable[[Any], Any]):
        if not callable(mapping):
            raise TypeError("FrameOperator requires a callable mapping.")
        self.mapping = mapping

    def apply(self, x: Any) -> Any:
        return self.mapping(x)

    def project_set(self, elements: Iterable[Any]) -> Set[Any]:
        return {self.mapping(x) for x in elements}
