# nexah_state_machine_ieee9.py

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from nexah_ieee9.controller.nexah_state_machine import (
    NexahStateMachineController,
    NexahMetrics,
    NexahThresholds,
)


# =============================
# CONFIG
# =============================

RUN_PATH = Path(
    "APPLICATIONS/power_systems/nexah_ieee9/results/run_20260412_225052"
)


# =============================
# LOAD DATA
# =============================

def load_data(run_path):
    risk = np.load(run_path / "risk.npy")
    residual = np.load(run_path / "residual.npy")
    distance = np.load(run_path / "distance.npy")

    # optional (falls vorhanden)
    d2c_path = run_path / "d2c.npy"
    if d2c_path.exists():
        d2c = np.load(d2c_path)
    else:
        d2c = np.zeros_like(risk)

    return risk, residual, distance, d2c


# =============================
# METRICS BUILDER
# =============================

def build_metrics(i, risk, residual, distance, d2c):
    if i == 0:
        slope = 0
    else:
        slope = risk[i] - risk[i - 1]

    return NexahMetrics(
        risk=float(risk[i]),
        risk_slope=float(slope),
        d2c=float(d2c[i]),
        residual=float(residual[i]),
        distance_to_sep=float(distance[i]),
    )


# =============================
# RUN CONTROLLER
# =============================

def run_controller(risk, residual, distance, d2c):
    controller = NexahStateMachineController(NexahThresholds())

    states = []
    actions = []

    for i in range(len(risk)):
        m = build_metrics(i, risk, residual, distance, d2c)
        action = controller.action(m)

        states.append(controller.state.value)
        actions.append(action)

    return np.array(states), actions


# =============================
# VISUALIZATION
# =============================

def plot_timeseries(risk, distance, states):
    plt.figure(figsize=(10, 6))

    plt.plot(risk, label="Risk")
    plt.plot(distance, label="Distance to Separatrix")
    plt.plot(states, "--", label="Controller State")

    plt.legend()
    plt.title("IEEE9 + NEXAH State Machine")
    plt.xlabel("Time Step")
    plt.grid(True)

    plt.show()


def plot_2d_field(risk, distance, states):
    plt.figure(figsize=(8, 6))

    scatter = plt.scatter(
        risk,
        distance,
        c=states,
        cmap="viridis",
        s=25,
    )

    plt.colorbar(scatter, label="State")
    plt.xlabel("Risk")
    plt.ylabel("Distance to Separatrix")
    plt.title("NEXAH Controller on IEEE9 Field")

    plt.grid(True)
    plt.show()


# =============================
# MAIN
# =============================

if __name__ == "__main__":
    print("\n=== NEXAH IEEE9 Controller Run ===\n")

    risk, residual, distance, d2c = load_data(RUN_PATH)

    states, actions = run_controller(risk, residual, distance, d2c)

    plot_timeseries(risk, distance, states)
    plot_2d_field(risk, distance, states)

    print("\n=== DONE ===\n")
