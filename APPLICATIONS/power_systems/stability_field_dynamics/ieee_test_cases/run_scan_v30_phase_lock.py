import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core_coupling import run_single_coupling


def run_phase_cycle(base_load=1.0, steps=24):
    results = []

    for t in range(steps):

        phase = 2 * np.pi * t / steps

        noise = 0.15 * np.sin(phase) + 0.15
        rotation = 0.5 + 0.3 * np.cos(phase)
        damping = 0.95 - 0.05 * np.sin(phase)

        print(f"t={t:02d} | noise={noise:.3f} | rot={rotation:.3f}")

        r = run_single_coupling(
            base_load=base_load,
            noise_strength=noise,
            flow_rotation=rotation,
            damping=damping,
        )

        results.append({
            "t": t,
            "C": r["C"],
            "loops": r["loops"],
            "states": r["states"],
        })

    return pd.DataFrame(results)


def analyze_frequency(signal, name="C"):
    signal = signal - np.mean(signal)

    fft = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(signal))

    power = np.abs(fft)

    return freqs, power


def main():
    print("\n--- V30 Phase Lock Analyzer ---\n")

    df = run_phase_cycle(base_load=1.0, steps=24)

    df.to_csv("v30_phase_timeseries.csv", index=False)

    print("\nSaved: v30_phase_timeseries.csv")

    # =========================
    # PLOTS (TIME SERIES)
    # =========================
    plt.figure(figsize=(10, 6))
    plt.plot(df["t"], df["C"], marker="o", label="C")
    plt.plot(df["t"], df["loops"], marker="o", label="loops")
    plt.plot(df["t"], df["states"], marker="o", label="states")
    plt.legend()
    plt.title("Time Series")
    plt.xlabel("t")
    plt.show()

    # =========================
    # FFT ANALYSIS
    # =========================
    freqs_C, power_C = analyze_frequency(df["C"].values, "C")
    freqs_L, power_L = analyze_frequency(df["loops"].values, "loops")

    plt.figure(figsize=(10, 6))
    plt.plot(freqs_C, power_C, label="C FFT")
    plt.plot(freqs_L, power_L, label="loops FFT")
    plt.legend()
    plt.title("Frequency Spectrum")
    plt.xlabel("Frequency")
    plt.ylabel("Power")
    plt.show()

    # =========================
    # DOMINANT FREQUENCY
    # =========================
    idx_C = np.argmax(power_C[1:]) + 1
    idx_L = np.argmax(power_L[1:]) + 1

    print("\n--- DOMINANT FREQUENCIES ---")
    print(f"C dominant freq: {freqs_C[idx_C]:.4f}")
    print(f"loops dominant freq: {freqs_L[idx_L]:.4f}")


if __name__ == "__main__":
    main()
