# run_ieee_cluster_structure_v55.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.cluster import DBSCAN

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

BASE_PATH = Path("APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs")
CASES = ["ieee30", "ieee57", "ieee118"]

# DBSCAN params
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

    return df


def cluster_case(df: pd.DataFrame):
    X = df[["distance", "residual"]].values

    model = DBSCAN(eps=EPS, min_samples=MIN_SAMPLES)
    labels = model.fit_predict(X)

    df = df.copy()
    df["cluster"] = labels

    cluster_rows = []
    valid_labels = sorted([lab for lab in np.unique(labels) if lab != -1])

    for lab in valid_labels:
        sub = df[df["cluster"] == lab]
        cluster_rows.append({
            "cluster": int(lab),
            "count": int(len(sub)),
            "center_distance": float(sub["distance"].mean()),
            "center_residual": float(sub["residual"].mean()),
            "tau_min": float(sub["tau"].min()),
            "tau_max": float(sub["tau"].max()),
        })

    return df, pd.DataFrame(cluster_rows)


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    print("RUNNING V55 — CLUSTER STRUCTURE EXTRACTION")

    summary_rows = []

    plt.figure(figsize=(9, 7))

    for case in CASES:
        print(f"\n--- {case.upper()} ---")

        df = load_case(case)
        if df is None:
            continue

        clustered_df, cluster_info = cluster_case(df)

        # save per-case cluster table
        cluster_path = BASE_PATH / f"{case}_v55_clusters.csv"
        cluster_info.to_csv(cluster_path, index=False)
        print(f"Saved: {cluster_path}")

        n_clusters = len(cluster_info)
        n_noise = int((clustered_df["cluster"] == -1).sum())

        print(cluster_info if n_clusters > 0 else f"[{case}] No clusters found")

        summary_rows.append({
            "case": case,
            "num_clusters": int(n_clusters),
            "num_noise_points": n_noise,
            "largest_cluster_size": int(cluster_info["count"].max()) if n_clusters > 0 else 0,
        })

        # overlay plot by case
        plt.scatter(
            clustered_df["distance"],
            clustered_df["residual"],
            s=28,
            alpha=0.65,
            label=case
        )

        # plot cluster centers
        if n_clusters > 0:
            plt.scatter(
                cluster_info["center_distance"],
                cluster_info["center_residual"],
                s=90,
                marker="x"
            )

    plt.axhline(0, linestyle="--", linewidth=1)
    plt.xlabel("Distance to Rift")
    plt.ylabel("Residual")
    plt.title("V55 — Cluster Structure Comparison")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    fig_path = BASE_PATH / "ieee_v55_cluster_structure.png"
    plt.savefig(fig_path, dpi=150)
    plt.close()

    summary_df = pd.DataFrame(summary_rows)
    summary_path = BASE_PATH / "ieee_v55_cluster_summary.csv"
    summary_df.to_csv(summary_path, index=False)

    print("\n--- V55 SUMMARY ---")
    print(summary_df)
    print(f"\nSaved: {fig_path}")
    print(f"Saved: {summary_path}")


if __name__ == "__main__":
    main()
