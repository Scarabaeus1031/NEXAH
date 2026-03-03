import pytest

from ENGINE.core.poset import FinitePoset
from ENGINE.core.closure_operator import ClosureOperator


def nonlattice_poset():
    """
    Poset that is NOT a lattice:
    0 <= a, 0 <= b, but a and b have no join (no top element).
    """
    elements = {"0", "a", "b"}

    order = {
        ("0", "0"), ("a", "a"), ("b", "b"),
        ("0", "a"), ("0", "b"),
    }

    def leq(x, y):
        return (x, y) in order

    return FinitePoset(elements, leq)


def test_strict_fixpoint_lattice_failure():
    P = nonlattice_poset()

    def gamma(x):
        return x  # identity closure operator (valid)

    closure = ClosureOperator(P, gamma)

    # strict=True requires Fix(Γ) to form a lattice
    with pytest.raises(ValueError):
        _ = closure.fixpoint_lattice(strict=True)
