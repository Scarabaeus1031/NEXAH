import pytest

from ENGINE.core.poset import FinitePoset
from ENGINE.core.closure_operator import ClosureOperator


def nondistributive_poset():
    elements = {"0", "a", "b", "c", "1"}

    order = {
        ("0","0"), ("a","a"), ("b","b"), ("c","c"), ("1","1"),
        ("0","a"), ("0","b"), ("0","c"),
        ("a","1"), ("b","1"), ("c","1"),
        ("0","1"),
    }

    def leq(x, y):
        return (x, y) in order

    return FinitePoset(elements, leq)


def test_strict_fixpoint_lattice_failure():
    P = nondistributive_poset()

    def gamma(x):
        return x  # identity closure

    closure = ClosureOperator(P, gamma)

    # strict=True should fail because lattice is not distributive
    with pytest.raises(ValueError):
        closure.fixpoint_lattice(strict=True)
