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

    # In original: 1 ≤ 2
    # So 1%2=1 ≤_F 0=2%2
    assert FP.is_leq(1, 0)

    # reflexivity
    for x in FP.elements:
        assert FP.is_leq(x, x)


def test_frame_non_injective_order():
    P = simple_chain()
    F = FrameOperator(lambda x: 0)

    FP = F.on_poset(P)

    # Only one element
    assert FP.elements == {0}

    # must be reflexive
    assert FP.is_leq(0, 0)
