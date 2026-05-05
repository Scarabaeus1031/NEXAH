import numpy as np
import matplotlib.pyplot as plt

# =========================
# SETTINGS
# =========================

N = 200
K = 2.5
dt = 0.05
T = 200

np.random.seed(42)

# intrinsic frequencies
omega = np.random.normal(0, 1, N)

# initial phases
theta0 = np.random.uniform(0, 2*np.pi, N)

# =========================
# CONTROL LAW (from V2)
# =========================

def control(phi):
    # smooth increasing control (from your fit)
    return 0.5 + 0.5 * (phi / (2*np.pi))

# =========================
# KURAMOTO STEP
# =========================

def kuramoto_step(theta, use_control=False):

    N = len(theta)
    sin_diff = np.sin(theta[:, None] - theta[None, :])
    coupling = -K / N * np.sum(sin_diff, axis=1)

    if use_control:
        phi = np.angle(np.mean(np.exp(1j * theta)))
        s = control(phi)
        coupling *= s

    return omega + coupling

# =========================
# RUN SIMULATION
# =========================

def run_sim(use_control=False):

    theta = theta0.copy()

    drift_series = []
    events = 0

    for t in range(int(T / dt)):

        dtheta = kuramoto_step(theta, use_control)
        theta += dt * dtheta

        # wrap
        theta = np.mod(theta, 2*np.pi)

        # drift measure
        drift = np.std(dtheta)
        drift_series.append(drift)

        # IOTA-like event
        if drift > np.mean(drift_series) + 2*np.std(drift_series):
            events += 1

    return np.array(drift_series), events

# =========================
# RUN BOTH CASES
# =========================

drift_no_ctrl, events_no = run_sim(use_control=False)
drift_ctrl, events_ctrl = run_sim(use_control=True)

# =========================
# RESULTS
# =========================

print("=== RESULTS ===")
print(f"No Control → mean drift: {np.mean(drift_no_ctrl):.4f}, events: {events_no}")
print(f"With Control → mean drift: {np.mean(drift_ctrl):.4f}, events: {events_ctrl}")

# =========================
# PLOT
# =========================

plt.figure(figsize=(10,5))
plt.plot(drift_no_ctrl, label="No Control")
plt.plot(drift_ctrl, label="With Control")
plt.title("Drift Comparison (Control vs No Control)")
plt.xlabel("Time")
plt.ylabel("Drift (std dθ)")
plt.legend()
plt.grid()
plt.show()
