"""
NEXAH Engine – Mini IR (minimal intermediate representation)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Protocol

from ENGINE.applications.constant_lattice import ConstVal, State


# ---------------------------------------------------------
# Instruction protocol
# ---------------------------------------------------------


class Instr(Protocol):
    def apply(self, st: State) -> State: ...


# ---------------------------------------------------------
# Concrete instructions
# ---------------------------------------------------------


@dataclass(frozen=True)
class Nop:
    def apply(self, st: State) -> State:
        return st


@dataclass(frozen=True)
class AssignConst:
    dst: str
    value: int

    def apply(self, st: State) -> State:
        return st.with_update(self.dst, ConstVal.const(self.value))


@dataclass(frozen=True)
class AssignVar:
    dst: str
    src: str

    def apply(self, st: State) -> State:
        return st.with_update(self.dst, st.get(self.src))


@dataclass(frozen=True)
class AddConst:
    """
    dst := src + k
    """
    dst: str
    src: str
    k: int

    def apply(self, st: State) -> State:
        v = st.get(self.src)

        if v.is_bottom:
            return st.with_update(self.dst, ConstVal.bottom())

        if v.is_top:
            return st.with_update(self.dst, ConstVal.top())

        assert v.value is not None
        return st.with_update(self.dst, ConstVal.const(v.value + self.k))


# ---------------------------------------------------------
# Program container
# ---------------------------------------------------------


@dataclass(frozen=True)
class Program:
    instrs: List[Instr]

    def __post_init__(self) -> None:
        if not self.instrs:
            raise ValueError("Program must contain at least one instruction.")

    def node_ids(self) -> List[int]:
        return list(range(1, len(self.instrs) + 1))

    def instr_at(self, node: int) -> Instr:
        if node < 1 or node > len(self.instrs):
            raise IndexError(
                f"Invalid node id {node}; valid range is 1..{len(self.instrs)}"
            )
        return self.instrs[node - 1]

    def linear_edges(self) -> set[tuple[int, int]]:
        n = len(self.instrs)
        return {(i, i + 1) for i in range(1, n)}


# ---------------------------------------------------------
# Transfer builder
# ---------------------------------------------------------


def make_transfer(program: Program) -> Callable[[int, State], State]:
    """
    Build a transfer function compatible with solve_worklist.
    """

    def transfer(node: int, st: State) -> State:
        instr = program.instr_at(node)
        return instr.apply(st)

    return transfer
