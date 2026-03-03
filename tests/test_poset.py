from ENGINE.core.poset import FinitePoset


def test_valid_poset_construction():
    elements = {"a", "b"}

    def leq(x, y):
        return x == y

    poset = FinitePoset(elements, leq)

    assert poset.is_leq("a", "a")
    assert poset.is_leq("b", "b")


def test_invalid_poset_transitivity():
    elements = {"a", "b", "c"}

    def bad_leq(x, y):
        if x == y:
            return True
        if x == "a" and y == "b":
            return True
        if x == "b" and y == "c":
            return True
        return False

    try:
        FinitePoset(elements, bad_leq)
        assert False  # Should not reach here
    except ValueError:
        assert True
