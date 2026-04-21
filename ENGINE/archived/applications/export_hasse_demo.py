from __future__ import annotations

from ENGINE.core.poset import FinitePoset
from ENGINE.visualization.dot_export import export_hasse_to_dot


def main() -> None:
    elems = {0, 1, 2}

    def leq(a: int, b: int) -> bool:
        return a <= b

    P = FinitePoset(elems, leq)

    dot = export_hasse_to_dot(P, name="Chain_0_1_2")
    with open("hasse_chain.dot", "w", encoding="utf-8") as f:
        f.write(dot)

    print("Wrote hasse_chain.dot")


if __name__ == "__main__":
    main()
