from ENGINE.core.poset import FinitePoset
from ENGINE.core.fixpoint_lattice import (
    build_fixpoint_poset,
    build_fixpoint_structure,
)


def poset_with_top():
    elements = {"0", "a", "1"}

    order = {
        ("0","0"), ("a","a"), ("1","1"),
        ("0","a"), ("a","1"),
        ("0","1"),
    }

    def leq(x, y):
        return (x, y) in order

    return FinitePoset(elements, leq)


def test_fixpoint_poset_multiple():
    P = poset_with_top()

    def gamma(x):
        return x

    fp = build_fixpoint_poset(P, gamma)

    assert fp.elements == {"0", "a", "1"}
    assert fp.is_leq("0", "1")


def test_fixpoint_structure_delegations():
    P = poset_with_top()

    def gamma(x):
        return x

    struct = build_fixpoint_structure(P, gamma)

    # Lattice checks
    assert struct.is_lattice()
    assert not struct.is_distributive()

    # Extremal elements
    assert struct.top() == "1"
    assert struct.bottom() == "0"

    # Join / Meet
    assert struct.join("0", "a") == "a"
    assert struct.meet("a", "1") == "a"
