"""
NEXAH Engine – Closure Operator

Defines a closure operator Γ on a finite poset and provides
fixpoint utilities and structural checks.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Set

from ENGINE.core.poset import FinitePoset


@dataclass(frozen=True)
class ClosureOperator:
    """
    Closure operator Γ on a finite poset.
    """

    poset: FinitePoset
    operator: Callable[[Any], Any]

    # -----------------------------
    # Basic properties
    # -----------------------------

    def is_extensive(self) -> bool:
        return all(
            self.poset.is_leq(x, self.operator(x))
            for x in self.poset.elements
        )

    def is_monotone(self) -> bool:
        for x in self.poset.elements:
            for y in self.poset.elements:
                if self.poset.is_leq(x, y):
                    if not self.poset.is_leq(
                        self.operator(x),
                        self.operator(y),
                    ):
                        return False
        return True

    def is_idempotent(self) -> bool:
        return all(
            self.operator(self.operator(x)) == self.operator(x)
            for x in self.poset.elements
        )

    def is_closure_operator(self) -> bool:
        return (
            self.is_extensive()
            and self.is_monotone()
            and self.is_idempotent()
        )

    # -----------------------------
    # Fixpoints
    # -----------------------------

    def fixpoints(self) -> Set[Any]:
        return {
            x for x in self.poset.elements
            if self.operator(x) == x
        }

    # -----------------------------
    # Induced lattice (lazy import)
    # -----------------------------

    def fixpoint_lattice(self):
        """
        Returns LatticeOps on the induced fixpoint poset.
        Lazy import prevents circular dependency.
        """
        from ENGINE.core.fixpoint_lattice import build_fixpoint_structure

        structure = build_fixpoint_structure(self.poset, self.operator)
        return structure.lattice
