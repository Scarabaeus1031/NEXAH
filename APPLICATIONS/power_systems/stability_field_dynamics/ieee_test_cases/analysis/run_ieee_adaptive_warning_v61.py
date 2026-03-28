import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

BASE_PATH = Path("APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs")
CASES = ["ieee30", "ieee57", "ieee118"]

STATE_MAP = {-1: 0, 0: 1, 1: 2}

# --------------------------------------------------
# LOAD
# --------------------------------------------------

def load_states(case):
    path = BASE_PATH / f"{case}_v56_clustered_states.csv"
    if not path.exists():
        print(f"Missing: {path}")
        return None
    return pd.read_csv(path)

# --------------------------------------------------
# TRANSITION MODEL (wie V60)
# --------------------------------------------------

def dynamic_transition_matrix(tau):

    P = np.array([
        [0.5, 0.0, 0.5],
        [0.06, 0.94, 0.0],
        [0.5, 0.5, 0.0]
    ], dtype=float)

    P[1, 0] += 0.35 * tau
    P[2, 0] += 0.35 * tau

    P = P / P.sum(axis=1, keepdims=True)

    return P

def build_state(cluster):
    v = np.zeros(3)
    v[STATE_MAP.get(cluster, 0)] = 1.0
    return v

# --------------------------------------------------
# WARNING SCORE (wie V60)
# --------------------------------------------------

def compute_warning(probs):

    noise = probs[:, 0]
    core = probs[:, 1]
    secondary = probs[:, 2]

    warning = (
        0.6 * secondary +
        0.3 * noise +
        0.3 * (1 - core)
    )

    return warning

# --------------------------------------------------
# ADAPTIVE DETECTION
# --------------------------------------------------

def detect_events(warning):

    # normalize
    warning = warning / np.max(warning)

    # Steigung
    slope = np.gradient(warning)

    # Beschleunigung
    accel = np.gradient(slope)

    events = []

    for i in range(2, len(warning)):

        cond1 = warning[i] > 0.6
        cond2 = slope[i] > 0.02
        cond3 = accel[i] > 0.005

        if cond1 and cond2 and cond3:
            events.append(i)

    return warning, slope, accel, events

# --------------------------------------------------
# RUN
# --------------------------------------------------

def simulate(case):
    print(f"\n--- {case} ---")

    df = load_states(case)
    if df is None:
        return

    clusters = df["cluster"].values
    tau = df["tau"].values if "tau" in df else np.linspace(0, 1, len(df))

    state = build_state(clusters[0])

    probs = []

    for i in range(len(tau)):
        P = dynamic_transition_matrix(tau[i])
        state = P @ state
        probs.append(state.copy())

    probs = np.array(probs)

    # --------------------------------------------------
    # DETECTION
    # --------------------------------------------------

    warning, slope, accel, events = detect_events(probs)

    print("⚠️ EVENTS:", events)

    # --------------------------------------------------
    # PLOT
    # --------------------------------------------------

    plt.figure(figsize=(10,5))

    plt.plot(warning, label="warning", color="orange")
    plt.plot(slope, label="slope", linestyle="--")
    plt.plot(accel, label="accel", linestyle=":")

    for e in events:
        plt.axvline(e, color="red", alpha=0.3)

    plt.title(f"{case} — Adaptive Warning (V61)")
    plt.legend()
    plt.grid()

    plt.savefig(BASE_PATH / f"{case}_v61_adaptive_warning.png", dpi=150)
    plt.close()

# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":
    print("RUNNING V61 — ADAPTIVE EARLY WARNING")

    for case in CASES:
        simulate(case)
