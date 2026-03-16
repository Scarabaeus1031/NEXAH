from __future__ import annotations

from typing import Dict, Set

from ENGINE.core.worklist_fixpoint import solve_worklist
from ENGINE.applications.constant_lattice import (
    ConstVal,
    State,
    build_state_lattice,
)


def main() -> None:

    variables: Set[str] = {"x", "y", "z"}
    constants: Set[int] = {1, 2}

    lattice = build_state_lattice(variables, constants)

    nodes: Set[int] = {1, 2, 3}
    edges: Set[tuple[int, int]] = {(1, 2), (2, 3)}

    bottom_atomic = ConstVal.bottom()
    bottom_state = State(
        frozenset((v, bottom_atomic) for v in variables)
    )

    initial: Dict[int, State] = {n: bottom_state for n in nodes}

    def transfer(node: int, state: State) -> State:

        if node == 2:
            return state.with_update("y", state.get("x"))

        if node == 3:
            y_val = state.get("y")
            if (
                not y_val.is_top
                and not y_val.is_bottom
                and y_val.value is not None
            ):
                return state.with_update(
                    "z",
                    ConstVal.const(y_val.value + 1),
                )
            return state.with_update("z", ConstVal.top())

        return state

    result = solve_worklist(
        nodes=nodes,
        edges=edges,
        value_poset=lattice,
        initial_in=initial,
        transfer=transfer,
        strict=True,
    )

    print("\nConstant Propagation Result:")
    for n in sorted(result.out_values):
        print(f"Node {n}: {result.out_values[n]}")


if __name__ == "__main__":
    main()
