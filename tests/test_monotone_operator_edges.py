import pytest
from ENGINE.core.poset import FinitePoset
from ENGINE.core.monotone_operator import MonotoneOperator


def simple_chain():
    elems = {0, 1}

    def leq(x, y):
        return x <= y

    return FinitePoset(elems, leq)


def test_cycle_detection():
    P = simple_chain()
    f = lambda x: 1 - x  # not monotone
    with pytest.raises(ValueError):
        MonotoneOperator(P, f)


def test_iterate_max_steps():
    P = simple_chain()
    f = lambda x: x
    op = MonotoneOperator(P, f)

    result, traj = op.iterate_from(0, max_steps=1)
    assert result == 0
    assert traj[-1] == 0


def test_iterate_invalid_start():
    P = simple_chain()
    f = lambda x: x
    op = MonotoneOperator(P, f)

    with pytest.raises(ValueError):
        op.iterate_from(42)  # not in carrier


def test_least_fixpoint_no_unique():
    elems = {"a", "b"}

    def leq(x, y):
        return x == y  # incomparable elements

    P = FinitePoset(elems, leq)
    op = MonotoneOperator(P, lambda x: x)

    with pytest.raises(ValueError):
        op.least_fixpoint()


def test_greatest_fixpoint_no_unique():
    elems = {"a", "b"}

    def leq(x, y):
        return x == y

    P = FinitePoset(elems, leq)
    op = MonotoneOperator(P, lambda x: x)

    with pytest.raises(ValueError):
        op.greatest_fixpoint()


def test_tarski_requires_lattice():
    elems = {"a", "b"}

    def leq(x, y):
        return x == y  # not a lattice

    P = FinitePoset(elems, leq)
    op = MonotoneOperator(P, lambda x: x)

    with pytest.raises(ValueError):
        op.tarski_least_fixpoint()


def test_no_prefixed_points():
    elems = {0, 1}

    def leq(x, y):
        return x <= y

    P = FinitePoset(elems, leq)

    # f(x) = 1 always → no f(x) ≤ x except maybe 1
    f = lambda x: 1
    op = MonotoneOperator(P, f)

    with pytest.raises(ValueError):
        op.tarski_least_fixpoint()


def test_no_postfixed_points():
    elems = {0, 1}

    def leq(x, y):
        return x <= y

    P = FinitePoset(elems, leq)

    # f(x) = 0 always → no x ≤ f(x) except maybe 0
    f = lambda x: 0
    op = MonotoneOperator(P, f)

    with pytest.raises(ValueError):
        op.tarski_greatest_fixpoint()
