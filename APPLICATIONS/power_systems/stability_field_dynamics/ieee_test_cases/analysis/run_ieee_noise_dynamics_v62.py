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
STATE_NAMES = ["noise", "core", "secondary"]

NOISE_LEVEL = 0.02   # 🔥 wichtig: klein halten!

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
# MODEL
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
# WARNING
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
# SIMULATION WITH NOISE
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

        # 🔥 NOISE INJECTION
        noise = np.random.normal(0, NOISE_LEVEL, size=state.shape)
        state = state + noise

        # clamp + normalize
        state = np.clip(state, 0, None)
        if np.sum(state) > 0:
            state = state / np.sum(state)

        probs.append(state.copy())

    probs = np.array(probs)

    # --------------------------------------------------
    # WARNING
    # --------------------------------------------------

    warning = compute_warning(probs)
    warning = warning / np.max(warning)

    # echte Events = Peaks
    slope = np.gradient(warning)

    events = []
    for i in range(2, len(warning)):
        if warning[i] > 0.6 and slope[i] > 0.01:
            events.append(i)

    print("⚠️ EVENTS:", events)

    # --------------------------------------------------
    # PLOTS
    # --------------------------------------------------

    plt.figure(figsize=(10,5))

    plt.plot(warning, label="warning", color="orange")
    plt.plot(slope, label="slope", linestyle="--")

    for e in events:
        plt.axvline(e, color="red", alpha=0.3)

    plt.title(f"{case} — Noise Dynamics (V62)")
    plt.legend()
    plt.grid()

    plt.savefig(BASE_PATH / f"{case}_v62_noise_warning.png", dpi=150)
    plt.close()

# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":
    print("RUNNING V62 — NOISE DYNAMICS")

    for case in CASES:
        simulate(case)
