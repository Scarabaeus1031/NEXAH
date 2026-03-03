"""
NEXAH Engine – Closure Operator (Γ)

Implements finite closure operators on a given FinitePoset.
"""

from typing import Callable
from .poset import FinitePoset
from .lattice import LatticeOps


class ClosureOperator:
    """
    Represents a closure operator Γ: Q → Q
    satisfying:

        1. Monotonicity
        2. Extensivity
        3. Idempotence
    """

    def __init__(self, poset: FinitePoset, operator: Callable):
        self.poset = poset
        self.operator = operator

        self._validate_closure_properties()

    # -----------------------------------------------------
    # Core Properties
    # -----------------------------------------------------

    def _validate_closure_properties(self):
        self._check_monotone()
        self._check_extensive()
        self._check_idempotent()

    def _check_monotone(self):
        for x in self.poset.elements:
            for y in self.poset.elements:
                if self.poset.is_leq(x, y):
                    if not self.poset.is_leq(
                        self.operator(x),
                        self.operator(y)
                    ):
                        raise ValueError("Closure operator is not monotone.")

    def _check_extensive(self):
        for x in self.poset.elements:
            if not self.poset.is_leq(x, self.operator(x)):
                raise ValueError("Closure operator is not extensive.")

    def _check_idempotent(self):
        for x in self.poset.elements:
            if self.operator(self.operator(x)) != self.operator(x):
                raise ValueError("Closure operator is not idempotent.")

    # -----------------------------------------------------
    # Application
    # -----------------------------------------------------

    def apply(self, x):
        return self.operator(x)

    def fixpoints(self):
        """
        Returns all fixpoints Γ(x) = x.
        """
        return {
            x for x in self.poset.elements
            if self.operator(x) == x
        }

    # -----------------------------------------------------
    # Fixpoint Structure
    # -----------------------------------------------------

    def fixpoint_poset(self) -> FinitePoset:
        """
        Returns the induced sub-poset on Fix(Γ) = { x | Γ(x) = x }.
        The order relation is inherited from the underlying poset.
        """
        fps = self.fixpoints()

        if not fps:
            raise ValueError("Closure operator has no fixpoints.")

        def inherited_leq(x, y):
            return self.poset.is_leq(x, y)

        return FinitePoset(fps, inherited_leq)

    def fixpoint_lattice(self, strict: bool = True) -> LatticeOps:
        """
        Returns lattice operations on the fixpoint set.

        If strict=True (default), raises ValueError if the
        fixpoints do not form a lattice under the inherited order.
        """
        fp_poset = self.fixpoint_poset()
        ops = LatticeOps(fp_poset)

        if strict and not ops.is_lattice():
            raise ValueError(
                "Fixpoints do not form a lattice under inherited order."
            )

        return ops
