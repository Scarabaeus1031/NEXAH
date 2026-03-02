"""
NEXAH Engine – Closure Operator (Γ)

Implements finite closure operators on a given FinitePoset.
"""

from typing import Callable
from .poset import FinitePoset


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
