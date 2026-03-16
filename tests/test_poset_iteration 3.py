from ENGINE.core.poset import FinitePoset


def simple_chain():
    elements = {0, 1, 2}

    def leq(x, y):
        return x <= y

    return FinitePoset(elements, leq)


def test_iterate_until_fixpoint():
    P = simple_chain()

    def f(x):
        return min(x + 1, 2)

    result = P.iterate_until_fixpoint(f, 0)

    assert result == 2
