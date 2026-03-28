# run_ieee_transition_probability_v57.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

BASE_PATH = Path("APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs")
CASES = ["ieee30", "ieee57", "ieee118"]

STATE_ORDER = [-1, 0, 1]

STATE_LABELS = {
    -1: "noise",
     0: "core",
     1: "secondary"
}

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def load_transitions(case):
    path = BASE_PATH / f"{case}_v56_transitions.csv"

    if not path.exists():
        print(f"Missing file: {path}")
        return None

    return pd.read_csv(path)


def build_matrix(df):
    mat = pd.DataFrame(0, index=STATE_ORDER, columns=STATE_ORDER)

    for _, row in df.iterrows():
        f = int(row["from_cluster"])
        t = int(row["to_cluster"])

        if f in STATE_ORDER and t in STATE_ORDER:
            mat.loc[f, t] += 1

    return mat


def normalize(mat):
    prob = mat.copy().astype(float)

    for i in prob.index:
        s = prob.loc[i].sum()
        if s > 0:
            prob.loc[i] /= s

    return prob


def label(mat):
    m = mat.copy()
    m.index = [STATE_LABELS[i] for i in m.index]
    m.columns = [STATE_LABELS[i] for i in m.columns]
    return m


def plot_heatmap(prob, case):
    plt.figure(figsize=(6,5))
    arr = prob.values

    plt.imshow(arr)

    plt.xticks(range(len(prob.columns)), prob.columns, rotation=30)
    plt.yticks(range(len(prob.index)), prob.index)

    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            plt.text(j, i, f"{arr[i,j]:.2f}", ha="center", va="center")

    plt.title(f"{case.upper()} — Transition Probabilities (V57)")
    plt.colorbar()

    out = BASE_PATH / f"{case}_v57_heatmap.png"
    plt.savefig(out, dpi=150)
    plt.close()

    print(f"Saved: {out}")


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    print("RUNNING V57 — TRANSITION PROBABILITY MODEL")

    for case in CASES:
        print(f"\n--- {case.upper()} ---")

        df = load_transitions(case)
        if df is None:
            continue

        counts = build_matrix(df)
        probs = normalize(counts)

        counts_l = label(counts)
        probs_l = label(probs)

        counts_path = BASE_PATH / f"{case}_v57_counts.csv"
        probs_path = BASE_PATH / f"{case}_v57_probs.csv"

        counts_l.to_csv(counts_path)
        probs_l.to_csv(probs_path)

        print("\nCounts:")
        print(counts_l)

        print("\nProbabilities:")
        print(probs_l.round(3))

        print(f"\nSaved: {counts_path}")
        print(f"Saved: {probs_path}")

        plot_heatmap(probs_l, case)


# --------------------------------------------------

if __name__ == "__main__":
    main()
