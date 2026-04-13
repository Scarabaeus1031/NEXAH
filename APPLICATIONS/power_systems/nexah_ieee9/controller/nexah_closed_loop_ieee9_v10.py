import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

# --- SETTINGS ---------------------------------------------------

STEPS = 160
lambda_val = 0.5

results = []

# --- MOCK SYSTEM (same behavior wie vorher) ---------------------

def simulate_system(lam):
    """
    Synthetic proxy for IEEE9 behavior
    """
    V = 1.0 - 0.2 * np.tanh((lam - 1.5))
    risk = max(0.0, (lam - 1.2)**2)
    dist = max(0.0, 1.2 - lam + 0.7)
    return V, risk, dist


def compute_gradient(prev_risk, risk):
    return risk - prev_risk


# --- V10 NAVIGATOR ---------------------------------------------

def compute_navigation_field(grad, distance, risk,
                             w_grad=1.0,
                             w_dist=0.5,
                             w_risk=0.3):

    field = - (w_grad * grad) \
            - (w_dist * (distance - 1.0)) \
            - (w_risk * risk)

    return field


def navigator_step(lambda_val, field, step_size=0.05, clamp=(0.5, 2.2)):
    lambda_new = lambda_val + step_size * field
    lambda_new = max(clamp[0], min(clamp[1], lambda_new))
    return lambda_new


# --- RUN --------------------------------------------------------

prev_risk = 0.0
prev_field = 0.0

for step in range(STEPS):

    V, risk, dist = simulate_system(lambda_val)
    grad = compute_gradient(prev_risk, risk)

    # --- NAVIGATOR FIELD ---
    field_raw = compute_navigation_field(grad, dist, risk)

    # smoothing (important!)
    field = 0.8 * prev_field + 0.2 * field_raw

    # --- UPDATE λ ---
    lambda_val = navigator_step(lambda_val, field)

    # pseudo phase (for visualization)
    psi = np.sin(lambda_val)

    print(f"[STEP {step}] lambda={lambda_val:.4f} psi={psi:.4f} "
          f"risk={risk:.4f} dist={dist:.4f} grad={grad:.4f} field={field:.4f}")

    results.append({
        "step": step,
        "lambda": lambda_val,
        "psi": psi,
        "risk": risk,
        "distance": dist,
        "grad": grad,
        "field": field,
        "V": V
    })

    prev_risk = risk
    prev_field = field


# --- SAVE -------------------------------------------------------

df = pd.DataFrame(results)

output_dir = "APPLICATIONS/power_systems/nexah_ieee9/results/controller_v10"
os.makedirs(output_dir, exist_ok=True)

csv_path = os.path.join(output_dir, "output_v10_data.csv")
plot_path = os.path.join(output_dir, "output_v10_plot.png")
phase_path = os.path.join(output_dir, "output_v10_phase.png")

df.to_csv(csv_path, index=False)

# --- PLOT λ + risk ---------------------------------------------

plt.figure()
plt.plot(df["lambda"], label="lambda")
plt.plot(df["risk"], label="risk")
plt.legend()
plt.title("V10 Navigator Dynamics")
plt.savefig(plot_path)
plt.close()

# --- PHASE PLOT (λ vs ψ) ---------------------------------------

plt.figure()
plt.plot(df["lambda"], df["psi"])
plt.xlabel("lambda")
plt.ylabel("psi")
plt.title("Phase Space (λ, ψ)")
plt.savefig(phase_path)
plt.close()

print("\nSaved:")
print(csv_path)
print(plot_path)
print(phase_path)
