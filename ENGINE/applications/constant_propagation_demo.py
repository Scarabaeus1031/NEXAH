from __future__ import annotations

from ENGINE.core.worklist_fixpoint import solve_worklist
from ENGINE.core.lattice import LatticeOps

from ENGINE.applications.constant_lattice import (
    ConstVal,
    State,
    build_state_lattice,
)


def main():

    variables = {"x", "y", "z"}
    constants = {1, 2}

    lattice = build_state_lattice(variables, constants)
    lat = LatticeOps(lattice)

    nodes = {1, 2, 3}
    edges = {(1, 2), (2, 3)}

    bottom_atomic = ConstVal.bottom()
    bottom_state = State(
        frozenset((v, bottom_atomic) for v in variables)
    )

    initial = {n: bottom_state for n in nodes}

    def transfer(node: int, state: State) -> State:

        if node == 1:
            return state.with_update("x", ConstVal.const(1))

        if node == 2:
            return state.with_update("y", state.get("x"))

        if node == 3:
            y_val = state.get("y")
            if not y_val.is_top and not y_val.is_bottom:
                return state.with_update("z", ConstVal.const(y_val.value + 1))
            return state.with_update("z", ConstVal.top())

        return state

    result = solve_worklist(
        nodes=nodes,
        edges=edges,
        value_poset=lattice,
        initial=initial,
        transfer=transfer,
    )

    print("\nConstant Propagation Result:")
    for n in sorted(result.values):
        print(f"Node {n}: {result.values[n]}")


if __name__ == "__main__":
    main()
