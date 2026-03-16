from ENGINE.applications.constant_lattice import (
    ConstVal,
    build_atomic_lattice,
    build_state_lattice,
)
import pytest


def test_constval_str_branches():
    assert str(ConstVal.bottom()) == "⊥"
    assert str(ConstVal.top()) == "⊤"
    assert str(ConstVal.const(5)) == "5"


def test_state_get_keyerror():
    lattice = build_state_lattice({"x"}, {1})
    state = next(iter(lattice.elements))
    with pytest.raises(KeyError):
        state.get("unknown")


def test_atomic_incomparability():
    atomic = build_atomic_lattice({1, 2})
    elems = list(atomic.elements)
    c1 = ConstVal.const(1)
    c2 = ConstVal.const(2)
    assert not atomic.is_leq(c1, c2)
    assert not atomic.is_leq(c2, c1)
