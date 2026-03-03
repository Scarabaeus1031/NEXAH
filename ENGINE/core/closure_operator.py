"""
NEXAH Engine – Closure Operator (Γ)

Implements finite closure operators on a given FinitePoset.
"""

from typing import Callable, Any, Set
from ENGINE.core.poset import FinitePoset
from ENGINE.core.lattice import LatticeOps


class ClosureOperator:
    """
    Represents a closure operator Γ: Q → Q
    satisfying:

        1. Monotonicity
        2. Extensivity
        3. Idempotence
    """

    def __init__(self, poset: FinitePoset, operator: Callable[[Any], Any]):
        self.poset = poset
        self.operator = operator

        self._validate_closure_properties()

    # -----------------------------------------------------
    # Validation
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
                        self.operator(y),
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
    # Basic Operations
    # -----------------------------------------------------

    def apply(self, x: Any) -> Any:
        return self.operator(x)

    def fixpoints(self) -> Set[Any]:
        """
        Returns all fixpoints Γ(x) = x.
        """
        return {
            x
            for x in self.poset.elements
            if self.operator(x) == x
        }

    # -----------------------------------------------------
    # Fixpoint Structure
    # -----------------------------------------------------

    def fixpoint_poset(self) -> FinitePoset:
        """
        Returns the induced FinitePoset on Fix(Γ)
        with inherited order ≤.
        """
        fps = self.fixpoints()

        def inherited_leq(x: Any, y: Any) -> bool:
            return self.poset.is_leq(x, y)

        return FinitePoset(fps, inherited_leq)

    def fixpoint_lattice(self, strict: bool = True) -> LatticeOps:
        """
        Returns LatticeOps on the fixpoint set.

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
