import pytest

from ENGINE.core.poset import FinitePoset
from ENGINE.core.monotone_operator import MonotoneOperator


def chain_3():
    # 0 < a < 1
    elements = {"0", "a", "1"}
    order = {
        ("0", "0"), ("a", "a"), ("1", "1"),
        ("0", "a"), ("a", "1"),
        ("0", "1"),
    }

    def leq(x, y):
        return (x, y) in order

    return FinitePoset(elements, leq)


# --------------------------------------------------
# Accepts monotone but non-closure operator
# --------------------------------------------------

def test_monotone_accepts_nonclosure():
    P = chain_3()

    # monotone, NOT extensive (a -> 0)
    def f(x):
        return {"0": "0", "a": "0", "1": "1"}[x]

    M = MonotoneOperator(P, f)
    assert M.apply("a") == "0"


# --------------------------------------------------
# Reject non-monotone
# --------------------------------------------------

def test_monotone_rejects_nonmonotone():
    P = chain_3()

    def bad(x):
        return {"0": "1", "a": "0", "1": "1"}[x]

    with pytest.raises(ValueError):
        MonotoneOperator(P, bad)


# --------------------------------------------------
# Fixpoints
# --------------------------------------------------

def test_fixpoints_and_least_greatest():
    P = chain_3()

    def f(x):
        return {"0": "0", "a": "1", "1": "1"}[x]

    M = MonotoneOperator(P, f)

    assert M.fixpoints() == {"0", "1"}
    assert M.least_fixpoint() == "0"
    assert M.greatest_fixpoint() == "1"


# --------------------------------------------------
# Iteration (monotone, inflationary → no cycles)
# --------------------------------------------------

def test_iteration_stabilizes():
    P = chain_3()

    # inflationary monotone operator
    def f(x):
        return {"0": "a", "a": "1", "1": "1"}[x]

    M = MonotoneOperator(P, f)

    fx, traj = M.iterate_from("0")
    assert fx == "1"
    assert traj[-1] == "1"
        # -----------------------------------------------------
    # Tarski characterization (finite case)
    # -----------------------------------------------------

    def tarski_least_fixpoint(self) -> Any:
        """
        lfp(f) = meet of all prefixed points {x | f(x) ≤ x}
        Requires the poset to be a lattice.
        """
        from ENGINE.core.lattice import LatticeOps

        lat = LatticeOps(self.poset)

        if not lat.is_lattice():
            raise ValueError("Poset is not a lattice.")

        pref = list(self.prefixed_points())
        if not pref:
            raise ValueError("No prefixed points exist.")

        result = pref[0]
        for x in pref[1:]:
            result = lat.meet(result, x)

        return result

    def test_tarski_matches_enumeration():
    P = chain_3()

    def f(x):
        return {"0": "0", "a": "1", "1": "1"}[x]

    M = MonotoneOperator(P, f)

    assert M.least_fixpoint() == M.tarski_least_fixpoint()
    assert M.greatest_fixpoint() == M.tarski_greatest_fixpoint()
