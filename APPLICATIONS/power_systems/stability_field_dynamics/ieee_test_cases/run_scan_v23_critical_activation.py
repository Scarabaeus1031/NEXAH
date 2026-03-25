import numpy as np
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core_coupling import run_single_coupling

print("\n--- V23 Critical Activation Map ---\n")

# Parameter ranges
load_values = np.linspace(1.0, 4.0, 8)
noise_values = np.linspace(0.0, 0.3, 10)

activation_map = np.zeros((len(load_values), len(noise_values)))
delta_loops_map = np.zeros_like(activation_map)
delta_states_map = np.zeros_like(activation_map)
delta_C_map = np.zeros_like(activation_map)

# Baseline (no noise)
baseline = {}
for i, load in enumerate(load_values):
    res = run_single_coupling(base_load=load, noise_strength=0.0)
    baseline[load] = res

# Scan
for i, load in enumerate(load_values):
    for j, noise in enumerate(noise_values):

        print(f"Load={load:.2f}, Noise={noise:.3f}")

        try:
            res = run_single_coupling(base_load=load, noise_strength=noise)
            base = baseline[load]

            # Differences
            d_loops = res["loops"] - base["loops"]
            d_states = res["states"] - base["states"]
            d_C = res["C"] - base["C"]

            delta_loops_map[i, j] = d_loops
            delta_states_map[i, j] = d_states
            delta_C_map[i, j] = d_C

            # Activation metric
            activation = (
                abs(d_loops)
                + abs(d_states)
                + abs(d_C) * 100  # scaled
            )

            activation_map[i, j] = activation

        except Exception as e:
            print("failed:", e)
            activation_map[i, j] = np.nan

# --- Plot ---
plt.figure()
plt.imshow(
    activation_map,
    aspect="auto",
    origin="lower",
    extent=[noise_values[0], noise_values[-1], load_values[0], load_values[-1]],
)
plt.colorbar(label="Activation Intensity")
plt.xlabel("Noise Strength")
plt.ylabel("Base Load")
plt.title("Critical Activation Map")
plt.show()

# --- Extra diagnostics ---
plt.figure()
plt.imshow(delta_loops_map, aspect="auto", origin="lower",
           extent=[noise_values[0], noise_values[-1], load_values[0], load_values[-1]])
plt.colorbar(label="Δ Loops")
plt.title("Loop Activation Map")
plt.show()

plt.figure()
plt.imshow(delta_states_map, aspect="auto", origin="lower",
           extent=[noise_values[0], noise_values[-1], load_values[0], load_values[-1]])
plt.colorbar(label="Δ States")
plt.title("State Activation Map")
plt.show()

plt.figure()
plt.imshow(delta_C_map, aspect="auto", origin="lower",
           extent=[noise_values[0], noise_values[-1], load_values[0], load_values[-1]])
plt.colorbar(label="Δ Coupling C")
plt.title("Coupling Shift Map")
plt.show()
