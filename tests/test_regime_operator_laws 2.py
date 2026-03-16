import pytest

from ENGINE.core.poset import FinitePoset
from ENGINE.core.regime_operator import RegimeOperator


# -------------------------------------------------
# Helper poset
# -------------------------------------------------

def simple_chain():
    elements = {1, 2, 3, 4}

    def leq(x, y):
        return x <= y

    return FinitePoset(elements, leq)


# -------------------------------------------------
# Idempotence: Δ_φ ∘ Δ_φ = Δ_φ
# -------------------------------------------------

def test_delta_idempotent():
    P = simple_chain()
    Δ = RegimeOperator(P)

    φ = lambda x: x >= 2

    P1 = Δ.restrict(φ)
    Δ1 = RegimeOperator(P1)

    P2 = Δ1.restrict(φ)

    assert P1.elements == P2.elements


# -------------------------------------------------
# Composition: Δ_φ ∘ Δ_ψ = Δ_{φ ∧ ψ}
# -------------------------------------------------

def test_delta_composition_equals_intersection():
    P = simple_chain()
    Δ = RegimeOperator(P)

    φ = lambda x: x >= 2
    ψ = lambda x: x % 2 == 0

    # Δ_ψ first
    Pψ = Δ.restrict(ψ)
    Δψ = RegimeOperator(Pψ)

    # then Δ_φ
    Pφψ = Δψ.restrict(φ)

    # Direct intersection
    P_direct = Δ.restrict(lambda x: φ(x) and ψ(x))

    assert Pφψ.elements == P_direct.elements


# -------------------------------------------------
# Predicate monotonicity:
# If φ ⊆ ψ then Δ_φ(P) ⊆ Δ_ψ(P)
# -------------------------------------------------

def test_delta_predicate_monotonicity():
    P = simple_chain()
    Δ = RegimeOperator(P)

    φ = lambda x: x >= 3
    ψ = lambda x: x >= 2

    Pφ = Δ.restrict(φ)
    Pψ = Δ.restrict(ψ)

    assert Pφ.elements.issubset(Pψ.elements)
