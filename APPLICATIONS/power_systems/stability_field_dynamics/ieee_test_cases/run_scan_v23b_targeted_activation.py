import numpy as np
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core_coupling import run_single_coupling

print("\n--- V23b Targeted Activation (Gap Injection) ---\n")

# Parameter ranges
load_values = np.linspace(1.0, 4.0, 8)
noise_values = np.linspace(0.0, 0.3, 10)

activation_map = np.zeros((len(load_values), len(noise_values)))

# --- SAFE WRAPPER ---
def safe_run(load, noise, mode="global"):
    try:
        return run_single_coupling(
            base_load=load,
            noise_strength=noise,
            noise_mode=mode  # 🔥 NEW
        )
    except TypeError:
        # fallback if not implemented yet
        return run_single_coupling(base_load=load)

# --- Baseline ---
baseline = {}
for load in load_values:
    baseline[load] = safe_run(load, 0.0)

# --- Scan ---
for i, load in enumerate(load_values):
    for j, noise in enumerate(noise_values):

        print(f"Load={load:.2f}, Noise={noise:.3f}")

        try:
            res = safe_run(load, noise, mode="gap")
            base = baseline[load]

            d_loops = res.get("loops", 0) - base.get("loops", 0)
            d_states = res.get("states", 0) - base.get("states", 0)
            d_C = res.get("C", 0) - base.get("C", 0)

            activation = abs(d_loops) + abs(d_states) + abs(d_C) * 100
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
plt.colorbar(label="Activation (Gap Targeted)")
plt.xlabel("Noise Strength")
plt.ylabel("Base Load")
plt.title("Targeted Activation Map (Gap)")
plt.show()
