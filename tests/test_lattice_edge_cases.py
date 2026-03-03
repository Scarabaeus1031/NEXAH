import pytest

from ENGINE.core.poset import FinitePoset
from ENGINE.core.lattice import LatticeOps


def nondistributive_poset():
    """
    Classic N5 lattice (guaranteed non-distributive)
    """

    elements = {"0", "a", "b", "c", "1"}

    def leq(x, y):
        if x == y:
            return True
        if x == "0":
            return True
        if y == "1":
            return True
        if x == "a" and y == "c":
            return True
        if x == "c" and y == "1":
            return True
        if x == "0" and y in {"a", "b"}:
            return True
        if x == "b" and y == "1":
            return True
        return False

    return FinitePoset(elements, leq)


def test_join_and_meet():
    P = nondistributive_poset()
    L = LatticeOps(P)

    assert L.join("a", "b") == "1"
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

    assert L.is_lattice()


def test_is_distributive_false():
    P = nondistributive_poset()
    L = LatticeOps(P)

    assert not L.is_distributive()
