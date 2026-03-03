from __future__ import annotations

"""
NEXAH Engine – Example 01
Stabilization via Closure Operator Γ
"""

from ENGINE.core.poset import FinitePoset
from ENGINE.core.closure_operator import ClosureOperator
from ENGINE.core.lattice import LatticeOps


# ---------------------------------------------------------
# 1) Define finite poset (Q, ≤)
# ---------------------------------------------------------

def build_poset() -> FinitePoset[str]:
    elements: set[str] = {"bottom", "a", "b", "top"}

    leq_pairs: set[tuple[str, str]] = {
        ("bottom", "bottom"),
        ("a", "a"),
        ("b", "b"),
        ("top", "top"),
        ("bottom", "a"),
        ("bottom", "b"),
        ("a", "top"),
        ("b", "top"),
        ("bottom", "top"),
    }

    def leq(x: str, y: str) -> bool:
        return (x, y) in leq_pairs

    return FinitePoset(elements, leq)


# ---------------------------------------------------------
# 2) Closure operator Γ
# ---------------------------------------------------------

def gamma(x: str) -> str:
    mapping: dict[str, str] = {
        "bottom": "a",
        "a": "a",
        "b": "top",
        "top": "top",
    }
    return mapping[x]


# ---------------------------------------------------------
# 3) Example execution
# ---------------------------------------------------------

def main() -> None:
    poset = build_poset()
    closure = ClosureOperator(poset, gamma)

    print("\n=== NEXAH Engine – Stabilization Example ===\n")
    print("Elements:", sorted(poset.elements))

    fixpoints = closure.fixpoints()

    print("\nFixpoints Γ(x)=x:")
    for x in sorted(fixpoints):
        print("  ", x)

    lat = LatticeOps(poset)

    print("\n--- Full Lattice ---")
    print("Is lattice:", lat.is_lattice())
    print("Top:", lat.top())
    print("Bottom:", lat.bottom())
    print("Is distributive:", lat.is_distributive())

    print("\nJoin / Meet:")
    print("  a OR b =", lat.join("a", "b"))
    print("  a AND b =", lat.meet("a", "b"))

    fp_structure = closure.fixpoint_lattice(strict=False)

    print("\n--- Fixpoint-Induced Structure ---")
    print("Fixpoint elements:", sorted(fp_structure.poset.elements))
    print("Is lattice:", fp_structure.is_lattice())

    if fp_structure.is_lattice():
        print("Top fixpoint:", fp_structure.top())
        print("Bottom fixpoint:", fp_structure.bottom())
        print("Distributive:", fp_structure.is_distributive())

    print("\nDone.\n")


if __name__ == "__main__":
    main()
