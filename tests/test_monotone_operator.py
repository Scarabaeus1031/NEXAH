import pytest

from ENGINE.core.poset import FinitePoset
from ENGINE.core.monotone_operator import MonotoneOperator


def chain_3():
    # 0 < a < 1
    elements = {"0", "a", "1"}
    order = {
        ("0", "0"), ("a", "a"), ("1", "1"),
        ("0", "a"), ("a", "1"),
        ("0", "1"),
    }

    def leq(x, y):
        return (x, y) in order

    return FinitePoset(elements, leq)


def test_monotone_accepts_nonclosure():
    P = chain_3()

    # Monotone but NOT extensive: f(1)=0 violates 1 ≤ f(1)
    def f(x):
        return {"0": "0", "a": "1", "1": "0"}[x]

    M = MonotoneOperator(P, f)
    assert M.apply("a") == "1"


def test_monotone_rejects_nonmonotone():
    P = chain_3()

    # Not monotone: 0 ≤ a but f(0)=1 not ≤ f(a)=0
    def bad(x):
        return {"0": "1", "a": "0", "1": "1"}[x]

    with pytest.raises(ValueError):
        MonotoneOperator(P, bad)


def test_fixpoints_and_least_greatest():
    P = chain_3()

    # f has fixpoints {0,1}
    def f(x):
        return {"0": "0", "a": "1", "1": "1"}[x]

    M = MonotoneOperator(P, f)
    assert M.fixpoints() == {"0", "1"}
    assert M.least_fixpoint() == "0"
    assert M.greatest_fixpoint() == "1"


def test_iteration_detects_cycle():
    P = chain_3()

    # 0 -> a -> 0 (cycle), 1 -> 1 (fixpoint)
    def f(x):
        return {"0": "a", "a": "0", "1": "1"}[x]

    M = MonotoneOperator(P, f)

    fx, traj = M.iterate_from("1")
    assert fx == "1"
    assert traj[-1] == "1"

    with pytest.raises(RuntimeError):
        M.iterate_from("0", max_steps=20)
