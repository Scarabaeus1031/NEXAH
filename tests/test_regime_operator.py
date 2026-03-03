import pytest

from ENGINE.core.poset import FinitePoset
from ENGINE.core.regime_operator import RegimeOperator
from ENGINE.core.lattice import LatticeOps
from ENGINE.core.closure_operator import ClosureOperator


# -------------------------------------------------
# Basic restriction
# -------------------------------------------------

def test_basic_restriction():
    elements = {1, 2, 3, 4}

    def leq(x, y):
        return x <= y

    P = FinitePoset(elements, leq)
    Δ = RegimeOperator(P)

    P2 = Δ.restrict(lambda x: x >= 3)

    assert P2.elements == {3, 4}
    assert P2.is_leq(3, 4)
    assert not P2.is_leq(4, 3)


# -------------------------------------------------
# Empty restriction must fail
# -------------------------------------------------

def test_empty_restriction_fails():
    elements = {1, 2}

    def leq(x, y):
        return x <= y

    P = FinitePoset(elements, leq)
    Δ = RegimeOperator(P)

    with pytest.raises(ValueError):
        Δ.restrict(lambda x: False)


# -------------------------------------------------
# Order structure preserved
# -------------------------------------------------

def test_restriction_preserves_order_structure():
    elements = {1, 2, 3, 4}

    def leq(x, y):
        return x <= y

    P = FinitePoset(elements, leq)
    Δ = RegimeOperator(P)

    P2 = Δ.restrict(lambda x: x % 2 == 0)

    # reflexivity
    for x in P2.elements:
        assert P2.is_leq(x, x)

    # transitivity
    for a in P2.elements:
        for b in P2.elements:
            for c in P2.elements:
                if P2.is_leq(a, b) and P2.is_leq(b, c):
                    assert P2.is_leq(a, c)


# -------------------------------------------------
# Δ can destroy lattice structure (true example)
# -------------------------------------------------

def test_lattice_can_be_destroyed():
    elements = {"bottom", "a", "b", "top"}

    order = {
        ("bottom", "bottom"),
        ("a", "a"),
        ("b", "b"),
        ("top", "top"),
        ("bottom", "a"),
        ("bottom", "b"),
        ("a", "top"),
        ("b", "top"),
        ("bottom", "top"),
    }

    def leq(x, y):
        return (x, y) in order

    P = FinitePoset(elements, leq)
    Δ = RegimeOperator(P)

    # Remove top element → destroys join for a,b
    P2 = Δ.restrict(lambda x: x != "top")

    lat = LatticeOps(P2)

    assert not lat.is_lattice()


# -------------------------------------------------
# Closure inside regime
# -------------------------------------------------

def test_closure_inside_regime():
    elements = {0, 1, 2}

    def leq(x, y):
        return x <= y

    P = FinitePoset(elements, leq)

    def gamma(x):
        return min(x + 1, 2)

    Γ = ClosureOperator(P, gamma)
    Δ = RegimeOperator(P)

    P2 = Δ.restrict(lambda x: x >= 1)

    # Closure restricted to regime
    Γ2 = ClosureOperator(P2, gamma)

    assert Γ2.apply(1) in P2.elements
