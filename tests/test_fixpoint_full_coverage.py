from ENGINE.core.poset import FinitePoset
from ENGINE.core.fixpoint_lattice import (
    build_fixpoint_poset,
    build_fixpoint_structure,
)


def lattice_poset():
    elements = {"0", "a", "b", "1"}

    order = {
        ("0","0"), ("a","a"), ("b","b"), ("1","1"),
        ("0","a"), ("0","b"),
        ("a","1"), ("b","1"),
        ("0","1"),
    }

    def leq(x, y):
        return (x, y) in order

    return FinitePoset(elements, leq)


def test_fixpoint_poset_basic():
    P = lattice_poset()

    def gamma(x):
        return x

    fp = build_fixpoint_poset(P, gamma)

    assert fp.elements == P.elements
    assert fp.is_leq("0", "1")


def test_structure_delegations_complete():
    P = lattice_poset()

    def gamma(x):
        return x

    struct = build_fixpoint_structure(P, gamma)

    # Direct delegation calls
    assert struct.is_lattice()
    assert not struct.is_distributive()

    assert struct.top() == "1"
    assert struct.bottom() == "0"

    # Explicitly call join/meet on multiple pairs
    assert struct.join("a", "b") == "1"
    assert struct.meet("a", "b") == "0"

    assert struct.join("0", "a") == "a"
    assert struct.meet("a", "1") == "a"
