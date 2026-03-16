import pytest

from ENGINE.core.poset import FinitePoset
from ENGINE.core.closure_operator import ClosureOperator


def non_lattice_poset():
    elements = {"x", "y"}

    def leq(a, b):
        return a == b  # no relation between x and y

    return FinitePoset(elements, leq)


def test_strict_failure():
    P = non_lattice_poset()

    def gamma(x):
        return x

    closure = ClosureOperator(P, gamma)

    with pytest.raises(ValueError):
        closure.fixpoint_lattice(strict=True)
