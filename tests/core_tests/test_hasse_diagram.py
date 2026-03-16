from ENGINE.core.poset import FinitePoset
from ENGINE.core.hasse import HasseDiagram


def simple_chain():
    elements = {0, 1, 2, 3}

    def leq(x, y):
        return x <= y

    return FinitePoset(elements, leq)


def test_chain_covers():
    P = simple_chain()
    H = HasseDiagram(P)

    covers = H.covers()

    assert covers == {(0, 1), (1, 2), (2, 3)}


def test_diamond_covers():
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
    H = HasseDiagram(P)

    covers = H.covers()

    assert covers == {
        ("bottom", "a"),
        ("bottom", "b"),
        ("a", "top"),
        ("b", "top"),
    }
