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

    value: Optional[int]  # None represents bottom or top
    is_top: bool = False
    is_bottom: bool = False

    @staticmethod
    def bottom() -> ConstVal:
        return ConstVal(value=None, is_bottom=True)

    @staticmethod
    def top() -> ConstVal:
        return ConstVal(value=None, is_top=True)

    @staticmethod
    def const(n: int) -> ConstVal:
        return ConstVal(value=n)

    def __str__(self) -> str:
        if self.is_bottom:
            return "⊥"
        if self.is_top:
            return "⊤"
        return f"{self.value}"


def build_const_lattice(constants: Set[int]) -> FinitePoset[ConstVal]:
    elements = {ConstVal.bottom(), ConstVal.top()}
    elements |= {ConstVal.const(c) for c in constants}

    def leq(a: ConstVal, b: ConstVal) -> bool:
        # bottom ≤ everything
        if a.is_bottom:
            return True

        # everything ≤ top
        if b.is_top:
            return True

        # equal constants
        if not a.is_top and not b.is_top and not a.is_bottom and not b.is_bottom:
            return a.value == b.value

        # constant ≤ itself
        return a == b

    return FinitePoset(elements, leq)
