"""
NEXAH Engine – Closure Operators on Finite Posets

A closure operator Γ on a poset (P, ≤) should satisfy:
1) Extensive:        x ≤ Γ(x)
2) Monotone:         x ≤ y  ⇒  Γ(x) ≤ Γ(y)
3) Idempotent:       Γ(Γ(x)) = Γ(x)

This module provides:
- ClosureOperator wrapper with validation
- Fixpoint poset / lattice construction helpers
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

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
        # Ensure gamma maps into the carrier set
        for x in self.poset.elements:
            gx = self.gamma(x)
            if gx not in self.poset.elements:
                raise ValueError(
                    f"gamma(x) must be in poset.elements. "
                    f"Got gamma({x})={gx}"
                )

        self._validate_extensive()
        self._validate_monotone()
        self._validate_idempotent()

    # -----------------------------------------------------
    # Closure Axioms
    # -----------------------------------------------------

    def _validate_extensive(self) -> None:
        for x in self.poset.elements:
            gx = self.gamma(x)
            if not self.poset.is_leq(x, gx):
                raise ValueError(
                    f"Not extensive: {x} ≤ gamma({x}) fails "
                    f"(gamma({x})={gx})."
                )

    def _validate_monotone(self) -> None:
        elems = list(self.poset.elements)
        for x in elems:
            for y in elems:
                if self.poset.is_leq(x, y):
                    gx = self.gamma(x)
                    gy = self.gamma(y)
                    if not self.poset.is_leq(gx, gy):
                        raise ValueError(
                            f"Not monotone: {x} ≤ {y} but "
                            f"gamma({x}) ≤ gamma({y}) fails "
                            f"(gamma({x})={gx}, gamma({y})={gy})."
                        )

    def _validate_idempotent(self) -> None:
        for x in self.poset.elements:
            gx = self.gamma(x)
            ggx = self.gamma(gx)
            if ggx != gx:
                raise ValueError(
                    f"Not idempotent: gamma(gamma({x})) != gamma({x}) "
                    f"(gamma({x})={gx}, gamma(gamma({x}))={ggx})."
                )

    # -----------------------------------------------------
    # Convenience API
    # -----------------------------------------------------

    def apply(self, x: Any) -> Any:
        return self.gamma(x)

    def fixpoints(self):
        """
        Returns the set {x in P | gamma(x) = x}.
        """
        return {
            x for x in self.poset.elements
            if self.gamma(x) == x
        }

    def fixpoint_lattice(self, strict: bool = False) -> FixpointStructure:
        """
        Builds Fix(Γ) with inherited order and lattice operations.

        If strict=True:
            Require the induced structure to be a lattice.
            Raise ValueError otherwise.
        """
        fp = build_fixpoint_structure(self.poset, self.gamma)

        if strict and not fp.is_lattice():
            raise ValueError(
                "Fixpoint structure is not a lattice (strict=True)."
            )

        return fp
    # -----------------------------
    # Convenience
    # -----------------------------

    def apply(self, x: Any) -> Any:
        return self.gamma(x)

    def fixpoint_lattice(self, strict: bool = False) -> FixpointStructure:
        """
        Builds Fix(Γ) with inherited order and lattice ops on that induced poset.

        If strict=True: additionally require the induced structure to be a lattice
        (i.e. every pair has unique join & meet). Raises ValueError otherwise.
        """
        fp = build_fixpoint_structure(self.poset, self.gamma)
        if strict and not fp.lattice.is_lattice():
            raise ValueError("Fixpoint structure is not a lattice (strict=True).")
        return fp
