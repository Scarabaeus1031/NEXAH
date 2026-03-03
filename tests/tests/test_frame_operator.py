from ENGINE.core.frame_operator import FrameOperator


def test_basic_projection():
    F = FrameOperator(lambda x: x % 2)

    assert F.apply(3) == 1
    assert F.apply(4) == 0


def test_project_set():
    F = FrameOperator(lambda x: x % 2)

    result = F.project_set({1, 2, 3, 4})

    assert result == {0, 1}


def test_non_injective_projection():
    F = FrameOperator(lambda x: 0)

    result = F.project_set({1, 2, 3})

    assert result == {0}
