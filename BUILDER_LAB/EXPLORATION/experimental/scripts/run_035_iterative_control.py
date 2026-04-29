import numpy as np
import matplotlib.pyplot as plt
import os, json

print("\n=== RUN 035 — ITERATIVE CONTROL TEST ===\n")

# =========================
# Trajectory (ersetzen mit echter!)
# =========================

t = np.linspace(0, 100, 100)
V = np.linspace(1, -4.2, 100)  # TODO: echte trajectory einsetzen

V_base = V.copy()

# =========================
# Flow
# =========================

dV = np.gradient(V)

# =========================
# Gate (wie vorher)
# =========================

gate_start = 22
gate_end   = 27

# =========================
# ITERATIVE CONTROL
# =========================

V_control = V.copy()

strength = 0.01          # kleiner als vorher
iterations = 5           # 🔥 entscheidend

for k in range(iterations):

    dV_local = np.gradient(V_control)

    for i in range(1, len(V_control)-1):

        if gate_start <= i <= gate_end:

            flow = dV_local[i]
            direction = np.sign(flow)

            # diesmal KEIN flip → sondern entlang Flow modulieren
            perturb = direction * strength

            V_control[i] += perturb

# =========================
# Metrics
# =========================

deviation = np.abs(V_control - V_base)

results = {
    "max_deviation": float(np.max(deviation)),
    "mean_deviation": float(np.mean(deviation)),
    "iterations": iterations,
    "interpretation": "Iterative control accumulates small flow-aligned perturbations."
}

print(results)

# =========================
# Output folder
# =========================

output_path = "../outputs/run_035_iterative_control"
os.makedirs(output_path, exist_ok=True)

# =========================
# Plot 1 — State Space
# =========================

plt.figure(figsize=(6,5))
plt.plot(V_base, np.gradient(V_base), color="black", label="baseline")
plt.plot(V_control, np.gradient(V_control), color="red", label="controlled")
plt.title("State Space: Iterative Control")
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
