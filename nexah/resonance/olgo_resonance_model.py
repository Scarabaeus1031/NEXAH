import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# OLGO / Root-432 experimental resonance model
# ============================================================

phi = (1 + np.sqrt(5)) / 2
pi = np.pi

# Core anchor
f0 = (phi ** 3) / (pi ** 2)   # ~0.429203...
epsilon = 0.029               # experimental band spacing

shells = np.array([
    f0,
    f0 + epsilon,
    f0 + 2 * epsilon
])

shell_names = [
    "Core Shell",
    "Transition Shell",
    "Expansion Shell"
]


# ------------------------------------------------------------
# 3D Lissajous-like trajectory with slow breathing axis
# ------------------------------------------------------------
def lissajous_3d(
    t,
    w1=3.0,
    w2=2.0,
    delta=np.pi / 2,
    A=1.0,
    B=1.0,
    z_center=None,
    z_amp=None,
    Omega=0.18
):
    """
    x, y -> Lissajous plane
    z    -> slow breathing modulation across shell band
    """
    if z_center is None:
        z_center = f0 + epsilon
    if z_amp is None:
        z_amp = epsilon

    x = A * np.sin(w1 * t)
    y = B * np.sin(w2 * t + delta)
    z = z_center + z_amp * np.sin(Omega * t)

    return x, y, z


# ------------------------------------------------------------
# Phase-lock measure
# ------------------------------------------------------------
def phase_lock_measure(t, w1=3.0, w2=2.0, delta=np.pi / 2):
    """
    Measures how close the two oscillations are to a phase-locked relation.
    Small values mean stronger alignment.
    """
    phase_gap = (w1 * t) - (w2 * t + delta)
    return abs(np.sin(phase_gap))


# ------------------------------------------------------------
# Hook detector
# ------------------------------------------------------------
def detect_resonance_hook(
    t,
    x,
    y,
    z,
    shells,
    z_tol=0.0035,
    phase_tol=0.08,
    radial_tol=0.20
):
    """
    A hook is counted only if:
    1. z is close to a shell
    2. the oscillations are close to phase-lock
    3. trajectory is near turning geometry in the x-y plane
    """
    hits = []

    r = np.sqrt(x**2 + y**2)
    phase_measure = phase_lock_measure(t)

    # turning geometry: near outer or inner swing thresholds
    turning_condition = (r > (1.0 - radial_tol)) or (r < radial_tol)

    for i, s in enumerate(shells):
        shell_condition = abs(z - s) < z_tol
        phase_condition = phase_measure < phase_tol

        if shell_condition and phase_condition and turning_condition:
            hits.append({
                "shell_index": i,
                "shell_name": shell_names[i],
                "shell_value": s,
                "z": z,
                "r": r,
                "phase_measure": phase_measure
            })

    return hits


# ------------------------------------------------------------
# Simulation
# ------------------------------------------------------------
def simulate(
    T=300.0,
    dt=0.01,
    w1=3.0,
    w2=2.0,
    delta=np.pi / 2,
    Omega=0.18
):
    t_values = np.arange(0.0, T, dt)

    trajectory = []
    hits = []

    for t in t_values:
        x, y, z = lissajous_3d(
            t,
            w1=w1,
            w2=w2,
            delta=delta,
            Omega=Omega
        )

        trajectory.append((t, x, y, z))

        current_hits = detect_resonance_hook(
            t=t,
            x=x,
            y=y,
            z=z,
            shells=shells
        )

        for h in current_hits:
            hits.append({
                "t": t,
                **h
            })

    return trajectory, hits


# ------------------------------------------------------------
# Summaries
# ------------------------------------------------------------
def summarize_hits(hits):
    summary = {name: 0 for name in shell_names}
    for h in hits:
        summary[h["shell_name"]] += 1
    return summary


# ------------------------------------------------------------
# Visualization
# ------------------------------------------------------------
def plot_trajectory_and_hits(trajectory, hits):
    xs = [p[1] for p in trajectory]
    ys = [p[2] for p in trajectory]
    zs = [p[3] for p in trajectory]

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(projection="3d")

    ax.plot(xs, ys, zs, linewidth=0.7)

    # mark shell planes as points on axis
    for i, s in enumerate(shells):
        ax.scatter([0], [0], [s], s=80, label=f"{shell_names[i]}: {s:.3f}")

    # mark hits
    if hits:
        hx = [np.sin(3.0 * h["t"]) for h in hits]
        hy = [np.sin(2.0 * h["t"] + np.pi / 2) for h in hits]
        hz = [h["z"] for h in hits]
        ax.scatter(hx, hy, hz, s=8)

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_title("OLGO Resonance Trajectory with Shell Hooks")
    ax.legend()
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
if __name__ == "__main__":
    trajectory, hits = simulate()

    print(f"Core f0: {f0}")
    print(f"Shells: {shells.tolist()}")
    print(f"Number of hook events: {len(hits)}")

    summary = summarize_hits(hits)
    print("\nHook summary by shell:")
    for name, count in summary.items():
        print(f"  {name}: {count}")

    print("\nFirst 10 hook events:")
    for h in hits[:10]:
        print(
            f"t={h['t']:.3f}, "
            f"{h['shell_name']}, "
            f"z={h['z']:.6f}, "
            f"phase={h['phase_measure']:.6f}, "
            f"r={h['r']:.6f}"
        )

    plot_trajectory_and_hits(trajectory, hits)
