import numpy as np
import matplotlib.pyplot as plt
import os, json

print("\n=== RUN 038 — REGIME ESCAPE DRIFT ===\n")

# =========================
# Trajectory (ersetzen!)
# =========================

t = np.linspace(0, 100, 100)
V = np.linspace(1, -4.2, 100)

V_base = V.copy()

# =========================
# Flow
# =========================

dV = np.gradient(V)

# =========================
# Gate (bewusst erweitert)
# =========================

gate_start = 18
gate_end   = 32

# =========================
# Drift Control
# =========================

V_control = V.copy()

base_strength = 0.02
flip_gain     = 4.0

# 👉 NEU: persistenter Drift nach Gate
drift_strength = 0.01

drift_active = False

for i in range(1, len(V)-1):

    flow = dV[i]
    direction = np.sign(flow)

    # =========================
    # Gate Phase
    # =========================

    if gate_start <= i <= gate_end:

        phase = (i - gate_start) / (gate_end - gate_start)

        if phase < 0.4:
            perturb = -direction * base_strength

        else:
            perturb = direction * base_strength * flip_gain

            # 👉 Trigger Drift
            drift_active = True

        V_control[i] += perturb

    # =========================
    # Post-Gate Drift (KEY!)
    # =========================

    elif i > gate_end and drift_active:

        # kleiner, aber persistenter Drift
        V_control[i] += direction * drift_strength


# =========================
# Metrics
# =========================

deviation = np.abs(V_control - V_base)

results = {
    "max_deviation": float(np.max(deviation)),
    "mean_deviation": float(np.mean(deviation)),
    "drift_active": drift_active,
    "interpretation": "Post-gate drift attempts regime escape."
}

print(results)

# =========================
# Output path FIX
# =========================

output_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "outputs", "run_038_regime_escape")
)
os.makedirs(output_path, exist_ok=True)

# =========================
# Plot 1 — State Space
# =========================

plt.figure(figsize=(6,5))
plt.plot(V_base, dV, color="black", label="baseline")
plt.plot(V_control, np.gradient(V_control), color="red", label="controlled")
plt.title("State Space: Regime Escape Drift")
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
