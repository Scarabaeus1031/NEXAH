import numpy as np
import matplotlib.pyplot as plt
import os
import json

# =========================
# OUTPUT PATH
# =========================

OUTPUT_DIR = "RESEARCH/VALIDATION/causality/results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# SETTINGS
# =========================

N = 200
K = 2.5
dt = 0.05
T = 200

np.random.seed(42)

omega = np.random.normal(0, 1, N)
theta0 = np.random.uniform(0, 2*np.pi, N)

# =========================
# CONTROL LAW (baseline)
# =========================

def s_base(phi):
    return 0.5 + 0.5 * (phi / (2*np.pi))

# variants
def s_invert(phi):
    return 1.5 - s_base(phi)

def s_damped(phi):
    return 1.0 - 0.5 * s_base(phi)

def s_inverse(phi):
    return 1.0 / (0.1 + s_base(phi))

# =========================
# STEP FUNCTION
# =========================

def kuramoto_step(theta, control_fn=None):

    N = len(theta)
    sin_diff = np.sin(theta[:, None] - theta[None, :])
    coupling = -K / N * np.sum(sin_diff, axis=1)

    if control_fn is not None:
        phi = np.angle(np.mean(np.exp(1j * theta)))
        s = control_fn(phi)
        coupling *= s

    return omega + coupling

# =========================
# RUN SIMULATION
# =========================

def run_sim(control_fn=None):

    theta = theta0.copy()
    drift_series = []
    events = 0

    for t in range(int(T / dt)):

        dtheta = kuramoto_step(theta, control_fn)
        theta += dt * dtheta
        theta = np.mod(theta, 2*np.pi)

        drift = np.std(dtheta)
        drift_series.append(drift)

        if drift > np.mean(drift_series) + 2*np.std(drift_series):
            events += 1

    return np.array(drift_series), events

# =========================
# RUN ALL CASES
# =========================

cases = {
    "no_control": None,
    "aligned": s_base,
    "invert": s_invert,
    "damped": s_damped,
    "inverse": s_inverse
}

results = {}

for name, fn in cases.items():
    drift, events = run_sim(fn)
    results[name] = {
        "mean_drift": float(np.mean(drift)),
        "events": int(events)
    }
    np.save(f"{OUTPUT_DIR}/drift_{name}.npy", drift)

# =========================
# PRINT RESULTS
# =========================

print("\n=== CONTROL TEST V4 RESULTS ===")

for k, v in results.items():
    print(f"{k:12s} → drift: {v['mean_drift']:.4f}, events: {v['events']}")

# =========================
# SAVE JSON
# =========================

with open(f"{OUTPUT_DIR}/control_v4_summary.json", "w") as f:
    json.dump(results, f, indent=4)

# =========================
# PLOT
# =========================

plt.figure(figsize=(12,6))

for name in cases.keys():
    drift = np.load(f"{OUTPUT_DIR}/drift_{name}.npy")
    plt.plot(drift, label=name)

plt.title("Control Comparison (V4)")
plt.xlabel("Time")
plt.ylabel("Drift (std dθ)")
plt.legend()
plt.grid()

plt.savefig(f"{OUTPUT_DIR}/control_v4_comparison.png", dpi=200)
plt.show()
