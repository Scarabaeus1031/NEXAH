from __future__ import annotations

from ENGINE.core.worklist_fixpoint import solve_worklist
from ENGINE.core.lattice import LatticeOps

from ENGINE.applications.constant_lattice import (
    ConstVal,
    build_const_lattice,
)


def main():
    # -------------------------------------------------
    # Lattice
    # -------------------------------------------------

    lattice = build_const_lattice({1, 2})
    lat = LatticeOps(lattice)

    # -------------------------------------------------
    # Control Flow Graph
    # -------------------------------------------------

    nodes = {1, 2, 3}
    edges = {(1, 2), (2, 3)}

    # -------------------------------------------------
    # Initial state
    # -------------------------------------------------

    bottom = ConstVal.bottom()

    initial = {
        1: bottom,
        2: bottom,
        3: bottom,
    }

    # -------------------------------------------------
    # Transfer function
    # -------------------------------------------------

    def transfer(node: int, val: ConstVal) -> ConstVal:
        if node == 1:
            return ConstVal.const(1)
        if node == 2:
            return val
        if node == 3:
            if not val.is_top and not val.is_bottom:
                return ConstVal.const(val.value + 1)
            return ConstVal.top()
        return ConstVal.top()

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
    for n, v in sorted(result.values.items()):
        print(f"Node {n}: {v}")


if __name__ == "__main__":
    main()
