from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Set

from ENGINE.core.poset import FinitePoset
from ENGINE.core.lattice import LatticeOps


# ---------------------------------------------------------
# Atomic constant lattice element
# ---------------------------------------------------------

@dataclass(frozen=True)
class ConstVal:
    value: Optional[int]
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
        return str(self.value)

    def __repr__(self) -> str:
        return self.__str__()


def build_atomic_lattice(constants: Set[int]) -> FinitePoset[ConstVal]:
    bottom = ConstVal.bottom()
    top = ConstVal.top()

    const_elems = {ConstVal.const(c) for c in constants}
    elements = {bottom, top} | const_elems

    def leq(a: ConstVal, b: ConstVal) -> bool:
        if a == b:
            return True
        if a.is_bottom:
            return True
        if b.is_top:
            return True
        if not a.is_top and not b.is_top and not a.is_bottom and not b.is_bottom:
            return a.value == b.value
        return False

    return FinitePoset(elements, leq)


# ---------------------------------------------------------
# State lattice (mapping variable -> ConstVal)
# ---------------------------------------------------------

@dataclass(frozen=True)
class State:
    values: Dict[str, ConstVal]

    def __repr__(self) -> str:
        return str(self.values)


def build_state_lattice(
    variables: Set[str],
    constants: Set[int],
) -> FinitePoset[State]:

    atomic = build_atomic_lattice(constants)
    atomic_ops = LatticeOps(atomic)

    # build full finite carrier
    atomic_elements = list(atomic.elements)

    def generate_states(vars_list, idx=0, current=None):
        if current is None:
            current = {}
        if idx == len(vars_list):
            yield State(dict(current))
            return
        var = vars_list[idx]
        for val in atomic_elements:
            current[var] = val
            yield from generate_states(vars_list, idx + 1, current)

    vars_list = sorted(list(variables))
    elements = set(generate_states(vars_list))

    def leq(a: State, b: State) -> bool:
        for v in vars_list:
            if not atomic.is_leq(a.values[v], b.values[v]):
                return False
        return True

    return FinitePoset(elements, leq)
