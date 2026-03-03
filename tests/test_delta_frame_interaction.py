import pytest

from ENGINE.core.poset import FinitePoset
from ENGINE.core.regime_operator import RegimeOperator
from ENGINE.core.frame_operator import FrameOperator


# -------------------------------------------------
# Helper: simple chain 1 ≤ 2 ≤ 3 ≤ 4
# -------------------------------------------------

def simple_chain():
    elements = {1, 2, 3, 4}

    def leq(x, y):
        return x <= y

    return FinitePoset(elements, leq)


# -------------------------------------------------
# Case 1 — Δ and F commute (trivial case)
# -------------------------------------------------

def test_delta_frame_commute_simple_case():
    P = simple_chain()

    Δ = RegimeOperator(P)
    F = FrameOperator(lambda x: x)  # identity frame

    P_delta = Δ.restrict(lambda x: x >= 2)
    P1 = F.on_poset(P_delta)

    P_frame = F.on_poset(P)
    Δ2 = RegimeOperator(P_frame)
    P2 = Δ2.restrict(lambda x: x >= 2)

    assert P1.elements == P2.elements


# -------------------------------------------------
# Case 2 — Δ ∘ F ≠ F ∘ Δ (non-commutative case)
# -------------------------------------------------

def test_delta_frame_non_commutative():
    P = simple_chain()

    Δ = RegimeOperator(P)
    F = FrameOperator(lambda x: x % 2)

    # Δ first, then F
    P_delta = Δ.restrict(lambda x: x >= 3)  # {3,4}
    P1 = F.on_poset(P_delta)

    # F first, then Δ
    P_frame = F.on_poset(P)  # {0,1}
    Δ2 = RegimeOperator(P_frame)
    P2 = Δ2.restrict(lambda x: x == 1)

    # They should differ structurally
    assert P1.elements != P2.elements


# -------------------------------------------------
# Case 3 — Frame collapses before regime
# -------------------------------------------------

def test_frame_collapses_structure_before_regime():
    P = simple_chain()

    Δ = RegimeOperator(P)
    F = FrameOperator(lambda x: 0)  # full collapse

    # F first collapses everything
    P_frame = F.on_poset(P)
    assert P_frame.elements == {0}

    Δ2 = RegimeOperator(P_frame)

    # Any non-empty restriction remains trivial
    P2 = Δ2.restrict(lambda x: True)
    assert P2.elements == {0}

    # Δ first keeps structure
    P_delta = Δ.restrict(lambda x: x >= 3)
    assert P_delta.elements == {3, 4}
