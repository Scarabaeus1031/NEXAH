import pytest

from ENGINE.core.poset import FinitePoset
from ENGINE.core.worklist_fixpoint import solve_worklist


def powerset_lattice(elements):
    """
    Build powerset lattice of a finite base set.
    Carrier = all frozensets.
    Order = subset.
    """
    base = list(elements)
    carrier = set()

    # brute-force powerset
    n = len(base)
    for mask in range(1 << n):
        s = frozenset(base[i] for i in range(n) if (mask >> i) & 1)
        carrier.add(s)

    def leq(a, b):
        return a.issubset(b)

    return FinitePoset(carrier, leq)


def test_reaches_fixpoint_on_chain():
    # nodes: A -> B -> C
    nodes = ["A", "B", "C"]
    edges = [("A", "B"), ("B", "C")]

    lat_poset = powerset_lattice({"x"})

    # initial facts: A has {x}, others empty
    init = {
        "A": frozenset({"x"}),
        "B": frozenset(),
        "C": frozenset(),
    }

    # propagate along edges: transfer just forwards input
    def transfer(node, in_val):
        return in_val

    res = solve_worklist(nodes, edges, lat_poset, init, transfer)

    assert res.values["A"] == frozenset({"x"})
    assert res.values["B"] == frozenset({"x"})
    assert res.values["C"] == frozenset({"x"})


def test_join_merges_multiple_predecessors():
    # A -> C, B -> C
    nodes = ["A", "B", "C"]
    edges = [("A", "C"), ("B", "C")]

    lat_poset = powerset_lattice({"x", "y"})

    init = {
        "A": frozenset({"x"}),
        "B": frozenset({"y"}),
        "C": frozenset(),
    }

    def transfer(node, in_val):
        return in_val

    res = solve_worklist(nodes, edges, lat_poset, init, transfer)

    assert res.values["C"] == frozenset({"x", "y"})


def test_transfer_must_return_lattice_element():
    nodes = ["A", "B"]
    edges = [("A", "B")]

    lat_poset = powerset_lattice({"x"})

    init = {"A": frozenset({"x"}), "B": frozenset()}

    def bad_transfer(node, in_val):
        return {"x"}  # not frozenset -> not in carrier

    with pytest.raises(ValueError):
        solve_worklist(nodes, edges, lat_poset, init, bad_transfer)


def test_missing_initial_raises():
    nodes = ["A", "B"]
    edges = [("A", "B")]

    lat_poset = powerset_lattice({"x"})

    init = {"A": frozenset({"x"})}  # missing B

    def transfer(node, in_val):
        return in_val

    with pytest.raises(ValueError):
        solve_worklist(nodes, edges, lat_poset, init, transfer)
