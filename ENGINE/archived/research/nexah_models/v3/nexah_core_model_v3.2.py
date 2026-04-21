# nexah_core_model_v3.2.py

import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Simulation Core (aus v3.1)
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

    # state init
    c = np.zeros((N, n_nodes))
    v = np.zeros((N, n_nodes))

    for i in range(n_nodes):
        c[0, i] = np.random.normal(0, 0.1)
        v[0, i] = np.random.normal(0, 0.1)

    # simulate
    for k in range(N - 1):
        mean_c = np.mean(c[k])
        for i in range(n_nodes):
            noise = noise_level * np.random.randn()

            coupling = coupling_k * (mean_c - c[k, i])

            # simple nonlinear oscillator + coupling
            v[k+1, i] = v[k, i] + dt * (
                -0.5 * c[k, i]
                + coupling
                + split_push * np.tanh(c[k, i])
            ) + noise

            c[k+1, i] = c[k, i] + dt * v[k, i]

    return t, c, v, voltage


# -----------------------------
# Detection logic
# -----------------------------

def detect_split(t, c, v):
    # coherence loss
    coherence = 1 / (1 + np.std(c, axis=1))

    # curvature proxy
    curvature = np.abs(np.gradient(np.mean(c, axis=1)))

    # winding proxy
    winding = np.abs(np.gradient(np.sign(np.mean(v, axis=1))))

    # normalized composite score
    score = (
        0.4 * (1 - coherence)
        + 0.3 * curvature / (np.max(curvature) + 1e-6)
        + 0.3 * winding / (np.max(winding) + 1e-6)
    )

    threshold = 0.6

    for i in range(len(score)):
        if score[i] > threshold:
            return t[i]

    return None


def detect_classic(t, voltage):
    threshold = 0.7
    for i in range(len(voltage)):
        if voltage[i] < threshold:
            return t[i]
    return None


# -----------------------------
# Parameter Scan (Heatmap)
# -----------------------------

def run_parameter_scan():

    couplings = np.linspace(0.1, 0.6, 12)
    split_push_vals = np.linspace(0.05, 0.35, 12)

    lead_map = np.zeros((len(couplings), len(split_push_vals)))

    for i, k in enumerate(couplings):
        for j, sp in enumerate(split_push_vals):

            t, c, v, voltage = simulate_system(
                coupling_k=k,
                split_push=sp
            )

            split_t = detect_split(t, c, v)
            classic_t = detect_classic(t, voltage)

            if split_t is not None and classic_t is not None:
                lead = classic_t - split_t
            else:
                lead = np.nan

            lead_map[i, j] = lead

            print(f"k={k:.2f}, sp={sp:.2f} → lead={lead}")

    return couplings, split_push_vals, lead_map


# -----------------------------
# Plot Heatmap
# -----------------------------

def plot_heatmap(couplings, split_push_vals, lead_map):

    plt.figure(figsize=(10, 6))

    im = plt.imshow(
        lead_map,
        origin='lower',
        aspect='auto',
        extent=[
            split_push_vals[0],
            split_push_vals[-1],
            couplings[0],
            couplings[-1]
        ]
    )

    plt.colorbar(im, label="Lead time (s)")

    plt.xlabel("split_push_gain")
    plt.ylabel("coupling_k")
    plt.title("NEXAH v3.2 – Lead Time Heatmap")

    plt.show()


# -----------------------------
# Main
# -----------------------------

if __name__ == "__main__":

    couplings, split_push_vals, lead_map = run_parameter_scan()

    plot_heatmap(couplings, split_push_vals, lead_map)
