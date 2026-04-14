# ============================================================
# NEXAH v6.6 — Pulse-Wave Analyzer
# ============================================================

import numpy as np
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# Dummy trajectory
# Replace later with your real trajectory if needed
# Format per point: (v, dv, mode, energy)
# ------------------------------------------------------------
def generate_dummy_traj(n=5000):
    traj = []

    for t in range(n):
        tt = t * 0.015

        # continuous wave part
        v = 0.78 + 0.14 * np.sin(tt) + 0.05 * np.sin(2.7 * tt + 0.3)
        dv = 0.028 * np.cos(tt) + 0.018 * np.cos(2.7 * tt + 0.3)

        # discrete mode switching
        mode = (t // 350) % 4

        energy = dv**2 + 0.08 * (v - 0.84)**2

        traj.append((v, dv, mode, energy))

    return traj


# ------------------------------------------------------------
# Convert trajectory to arrays
# ------------------------------------------------------------
def unpack_traj(traj):
    v = np.array([p[0] for p in traj], dtype=float)
    dv = np.array([p[1] for p in traj], dtype=float)
    mode = np.array([int(p[2]) for p in traj], dtype=int)
    energy = np.array([p[3] for p in traj], dtype=float)
    t = np.arange(len(traj), dtype=float)
    return t, v, dv, mode, energy


# ------------------------------------------------------------
# Pulse detection:
# a pulse is a mode switch
# ------------------------------------------------------------
def detect_pulses(mode):
    pulse_idx = []

    for i in range(1, len(mode)):
        if mode[i] != mode[i - 1]:
            pulse_idx.append(i)

    return np.array(pulse_idx, dtype=int)


# ------------------------------------------------------------
# Wave segment analysis:
# each interval between pulses is a wave segment
# ------------------------------------------------------------
def analyze_wave_segments(t, v, dv, mode, energy, pulse_idx):
    boundaries = [0] + pulse_idx.tolist() + [len(t) - 1]

    segments = []

    for k in range(len(boundaries) - 1):
        i0 = boundaries[k]
        i1 = boundaries[k + 1]

        if i1 <= i0 + 2:
            continue

        ts = t[i0:i1 + 1]
        vs = v[i0:i1 + 1]
        dvs = dv[i0:i1 + 1]
        es = energy[i0:i1 + 1]
        ms = mode[i0:i1 + 1]

        amp = 0.5 * (np.max(vs) - np.min(vs))
        duration = ts[-1] - ts[0]
        mean_energy = np.mean(es)
        rms_dv = np.sqrt(np.mean(dvs**2))

        # crude oscillation estimate by sign changes in dv
        sign_changes = np.sum(np.diff(np.sign(dvs + 1e-12)) != 0)

        segments.append({
            "segment_id": k,
            "start": int(i0),
            "end": int(i1),
            "duration": float(duration),
            "amplitude": float(amp),
            "mean_energy": float(mean_energy),
            "rms_dv": float(rms_dv),
            "sign_changes": int(sign_changes),
            "dominant_mode": int(np.bincount(ms).argmax()),
        })

    return segments


# ------------------------------------------------------------
# Pulse statistics
# ------------------------------------------------------------
def analyze_pulses(t, pulse_idx):
    if len(pulse_idx) == 0:
        return {
            "count": 0,
            "intervals": np.array([]),
            "mean_interval": None,
            "std_interval": None,
            "frequency": 0.0,
        }

    if len(pulse_idx) == 1:
        intervals = np.array([])
        mean_interval = None
        std_interval = None
    else:
        intervals = np.diff(pulse_idx)
        mean_interval = float(np.mean(intervals))
        std_interval = float(np.std(intervals))

    frequency = len(pulse_idx) / max(1.0, (t[-1] - t[0]))

    return {
        "count": int(len(pulse_idx)),
        "intervals": intervals,
        "mean_interval": mean_interval,
        "std_interval": std_interval,
        "frequency": float(frequency),
    }


# ------------------------------------------------------------
# Coupling analysis:
# compare pulse timing with wave energy before pulse
# ------------------------------------------------------------
def pulse_wave_coupling(v, dv, energy, pulse_idx, lookback=50):
    rows = []

    for idx in pulse_idx:
        i0 = max(0, idx - lookback)
        i1 = idx

        vs = v[i0:i1]
        dvs = dv[i0:i1]
        es = energy[i0:i1]

        if len(vs) < 5:
            continue

        rows.append({
            "pulse_index": int(idx),
            "pre_amp": float(0.5 * (np.max(vs) - np.min(vs))),
            "pre_mean_energy": float(np.mean(es)),
            "pre_rms_dv": float(np.sqrt(np.mean(dvs**2))),
            "pre_last_v": float(v[idx - 1]),
            "pre_last_dv": float(dv[idx - 1]),
        })

    return rows


# ------------------------------------------------------------
# Plot 1: full signal + pulses
# ------------------------------------------------------------
def plot_signal_with_pulses(t, v, pulse_idx):
    plt.figure(figsize=(10, 4))
    plt.plot(t, v, label="wave signal")
    if len(pulse_idx) > 0:
        plt.scatter(t[pulse_idx], v[pulse_idx], c="red", s=25, label="pulses")
    plt.title("NEXAH v6.6 — Wave Signal with Pulses")
    plt.xlabel("time")
    plt.ylabel("v")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# Plot 2: mode timeline
# ------------------------------------------------------------
def plot_mode_timeline(t, mode, pulse_idx):
    plt.figure(figsize=(10, 3))
    plt.step(t, mode, where="post", label="mode")
    if len(pulse_idx) > 0:
        for p in pulse_idx:
            plt.axvline(t[p], color="red", alpha=0.25)
    plt.title("Mode Timeline (Pulse = mode switch)")
    plt.xlabel("time")
    plt.ylabel("mode")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# Plot 3: pulse interval histogram
# ------------------------------------------------------------
def plot_pulse_intervals(pulse_stats):
    intervals = pulse_stats["intervals"]
    if len(intervals) == 0:
        print("No pulse interval histogram to show.")
        return

    plt.figure(figsize=(6, 4))
    plt.hist(intervals, bins=20)
    plt.title("Pulse Interval Distribution")
    plt.xlabel("interval")
    plt.ylabel("count")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# Plot 4: segment amplitude vs energy
# ------------------------------------------------------------
def plot_wave_segments(segments):
    if len(segments) == 0:
        print("No wave segments to plot.")
        return

    amp = np.array([s["amplitude"] for s in segments])
    en = np.array([s["mean_energy"] for s in segments])
    dur = np.array([s["duration"] for s in segments])
    seg_id = np.array([s["segment_id"] for s in segments])

    plt.figure(figsize=(7, 5))
    sc = plt.scatter(amp, en, c=dur, s=60)
    plt.colorbar(sc, label="duration")
    for i in range(len(seg_id)):
        plt.text(amp[i], en[i], str(seg_id[i]), fontsize=8)
    plt.title("Wave Segments: Amplitude vs Mean Energy")
    plt.xlabel("amplitude")
    plt.ylabel("mean_energy")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# Plot 5: coupling scatter
# ------------------------------------------------------------
def plot_pulse_wave_coupling(rows):
    if len(rows) == 0:
        print("No pulse-wave coupling data to plot.")
        return

    x = np.array([r["pre_amp"] for r in rows])
    y = np.array([r["pre_mean_energy"] for r in rows])

    plt.figure(figsize=(6, 5))
    plt.scatter(x, y, s=40)
    plt.title("Pulse-Wave Coupling")
    plt.xlabel("pre-pulse amplitude")
    plt.ylabel("pre-pulse mean energy")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# Print summary
# ------------------------------------------------------------
def print_summary(pulse_stats, segments, coupling_rows):
    print("\n=== Pulse Summary ===")
    print(f"pulse count: {pulse_stats['count']}")
    print(f"pulse frequency: {pulse_stats['frequency']:.6f}")

    if pulse_stats["mean_interval"] is not None:
        print(f"mean pulse interval: {pulse_stats['mean_interval']:.4f}")
        print(f"std pulse interval:  {pulse_stats['std_interval']:.4f}")
    else:
        print("not enough pulses for interval stats")

    print("\n=== Wave Segment Summary ===")
    print(f"segment count: {len(segments)}")
    if len(segments) > 0:
        amps = [s["amplitude"] for s in segments]
        ens = [s["mean_energy"] for s in segments]
        durs = [s["duration"] for s in segments]
        print(f"mean amplitude:   {np.mean(amps):.6f}")
        print(f"mean energy:      {np.mean(ens):.6f}")
        print(f"mean duration:    {np.mean(durs):.6f}")

    print("\n=== Pulse-Wave Coupling Summary ===")
    print(f"coupling samples: {len(coupling_rows)}")
    if len(coupling_rows) > 0:
        pamp = [r["pre_amp"] for r in coupling_rows]
        peng = [r["pre_mean_energy"] for r in coupling_rows]
        print(f"mean pre-pulse amplitude: {np.mean(pamp):.6f}")
        print(f"mean pre-pulse energy:    {np.mean(peng):.6f}")


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
if __name__ == "__main__":
    # Replace with your real trajectory later:
    # traj = YOUR_REAL_TRAJECTORY
    traj = generate_dummy_traj()

    t, v, dv, mode, energy = unpack_traj(traj)

    pulse_idx = detect_pulses(mode)
    pulse_stats = analyze_pulses(t, pulse_idx)
    segments = analyze_wave_segments(t, v, dv, mode, energy, pulse_idx)
    coupling_rows = pulse_wave_coupling(v, dv, energy, pulse_idx, lookback=50)

    print_summary(pulse_stats, segments, coupling_rows)

    plot_signal_with_pulses(t, v, pulse_idx)
    plot_mode_timeline(t, mode, pulse_idx)
    plot_pulse_intervals(pulse_stats)
    plot_wave_segments(segments)
    plot_pulse_wave_coupling(coupling_rows)
