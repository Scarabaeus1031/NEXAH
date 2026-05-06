from __future__ import annotations

from typing import List, Tuple

from ENGINE.visualization.dot_export import export_cfg_to_dot


def build_cfg() -> tuple[List[str], List[Tuple[str, str]]]:
    """
    Simple demo control-flow graph.
    """

    nodes: List[str] = [
        "start",
        "cond_x_gt_0",
        "branch_A",
        "branch_B",
        "join",
        "end",
    ]

    edges: List[Tuple[str, str]] = [
        ("start", "cond_x_gt_0"),
        ("cond_x_gt_0", "branch_A"),
        ("cond_x_gt_0", "branch_B"),
        ("branch_A", "join"),
        ("branch_B", "join"),
        ("join", "end"),
    ]

    return nodes, edges


def export_dot(nodes: List[str], edges: List[Tuple[str, str]], filename: str = "cfg_demo.dot") -> None:
    """
    Export CFG graph as DOT file using the engine exporter.
    """

    dot = export_cfg_to_dot(nodes, edges)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(dot)

    print(f"Wrote {filename}")


def main() -> None:
    nodes, edges = build_cfg()
    export_dot(nodes, edges)


if __name__ == "__main__":
    main()
