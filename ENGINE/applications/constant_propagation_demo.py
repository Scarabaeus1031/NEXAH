from __future__ import annotations

from ENGINE.core.worklist_fixpoint import solve_worklist
from ENGINE.applications.constant_lattice import ConstVal, State, build_state_lattice


def main() -> None:
    variables = {"x", "y", "z"}
    constants = {1, 2}

    lattice = build_state_lattice(variables, constants)

    # Program graph
    nodes = {1, 2, 3}
    edges = {(1, 2), (2, 3)}

    bottom_atomic = ConstVal.bottom()
    bottom_state = State(frozenset((v, bottom_atomic) for v in variables))

    # IMPORTANT:
    # Dein solver nutzt: cand = transfer(v, u_val) und joint das in values[v].
    # D.h. "Statement an Node 1" wirkt nicht automatisch auf Node 1,
    # sondern würde nur über Kanten propagieren.
    #
    # Wir modellieren hier deshalb: Node 1 hat bereits den Effekt "x := 1"
    # als initial state (Entry-State nach Statement).
    initial = {n: bottom_state for n in nodes}

    def transfer(node: int, state: State) -> State:
        # Node 2: y := x
        if node == 2:
            return state.with_update("y", state.get("x"))

        # Node 3: z := y + 1  (wenn y konstant), sonst ⊤
        if node == 3:
            y_val = state.get("y")
            if not y_val.is_top and not y_val.is_bottom and y_val.value is not None:
                return state.with_update("z", ConstVal.const(y_val.value + 1))
            return state.with_update("z", ConstVal.top())

        return state

    result = solve_worklist(
        nodes=nodes,
        edges=edges,
        value_poset=lattice,
        initial=initial,
        transfer=transfer,
        strict=True,
    )

    print("\nConstant Propagation Result:")
    for n in sorted(result.values):
        print(f"Node {n}: {result.values[n]}")


if __name__ == "__main__":
    main()
