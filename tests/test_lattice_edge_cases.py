import pytest

from ENGINE.core.poset import FinitePoset
from ENGINE.core.lattice import LatticeOps


def diamond_poset():
    # classic diamond M3 (non-distributive)
    elements = {"bottom", "a", "b", "top"}

    def leq(x, y):
        if x == y:
            return True
        if x == "bottom":
            return True
        if y == "top":
            return True
        return False

    return FinitePoset(elements, leq)


def test_join_not_unique():
    P = diamond_poset()
    L = LatticeOps(P)

    # join(a, b) = top (unique)
    assert L.join("a", "b") == "top"

    # meet(a, b) = bottom
    assert L.meet("a", "b") == "bottom"


def test_upper_bounds_empty_subset():
    P = diamond_poset()
    L = LatticeOps(P)

    with pytest.raises(ValueError):
        L.upper_bounds([])

    with pytest.raises(ValueError):
        L.lower_bounds([])


def test_is_lattice_true():
    P = diamond_poset()
    L = LatticeOps(P)

    assert L.is_lattice()


def test_is_distributive_false():
    P = diamond_poset()
    L = LatticeOps(P)

    # diamond is NOT distributive
    assert not L.is_distributive()
