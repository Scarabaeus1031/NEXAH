"""
NEXAH Engine – Monotone Operators on Finite Posets

A monotone operator f on a poset (P, ≤) satisfies:
    x ≤ y  ⇒  f(x) ≤ f(y)

Unlike closure operators, we do NOT assume:
- extensivity (x ≤ f(x))
- idempotence (f(f(x)) = f(x))

This module provides:
- MonotoneOperator wrapper with monotonicity validation
- General fixpoint enumeration on finite posets
- Cycle-safe iteration from an arbitrary start point
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

from ENGINE.core.poset import FinitePoset


@dataclass(frozen=True)
class MonotoneOperator:
    poset: FinitePoset
    f: Callable[[Any], Any]

    def __post_init__(self) -> None:
        # Ensure f maps into the carrier set
        for x in self.poset.elements:
            fx = self.f(x)
            if fx not in self.poset.elements:
                raise ValueError(f"f({x})={fx} not in poset.elements")
        self._validate_monotone()

    # -----------------------------------------------------
    # Axiom
    # -----------------------------------------------------

    def _validate_monotone(self) -> None:
        elems = list(self.poset.elements)
        for x in elems:
            for y in elems:
                if self.poset.is_leq(x, y):
                    if not self.poset.is_leq(self.f(x), self.f(y)):
                        raise ValueError(
                            f"Not monotone: {x} ≤ {y} but f({x}) ≤ f({y}) fails."
                        )

    # -----------------------------------------------------
    # Core API
    # -----------------------------------------------------

    def apply(self, x: Any) -> Any:
        return self.f(x)

    def iterate_from(
        self,
        x0: Any,
        max_steps: int = 100,
    ) -> Tuple[Any, List[Any]]:
        """
        Iterate x_{n+1} = f(x_n) from x0.

        Returns (result, trajectory).
        - If a fixpoint is reached, result is that fixpoint.
        - If a cycle occurs (period > 1), raises RuntimeError with trajectory info.
        """
        if x0 not in self.poset.elements:
            raise ValueError(f"x0={x0} not in poset.elements")

        seen: Dict[Any, int] = {}
        traj: List[Any] = [x0]
        current = x0

        for step in range(max_steps):
            if current in seen:
                # cycle detected
                i = seen[current]
                cycle = traj[i:]
                raise RuntimeError(
                    f"Cycle detected after {step} steps. Cycle={cycle}"
                )

            seen[current] = len(traj) - 1
            nxt = self.f(current)
            traj.append(nxt)

            if nxt == current:
                return nxt, traj

            current = nxt

        raise RuntimeError(
            f"No fixpoint within {max_steps} steps from {x0}. Trajectory={traj}"
        )

    # -----------------------------------------------------
    # Fixpoint sets (finite, exact)
    # -----------------------------------------------------

    def fixpoints(self) -> Set[Any]:
        return {x for x in self.poset.elements if self.f(x) == x}

    def prefixed_points(self) -> Set[Any]:
        """Pre-fixpoints: f(x) ≤ x"""
        return {x for x in self.poset.elements if self.poset.is_leq(self.f(x), x)}

    def postfixed_points(self) -> Set[Any]:
        """Post-fixpoints: x ≤ f(x)"""
        return {x for x in self.poset.elements if self.poset.is_leq(x, self.f(x))}

    # -----------------------------------------------------
    # Least / Greatest fixpoint (exact, by order)
    # -----------------------------------------------------

    def least_fixpoint(self) -> Any:
        """
        Exact least fixpoint (if it exists uniquely) by enumerating fixpoints.
        On a finite poset: compute Fix(f), then select the unique minimal element.
        """
        fps = list(self.fixpoints())
        if not fps:
            raise ValueError("No fixpoints exist.")

        minimals = []
        for x in fps:
            if all(not self.poset.is_leq(y, x) or y == x for y in fps):
                minimals.append(x)

        if len(minimals) != 1:
            raise ValueError(f"Least fixpoint not unique. Minim als={minimals}")
        return minimals[0]

    def greatest_fixpoint(self) -> Any:
        """
        Exact greatest fixpoint (if it exists uniquely) by enumerating fixpoints.
        """
        fps = list(self.fixpoints())
        if not fps:
            raise ValueError("No fixpoints exist.")

        maximals = []
        for x in fps:
            if all(not self.poset.is_leq(x, y) or y == x for y in fps):
                maximals.append(x)

        if len(maximals) != 1:
            raise ValueError(f"Greatest fixpoint not unique. Maxim als={maximals}")
        return maximals[0]

    # -----------------------------------------------------
    # Optional: “safe” bottom/top start iteration if inflationary/deflationary
    # -----------------------------------------------------

    def iterate_from_bottom_if_inflationary(self, max_steps: int = 100) -> Any:
        """
        If x ≤ f(x) for all x (inflationary), then iterating from bottom is ascending
        and must stabilize in finite posets.
        """
        bottom = self.poset.bottom()
        if bottom is None:
            raise ValueError("No unique bottom element.")
        if any(not self.poset.is_leq(x, self.f(x)) for x in self.poset.elements):
            raise ValueError("Operator is not inflationary (x ≤ f(x)) for all x.")
        fx, _ = self.iterate_from(bottom, max_steps=max_steps)
        return fx

    def iterate_from_top_if_deflationary(self, max_steps: int = 100) -> Any:
        """
        If f(x) ≤ x for all x (deflationary), then iterating from top is descending
        and must stabilize in finite posets.
        """
        top = self.poset.top()
        if top is None:
            raise ValueError("No unique top element.")
        if any(not self.poset.is_leq(self.f(x), x) for x in self.poset.elements):
            raise ValueError("Operator is not deflationary (f(x) ≤ x) for all x.")
        fx, _ = self.iterate_from(top, max_steps=max_steps)
        return fx
