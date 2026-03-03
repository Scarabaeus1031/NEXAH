import pytest
from ENGINE.core.worklist_fixpoint import solve_worklist
from ENGINE.core.poset import FinitePoset


def simple_lattice():
    elems = {0}
    def leq(x, y): return True
    return FinitePoset(elems, leq)


def test_missing_initial():
    P = simple_lattice()
    nodes = {1}
    edges = set()

    with pytest.raises(ValueError):
        solve_worklist(
            nodes=nodes,
            edges=edges,
            value_poset=P,
            initial_in={},   # missing
            transfer=lambda n, v: v,
        )


def test_max_pops_trigger():
    P = simple_lattice()
    nodes = {1}
    edges = {(1, 1)}

    initial = {1: 0}

    def transfer(n, v):
        return v

    with pytest.raises(RuntimeError):
        solve_worklist(
            nodes=nodes,
            edges=edges,
            value_poset=P,
            initial_in=initial,
            transfer=transfer,
            max_pops=0,
        )
