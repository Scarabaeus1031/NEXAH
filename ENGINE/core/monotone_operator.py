"""
NEXAH Engine – Monotone Operators on Finite Posets
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Set, Tuple

from ENGINE.core.poset import FinitePoset


@dataclass(frozen=True)
class MonotoneOperator:
    poset: FinitePoset
    f: Callable[[Any], Any]

    def __post_init__(self) -> None:
        # ensure mapping into carrier
        for x in self.poset.elements:
            fx = self.f(x)
            if fx not in self.poset.elements:
                raise ValueError(f"f({x})={fx} not in poset.elements")
        self._validate_monotone()

    # -----------------------------------------------------
    # Monotonicity
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

    def iterate_from(self, x0: Any, max_steps: int = 100) -> Tuple[Any, List[Any]]:
        if x0 not in self.poset.elements:
            raise ValueError(f"{x0} not in poset")

        seen: Dict[Any, int] = {}
        traj: List[Any] = [x0]
        current = x0

        for _ in range(max_steps):
            if current in seen:
                raise RuntimeError(f"Cycle detected: {traj}")

            seen[current] = len(traj) - 1
            nxt = self.f(current)
            traj.append(nxt)

            if nxt == current:
                return nxt, traj

            current = nxt

        raise RuntimeError(f"No stabilization from {x0}")

    # -----------------------------------------------------
    # Fixpoint sets
    # -----------------------------------------------------

    def fixpoints(self) -> Set[Any]:
        return {x for x in self.poset.elements if self.f(x) == x}

    def prefixed_points(self) -> Set[Any]:
        return {x for x in self.poset.elements if self.poset.is_leq(self.f(x), x)}

    def postfixed_points(self) -> Set[Any]:
        return {x for x in self.poset.elements if self.poset.is_leq(x, self.f(x))}

    # -----------------------------------------------------
    # Enumeration-based least / greatest fixpoint
    # -----------------------------------------------------

    def least_fixpoint(self) -> Any:
        fps = list(self.fixpoints())
        if not fps:
            raise ValueError("No fixpoints")

        minimals = [
            x for x in fps
            if all(not self.poset.is_leq(y, x) or y == x for y in fps)
        ]

        if len(minimals) != 1:
            raise ValueError("Least fixpoint not unique")

        return minimals[0]

    def greatest_fixpoint(self) -> Any:
        fps = list(self.fixpoints())
        if not fps:
            raise ValueError("No fixpoints")

        maximals = [
            x for x in fps
            if all(not self.poset.is_leq(x, y) or y == x for y in fps)
        ]

        if len(maximals) != 1:
            raise ValueError("Greatest fixpoint not unique")

        return maximals[0]

    # -----------------------------------------------------
    # Tarski characterization
    # -----------------------------------------------------

    def tarski_least_fixpoint(self) -> Any:
        from ENGINE.core.lattice import LatticeOps

        lat = LatticeOps(self.poset)
        if not lat.is_lattice():
            raise ValueError("Poset not a lattice")

        pref = list(self.prefixed_points())
        if not pref:
            raise ValueError("No prefixed points")

        result = pref[0]
        for x in pref[1:]:
            result = lat.meet(result, x)

        return result

    def tarski_greatest_fixpoint(self) -> Any:
        from ENGINE.core.lattice import LatticeOps

        lat = LatticeOps(self.poset)
        if not lat.is_lattice():
            raise ValueError("Poset not a lattice")

        post = list(self.postfixed_points())
        if not post:
            raise ValueError("No postfixed points")

        result = post[0]
        for x in post[1:]:
            result = lat.join(result, x)

        return result
