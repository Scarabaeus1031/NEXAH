"""
NEXAH Engine – Core Layer
Finite Partially Ordered Set (Poset) Implementation
"""

from typing import Iterable, Callable, Dict, Set


class FinitePoset:
    """
    Represents a finite partially ordered set (Q, <=).

    The order relation is given as a binary predicate.
    """

    def __init__(self, elements: Iterable, leq: Callable):
        self.elements: Set = set(elements)
        self.leq = leq

        self._validate_partial_order()

    # -----------------------------------------------------
    # Order Validation
    # -----------------------------------------------------

    def _validate_partial_order(self):
        self._check_reflexive()
        self._check_antisymmetric()
        self._check_transitive()

    def _check_reflexive(self):
        for x in self.elements:
            if not self.leq(x, x):
                raise ValueError("Relation is not reflexive.")

    def _check_antisymmetric(self):
        for x in self.elements:
            for y in self.elements:
                if self.leq(x, y) and self.leq(y, x) and x != y:
                    raise ValueError("Relation is not antisymmetric.")

    def _check_transitive(self):
        for x in self.elements:
            for y in self.elements:
                for z in self.elements:
                    if self.leq(x, y) and self.leq(y, z) and not self.leq(x, z):
                        raise ValueError("Relation is not transitive.")

    # -----------------------------------------------------
    # Order Queries
    # -----------------------------------------------------

    def is_leq(self, x, y) -> bool:
        return self.leq(x, y)

    def minimal_elements(self) -> Set:
        return {
            x for x in self.elements
            if not any(self.leq(y, x) and y != x for y in self.elements)
        }

    def maximal_elements(self) -> Set:
        return {
            x for x in self.elements
            if not any(self.leq(x, y) and y != x for y in self.elements)
        }

    # -----------------------------------------------------
    # Closure Iteration (generic)
    # -----------------------------------------------------

    def iterate_until_fixpoint(self, f: Callable, start):
        """
        Iteratively applies a monotone function until stabilization.
        """
        current = start
        while True:
            next_val = f(current)
            if next_val == current:
                return current
            current = next_val
