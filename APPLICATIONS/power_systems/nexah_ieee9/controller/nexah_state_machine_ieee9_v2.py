import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

from nexah_ieee9.controller.nexah_state_machine import (
    NexahStateMachineController,
    NexahMetrics,
    NexahThresholds,
    NexahState
)

# =========================
# CONFIG
# =========================

SAVE_DIR = "APPLICATIONS/power_systems/nexah_ieee9/results/controller_runs"
os.makedirs(SAVE_DIR, exist_ok=True)

RUN_ID = datetime.now().strftime("run_controller_%Y%m%d_%H%M%S")

# =========================
# CONTROLLER EXTENSION
# =========================

class StableNexahController(NexahStateMachineController):
    def __init__(self, thresholds):
        super().__init__(thresholds)
        self.cooldown = 0
        self.min_hold_steps = 3
        self.last_state_change = 0

    def transition(self, m: NexahMetrics, step: int):
        t = self.thresholds

        if self.cooldown > 0:
            self.cooldown -= 1
            return self.state

        prev_state = self.state

        # ---- ORIGINAL LOGIC ----
        super().transition(m)

        # ---- HYSTERESIS ----
        if self.state != prev_state:
            if step - self.last_state_change < self.min_hold_steps:
                self.state = prev_state
            else:
                self.cooldown = 2
                self.last_state_change = step

        return self.state

    def action(self, m: NexahMetrics, step: int):
        state = self.transition(m, step)

        # ---- STEERING LOGIC ----
        if state == NexahState.NEXIT:
            return "MONITOR"

        if state == NexahState.ENGAGE:
            return "PREEMPTIVE_STABILIZE"

        if state == NexahState.LOCK:
            if m.distance_to_sep < 0.3:
                return "STRONG_INTERVENTION + STEER_OUT"
            return "STRONG_INTERVENTION"

        if state == NexahState.RELEASE:
            return "DAMPEN + RECOVER"

        return "MONITOR"


# =========================
# FAKE IEEE9-LIKE DATA
# =========================

N = 120
risk = np.zeros(N)
distance = np.zeros(N)

# stable region
for i in range(90):
    risk[i] = 0.02 + 0.01 * np.sin(i / 5)
    distance[i] = 0.75 - 0.007 * i

# collapse spike
risk[90:100] = np.linspace(0.1, 0.8, 10)
distance[90:100] = np.linspace(0.1, 0.02, 10)

# recovery
risk[100:] = np.linspace(0.3, 0.01, 20)
distance[100:] = np.linspace(0.2, 0.4, 20)

risk_slope = np.gradient(risk)
d2c = np.gradient(np.gradient(risk))
residual = np.abs(risk - np.mean(risk))

# =========================
# RUN CONTROLLER
# =========================

thresholds = NexahThresholds()
controller = StableNexahController(thresholds)

states = []
actions = []

log_lines = []

print("\n=== NEXAH Controller v2 Run ===\n")

for i in range(N):
    m = NexahMetrics(
        risk=risk[i],
        risk_slope=risk_slope[i],
        d2c=d2c[i],
        residual=residual[i],
        distance_to_sep=distance[i],
    )

    prev_state = controller.state
    action = controller.action(m, i)
    new_state = controller.state

    states.append(new_state.value)
    actions.append(action)

    line = f"[STEP {i}] state={new_state.name} | risk={m.risk:.3f} | d={m.distance_to_sep:.3f} | action={action}"
    print(line)
    log_lines.append(line)

    if prev_state != new_state:
        change = f"[STATE CHANGE] {prev_state.name} → {new_state.name}"
        print(change)
        log_lines.append(change)

# =========================
# SAVE LOG
# =========================

log_path = os.path.join(SAVE_DIR, f"{RUN_ID}.txt")
with open(log_path, "w") as f:
    f.write("\n".join(log_lines))

# =========================
# PLOT
# =========================

plt.figure(figsize=(10, 5))

plt.plot(risk, label="Risk")
plt.plot(distance, label="Distance to Separatrix")
plt.plot(states, "--", label="Controller State")

plt.title("NEXAH Controller v2 (Stabilized + Steering)")
plt.xlabel("Time Step")
plt.ylabel("Value")
plt.legend()
plt.grid(True)

img_path = os.path.join(SAVE_DIR, f"{RUN_ID}.png")
plt.savefig(img_path, dpi=200)
plt.close()

print(f"\nSaved:\n{log_path}\n{img_path}")
