import pytest

from ENGINE.core.poset import FinitePoset
from ENGINE.core.regime_operator import RegimeOperator


def test_basic_restriction():
    elements = {1, 2, 3, 4}
    def leq(x, y): return x <= y

    P = FinitePoset(elements, leq)
    Δ = RegimeOperator(P)

    P2 = Δ.restrict(lambda x: x >= 3)

    assert P2.elements == {3, 4}
    assert P2.is_leq(3, 4)
    assert not P2.is_leq(4, 3)


def test_empty_restriction_fails():
    elements = {1, 2}
    def leq(x, y): return x <= y

    P = FinitePoset(elements, leq)
    Δ = RegimeOperator(P)

    with pytest.raises(ValueError):
        Δ.restrict(lambda x: False)
