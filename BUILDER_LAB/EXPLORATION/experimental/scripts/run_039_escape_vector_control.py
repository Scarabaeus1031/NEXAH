import numpy as np
import matplotlib.pyplot as plt
import os, json

print("\n=== RUN 039 — ESCAPE VECTOR CONTROL ===\n")

# =========================
# Load / trajectory
# =========================

t = np.linspace(0, 100, 100)
V = np.linspace(1, -4.2, 100)  # TODO: echte trajectory einsetzen

V_base = V.copy()

# =========================
# First + second derivative
# =========================

dV  = np.gradient(V)
ddV = np.gradient(dV)   # ← KEY: curvature!

# =========================
# Gate window
# =========================

gate_start = 20
gate_end   = 30

# =========================
# Escape control (orthogonal)
# =========================

V_control = V.copy()

strength = 0.08   # stärker als vorher, aber gezielt

for i in range(2, len(V)-2):

    if gate_start <= i <= gate_end:

        curvature = ddV[i]

        # normalize curvature direction
        direction = np.sign(curvature)

        # orthogonal push (gegen lokale Krümmung)
        perturb = direction * strength

        V_control[i] += perturb

# =========================
# Metrics
# =========================

deviation = np.abs(V_control - V_base)

results = {
    "max_deviation": float(np.max(deviation)),
    "mean_deviation": float(np.mean(deviation)),
    "interpretation": "Curvature-based control attempts true escape from flow manifold."
}

print(results)

# =========================
# Output path FIX
# =========================

output_path = "outputs/run_039_escape_vector"
os.makedirs(output_path, exist_ok=True)

# =========================
# Plot 1 — State space
# =========================

plt.figure(figsize=(6,5))
plt.plot(V_base, dV, color="black", label="baseline")
plt.plot(V_control, np.gradient(V_control), color="red", label="controlled")
plt.title("State Space: Escape Vector Control")
plt.xlabel("V")
plt.ylabel("dV")
plt.legend()
plt.grid()

plt.savefig(f"{output_path}/figure_01_state.png")

# =========================
# Plot 2 — Time series
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

# =========================
# Plot 4 — Curvature
# =========================

plt.figure(figsize=(6,4))
plt.plot(ddV, color="purple")
plt.title("Curvature Field (d²V/dt²)")
plt.xlabel("time")
plt.ylabel("curvature")
plt.grid()

plt.savefig(f"{output_path}/figure_04_curvature.png")

# =========================
# Save results
# =========================

with open(f"{output_path}/results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nSaved to:", output_path)
