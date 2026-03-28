# run_ieee_transition_probabilities_v57.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

BASE_PATH = Path("APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs")
CASES = ["ieee30", "ieee57", "ieee118"]

# fixed cluster order for comparable matrices
STATE_ORDER = [-1, 0, 1]
STATE_LABELS = {
    -1: "noise/transition",
     0: "core",
     1: "secondary"
}

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def load_transitions(case: str):
    file_path = BASE_PATH / f"{case}_v56_transitions.csv"
    if not file_path.exists():
        print(f"Missing file: {file_path}")
        return None

    df = pd.read_csv(file_path).dropna()

    required = {"from_cluster", "to_cluster"}
    if not required.issubset(df.columns):
        print(f"[{case}] Missing required columns: {required - set(df.columns)}")
        return None

    return df


def build_transition_count_matrix(df: pd.DataFrame):
    mat = pd.DataFrame(
        0,
        index=STATE_ORDER,
        columns=STATE_ORDER,
        dtype=int
    )

    for _, row in df.iterrows():
        f = int(row["from_cluster"])
        t = int(row["to_cluster"])

        if f in mat.index and t in mat.columns:
            mat.loc[f, t] += 1

    return mat


def normalize_rows(mat: pd.DataFrame):
    prob = mat.astype(float).copy()

    for idx in prob.index:
        row_sum = prob.loc[idx].sum()
        if row_sum > 0:
            prob.loc[idx] = prob.loc[idx] / row_sum

    return prob


def relabel_matrix(mat: pd.DataFrame):
    out = mat.copy()
    out.index = [STATE_LABELS[i] for i in out.index]
    out.columns = [STATE_LABELS[i] for i in out.columns]
    return out


def plot_heatmap(prob_mat: pd.DataFrame, case: str):
    fig, ax = plt.subplots(figsize=(6, 5))

    arr = prob_mat.values
    im = ax.imshow(arr)

    ax.set_xticks(range(len(prob_mat.columns)))
    ax.set_yticks(range(len(prob_mat.index)))
    ax.set_xticklabels(prob_mat.columns, rotation=30, ha="right")
    ax.set_yticklabels(prob_mat.index)

    ax.set_title(f"{case.upper()} — Transition Probabilities (V57)")
    ax.set_xlabel("to state")
    ax.set_ylabel("from state")

    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            ax.text(j, i, f"{arr[i, j]:.2f}", ha="center", va="center")

    fig.colorbar(im, ax=ax, label="Probability")
    fig.tight_layout()

    out_path = BASE_PATH / f"{case}_v57_transition_probabilities.png"
    plt.savefig(out_path, dpi=150)
    plt.close()

    return out_path


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    print("RUNNING V57 — TRANSITION PROBABILITY MODEL")

    overview_rows = []

    for case in CASES:
        print(f"\n--- {case.upper()} ---")

        df = load_transitions(case)
        if df is None:
            continue

        count_mat = build_transition_count_matrix(df)
        prob_mat = normalize_rows(count_mat)

        count_labeled = relabel_matrix(count_mat)
        prob_labeled = relabel_matrix(prob_mat)

        count_path = BASE_PATH / f"{case}_v57_transition_counts.csv"
        prob_path = BASE_PATH / f"{case}_v57_transition_probabilities.csv"

        count_labeled.to_csv(count_path)
        prob_labeled.to_csv(prob_path)

        fig_path = plot_heatmap(prob_labeled, case)

        print("\nTransition counts:")
        print(count_labeled)
        print("\nTransition probabilities:")
        print(prob_labeled)

        print(f"\nSaved: {count_path}")
       
