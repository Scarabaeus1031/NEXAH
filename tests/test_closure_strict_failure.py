import pytest

from ENGINE.core.poset import FinitePoset
from ENGINE.core.closure_operator import ClosureOperator


def non_lattice_poset():
    """
    Poset where join does not exist uniquely.
    """
    elements = {"0", "a", "b"}

    # 0 < a
    # 0 < b
    # a and b incomparable
    order = {
        ("0", "0"), ("a", "a"), ("b", "b"),
        ("0", "a"), ("0", "b"),
    }

    def leq(x, y):
        return (x, y) in order

    return FinitePoset(elements, leq)


def test_strict_fixpoint_lattice_failure():
    P = non_lattice_poset()

    def gamma(x):
        return x  # identity closure

    closure = ClosureOperator(P, gamma)

    # Fix(Γ) = P, but P is NOT a lattice
    with pytest.raises(ValueError):
        closure.fixpoint_lattice(strict=True)
