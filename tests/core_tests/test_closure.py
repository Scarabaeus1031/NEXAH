import pytest
from ENGINE.core.poset import FinitePoset
from ENGINE.core.closure_operator import ClosureOperator


def simple_poset():
    elements = {"a", "b"}

    def leq(x, y):
        return x == y

    return FinitePoset(elements, leq)


def test_valid_closure():
    poset = simple_poset()

    def gamma(x):
        return x

    closure = ClosureOperator(poset, gamma)

    assert closure.fixpoints() == {"a", "b"}


def test_invalid_closure_extensive():
    poset = simple_poset()

    def bad_gamma(x):
        return "a" if x == "b" else x

    with pytest.raises(ValueError):
        ClosureOperator(poset, bad_gamma)
