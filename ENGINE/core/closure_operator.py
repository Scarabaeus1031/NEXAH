"""
NEXAH Engine – Closure Operators on Finite Posets

A closure operator Γ on a poset (P, ≤) should satisfy:
1) Extensive:        x ≤ Γ(x)
2) Monotone:         x ≤ y  ⇒  Γ(x) ≤ Γ(y)
3) Idempotent:       Γ(Γ(x)) = Γ(x)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Set

from ENGINE.core.poset import FinitePoset
from ENGINE.core.fixpoint_lattice import (
    FixpointStructure,
    build_fixpoint_structure,
)


@dataclass(frozen=True)
class ClosureOperator:
    """
    Wrapper around a candidate closure operator Γ on a FinitePoset.
    """

    poset: FinitePoset
    gamma: Callable[[Any], Any]

    # -----------------------------------------------------
    # Initialization + Validation
    # -----------------------------------------------------

    def __post_init__(self) -> None:
        for x in self.poset.elements:
            gx = self.gamma(x)
            if gx not in self.poset.elements:
                raise ValueError(
                    f"gamma({x})={gx} not in poset.elements"
                )

        self._validate_extensive()
        self._validate_monotone()
        self._validate_idempotent()

    # -----------------------------------------------------
    # Closure Axioms
    # -----------------------------------------------------

    def _validate_extensive(self) -> None:
        for x in self.poset.elements:
            if not self.poset.is_leq(x, self.gamma(x)):
                raise ValueError(f"Not extensive at {x}")

    def _validate_monotone(self) -> None:
        elems = list(self.poset.elements)
        for x in elems:
            for y in elems:
                if self.poset.is_leq(x, y):
                    if not self.poset.is_leq(
                        self.gamma(x), self.gamma(y)
                    ):
                        raise ValueError(
                            f"Not monotone: {x} ≤ {y}"
                        )

    def _validate_idempotent(self) -> None:
        for x in self.poset.elements:
            if self.gamma(self.gamma(x)) != self.gamma(x):
                raise ValueError(f"Not idempotent at {x}")

    # -----------------------------------------------------
    # Core API
    # -----------------------------------------------------

    def apply(self, x: Any) -> Any:
        return self.gamma(x)

    def stabilize(self, x: Any, max_steps: int = 100) -> Any:
        current = x
        for _ in range(max_steps):
            nxt = self.gamma(current)
            if nxt == current:
                return current
            current = nxt
        raise RuntimeError(f"No stabilization from {x}")

    # -----------------------------------------------------
    # Fixpoints
    # -----------------------------------------------------

    def fixpoints(self) -> Set[Any]:
        return {
            x for x in self.poset.elements
            if self.gamma(x) == x
        }

    def least_fixpoint(self) -> Any:
        bottom = self.poset.bottom()
        if bottom is None:
            raise ValueError("No unique bottom element.")
        return self.stabilize(bottom)

    def greatest_fixpoint(self) -> Any:
        top = self.poset.top()
        if top is None:
            raise ValueError("No unique top element.")
        return self.stabilize(top)

    # -----------------------------------------------------
    # Fixpoint-Induced Structure
    # -----------------------------------------------------

    def fixpoint_lattice(self, strict: bool = False) -> FixpointStructure:
        fp = build_fixpoint_structure(self.poset, self.gamma)

        if strict and not fp.is_lattice():
            raise ValueError(
                "Fixpoint structure is not a lattice (strict=True)."
            )

        return fp
