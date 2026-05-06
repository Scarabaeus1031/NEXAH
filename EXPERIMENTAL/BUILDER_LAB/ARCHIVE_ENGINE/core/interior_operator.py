"""
NEXAH Engine — Interior Operator Ι

Interior operator is dual to closure:
- contractive: I(x) ≤ x
- monotone: x ≤ y => I(x) ≤ I(y)
- idempotent: I(I(x)) = I(x)

Finite setting: validated defensively on construction.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, Set, TypeVar
from collections.abc import Hashable

from ENGINE.core.poset import FinitePoset

T = TypeVar("T", bound=Hashable)


@dataclass(frozen=True)
class InteriorOperator(Generic[T]):
    poset: FinitePoset[T]
    iota: Callable[[T], T]

    def __post_init__(self) -> None:
        self._validate_returns_in_carrier()
        self._validate_contractive()
        self._validate_monotone()
        self._validate_idempotent()

    def apply(self, x: T) -> T:
        if x not in self.poset.elements:
            raise ValueError("InteriorOperator.apply called with element not in carrier.")
        return self.iota(x)

    def fixpoints(self) -> Set[T]:
        return {x for x in self.poset.elements if self.iota(x) == x}

    def stabilize(self, x: T) -> T:
        """
        Defensive finite iteration until a fixpoint is reached.
        Raises RuntimeError if a cycle is detected.
        """
        if x not in self.poset.elements:
            raise ValueError("InteriorOperator.stabilize called with element not in carrier.")

        seen: Set[T] = set()
        cur: T = x

        while True:
            if cur in seen:
                raise RuntimeError("Interior stabilize did not converge (cycle detected).")
            seen.add(cur)

            nxt = self.iota(cur)
            if nxt == cur:
                return cur
            cur = nxt

    # -----------------
    # Validation
    # -----------------

    def _validate_returns_in_carrier(self) -> None:
        for x in self.poset.elements:
            y = self.iota(x)
            if y not in self.poset.elements:
                raise ValueError(
                    f"Interior operator returned non-carrier element at {x}: {y!r}"
                )

    def _validate_contractive(self) -> None:
        for x in self.poset.elements:
            if not self.poset.is_leq(self.iota(x), x):
                raise ValueError(f"Not contractive at {x!r}")

    def _validate_monotone(self) -> None:
        elems = list(self.poset.elements)
        for x in elems:
            for y in elems:
                if self.poset.is_leq(x, y):
                    if not self.poset.is_leq(self.iota(x), self.iota(y)):
                        raise ValueError(f"Not monotone at ({x!r}, {y!r})")

    def _validate_idempotent(self) -> None:
        for x in self.poset.elements:
            if self.iota(self.iota(x)) != self.iota(x):
                raise ValueError(f"Not idempotent at {x!r}")
