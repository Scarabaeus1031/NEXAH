# run_ieee_state_transitions_v56.py

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.cluster import DBSCAN

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

BASE_PATH = Path("APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs")
CASES = ["ieee30", "ieee57", "ieee118"]

EPS = 0.018
MIN_SAMPLES = 2

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def load_case(case: str):
    file_path = BASE_PATH / f"{case}_v52_residual_vs_distance.csv"
    if not file_path.exists():
        print(f"Missing file: {file_path}")
        return None

    df = pd.read_csv(file_path).dropna()

    required = {"distance", "residual", "tau"}
    if not required.issubset(df.columns):
        print(f"[{case}] Missing required columns: {required - set(df.columns)}")
        return None

    return df.sort_values("tau").reset_index(drop=True)


def assign_clusters(df: pd.DataFrame):
    X = df[["distance", "residual"]].values
    model = DBSCAN(eps=EPS, min_samples=MIN_SAMPLES)
    labels = model.fit_predict(X)

    out = df.copy()
    out["cluster"] = labels
    return out


def build_transition_table(df: pd.DataFrame):
    transitions = []

    for i in range(len(df) - 1):
        c_from = int(df.loc[i, "cluster"])
        c_to = int(df.loc[i + 1, "cluster"])
        tau_from = float(df.loc[i, "tau"])
        tau_to = float(df.loc[i + 1, "tau"])

        transitions.append({
            "from_cluster": c_from,
            "to_cluster": c_to,
            "tau_from": tau_from,
            "tau_to": tau_to
        })

    trans_df = pd.DataFrame(transitions)

    if trans_df.empty:
        summary = pd.DataFrame(columns=["from_cluster", "to_cluster", "count"])
    else:
        summary = (
            trans_df.groupby(["from_cluster", "to_cluster"])
            .size()
            .reset_index(name="count")
            .sort_values("count", ascending=False)
            .reset_index(drop=True)
        )

    return trans_df, summary


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    print("RUNNING V56 — STATE TRANSITIONS")

    summary_rows = []

    for case in CASES:
        print(f"\n--- {case.upper()} ---")

        df = load_case(case)
        if df is None:
            continue

        df_clustered = assign_clusters(df)

        # save clustered trajectory
        clustered_path = BASE_PATH / f"{case}_v56_clustered_states.csv"
        df_clustered.to_csv(clustered_path, index=False)
        print(f"Saved: {clustered_path}")

        # transitions
        trans_df, trans_summary = build_transition_table(df_clustered)

        trans_path = BASE_PATH / f"{case}_v56_transitions.csv"
        trans_summary_path = BASE_PATH / f"{case}_v56_transition_summary.csv"

        trans_df.to_csv(trans_path, index=False)
        trans_summary.to_csv(trans_summary_path, index=False)

        print(f"Saved: {trans_path}")
        print(f"Saved: {trans_summary_path}")

        print("\nTransition summary:")
        print(trans_summary if not trans_summary.empty else "[No transitions found]")

        # plot 1: cluster over tau
        plt.figure(figsize=(9, 4))
        plt.scatter(df_clustered["tau"], df_clustered["cluster"], c=df_clustered["cluster"], s=30)
        plt.xlabel("tau")
        plt.ylabel("cluster")
        plt.title(f"{case.upper()} — Cluster State over tau (V56)")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(BASE_PATH / f"{case}_v56_cluster_vs_tau.png", dpi=150)
        plt.close()

        # plot 2: trajectory colored by cluster
        plt.figure(figsize=(8, 6))
        plt.scatter(
            df_clustered["distance"],
            df_clustered["residual"],
            c=df_clustered["cluster"],
            s=32
        )
        plt.axhline(0, linestyle="--", linewidth=1)
        plt.xlabel("Distance to Rift")
        plt.ylabel("Residual")
        plt.title(f"{case.upper()} — State Transition Geometry (V56)")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(BASE_PATH / f"{case}_v56_transition_geometry.png", dpi=150)
        plt.close()

        summary_rows.append({
            "case": case,
            "num_points": int(len(df_clustered)),
            "num_clusters_detected": int(df_clustered["cluster"].nunique()),
            "num_noise_points": int((df_clustered["cluster"] == -1).sum()),
            "num_transition_types": int(len(trans_summary))
        })

    summary_df = pd.DataFrame(summary_rows)
    summary_path = BASE_PATH / "ieee_v56_transition_overview.csv"
    summary_df.to_csv(summary_path, index=False)

    print("\n--- V56 OVERVIEW ---")
    print(summary_df)
    print(f"\nSaved: {summary_path}")


if __name__ == "__main__":
    main()
