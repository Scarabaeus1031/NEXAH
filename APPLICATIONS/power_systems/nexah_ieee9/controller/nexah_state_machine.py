# nexah_state_machine_demo.py

from enum import Enum, auto
from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt


# =============================
# STATE MACHINE
# =============================

class NexahState(Enum):
    NEXIT = auto()
    ENGAGE = auto()
    LOCK = auto()
    RELEASE = auto()


@dataclass
class NexahMetrics:
    risk: float
    risk_slope: float
    d2c: float
    residual: float
    distance_to_sep: float


@dataclass
class NexahThresholds:
    d_engage: float = 4.0
    d_lock: float = 1.8
    d_release: float = 4.5

    r_engage: float = 0.18
    r_release: float = 0.12

    c_lock: float = 0.08
    res_lock: float = 0.25


class NexahStateMachineController:
    def __init__(self, thresholds: NexahThresholds):
        self.thresholds = thresholds
        self.state = NexahState.NEXIT

    def transition(self, m: NexahMetrics) -> NexahState:
        prev_state = self.state
        t = self.thresholds

        if self.state == NexahState.NEXIT:
            if (
                m.distance_to_sep < t.d_engage
                and m.risk > t.r_engage
                and m.risk_slope > 0
            ):
                self.state = NexahState.ENGAGE

        elif self.state == NexahState.ENGAGE:
            if (
                m.distance_to_sep < t.d_lock
                and (m.d2c > t.c_lock or m.residual > t.res_lock)
            ):
                self.state = NexahState.LOCK
            elif m.distance_to_sep > t.d_release and m.risk < t.r_release:
                self.state = NexahState.NEXIT

        elif self.state == NexahState.LOCK:
            if m.risk_slope <= 0 or m.distance_to_sep > t.d_lock:
                self.state = NexahState.RELEASE

        elif self.state == NexahState.RELEASE:
            if m.distance_to_sep > t.d_release and m.risk < t.r_release:
                self.state = NexahState.NEXIT
            elif m.distance_to_sep < t.d_lock:
                self.state = NexahState.LOCK

        if prev_state != self.state:
            print(f"[STATE CHANGE] {prev_state.name} → {self.state.name}")

        return self.state

    def action(self, m: NexahMetrics) -> str:
        state = self.transition(m)

        if state == NexahState.NEXIT:
            action = "MONITOR"

        elif state == NexahState.ENGAGE:
            action = "PREEMPTIVE_STABILIZE"

        elif state == NexahState.LOCK:
            if m.residual > self.thresholds.res_lock:
                action = "REDUCE_LOAD + REACTIVE_SUPPORT"
            else:
                action = "STRONG_INTERVENTION"

        elif state == NexahState.RELEASE:
            action = "DAMPEN + SMOOTH_RECOVERY"

        else:
            action = "MONITOR"

        print(
            f"[STEP] state={state.name} | "
            f"risk={m.risk:.3f} | "
            f"d={m.distance_to_sep:.2f} | "
            f"slope={m.risk_slope:.3f} | "
            f"action={action}"
        )

        return action


# =============================
# SIMULATION
# =============================

def simulate():
    controller = NexahStateMachineController(NexahThresholds())

    steps = 100

    risk_values = []
    distance_values = []
    state_values = []

    for step in range(steps):
        risk = 1 / (1 + np.exp(-(step - 60) * 0.1))
        distance = 5 - 0.04 * step
        d2c = 0.05 + 0.002 * step
        residual = 0.1 + 0.01 * step

        if step > 70:
            risk_slope = -0.03
        else:
            risk_slope = 0.02

        m = NexahMetrics(
            risk=risk,
            risk_slope=risk_slope,
            d2c=d2c,
            residual=residual,
            distance_to_sep=distance,
        )

        action = controller.action(m)

        risk_values.append(risk)
        distance_values.append(distance)
        state_values.append(controller.state.value)

    return risk_values, distance_values, state_values


# =============================
# VISUALIZATION
# =============================

def plot_results(risk, distance, states):
    plt.figure(figsize=(10, 6))

    plt.plot(risk, label="Risk")
    plt.plot(distance, label="Distance to Separatrix")
    plt.plot(states, label="State (numeric)", linestyle="--")

    plt.legend()
    plt.title("NEXAH State Machine Dynamics")
    plt.xlabel("Time Step")
    plt.ylabel("Value")

    plt.grid(True)
    plt.show()


# =============================
# MAIN
# =============================

if __name__ == "__main__":
    risk, distance, states = simulate()
    plot_results(risk, distance, states)
