from ENGINE.core.poset import FinitePoset
from ENGINE.core.lattice import LatticeOps


def test_boolean_lattice_two_elements():
    elements = {"bottom", "top"}

    def leq(x, y):
        if x == y:
            return True
        if x == "bottom" and y == "top":
            return True
        return False

    poset = FinitePoset(elements, leq)
    lat = LatticeOps(poset)

    assert lat.is_lattice()
    assert lat.top() == "top"
    assert lat.bottom() == "bottom"
