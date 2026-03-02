"""
NEXAH Engine – Example 01: Stabilization via Closure Operator (Γ)

This example demonstrates:
- building a small finite poset
- defining a closure operator Γ
- iterating Γ until stabilization (fixpoint)
- listing fixpoints of Γ

Requires:
- ENGINE/core/poset.py  (FinitePoset)
- ENGINE/core/closure_operator.py (ClosureOperator)
"""

from ENGINE.core.poset import FinitePoset
from ENGINE.core.closure_operator import ClosureOperator


def main():
    # ---------------------------------------------------------
    # 1) Define a small finite poset (Q, ≤)
    #
    # We'll use a simple "diamond" poset:
    #
    #        top
    #       /   \
    #      a     b
    #       \   /
    #       bottom
    #
    # Relations (cover edges):
    # bottom ≤ a ≤ top
    # bottom ≤ b ≤ top
    # ---------------------------------------------------------

    elements = {"bottom", "a", "b", "top"}

    # Define the relation as a set of (x, y) pairs meaning x ≤ y
    # Include at least the cover relations; FinitePoset should close/reflexive-check internally,
    # but we also include reflexive pairs explicitly to be safe.
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

    poset = FinitePoset(elements=elements, leq_pairs=leq_pairs)

    # ---------------------------------------------------------
    # 2) Define a closure operator Γ: Q → Q
    #
    # Example closure: "push everything upward to the nearest stable layer"
    # Let's define:
    #   Γ(bottom) = a
    #   Γ(a)      = a
    #   Γ(b)      = top
    #   Γ(top)    = top
    #
    # This is just a toy model showing two basins: {bottom,a}→a and {b,top}→top
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
        raise RuntimeError(f"Did not stabilize within {max_steps} steps from {x}.")

    print("\n--- NEXAH Example: Stabilization (Γ) ---\n")
    print("Elements:", sorted(poset.elements))

    print("\nStabilization results:")
    for x in sorted(poset.elements):
        fx = stabilize(x)
        print(f"  {x:>7}  ->  {fx}")

    # ---------------------------------------------------------
    # 4) Fixpoints of Γ
    # ---------------------------------------------------------

    fps = closure.fixpoints()
    print("\nFixpoints Γ(x)=x:")
    for x in sorted(fps):
        print(" ", x)

    print("\nDone.\n")


if __name__ == "__main__":
    main()
