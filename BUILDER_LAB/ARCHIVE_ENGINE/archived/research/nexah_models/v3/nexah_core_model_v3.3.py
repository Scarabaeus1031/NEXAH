# nexah_core_model_v3.3.py

import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Simulation Core (gleich wie v3.2)
# -----------------------------

def simulate_system(
    n_nodes=8,
    T=120,
    dt=0.01,
    coupling_k=0.3,
    split_push=0.2,
    noise_level=0.02,
    collapse_mid=76.0
):
    t = np.arange(0, T, dt)
    N = len(t)

    # classical collapse proxy
    voltage = 1.0 / (1 + 0.02 * (t - collapse_mid) ** 2)
    voltage = np.clip(voltage, 0.1, 1.0)

    c = np.zeros((N, n_nodes))
    v = np.zeros((N, n_nodes))

    for i in range(n_nodes):
        c[0, i] = np.random.normal(0, 0.1)
        v[0, i] = np.random.normal(0, 0.1)

    for k in range(N - 1):
        mean_c = np.mean(c[k])
        for i in range(n_nodes):
            noise = noise_level * np.random.randn()

            coupling = coupling_k * (mean_c - c[k, i])

            v[k+1, i] = v[k, i] + dt * (
                -0.5 * c[k, i]
                + coupling
                + split_push * np.tanh(c[k, i])
            ) + noise

            c[k+1, i] = c[k, i] + dt * v[k, i]

    return t, c, v, voltage


# -----------------------------
# Detection v3.3 (FIXED)
# -----------------------------

def detect_split_v3(t, c, v):

    coherence = 1 / (1 + np.std(c, axis=1))
    curvature = np.abs(np.gradient(np.mean(c, axis=1)))
    winding = np.abs(np.gradient(np.sign(np.mean(v, axis=1))))

    # normalize
    curvature_n = curvature / (np.max(curvature) + 1e-6)
    winding_n = winding / (np.max(winding) + 1e-6)

    score = (
        0.4 * (1 - coherence)
        + 0.3 * curvature_n
        + 0.3 * winding_n
    )

    # -----------------------------
    # 🔥 FIX 1: Burn-in
    # -----------------------------
    MIN_TIME = 20.0

    # -----------------------------
    # 🔥 FIX 2: Adaptive threshold
    # -----------------------------
    burn_idx = np.where(t < MIN_TIME)[0]
    baseline_mean = np.mean(score[burn_idx])
    baseline_std = np.std(score[burn_idx])

    threshold = baseline_mean + 1.5 * baseline_std

    # -----------------------------
    # 🔥 FIX 3: Persistence
    # -----------------------------
    WINDOW = 50  # ~0.5s

    for i in range(len(score) - WINDOW):

        if t[i] < MIN_TIME:
            continue

        if np.all(score[i:i+WINDOW] > threshold):
            return t[i]

    return None


def detect_classic(t, voltage):
    threshold = 0.7
    for i in range(len(voltage)):
        if voltage[i] < threshold:
            return t[i]
    return None


# -----------------------------
# Single Run Test
# -----------------------------

def run_single_test():

    t, c, v, voltage = simulate_system()

    split_t = detect_split_v3(t, c, v)
    classic_t = detect_classic(t, voltage)

    lead = None
    if split_t and classic_t:
        lead = classic_t - split_t

    print("\nNEXAH v3.3 result")
    print("------------------")
    print(f"split:   {split_t}")
    print(f"classic: {classic_t}")
    print(f"lead:    {lead}")

    plt.figure(figsize=(10, 4))
    plt.plot(t, voltage, label="voltage")

    if split_t:
        plt.axvline(split_t, color='green', label="split")
    if classic_t:
        plt.axvline(classic_t, color='red', label="classic")

    plt.axhline(0.7, linestyle="--")
    plt.legend()
    plt.show()


# -----------------------------
# Robustness Test
# -----------------------------

def robustness_test(n_runs=20):

    leads = []

    for i in range(n_runs):

        t, c, v, voltage = simulate_system(
            noise_level=0.02 + 0.01*np.random.rand()
        )

        split_t = detect_split_v3(t, c, v)
        classic_t = detect_classic(t, voltage)

        if split_t and classic_t:
            lead = classic_t - split_t
            leads.append(lead)
            print(f"run {i:02d} | split={split_t:.2f} | lead={lead:.2f}")

    if len(leads) > 0:
        print("\n--- Summary ---")
        print(f"mean lead: {np.mean(leads):.2f}s")
        print(f"std lead:  {np.std(leads):.2f}s")
        print(f"min lead:  {np.min(leads):.2f}s")
        print(f"max lead:  {np.max(leads):.2f}s")
        print(f"success rate: {len(leads)}/{n_runs}")


# -----------------------------
# Main
# -----------------------------

if __name__ == "__main__":

    run_single_test()
    robustness_test()
