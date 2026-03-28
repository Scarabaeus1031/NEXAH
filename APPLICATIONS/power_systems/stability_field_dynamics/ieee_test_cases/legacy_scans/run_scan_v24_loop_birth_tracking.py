import numpy as np
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core_coupling import run_single_coupling

print("\n--- V24 Loop / State Birth Tracking ---\n")

# Parameter (gezielt!)
base_load = 2.5
noise_strength = 0.15
steps = 20

loop_history = []
state_history = []
C_history = []

# --- Iterative evolution ---
for t in range(steps):

    print(f"Step {t}")

    try:
        res = run_single_coupling(
            base_load=base_load,
            noise_strength=noise_strength,
            noise_mode="gap"
        )

        loops = res.get("loops", 0)
        states = res.get("states", 0)
        C = res.get("C", 0)

        loop_history.append(loops)
        state_history.append(states)
        C_history.append(C)

    except Exception as e:
        print("failed:", e)
        loop_history.append(0)
        state_history.append(0)
        C_history.append(0)

# --- Plot ---
plt.figure()
plt.plot(loop_history, label="Loops")
plt.plot(state_history, label="States")
plt.xlabel("Time Step")
plt.ylabel("Count")
plt.title("Loop / State Birth Over Time")
plt.legend()
plt.show()

plt.figure()
plt.plot(C_history, label="Coupling C")
plt.xlabel("Time Step")
plt.ylabel("C")
plt.title("Coupling Evolution")
plt.legend()
plt.show()
