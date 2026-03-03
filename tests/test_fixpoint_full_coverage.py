from ENGINE.core.poset import FinitePoset
from ENGINE.core.fixpoint_lattice import (
    build_fixpoint_poset,
    build_fixpoint_structure,
)


def small_poset():
    elements = {"0", "a", "1"}

    order = {
        ("0","0"), ("a","a"), ("1","1"),
        ("0","a"), ("a","1"),
        ("0","1"),
    }

    def leq(x, y):
        return (x, y) in order

    return FinitePoset(elements, leq)


def test_no_fixpoints_except_top():
    P = small_poset()

    def gamma(x):
        return "1"

    fp = build_fixpoint_poset(P, gamma)

    assert fp.elements == {"1"}


def test_no_fixpoints_case():
    P = small_poset()

    def gamma(x):
        return "a"  # no element maps to itself except a

    fp = build_fixpoint_poset(P, gamma)

    assert "a" in fp.elements


def test_leq_inheritance_strict():
    P = small_poset()

    def gamma(x):
        return x

    fp = build_fixpoint_poset(P, gamma)

    assert fp.is_leq("0", "1")
    assert not fp.is_leq("1", "0")


def test_structure_builds_lattice_wrapper():
    P = small_poset()

    def gamma(x):
        return x

    struct = build_fixpoint_structure(P, gamma)

    assert hasattr(struct, "poset")
    assert hasattr(struct, "lattice")
    assert struct.lattice.is_lattice()
