from ENGINE.core.poset import FinitePoset
from ENGINE.core.closure_operator import ClosureOperator


def simple_chain():
    elements = {"0", "1"}

    def leq(x, y):
        if x == y:
            return True
        if x == "0" and y == "1":
            return True
        return False

    return FinitePoset(elements, leq)


def test_apply_method():
    P = simple_chain()

    def gamma(x):
        return "1"

    closure = ClosureOperator(P, gamma)

    assert closure.apply("0") == "1"


def test_fixpoint_lattice_non_strict():
    P = simple_chain()

    def gamma(x):
        return x

    closure = ClosureOperator(P, gamma)

    struct = closure.fixpoint_lattice(strict=False)

    assert struct.lattice.is_lattice()


def test_fixpoint_lattice_strict_success():
    P = simple_chain()

    def gamma(x):
        return x

    closure = ClosureOperator(P, gamma)

    struct = closure.fixpoint_lattice(strict=True)

    assert struct.lattice.is_lattice()
