import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# 1. SIGNAL DESIGN (true regime transition)
# ============================================================

def generate_signal(t, seed=0):
    np.random.seed(seed)
    x = np.zeros_like(t)

    # Phase 1 — stable
    x += 0.2 * np.sin(0.5 * t)

    # Phase 2 — energy build-up
    mask2 = t > 30
    x[mask2] += 0.05 * (t[mask2] - 30) * np.sin(1.5 * t[mask2])

    # Phase 3 — destructive interference (counter-wave)
    mask3 = t > 60
    x[mask3] += -0.8 * np.sin(1.5 * t[mask3] + np.pi/4)

    # Phase 4 — breakdown / decoherence
    mask4 = t > 75
    x[mask4] += 0.3 * np.random.randn(np.sum(mask4))

    return x


# ============================================================
# 2. COHERENCE METRIC (multi-lag)
# ============================================================

def compute_coherence(x, window=25):
    C = np.full(len(x), np.nan)

    for i in range(window, len(x)):
        segment = x[i-window:i]

        lags = [1, 2, 3, 5]
        vals = []

        for lag in lags:
            if len(segment) > lag:
                c = np.corrcoef(segment[:-lag], segment[lag:])[0, 1]
                if not np.isnan(c):
                    vals.append(c)

        if vals:
            C[i] = np.mean(vals)

    return C


# ============================================================
# 3. GATE DETECTION (sustained collapse)
# ============================================================

def detect_gates(C, epsilon=0.2, min_duration=8):
    mask = C < epsilon
    gates = []

    start = None

    for i, val in enumerate(mask):
        if val and start is None:
            start = i
        elif not val and start is not None:
            if i - start >= min_duration:
                gates.append((start, i))
            start = None

    return gates


# ============================================================
# 4. MAIN PIPELINE
# ============================================================

def run_simulation():
    t = np.linspace(0, 100, 1000)

    x = generate_signal(t)
    C = compute_coherence(x)
    gates = detect_gates(C)

    print("\n--- NEXAH IEEE Gate Detection v2 ---")
    print(f"Detected gates: {len(gates)}")

    for g in gates:
        print(f"Gate interval: t = {t[g[0]]:.2f} → {t[g[1]]:.2f}")

    return t, x, C, gates


# ============================================================
# 5. VISUALIZATION
# ============================================================

def plot_results(t, x, C, gates, save_path=None):

    fig, axes = plt.subplots(3, 1, figsize=(12, 10))

    # --- Panel 1: Signal ---
    axes[0].plot(t, x)
    axes[0].set_title("System Dynamics x(t)")
    axes[0].set_xlabel("time")
    axes[0].set_ylabel("x(t)")

    # --- Panel 2: Coherence ---
    axes[1].plot(t, C)
    axes[1].axhline(0.2, linestyle="--", label="coherence threshold")

    for (s, e) in gates:
        axes[1].axvspan(t[s], t[e], alpha=0.2)

    axes[1].set_title("Coherence C(t)")
    axes[1].set_xlabel("time")
    axes[1].set_ylabel("C(t)")
    axes[1].legend()

    # --- Panel 3: Gate regions ---
    axes[2].set_title("Gate Detection")
    axes[2].set_xlim(t[0], t[-1])
    axes[2].set_ylim(0, 1)

    for (s, e) in gates:
        axes[2].axvspan(t[s], t[e], alpha=0.4)

    axes[2].set_xlabel("time")
    axes[2].set_yticks([])

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"\nSaved to: {save_path}")

    plt.show()


# ============================================================
# 6. MULTI-RUN VALIDATION
# ============================================================

def multi_run_test(runs=20):
    gate_counts = []

    for r in range(runs):
        t = np.linspace(0, 100, 1000)
        x = generate_signal(t, seed=r)
        C = compute_coherence(x)
        gates = detect_gates(C)

        gate_counts.append(len(gates))

    print("\n--- Multi-run stats ---")
    print(f"Runs: {runs}")
    print(f"Mean gates: {np.mean(gate_counts):.2f} ± {np.std(gate_counts):.2f}")


# ============================================================
# 7. EXECUTION
# ============================================================

if __name__ == "__main__":
    t, x, C, gates = run_simulation()

    plot_results(
        t, x, C, gates,
        save_path="NEXAH_CORE/outputs/ieee_gates/ieee_gate_detection_v2.png"
    )

    multi_run_test(runs=20)
