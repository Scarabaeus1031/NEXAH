"""
NEXAH Engine – Example 01: Stabilization via Closure Operator (Γ)
"""

from ENGINE.core.poset import FinitePoset
from ENGINE.core.closure_operator import ClosureOperator
from ENGINE.core.lattice import LatticeOps


def main():
    # ---------------------------------------------------------
    # 1) Define a small finite poset (Q, ≤)
    # ---------------------------------------------------------

    elements = {"bottom", "a", "b", "top"}

    leq_pairs = {
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

    def leq(x, y):
        return (x, y) in leq_pairs

    poset = FinitePoset(elements, leq)

    # ---------------------------------------------------------
    # 2) Define closure operator Γ
    # ---------------------------------------------------------

    def gamma(x: str) -> str:
        mapping = {
            "bottom": "a",
            "a": "a",
            "b": "top",
            "top": "top",
        }
        return mapping[x]

    closure = ClosureOperator(poset=poset, operator=gamma)

    # ---------------------------------------------------------
    # 3) Iterate Γ until stabilization
    # ---------------------------------------------------------

    def stabilize(x: str, max_steps: int = 25) -> str:
        current = x
        for _ in range(max_steps):
            nxt = closure.apply(current)
            if nxt == current:
                return current
            current = nxt
        raise RuntimeError(
            f"Did not stabilize within {max_steps} steps from {x}."
        )

    print("\n--- NEXAH Example: Stabilization (Γ) ---\n")
    print("Elements:", sorted(poset.elements))

    print("\nStabilization results:")
    for x in sorted(poset.elements):
        fx = stabilize(x)
        print(f"  {x:>7}  ->  {fx}")

    fps = closure.fixpoints()

    print("\nFixpoints Γ(x)=x:")
    for x in sorted(fps):
        print(" ", x)

    # ---------------------------------------------------------
    # 4) Lattice structure (full poset)
    # ---------------------------------------------------------

    lat = LatticeOps(poset)

    print("\n--- Lattice Structure (Full Poset) ---\n")
    print("Is lattice:", lat.is_lattice())
    print("Top element:", lat.top())
    print("Bottom element:", lat.bottom())

    print("\nJoin / Meet examples:")
    print("  a ∨ b =", lat.join("a", "b"))
    print("  a ∧ b =", lat.meet("a", "b"))
    print("  a ∨ bottom =", lat.join("a", "bottom"))
    print("  b ∧ top =", lat.meet("b", "top"))

    print("Is distributive:", lat.is_distributive())

    # ---------------------------------------------------------
    # 5) Fixpoint-induced structure
    # ---------------------------------------------------------

    print("\n--- Fixpoint Structure ---\n")

    fp_lat = closure.fixpoint_lattice(strict=False)

    print("Fixpoint elements:", sorted(fp_lat.poset.elements))
    print("Is fixpoint-poset a lattice?:", fp_lat.is_lattice())

    if fp_lat.is_lattice():
        print("Top fixpoint:", fp_lat.top())
        print("Bottom fixpoint:", fp_lat.bottom())
        print("Is distributive (fixpoints)?:", fp_lat.is_distributive())

    print("\nDone.\n")


if __name__ == "__main__":
    main()
