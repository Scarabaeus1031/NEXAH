import pytest

from ENGINE.core.poset import FinitePoset
from ENGINE.core.lattice import LatticeOps


def nondistributive_poset():
    """
    True M3 lattice (5 elements, non-distributive).
    """

    elements = {"0", "a", "b", "c", "1"}

    order = {
        # reflexive
        ("0", "0"), ("a", "a"), ("b", "b"), ("c", "c"), ("1", "1"),

        # bottom relations
        ("0", "a"), ("0", "b"), ("0", "c"),

        # top relations
        ("a", "1"), ("b", "1"), ("c", "1"),

        # transitive
        ("0", "1"),
    }

    def leq(x, y):
        return (x, y) in order

    return FinitePoset(elements, leq)


def test_join_and_meet():
    P = nondistributive_poset()
    L = LatticeOps(P)

    # join of incomparable elements → top
    assert L.join("a", "b") == "1"

    # meet of incomparable elements → bottom
    assert L.meet("a", "b") == "0"


def test_upper_bounds_empty_subset():
    P = nondistributive_poset()
    L = LatticeOps(P)

    with pytest.raises(ValueError):
        L.upper_bounds([])

    with pytest.raises(ValueError):
        L.lower_bounds([])


def test_is_lattice_true():
    P = nondistributive_poset()
    L = LatticeOps(P)

    # M3 is a lattice (but not distributive)
    assert L.is_lattice()


def test_is_distributive_false():
    P = nondistributive_poset()
    L = LatticeOps(P)

    # M3 is NOT distributive
    assert not L.is_distributive()
