from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, Set, TypeVar

from ENGINE.core.poset import FinitePoset
from ENGINE.core.fixpoint_lattice import build_fixpoint_poset
from ENGINE.core.lattice import LatticeOps

T = TypeVar("T")


@dataclass(frozen=True)
class ClosureOperator(Generic[T]):
    poset: FinitePoset[T]
    gamma: Callable[[T], T]

    def __post_init__(self) -> None:
        self._validate_returns_in_carrier()
        self._validate_extensive()
        self._validate_monotone()
        self._validate_idempotent()

    # -------------------------------------------------
    # Public API
    # -------------------------------------------------

    def apply(self, x: T) -> T:
        return self.gamma(x)

    def fixpoints(self) -> Set[T]:
        return {x for x in self.poset.elements if self.apply(x) == x}

    def stabilize(self, x: T) -> T:
        return self.poset.iterate_until_fixpoint(self.gamma, x)

    def fixpoint_lattice(self, strict: bool = False):
        """
        Return induced fixpoint poset.
        If strict=True, require it to form a lattice.
        """
        fp_poset = build_fixpoint_poset(self.poset, self.gamma)

        if strict:
            lat = LatticeOps(fp_poset)
            if not lat.is_lattice():
                raise ValueError("Fixpoint structure is not a lattice.")

        return fp_poset

    # -------------------------------------------------
    # Validation
    # -------------------------------------------------

    def _validate_returns_in_carrier(self) -> None:
        for x in self.poset.elements:
            y = self.gamma(x)
            if y not in self.poset.elements:
                raise ValueError("Closure returned element not in carrier.")

    def _validate_extensive(self) -> None:
        for x in self.poset.elements:
            if not self.poset.is_leq(x, self.gamma(x)):
                raise ValueError("Not extensive.")

    def _validate_monotone(self) -> None:
        for x in self.poset.elements:
            for y in self.poset.elements:
                if self.poset.is_leq(x, y):
                    if not self.poset.is_leq(self.gamma(x), self.gamma(y)):
                        raise ValueError("Not monotone.")

    def _validate_idempotent(self) -> None:
        for x in self.poset.elements:
            if self.gamma(self.gamma(x)) != self.gamma(x):
                raise ValueError("Not idempotent.")
