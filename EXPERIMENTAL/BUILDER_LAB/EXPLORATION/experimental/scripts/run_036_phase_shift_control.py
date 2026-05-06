import numpy as np
import matplotlib.pyplot as plt
import os, json

print("\n=== RUN 036 — PHASE-SHIFT CONTROL ===\n")

# =========================
# Trajectory (ersetzen!)
# =========================

t = np.linspace(0, 100, 100)
V = np.linspace(1, -4.2, 100)  # TODO: echte trajectory

V_base = V.copy()

# =========================
# Flow
# =========================

# =========================
# Gate definition
# =========================

gate_start = 20
gate_end   = 30

# =========================
# PHASE-SHIFT CONTROL
# =========================

V_control = V.copy()

base_strength = 0.008
iterations = 6

for k in range(iterations):

    dV_local = np.gradient(V_control)

    for i in range(1, len(V_control)-1):

        if gate_start <= i <= gate_end:

            flow = dV_local[i]
            direction = np.sign(flow)

            # 🔥 Phase ramp (entscheidend!)
            phase = (i - gate_start) / (gate_end - gate_start)

            # steigende + oszillierende Kontrolle
            strength = base_strength * (1 + 2*phase)

            # optional: leichte Oszillation
            oscillation = np.sin(phase * np.pi)

            perturb = direction * strength * oscillation

            V_control[i] += perturb

# =========================
# Metrics
# =========================

deviation = np.abs(V_control - V_base)

results = {
    "max_deviation": float(np.max(deviation)),
    "mean_deviation": float(np.mean(deviation)),
    "interpretation": "Phase-aligned control injects structured drift across gate."
}

print(results)

# =========================
# Output
# =========================

BASE_DIR = "/Users/tho2020/Documents/GitHub/NEXAH"
output_path = os.path.join(BASE_DIR, "outputs/run_036_phase_control")
os.makedirs(output_path, exist_ok=True)

# =========================
# Plot 1 — State Space
# =========================

plt.figure(figsize=(6,5))
plt.plot(V_base, np.gradient(V_base), color="black", label="baseline")
plt.plot(V_control, np.gradient(V_control), color="red", label="controlled")
plt.title("State Space: Phase-Shift Control")
plt.xlabel("V")
plt.ylabel("dV")
plt.legend()
plt.grid()

plt.savefig(f"{output_path}/figure_01_state.png")
plt.close()

# =========================
# Plot 2 — Time Series
# =========================

plt.figure(figsize=(6,4))
plt.plot(V_base, label="baseline")
plt.plot(V_control, label="controlled", color="red")
plt.title("Time Series")
plt.xlabel("time")
plt.ylabel("V")
plt.legend()
plt.grid()

plt.savefig(f"{output_path}/figure_02_time.png")
plt.close()

# =========================
# Plot 3 — Deviation
# =========================

plt.figure(figsize=(6,4))
plt.plot(deviation, color="orange")
plt.title("Control Impact (|ΔV|)")
plt.xlabel("time")
plt.ylabel("difference")
plt.grid()

plt.savefig(f"{output_path}/figure_03_deviation.png")
plt.close()

# =========================
# Save results
# =========================

with open(f"{output_path}/results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nSaved to:", output_path)
