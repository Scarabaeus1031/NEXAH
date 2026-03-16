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


def test_mini_ir_linear_propagation():

    variables = {"x", "y", "z"}
    constants = {1, 2, 3}

    lattice = build_state_lattice(variables, constants)

    bottom = ConstVal.bottom()
    bottom_state = State(
        frozenset((v, bottom) for v in variables)
    )

    prog = Program([
        AssignConst("x", 1),     # 1
        AssignVar("y", "x"),     # 2
        AddConst("z", "y", 1),   # 3
    ])

    nodes = set(prog.node_ids())
    edges = prog.linear_edges()
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

    assert out[1].get("x").value == 1
    assert out[2].get("y").value == 1
    assert out[3].get("z").value == 2
