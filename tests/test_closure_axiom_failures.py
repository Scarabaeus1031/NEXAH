import pytest

from ENGINE.core.poset import FinitePoset
from ENGINE.core.closure_operator import ClosureOperator


def simple_poset():
    elements = {"0", "1"}

    def leq(x, y):
        if x == y:
            return True
        if x == "0" and y == "1":
            return True
        return False

    return FinitePoset(elements, leq)


def test_gamma_not_in_carrier():
    P = simple_poset()

    def gamma(x):
        return "invalid"

    with pytest.raises(ValueError):
        ClosureOperator(P, gamma)


def test_not_extensive():
    P = simple_poset()

    def gamma(x):
        return "0"  # 1 ↦ 0 violates extensiveness

    with pytest.raises(ValueError):
        ClosureOperator(P, gamma)


def test_not_monotone():
    P = simple_poset()

    def gamma(x):
        if x == "0":
            return "1"
        return "0"  # breaks monotonicity

    with pytest.raises(ValueError):
        ClosureOperator(P, gamma)


def test_not_idempotent():
    P = simple_poset()

    def gamma(x):
        return "1" if x == "0" else "0"  # flips each time

    with pytest.raises(ValueError):
        ClosureOperator(P, gamma)
