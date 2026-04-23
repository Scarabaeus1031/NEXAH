from __future__ import annotations

from typing import Dict, Set

from ENGINE.core.worklist_fixpoint import solve_worklist
from ENGINE.applications.constant_lattice import (
    ConstVal,
    State,
    build_state_lattice,
)
from ENGINE.applications.mini_ir import (
    Program,
    Nop,
    AssignConst,
    AssignVar,
    make_transfer,
)


def main() -> None:

    variables: Set[str] = {"x", "y"}
    constants: Set[int] = {1, 2}

    lattice = build_state_lattice(variables, constants)

    bottom = ConstVal.bottom()
    bottom_state = State(
        frozenset((v, bottom) for v in variables)
    )

    prog = Program([
        Nop(),                    # 1
        AssignConst("x", 1),      # 2
        AssignConst("x", 2),      # 3
        AssignVar("y", "x"),      # 4
    ])

    nodes: Set[int] = set(prog.node_ids())

    edges: Set[tuple[int, int]] = {
        (1, 2),
        (1, 3),
        (2, 4),
        (3, 4),
    }

    transfer = make_transfer(prog)

    initial: Dict[int, State] = {n: bottom_state for n in nodes}

    result = solve_worklist(
        nodes=nodes,
        edges=edges,
        value_poset=lattice,
        initial_in=initial,
        transfer=transfer,
    )

    print("\nMini IR Branch Analysis (OUT):")
    for n in sorted(result.out_values):
        print(f"Node {n}: {result.out_values[n]}")


if __name__ == "__main__":
    main()
