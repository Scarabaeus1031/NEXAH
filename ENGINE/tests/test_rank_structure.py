from ENGINE.core.poset import FinitePoset
from ENGINE.core.rank import RankStructure


def simple_chain():
    elements = {0, 1, 2, 3}

    def leq(x, y):
        return x <= y

    return FinitePoset(elements, leq)


def test_chain_height():
    P = simple_chain()
    R = RankStructure(P)

    assert R.height(0) == 0
    assert R.height(1) == 1
    assert R.height(2) == 2
    assert R.height(3) == 3
    assert R.max_height() == 3


def test_diamond_poset():
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
    R = RankStructure(P)

    assert R.height("bottom") == 0
    assert R.height("a") == 1
    assert R.height("b") == 1
    assert R.height("top") == 2
    assert R.max_height() == 2
