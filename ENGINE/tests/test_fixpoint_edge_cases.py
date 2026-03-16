import pytest

from ENGINE.core.poset import FinitePoset
from ENGINE.core.fixpoint_lattice import (
    build_fixpoint_poset,
    build_fixpoint_structure,
)


def sample_poset():
    elements = {"0", "a", "b", "1"}

    order = {
        ("0", "0"), ("a", "a"), ("b", "b"), ("1", "1"),
        ("0", "a"), ("0", "b"),
        ("a", "1"), ("b", "1"),
        ("0", "1"),
    }

    def leq(x, y):
        return (x, y) in order

    return FinitePoset(elements, leq)


def test_only_fixpoints_selected():
    P = sample_poset()

    def gamma(x):
        if x == "a":
            return "1"
        return x

    fp = build_fixpoint_poset(P, gamma)

    # a is NOT a fixpoint anymore
    assert "a" not in fp.elements
    assert "0" in fp.elements
    assert "b" in fp.elements
    assert "1" in fp.elements


def test_leq_inherited_correctly():
    P = sample_poset()

    def gamma(x):
        return x

    fp = build_fixpoint_poset(P, gamma)

    # inherited order must behave exactly as base
    assert fp.is_leq("0", "1")
    assert not fp.is_leq("a", "b")


def test_build_fixpoint_structure_contains_lattice():
    P = sample_poset()

    def gamma(x):
        return x

    struct = build_fixpoint_structure(P, gamma)

    assert struct.poset is not None
    assert struct.lattice is not None
    assert struct.lattice.is_lattice()
