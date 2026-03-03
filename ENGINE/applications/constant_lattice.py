from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Set

from ENGINE.core.poset import FinitePoset


@dataclass(frozen=True)
class ConstVal:
    """
    Finite constant-propagation lattice element.

    ⊥  = bottom (no information)
    Const(n)
    ⊤  = top (conflict / unknown)
    """

    value: Optional[int]
    is_top: bool = False
    is_bottom: bool = False

    # -------------------------------------------------
    # Constructors
    # -------------------------------------------------

    @staticmethod
    def bottom() -> ConstVal:
        return ConstVal(value=None, is_bottom=True)

    @staticmethod
    def top() -> ConstVal:
        return ConstVal(value=None, is_top=True)

    @staticmethod
    def const(n: int) -> ConstVal:
        return ConstVal(value=n)

    # -------------------------------------------------
    # Pretty print
    # -------------------------------------------------

    def __str__(self) -> str:
        if self.is_bottom:
            return "⊥"
        if self.is_top:
            return "⊤"
        return str(self.value)

    def __repr__(self) -> str:
        return self.__str__()


# ---------------------------------------------------------
# Lattice builder
# ---------------------------------------------------------

def build_const_lattice(constants: Set[int]) -> FinitePoset[ConstVal]:
    """
    Builds a finite constant propagation lattice:

           ⊤
        /   |   \
    Const(n) ...
        \   |   /
           ⊥
    """

    bottom = ConstVal.bottom()
    top = ConstVal.top()

    const_elems = {ConstVal.const(c) for c in constants}
    elements = {bottom, top} | const_elems

    def leq(a: ConstVal, b: ConstVal) -> bool:
        # identical elements
        if a == b:
            return True

        # bottom ≤ everything
        if a.is_bottom:
            return True

        # everything ≤ top
        if b.is_top:
            return True

        # constants only ≤ themselves
        if (
            not a.is_bottom
            and not a.is_top
            and not b.is_bottom
            and not b.is_top
        ):
            return a.value == b.value

        return False

    return FinitePoset(elements, leq)
