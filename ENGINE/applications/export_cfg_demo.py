# ENGINE/applications/export_cfg_demo.py

def build_cfg():
    """
    Simple demo control-flow graph.
    """
    nodes = [
        "start",
        "cond_x_gt_0",
        "branch_A",
        "branch_B",
        "join",
        "end"
    ]

    edges = [
        ("start", "cond_x_gt_0"),
        ("cond_x_gt_0", "branch_A"),
        ("cond_x_gt_0", "branch_B"),
        ("branch_A", "join"),
        ("branch_B", "join"),
        ("join", "end"),
    ]

    return nodes, edges


def export_dot(nodes, edges, filename="cfg_demo.dot"):
    with open(filename, "w") as f:
        f.write("digraph CFG {\n")
        f.write("  rankdir=TB;\n")
        f.write("  node [shape=box];\n\n")

        for n in nodes:
            f.write(f'  "{n}";\n')

        f.write("\n")

        for src, dst in edges:
            f.write(f'  "{src}" -> "{dst}";\n')

        f.write("}\n")

    print(f"Wrote {filename}")


def main():
    nodes, edges = build_cfg()
    export_dot(nodes, edges)


if __name__ == "__main__":
    main()
