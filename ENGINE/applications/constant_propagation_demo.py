from __future__ import annotations

from ENGINE.core.worklist_fixpoint import solve_worklist
from ENGINE.core.lattice import LatticeOps

from ENGINE.applications.constant_lattice import (
    ConstVal,
    State,
    build_state_lattice,
)


def main():
    # -------------------------------------------------
    # Variables
    # -------------------------------------------------

    variables = {"x", "y", "z"}
    constants = {1, 2}

    lattice = build_state_lattice(variables, constants)
    lat = LatticeOps(lattice)

    # -------------------------------------------------
    # CFG
    # -------------------------------------------------

    nodes = {1, 2, 3}
    edges = {(1, 2), (2, 3)}

    # -------------------------------------------------
    # Initial state
    # -------------------------------------------------

    bottom_atomic = ConstVal.bottom()
    bottom_state = State({v: bottom_atomic for v in variables})

    initial = {n: bottom_state for n in nodes}

    # -------------------------------------------------
    # Transfer functions
    # -------------------------------------------------

    def transfer(node: int, state: State) -> State:
        new_vals = dict(state.values)

        if node == 1:
            new_vals["x"] = ConstVal.const(1)

        if node == 2:
            new_vals["y"] = state.values["x"]

        if node == 3:
            x_val = state.values["y"]
            if not x_val.is_top and not x_val.is_bottom:
                new_vals["z"] = ConstVal.const(x_val.value + 1)
            else:
                new_vals["z"] = ConstVal.top()

        return State(new_vals)

    # -------------------------------------------------
    # Solve
    # -------------------------------------------------

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
