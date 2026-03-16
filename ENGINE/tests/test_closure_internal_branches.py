import pytest

from ENGINE.core.poset import FinitePoset
from ENGINE.core.closure_operator import ClosureOperator


def chain_poset():
    elements = {"0", "1"}

    def leq(x, y):
        if x == y:
            return True
        if x == "0" and y == "1":
            return True
        return False

    return FinitePoset(elements, leq)


def test_extensive_branch_message():
    P = chain_poset()

    def gamma(x):
        return "0"  # breaks extensiveness for x="1"

    with pytest.raises(ValueError):
        ClosureOperator(P, gamma)


def test_monotone_branch_message():
    P = chain_poset()

    def gamma(x):
        if x == "0":
            return "1"
        return "0"  # breaks monotonicity

    with pytest.raises(ValueError):
        ClosureOperator(P, gamma)


def test_idempotent_branch_message():
    P = chain_poset()

    def gamma(x):
        return "1" if x == "0" else "0"  # not idempotent

    with pytest.raises(ValueError):
        ClosureOperator(P, gamma)


def test_strict_true_error_branch():
    # Non-lattice poset to trigger strict=True failure
    elements = {"0", "a", "b"}

    order = {
        ("0","0"), ("a","a"), ("b","b"),
        ("0","a"), ("0","b"),
    }

    def leq(x, y):
        return (x, y) in order

    P = FinitePoset(elements, leq)

    def gamma(x):
        return x

    closure = ClosureOperator(P, gamma)

    with pytest.raises(ValueError):
        closure.fixpoint_lattice(strict=True)
