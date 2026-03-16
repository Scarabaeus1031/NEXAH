from ENGINE.core.poset import FinitePoset
from ENGINE.core.frame_operator import FrameOperator


def simple_chain():
    elements = {1, 2, 3, 4}

    def leq(x, y):
        return x <= y

    return FinitePoset(elements, leq)


def test_frame_on_poset_elements():
    P = simple_chain()
    F = FrameOperator(lambda x: x % 2)

    FP = F.on_poset(P)

    assert FP.elements == {0, 1}


def test_frame_induced_order():
    P = simple_chain()
    F = FrameOperator(lambda x: x % 2)

    FP = F.on_poset(P)

    assert FP.is_leq(1, 0)

    for x in FP.elements:
        assert FP.is_leq(x, x)


def test_frame_non_injective_order():
    P = simple_chain()
    F = FrameOperator(lambda x: 0)

    FP = F.on_poset(P)

    assert FP.elements == {0}
    assert FP.is_leq(0, 0)
