from __future__ import annotations

from ENGINE.core.worklist_fixpoint import solve_worklist
from ENGINE.applications.constant_lattice import (
    ConstVal,
    State,
    build_state_lattice,
)
from ENGINE.applications.mini_ir import (
    Program,
    AssignConst,
    AssignVar,
    AddConst,
    make_transfer,
)


def main():

    # -------------------------------------
    # Define variables + lattice
    # -------------------------------------

    variables = {"x", "y", "z"}
    constants = {1, 2, 3}

    lattice = build_state_lattice(variables, constants)

    bottom = ConstVal.bottom()
    bottom_state = State(
        frozenset((v, bottom) for v in variables)
    )

    # -------------------------------------
    # Build program
    # -------------------------------------

    prog = Program([
        AssignConst("x", 1),     # 1
        AssignVar("y", "x"),     # 2
        AddConst("z", "y", 1),   # 3
    ])

    nodes = set(prog.node_ids())
    edges = prog.linear_edges()

    transfer = make_transfer(prog)

    initial = {n: bottom_state for n in nodes}

    # -------------------------------------
    # Run analysis
    # -------------------------------------

    result = solve_worklist(
        nodes=nodes,
        edges=edges,
        value_poset=lattice,
        initial_in=initial,
        transfer=transfer,
    )

    print("\nMini IR Analysis (OUT):")
    for n in sorted(result.out_values):
        print(f"Node {n}: {result.out_values[n]}")


if __name__ == "__main__":
    main()
