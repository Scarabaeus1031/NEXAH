import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import networkx as nx

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

BASE_PATH = Path("APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs")
CASES = ["ieee30", "ieee57", "ieee118"]

STATE_LABELS = {
    -1: "noise",
     0: "core",
     1: "secondary"
}

# --------------------------------------------------
# LOAD
# --------------------------------------------------

def load_transition_summary(case):
    path = BASE_PATH / f"{case}_v56_transition_summary.csv"
    if not path.exists():
        print(f"Missing: {path}")
        return None
    return pd.read_csv(path)

# --------------------------------------------------
# BUILD GRAPH
# --------------------------------------------------

def build_graph(df):
    G = nx.DiGraph()

    for _, row in df.iterrows():
        src = int(row["from_cluster"])
        dst = int(row["to_cluster"])
        weight = int(row["count"])

        src_label = STATE_LABELS.get(src, f"state_{src}")
        dst_label = STATE_LABELS.get(dst, f"state_{dst}")

        if src_label not in G:
            G.add_node(src_label)
        if dst_label not in G:
            G.add_node(dst_label)

        G.add_edge(src_label, dst_label, weight=weight)

    return G

# --------------------------------------------------
# DRAW
# --------------------------------------------------

def draw_graph(G, case):
    plt.figure(figsize=(8, 6))

    pos = nx.spring_layout(G, seed=42)

    edge_widths = [G[u][v]["weight"] for u, v in G.edges()]
    edge_labels = {(u, v): G[u][v]["weight"] for u, v in G.edges()}

    nx.draw_networkx_nodes(G, pos, node_size=2200)
    nx.draw_networkx_labels(G, pos, font_size=12)
    nx.draw_networkx_edges(G, pos, width=edge_widths, arrows=True, arrowsize=24)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

    plt.title(f"{case.upper()} — Collapse Corridor Graph (V64)")
    plt.axis("off")
    plt.tight_layout()

    out_path = BASE_PATH / f"{case}_v64_corridor_graph.png"
    plt.savefig(out_path, dpi=150)
    plt.close()

    print(f"Saved: {out_path}")

# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    print("RUNNING V64 — COLLAPSE CORRIDOR GRAPH")

    summary_rows = []

    for case in CASES:
        print(f"\n--- {case.upper()} ---")

        df = load_transition_summary(case)
        if df is None:
            continue

        G = build_graph(df)
        draw_graph(G, case)

        summary_rows.append({
            "case": case,
            "num_nodes": G.number_of_nodes(),
            "num_edges": G.number_of_edges(),
            "nodes": ", ".join(G.nodes())
        })

        print(df)

    summary_df = pd.DataFrame(summary_rows)
    out_summary = BASE_PATH / "ieee_v64_corridor_graph_summary.csv"
    summary_df.to_csv(out_summary, index=False)

    print("\n--- V64 SUMMARY ---")
    print(summary_df)
    print(f"\nSaved: {out_summary}")

# --------------------------------------------------

if __name__ == "__main__":
    main()
