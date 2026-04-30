from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet, Iterable, Optional, Set, Tuple

from ENGINE.core.poset import FinitePoset


# =========================================================
# Atomic lattice element: ⊥, Const(n), ⊤
# =========================================================

@dataclass(frozen=True)
class ConstVal:
    """
    Atomic constant-propagation lattice element.

    ⊥  = bottom (no information)
    Const(n)
    ⊤  = top (conflict / unknown)
    """

    value: Optional[int] = None
    is_top: bool = False
    is_bottom: bool = False

    @staticmethod
    def bottom() -> "ConstVal":
        return ConstVal(value=None, is_bottom=True)

    @staticmethod
    def top() -> "ConstVal":
        return ConstVal(value=None, is_top=True)

    @staticmethod
    def const(n: int) -> "ConstVal":
        return ConstVal(value=n, is_top=False, is_bottom=False)

    def __str__(self) -> str:
        if self.is_bottom:
            return "⊥"
        if self.is_top:
            return "⊤"
        return str(self.value)

    def __repr__(self) -> str:
        return str(self)


def build_atomic_lattice(constants: Set[int]) -> FinitePoset[ConstVal]:
    """
    Carrier = {⊥, ⊤} ∪ {Const(c) | c in constants}

    Order:
      ⊥ ≤ x for all x
      x ≤ ⊤ for all x
      Const(a) ≤ Const(b) iff a == b
    """
    bottom = ConstVal.bottom()
    top = ConstVal.top()
    const_elems = {ConstVal.const(c) for c in constants}
    elements: Set[ConstVal] = {bottom, top} | const_elems

    def leq(a: ConstVal, b: ConstVal) -> bool:
        if a == b:
            return True
        if a.is_bottom:
            return True
        if b.is_top:
            return True
        # Distinct constants are incomparable
        return False

    return FinitePoset(elements, leq)


# =========================================================
# State lattice: product of atomic lattices (hashable!)
# =========================================================

@dataclass(frozen=True)
class State:
    """
    Hashable store: a frozenset of (var, ConstVal).

    IMPORTANT: values must be a FrozenSet[Tuple[str, ConstVal]]
    so State can live in FinitePoset.elements (a set).
    """

    values: FrozenSet[Tuple[str, ConstVal]]

    def get(self, key: str) -> ConstVal:
        for k, v in self.values:
            if k == key:
                return v
        raise KeyError(key)

    def with_update(self, key: str, value: ConstVal) -> "State":
        d = dict(self.values)
        d[key] = value
        return State(frozenset(d.items()))

    def __repr__(self) -> str:
        # Pretty output
        return str({k: v for k, v in sorted(self.values)})


def build_state_lattice(variables: Set[str], constants: Set[int]) -> FinitePoset[State]:
    """
    Finite product lattice over variables:
      State = Π_{v in variables} Atomic

    Order is pointwise:
      s ≤ t  iff  for all var: s[var] ≤ t[var]  (in atomic lattice)

    Carrier is finite:
      |Atomic|^(|variables|)
    """
    atomic = build_atomic_lattice(constants)
    atomic_elements = list(atomic.elements)
    vars_list = sorted(variables)

    def generate_states(idx: int, current: dict[str, ConstVal]) -> Iterable[State]:
        if idx == len(vars_list):
            yield State(frozenset(current.items()))
            return
        var = vars_list[idx]
        for val in atomic_elements:
            current[var] = val
            yield from generate_states(idx + 1, current)

    elements: Set[State] = set(generate_states(0, {}))

    def leq(a: State, b: State) -> bool:
        for var in vars_list:
            if not atomic.is_leq(a.get(var), b.get(var)):
                return False
        return True

    return FinitePoset(elements, leq)
