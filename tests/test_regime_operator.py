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
def test_restriction_preserves_order_structure():
    elements = {1, 2, 3, 4}
    def leq(x, y): return x <= y

    P = FinitePoset(elements, leq)
    Δ = RegimeOperator(P)

    P2 = Δ.restrict(lambda x: x % 2 == 0)

    # check reflexivity
    for x in P2.elements:
        assert P2.is_leq(x, x)

    # check transitivity
    for a in P2.elements:
        for b in P2.elements:
            for c in P2.elements:
                if P2.is_leq(a, b) and P2.is_leq(b, c):
                    assert P2.is_leq(a, c)

from ENGINE.core.lattice import LatticeOps


def test_lattice_can_be_destroyed():
    elements = {0, 1, 2}
    def leq(x, y): return x <= y

    P = FinitePoset(elements, leq)
    Δ = RegimeOperator(P)

    # remove top element
    P2 = Δ.restrict(lambda x: x < 2)

    lat = LatticeOps(P2)

    # This might no longer be a full lattice
    assert not lat.is_lattice()

from ENGINE.core.closure_operator import ClosureOperator


def test_closure_inside_regime():
    elements = {0, 1, 2}
    def leq(x, y): return x <= y

    P = FinitePoset(elements, leq)

    def gamma(x):
        return min(x + 1, 2)

    Γ = ClosureOperator(P, gamma)
    Δ = RegimeOperator(P)

    P2 = Δ.restrict(lambda x: x >= 1)

    # closure inside regime
    Γ2 = ClosureOperator(P2, gamma)

    assert Γ2.apply(1) in P2.elements
