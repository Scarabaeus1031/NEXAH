import pytest

from ENGINE.core.poset import FinitePoset
from ENGINE.core.fixpoint_lattice import (
    build_fixpoint_poset,
    build_fixpoint_structure,
)


# Simple chain poset: 0 <= 1 <= 2
def chain_poset():
    elements = {0, 1, 2}

    def leq(x, y):
        return x <= y

    return FinitePoset(elements=elements, leq=leq)


# -------------------------
# 1. All elements fixpoints
# -------------------------

def test_all_fixpoints():
    P = chain_poset()

    def identity(x):
        return x

    fp = build_fixpoint_poset(P, identity)

    assert fp.elements == {0, 1, 2}
    assert fp.is_leq(0, 2)


# -------------------------
# 2. Only top is fixpoint
# -------------------------

def test_single_fixpoint():
    P = chain_poset()

    def collapse_to_top(x):
        return 2

    fp = build_fixpoint_poset(P, collapse_to_top)

    assert fp.elements == {2}
    assert fp.is_leq(2, 2)


# -------------------------
# 3. No fixpoints
# -------------------------

def test_no_fixpoints():
    P = chain_poset()

    def shift(x):
        return (x + 1) % 3

    fp = build_fixpoint_poset(P, shift)

    assert fp.elements == set()


# -------------------------
# 4. Structure wrapper
# -------------------------

def test_fixpoint_structure_wrapper():
    P = chain_poset()

    def identity(x):
        return x

    structure = build_fixpoint_structure(P, identity)

    assert structure.poset.elements == {0, 1, 2}
    assert structure.lattice.poset is structure.poset
