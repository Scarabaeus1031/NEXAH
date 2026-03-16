from ENGINE.core.poset import FinitePoset
from ENGINE.core.closure_operator import ClosureOperator


def test_fixpoint_lattice_structure():
    elements = {"bottom", "a", "top"}

    def leq(x, y):
        if x == y:
            return True
        if x == "bottom":
            return True
        if y == "top":
            return True
        return False

    poset = FinitePoset(elements, leq)

    def gamma(x):
        if x == "bottom":
            return "a"
        return x

    closure = ClosureOperator(poset, gamma)

    fp_lattice = closure.fixpoint_lattice(strict=True)

    assert fp_lattice.is_lattice()
