import pytest

from ENGINE.core.poset import FinitePoset
from ENGINE.core.interior_operator import InteriorOperator


def chain_poset(n=3):
    elements = set(range(n + 1))

    def leq(x, y):
        return x <= y

    return FinitePoset(elements, leq)


# ----------------------------
# A correct interior example:
# clamp to {0,2} by mapping:
# I(0)=0, I(1)=0, I(2)=2, I(3)=2, ...
# This is contractive, monotone, idempotent.
# ----------------------------

def test_interior_axioms_hold():
    P = chain_poset(3)

    def I(x):
        return 0 if x < 2 else 2

    op = InteriorOperator(P, I)

    # contractive
    for x in P.elements:
        assert P.is_leq(op.apply(x), x)

    # monotone (checked in ctor, but we sanity-check)
    for x in P.elements:
        for y in P.elements:
            if P.is_leq(x, y):
                assert P.is_leq(op.apply(x), op.apply(y))

    # idempotent
    for x in P.elements:
        assert op.apply(op.apply(x)) == op.apply(x)


def test_interior_not_contractive_fails():
    P = chain_poset(2)

    def bad_I(x):
        return min(2, x + 1)  # expansive -> violates contractive

    with pytest.raises(ValueError):
        InteriorOperator(P, bad_I)


def test_interior_not_idempotent_fails():
    P = chain_poset(3)

    def not_idempotent(x):
        return max(0, x - 1)  # contractive+monotone, but NOT idempotent

    with pytest.raises(ValueError):
        InteriorOperator(P, not_idempotent)


def test_interior_fixpoints():
    P = chain_poset(3)

    def I(x):
        return 0 if x < 2 else 2

    op = InteriorOperator(P, I)
    assert op.fixpoints() == {0, 2}


def test_interior_stabilize():
    P = chain_poset(5)

    def I(x):
        return 0 if x < 2 else 2

    op = InteriorOperator(P, I)
    assert op.stabilize(5) == 2
    assert op.stabilize(1) == 0


def test_interior_must_return_carrier_element():
    P = chain_poset(2)

    def bad_I(x):
        return "oops"  # not in carrier

    with pytest.raises(ValueError):
        InteriorOperator(P, bad_I)
