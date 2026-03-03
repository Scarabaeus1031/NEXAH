from ENGINE.core.poset import FinitePoset
from ENGINE.core.fixpoint_lattice import (
    build_fixpoint_poset,
    build_fixpoint_structure,
)


def sample_poset():
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


def test_multiple_fixpoints():
    P = sample_poset()

    def gamma(x):
        if x == "a":
            return "1"
        return x

    fp = build_fixpoint_poset(P, gamma)

    assert fp.elements == {"0", "b", "1"}


def test_single_fixpoint():
    P = sample_poset()

    def gamma(x):
        return "1"

    fp = build_fixpoint_poset(P, gamma)

    assert fp.elements == {"1"}


def test_leq_is_inherited():
    P = sample_poset()

    def gamma(x):
        return x

    fp = build_fixpoint_poset(P, gamma)

    assert fp.is_leq("0", "1")
    assert not fp.is_leq("a", "b")


def test_structure_wrapper():
    P = sample_poset()

    def gamma(x):
        return x

    struct = build_fixpoint_structure(P, gamma)

    assert struct.poset.elements == P.elements
    assert struct.lattice.is_lattice()
