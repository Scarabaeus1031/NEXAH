from __future__ import annotations

from ENGINE.core.worklist_fixpoint import solve_worklist
from ENGINE.core.lattice import LatticeOps

from ENGINE.applications.constant_lattice import (
    ConstVal,
    State,
    build_state_lattice,
)


def main():

    variables = {"x"}
    constants = {1, 2}

    lattice = build_state_lattice(variables, constants)

    nodes = {1, 2, 3, 4}
    edges = {
        (1, 2),
        (1, 3),
        (2, 4),
        (3, 4),
    }

    bottom = ConstVal.bottom()
    bottom_state = State(
        frozenset((v, bottom) for v in variables)
    )

    initial = {n: bottom_state for n in nodes}

    def transfer(node: int, state: State) -> State:

        if node == 2:
            return state.with_update("x", ConstVal.const(1))

        if node == 3:
            return state.with_update("x", ConstVal.const(2))

        return state

    result = solve_worklist(
        nodes=nodes,
        edges=edges,
        value_poset=lattice,
        initial_in=initial,
        transfer=transfer,
    )

    print("\nBranch Conflict Result (OUT):")
    for n in sorted(result.out_values):
        print(f"Node {n}: {result.out_values[n]}")


if __name__ == "__main__":
    main()
