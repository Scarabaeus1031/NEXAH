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


def test_mini_ir_branch_conflict():

    variables = {"x", "y"}
    constants = {1, 2}

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

    nodes = set(prog.node_ids())
    edges = {
        (1, 2),
        (1, 3),
        (2, 4),
        (3, 4),
    }

    transfer = make_transfer(prog)
    initial = {n: bottom_state for n in nodes}

    result = solve_worklist(
        nodes=nodes,
        edges=edges,
        value_poset=lattice,
        initial_in=initial,
        transfer=transfer,
    )

    out = result.out_values

    # Branch conflict at node 4
    assert out[4].get("x").is_top
    assert out[4].get("y").is_top
