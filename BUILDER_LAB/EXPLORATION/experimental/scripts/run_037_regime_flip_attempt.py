import numpy as np
import matplotlib.pyplot as plt
import os, json

print("\n=== RUN 037 — REGIME FLIP ATTEMPT ===\n")

# =========================
# Trajectory (placeholder → ersetze mit echter!)
# =========================

t = np.linspace(0, 100, 100)
V = np.linspace(1, -4.2, 100)

V_base = V.copy()

# =========================
# Flow
# =========================

dV = np.gradient(V)

# =========================
# Gate (aus bisherigen Runs)
# =========================

gate_start = 20
gate_end   = 28

# =========================
# Regime Flip Control
# =========================

V_control = V.copy()

base_strength = 0.02   # etwas stärker als vorher
flip_gain     = 3.0    # entscheidend!

for i in range(1, len(V)-1):

    if gate_start <= i <= gate_end:

        flow = dV[i]
        direction = np.sign(flow)

        # Phase innerhalb Gate
        phase = (i - gate_start) / (gate_end - gate_start)

        # 🚨 entscheidender Punkt:
        # erst sanft → dann überkritisch
        if phase < 0.5:
            perturb = -direction * base_strength
        else:
            perturb = direction * base_strength * flip_gain

        V_control[i] += perturb


# =========================
# Metrics
# =========================

deviation = np.abs(V_control - V_base)

results = {
    "max_deviation": float(np.max(deviation)),
    "mean_deviation": float(np.mean(deviation)),
    "interpretation": "Attempted regime flip using asymmetric gate forcing."
}

print(results)

# =========================
# Output path FIX
# =========================

output_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "outputs", "run_037_regime_flip")
)
os.makedirs(output_path, exist_ok=True)

# =========================
# Plot 1 — State Space
# =========================

plt.figure(figsize=(6,5))
plt.plot(V_base, dV, color="black", label="baseline")
plt.plot(V_control, np.gradient(V_control), color="red", label="controlled")
plt.title("State Space: Regime Flip Attempt")
plt.xlabel("V")
plt.ylabel("dV")
plt.legend()
plt.grid()

plt.savefig(os.path.join(output_path, "figure_01_state.png"))
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

plt.savefig(os.path.join(output_path, "figure_02_time.png"))
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

plt.savefig(os.path.join(output_path, "figure_03_deviation.png"))
plt.close()

# =========================
# Save results
# =========================

with open(os.path.join(output_path, "results.json"), "w") as f:
    json.dump(results, f, indent=2)

print("\nSaved to:", output_path)
