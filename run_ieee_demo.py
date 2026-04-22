import numpy as np
import matplotlib.pyplot as plt
import os


def generate_mock_ieee_signal(T=1000):
    """
    Minimal stand-in for IEEE voltage trajectory.
    Simulates slow degradation + sudden collapse.
    """
    t = np.arange(T)

    # baseline voltage
    voltage = 1.0 - 0.0005 * t

    # add collapse event
    collapse_start = int(T * 0.7)
    voltage[collapse_start:] -= np.linspace(0, 0.5, T - collapse_start)

    # small noise
    voltage += 0.002 * np.random.randn(T)

    return t, voltage, collapse_start


def compute_nexah_signal(voltage):
    """
    Simple structural signal:
    curvature × gradient
    """
    grad = np.gradient(voltage)
    curvature = np.gradient(grad)

    grad_norm = np.abs(grad) / (np.max(np.abs(grad)) + 1e-8)
    curv_norm = np.abs(curvature) / (np.max(np.abs(curvature)) + 1e-8)

    risk = grad_norm * curv_norm

    return risk


def main():
    print("\n⚡ NEXAH Demo — Collapse Detection (IEEE-style)\n")

    # --- 1. Generate signal ---
    t, voltage, collapse_idx = generate_mock_ieee_signal()
    print("✔ Generated system trajectory")

    # --- 2. Compute signal ---
    risk = compute_nexah_signal(voltage)
    print("✔ Computed structural signal")

    # --- 3. Detect peak (early warning) ---
    threshold = np.percentile(risk, 99)
    peaks = np.where(risk > threshold)[0]

    first_peak = peaks[0] if len(peaks) > 0 else None

    # --- 4. Plot ---
    plt.figure(figsize=(10, 5))

    plt.plot(t, voltage, label="Voltage")
    plt.plot(t, risk, label="NEXAH Signal", alpha=0.7)

    if first_peak is not None:
        plt.axvline(first_peak, linestyle="--", label="NEXAH Detection")

    plt.axvline(collapse_idx, linestyle=":", label="Actual Collapse")

    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title("NEXAH — Early Detection of Collapse")
    plt.legend()

    plt.tight_layout()

    # --- 5. Save ---
    out_dir = "outputs/demo"
    os.makedirs(out_dir, exist_ok=True)

    out_path = os.path.join(out_dir, "nexah_ieee_collapse.png")
    plt.savefig(out_path, dpi=200)

    print(f"✔ Saved plot → {out_path}")

    plt.show()

    # --- 6. Result ---
    print("\n🔥 Result:")

    if first_peak is not None:
        delta = collapse_idx - first_peak
        print(f"Early detection: {delta} time steps before collapse")
    else:
        print("No early detection signal found")

    print("\n📊 Stats:")
    print(f"Max signal: {np.max(risk):.3f}")
    print(f"Mean signal: {np.mean(risk):.3f}")
    print(f"Peak count: {len(peaks)}")


if __name__ == "__main__":
    main()
