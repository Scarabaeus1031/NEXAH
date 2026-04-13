# nexah_closed_loop_ieee9_v10.py
# V10.1 — Minimal Navigator with Boundary Repulsion (Fix)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# --- config ---
STEPS = 160
LAMBDA_INIT = 0.5
LAMBDA_MIN = 0.5
LAMBDA_MAX = 2.2

# --- synthetic fields (same as before) ---
def compute_risk(lmbda):
    return 1 / (1 + np.exp(-(lmbda - 1.6) * 5))

def compute_distance(lmbda):
    return 1.4 - 0.4 * np.exp(-(lmbda - 1.5)**2 * 3)

def compute_navigation_field(grad, dist, risk):
    return -grad - (dist - 1.0) - risk

# --- init ---
lambda_val = LAMBDA_INIT
lambda_history = []
risk_history = []
dist_history = []
field_history = []

prev_risk = None

# --- loop ---
for step in range(STEPS):

    risk = compute_risk(lambda_val)
    dist = compute_distance(lambda_val)

    if prev_risk is None:
        grad = risk
    else:
        grad = risk - prev_risk

    # --- 🔥 NEW: boundary repulsion (fix) ---
    center = 1.3
    repulsion = 0.3 * (center - lambda_val)

    # --- field ---
    field_raw = compute_navigation_field(grad, dist, risk) + repulsion

    # smooth update
    field = 0.8 * (field_history[-1] if field_history else 0) + 0.2 * field_raw

    # update lambda
    lambda_val += 0.05 * field

    # clamp
    lambda_val = np.clip(lambda_val, LAMBDA_MIN, LAMBDA_MAX)

    # store
    lambda_history.append(lambda_val)
    risk_history.append(risk)
    dist_history.append(dist)
    field_history.append(field)

    prev_risk = risk

    print(f"[STEP {step}] lambda={lambda_val:.4f} risk={risk:.4f} dist={dist:.4f} grad={grad:.4f} field={field:.4f}")

# --- save ---
out_dir = "APPLICATIONS/power_systems/nexah_ieee9/results/controller_v10"
os.makedirs(out_dir, exist_ok=True)

df = pd.DataFrame({
    "lambda": lambda_history,
    "risk": risk_history,
    "distance": dist_history,
    "field": field_history
})

df.to_csv(f"{out_dir}/output_v10_data.csv", index=False)

# --- plot ---
plt.figure(figsize=(10,5))
plt.plot(lambda_history, label="lambda")
plt.plot(risk_history, label="risk")
plt.plot(dist_history, label="distance")
plt.legend()
plt.title("V10.1 Navigator Dynamics")
plt.savefig(f"{out_dir}/output_v10_plot.png")
plt.close()

# --- phase plot ---
plt.figure(figsize=(6,6))
plt.plot(lambda_history, risk_history)
plt.xlabel("lambda")
plt.ylabel("risk")
plt.title("Phase: lambda vs risk")
plt.savefig(f"{out_dir}/output_v10_phase.png")
plt.close()

print("\nSaved:")
print(f"{out_dir}/output_v10_data.csv")
print(f"{out_dir}/output_v10_plot.png")
print(f"{out_dir}/output_v10_phase.png")
