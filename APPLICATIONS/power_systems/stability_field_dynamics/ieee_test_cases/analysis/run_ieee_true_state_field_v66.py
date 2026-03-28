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
# LOAD
# --------------------------------------------------

def load_dataset(case):
    path = BASE_PATH / f"{case}_v43_dataset.csv"
    if not path.exists():
        print(f"Missing dataset: {path}")
        return None
    return pd.read_csv(path)


def load_states(case):
    path = BASE_PATH / f"{case}_v56_clustered_states.csv"
    if not path.exists():
        print(f"Missing states: {path}")
        return None
    return pd.read_csv(path)


def load_fit(case):
    path = BASE_PATH / "ieee_v43_manifold_fit.csv"
    df = pd.read_csv(path)
    return df[df["case"] == case].iloc[0]

# --------------------------------------------------
# CORE FUNCTIONS
# --------------------------------------------------

def power_model(c, dc, a, p, q):
    return a * (np.abs(c) ** p) * (np.abs(dc) ** q)


def compute_residual(df, fit_params):
    c = df["c"].values
    dc = df["dc"].values
    d2c = df["d2c"].values

    model = power_model(c, dc,
                        fit_params["power_a"],
                        fit_params["power_p"],
                        fit_params["power_q"])

    residual = d2c - model
    return residual


def compute_distance(c, dc):
    # einfache Distanz zum Ursprung als Proxy für Rift-Nähe
    return np.sqrt(c**2 + dc**2)

# --------------------------------------------------
# TRAIN
# --------------------------------------------------

def train_classifier(df_states):
    X = df_states[["distance", "residual"]].values
    y = df_states["cluster"].values

    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(X, y)

    return model

# --------------------------------------------------
# MAIN
# --------------------------------------------------

def run(case):
    print(f"\n--- {case.upper()} ---")

    df = load_dataset(case)
    df_states = load_states(case)
    fit = load_fit(case)

    if df is None or df_states is None:
        return

    # 🔥 KEIN FILTER MEHR → FULL SYSTEM
    c = df["c"].values
    dc = df["dc"].values

    residual = compute_residual(df, fit)
    distance = compute_distance(c, dc)

    X = np.column_stack([distance, residual])

    model = train_classifier(df_states)
    pred = model.predict(X)

    # --------------------------------------------------
    # PLOT
    # --------------------------------------------------

    plt.figure(figsize=(8, 6))

    for state in np.unique(pred):
        mask = pred == state
        plt.scatter(
            c[mask],
            dc[mask],
            label=STATE_LABELS.get(state, str(state)),
            color=STATE_COLORS.get(state, "black"),
            s=30,
            alpha=0.7
        )

    plt.xlabel("c")
    plt.ylabel("dc")
    plt.title(f"{case.upper()} — TRUE STATE FIELD (V66)")
    plt.legend()
    plt.grid(True)

    out = BASE_PATH / f"{case}_v66_true_state_field.png"
    plt.savefig(out, dpi=150)
    plt.close()

    print(f"Saved: {out}")

# --------------------------------------------------

if __name__ == "__main__":
    print("RUNNING V66 — TRUE STATE FIELD")

    for case in CASES:
        run(case)
