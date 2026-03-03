"""
NEXAH Engine – Monotone Operators on Finite Posets
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Generic, List, Set, Tuple, TypeVar
from collections.abc import Hashable

from ENGINE.core.poset import FinitePoset

T = TypeVar("T", bound=Hashable)


@dataclass(frozen=True)
class MonotoneOperator(Generic[T]):
    poset: FinitePoset[T]
    f: Callable[[T], T]

    def __post_init__(self) -> None:
        # Ensure mapping into carrier
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

    def apply(self, x: T) -> T:
        return self.f(x)

    def iterate_from(self, x0: T, max_steps: int = 100) -> Tuple[T, List[T]]:
        if x0 not in self.poset.elements:
            raise ValueError(f"{x0} not in poset")

        seen: Dict[T, int] = {}
        traj: List[T] = [x0]
        current: T = x0

        for _ in range(max_steps):
            if current in seen:
                raise RuntimeError(f"Cycle detected: {traj}")

            seen[current] = len(traj) - 1
            nxt: T = self.f(current)
            traj.append(nxt)

            if nxt == current:
                return nxt, traj

            current = nxt

        raise RuntimeError(f"No stabilization from {x0}")

    # -----------------------------------------------------
    # Fixpoint sets
    # -----------------------------------------------------

    def fixpoints(self) -> Set[T]:
        return {x for x in self.poset.elements if self.f(x) == x}

    def prefixed_points(self) -> Set[T]:
        return {x for x in self.poset.elements if self.poset.is_leq(self.f(x), x)}

    def postfixed_points(self) -> Set[T]:
        return {x for x in self.poset.elements if self.poset.is_leq(x, self.f(x))}

    # -----------------------------------------------------
    # Enumeration-based least / greatest fixpoint
    # -----------------------------------------------------

    def least_fixpoint(self) -> T:
        fps = list(self.fixpoints())
        if not fps:
            raise ValueError("No fixpoints")

        minimals = [
            x
            for x in fps
            if all(not self.poset.is_leq(y, x) or y == x for y in fps)
        ]

        if len(minimals) != 1:
            raise ValueError("Least fixpoint not unique")

        return minimals[0]

    def greatest_fixpoint(self) -> T:
        fps = list(self.fixpoints())
        if not fps:
            raise ValueError("No fixpoints")

        maximals = [
            x
            for x in fps
            if all(not self.poset.is_leq(x, y) or y == x for y in fps)
        ]

        if len(maximals) != 1:
            raise ValueError("Greatest fixpoint not unique")

        return maximals[0]

    # -----------------------------------------------------
    # Tarski characterization
    # -----------------------------------------------------

    def tarski_least_fixpoint(self) -> T:
        from ENGINE.core.lattice import LatticeOps

        lat = LatticeOps(self.poset)
        if not lat.is_lattice():
            raise ValueError("Poset not a lattice")

        pref = list(self.prefixed_points())
        if not pref:
            raise ValueError("No prefixed points")

        result: T = pref[0]
        for x in pref[1:]:
            result = lat.meet(result, x)

        return result

    def tarski_greatest_fixpoint(self) -> T:
        from ENGINE.core.lattice import LatticeOps

        lat = LatticeOps(self.poset)
        if not lat.is_lattice():
            raise ValueError("Poset not a lattice")

        post = list(self.postfixed_points())
        if not post:
            raise ValueError("No postfixed points")

        result: T = post[0]
        for x in post[1:]:
            result = lat.join(result, x)

        return result
