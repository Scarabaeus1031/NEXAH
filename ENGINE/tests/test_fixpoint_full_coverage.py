from ENGINE.core.poset import FinitePoset
from ENGINE.core.fixpoint_lattice import (
    build_fixpoint_poset,
    build_fixpoint_structure,
)


def full_lattice():
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


def test_reduced_fixpoints():
    P = full_lattice()

    def gamma(x):
        if x == "a":
            return "1"
        return x

    fp = build_fixpoint_poset(P, gamma)

    assert fp.elements == {"0", "b", "1"}


def test_full_structure_calls_all_delegations():
    P = full_lattice()

    def gamma(x):
        return x

    struct = build_fixpoint_structure(P, gamma)

    # Delegations
    assert struct.is_lattice()
    assert struct.is_distributive()

    # Extremal
    assert struct.top() == "1"
    assert struct.bottom() == "0"

    # Join / Meet — trigger multiple paths
    assert struct.join("a", "b") == "1"
    assert struct.join("0", "a") == "a"

    assert struct.meet("a", "b") == "0"
    assert struct.meet("a", "1") == "a"


def test_single_fixpoint_case():
    P = full_lattice()

    def gamma(x):
        return "1"

    struct = build_fixpoint_structure(P, gamma)

    assert struct.poset.elements == {"1"}
    assert struct.top() == "1"
    assert struct.bottom() == "1"
