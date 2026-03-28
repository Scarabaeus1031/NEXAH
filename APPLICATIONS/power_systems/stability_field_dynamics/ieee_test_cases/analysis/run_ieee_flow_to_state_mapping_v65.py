import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.neighbors import KNeighborsClassifier

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

STATE_COLORS = {
    -1: "purple",
     0: "green",
     1: "orange"
}

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

def load_dataset(case):
    path = BASE_PATH / f"{case}_v43_dataset.csv"
    if not path.exists():
        return None
    return pd.read_csv(path)


def load_states(case):
    path = BASE_PATH / f"{case}_v56_clustered_states.csv"
    if not path.exists():
        return None
    return pd.read_csv(path)


# --------------------------------------------------
# TRAIN STATE CLASSIFIER
# --------------------------------------------------

def train_classifier(df_states):
    X = df_states[["distance", "residual"]].values
    y = df_states["cluster"].values

    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(X, y)

    return model


# --------------------------------------------------
# FLOW SAMPLING (FROM DATASET)
# --------------------------------------------------

def build_flow_points(df):
    c = df["c"].values
    dc = df["dc"].values

    return np.column_stack([c, dc])


# --------------------------------------------------
# MAP FLOW → STATES
# --------------------------------------------------

def map_flow_to_states(df, model):
    # echte Features verwenden!
    distance = df["c"].values   # besser als proxy, aber wir erweitern gleich
    residual = df["d2c"].values  # besser als dc

    X = np.column_stack([distance, residual])

    pred = model.predict(X)
    return pred

    # fake residual/distance approximation
    # (since flow points are in (c,dc), we approximate)
    distance = flow_points[:, 0]  # proxy
    residual = flow_points[:, 1]  # proxy

    X = np.column_stack([distance, residual])

    pred = model.predict(X)
    return pred


# --------------------------------------------------
# PLOT
# --------------------------------------------------

def plot_mapping(flow_points, states, case):
    plt.figure(figsize=(8, 6))

    for state in np.unique(states):
        mask = states == state
        plt.scatter(
            flow_points[mask, 0],
            flow_points[mask, 1],
            label=STATE_LABELS.get(state, str(state)),
            color=STATE_COLORS.get(state, "black"),
            s=30,
            alpha=0.7
        )

    plt.xlabel("c")
    plt.ylabel("dc")
    plt.title(f"{case.upper()} — Flow → State Mapping (V65)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    out = BASE_PATH / f"{case}_v65_flow_state_mapping.png"
    plt.savefig(out, dpi=150)
    plt.close()

    print(f"Saved: {out}")


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    print("RUNNING V65 — FLOW TO STATE MAPPING")

    for case in CASES:
        print(f"\n--- {case.upper()} ---")

        df = load_dataset(case)
        df_states = load_states(case)

        if df is None or df_states is None:
            print("Missing data")
            continue

        model = train_classifier(df_states)

        flow_points = build_flow_points(df)
        states = map_flow_to_states(df, model)
        flow_points = np.column_stack([df["c"].values, df["dc"].values])

        plot_mapping(flow_points, states, case)


# --------------------------------------------------

if __name__ == "__main__":
    main()
