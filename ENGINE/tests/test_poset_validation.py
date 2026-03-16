import pytest
from ENGINE.core.poset import FinitePoset


# -------------------------
# 1. Singleton Poset
# -------------------------

def test_singleton_poset():
    P = FinitePoset(elements={1}, leq=lambda x, y: True)
    assert P.is_leq(1, 1)


# -------------------------
# 2. Empty Poset
# -------------------------

def test_empty_poset():
    P = FinitePoset(elements=set(), leq=lambda x, y: False)
    assert P.elements == set()


# -------------------------
# 3. Reflexivity violation
# -------------------------

def test_non_reflexive():
    def leq(x, y):
        return x < y  # strict order, not reflexive

    with pytest.raises(ValueError):
        FinitePoset(elements={0, 1}, leq=leq)


# -------------------------
# 4. Antisymmetry violation
# -------------------------

def test_non_antisymmetric():
    def leq(x, y):
        return True  # everything comparable

    with pytest.raises(ValueError):
        FinitePoset(elements={0, 1}, leq=leq)


# -------------------------
# 5. Transitivity violation
# -------------------------

def test_non_transitive():
    def leq(x, y):
        return (x == y) or (x == 0 and y == 1) or (x == 1 and y == 2)

    with pytest.raises(ValueError):
        FinitePoset(elements={0, 1, 2}, leq=leq)
