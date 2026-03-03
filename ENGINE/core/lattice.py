import pytest
from ENGINE.core.poset import FinitePoset
from ENGINE.core.lattice import LatticeOps


# -------------------------------------------------
# Helper posets
# -------------------------------------------------

def chain_poset():
    # 0 <= 1 <= 2
    elements = {0, 1, 2}
    return FinitePoset(elements, lambda x, y: x <= y)


def vee_poset():
    # V-shape:
    #   1   2
    #    \ /
    #     0
    elements = {0, 1, 2}

    def leq(x, y):
        if x == y:
            return True
        if x == 0:
            return True
        return False

    return FinitePoset(elements, leq)


# -------------------------------------------------
# 1. upper_bounds / lower_bounds empty input
# -------------------------------------------------

def test_upper_bounds_empty():
    L = LatticeOps(chain_poset())
    with pytest.raises(ValueError):
        L.upper_bounds([])


def test_lower_bounds_empty():
    L = LatticeOps(chain_poset())
    with pytest.raises(ValueError):
        L.lower_bounds([])


# -------------------------------------------------
# 2. join does not exist (vee shape)
# -------------------------------------------------

def test_join_not_unique():
    L = LatticeOps(vee_poset())
    with pytest.raises(ValueError):
        L.join(1, 2)


def test_meet_not_unique():
    L = LatticeOps(vee_poset())
    with pytest.raises(ValueError):
        L.meet(1, 2)


# -------------------------------------------------
# 3. is_lattice false
# -------------------------------------------------

def test_is_not_lattice():
    L = LatticeOps(vee_poset())
    assert not L.is_lattice()


# -------------------------------------------------
# 4. distributivity failure (diamond lattice M3)
# -------------------------------------------------

def diamond_poset():
    # classic nondistributive lattice M3
    #    3
    #   / \
    #  1   2
    #   \ /
    #    0
    elements = {0, 1, 2, 3}

    def leq(x, y):
        if x == y:
            return True
        if x == 0:
            return True
        if y == 3:
            return True
        if x in {1, 2} and y == 3:
            return True
        return False

    return FinitePoset(elements, leq)


def test_not_distributive():
    L = LatticeOps(diamond_poset())
    assert L.is_lattice()
    assert not L.is_distributive()


# -------------------------------------------------
# 5. top / bottom
# -------------------------------------------------

def test_top_bottom_chain():
    L = LatticeOps(chain_poset())
    assert L.top() == 2
    assert L.bottom() == 0


def test_no_unique_top():
    L = LatticeOps(vee_poset())
    assert L.top() is None
