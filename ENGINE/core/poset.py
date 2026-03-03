"""
NEXAH Engine – Core Layer
Finite Partially Ordered Set (Poset) Implementation
"""

from typing import Iterable, Callable, Set


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
            current = next_val        Raises ValueError if not unique / doesn't exist.
        """
        L = self.lower_bounds({a, b})
        maxs = self.maximal_in(L)
        if len(maxs) != 1:
            raise ValueError(f"meet({a},{b}) not unique / does not exist. Candidates={maxs}")
        return next(iter(maxs))

    # -----------------------------
    # Lattice checks
    # -----------------------------

    def is_lattice(self) -> bool:
        """
        True iff every pair has a unique join and meet.
        """
        elems = list(self.poset.elements)
        for a in elems:
            for b in elems:
                try:
                    _ = self.join(a, b)
                    _ = self.meet(a, b)
                except ValueError:
                    return False
        return True

    # -----------------------------
    # Distributivity
    # -----------------------------

    def is_distributive(self) -> bool:
        """
        Checks distributivity:
        a ∧ (b ∨ c) = (a ∧ b) ∨ (a ∧ c)
        for all triples (a, b, c).
        """
        elems = list(self.poset.elements)
        for a in elems:
            for b in elems:
                for c in elems:
                    try:
                        left = self.meet(a, self.join(b, c))
                        right = self.join(self.meet(a, b), self.meet(a, c))
                        if left != right:
                            return False
                    except ValueError:
                        return False
        return True

    # -----------------------------
    # Extremal elements
    # -----------------------------

    def top(self) -> Optional[Any]:
        mx = self.poset.maximal_elements()
        return next(iter(mx)) if len(mx) == 1 else None

    def bottom(self) -> Optional[Any]:
        mn = self.poset.minimal_elements()
        return next(iter(mn)) if len(mn) == 1 else None
