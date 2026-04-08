# nexah_navigation_kernel_v1.py

import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# NEXAH Navigation Kernel v1
# ------------------------------------------------------------
# Purpose:
# - use the NEXAH axis as navigation spine
# - detect grey-channel behavior
# - generate active strand oscillation
# - visualize trajectory + switch behavior
#
# This replaces the first minimal test version.
# ============================================================


# ------------------------------------------------------------
# PARAMETERS
# ------------------------------------------------------------
axis_slope = 0.53
axis_intercept = -0.2

grey_threshold = 2.0
switch_offset = 1.0

step_size = 0.15
osc_strength = 0.40
osc_freq = 0.08

n_steps = 800


# ------------------------------------------------------------
# GEOMETRY HELPERS
# ------------------------------------------------------------
def line_projection(x: float, y: float, m: float, b: float) -> tuple[float, float]:
    """
    Orthogonal projection of point (x, y) onto line y = m*x + b
    """
    x_proj = (x + m * (y - b)) / (1 + m * m)
    y_proj = m * x_proj + b
    return x_proj, y_proj


def signed_distance(x: float, y: float, m: float, b: float) -> float:
    """
    Signed distance to line y = m*x + b
    """
    return (m * x - y + b) / np.sqrt(m * m + 1)


# ------------------------------------------------------------
# CHANNEL DETECTION
# ------------------------------------------------------------
def detect_channel(x: float, y: float) -> str:
    dist = abs(signed_distance(x, y, axis_slope, axis_intercept))
    return "grey" if dist < grey_threshold else "field"


# ------------------------------------------------------------
# SWITCH DETECTION
# ------------------------------------------------------------
def detect_switch(x: float, y: float) -> str:
    d = signed_distance(x, y, axis_slope, axis_intercept)

    if d > switch_offset:
        return "lower"
    elif d < -switch_offset:
        return "upper"
    else:
        return "neutral"


# ------------------------------------------------------------
# SIGNALS
# ------------------------------------------------------------
def compute_signals(x: float, y: float, prev_x: float, prev_y: float) -> dict:
    dx = x - prev_x
    dy = y - prev_y

    drift = np.sqrt(dx**2 + dy**2)

    x_proj, y_proj = line_projection(x, y, axis_slope, axis_intercept)
    dist = np.sqrt((x - x_proj) ** 2 + (y - y_proj) ** 2)

    coherence = 1.0 / (1.0 + dist)
    collapse = max(0.0, dist - grey_threshold)

    return {
        "drift": drift,
        "coherence": coherence,
        "collapse": collapse,
    }


# ------------------------------------------------------------
# KERNEL STEP
# ------------------------------------------------------------
def nexah_kernel_step(
    x: float,
    y: float,
    prev_x: float,
    prev_y: float,
    t: int,
) -> tuple[float, float, str, str, dict]:
    """
    One navigation step.
    """

    channel = detect_channel(x, y)
    switch = detect_switch(x, y)
    signals = compute_signals(x, y, prev_x, prev_y)

    # --------------------------------------------------------
    # Base direction: project toward axis
    # --------------------------------------------------------
    x_proj, y_proj = line_projection(x, y, axis_slope, axis_intercept)

    dx = x_proj - x
    dy = y_proj - y

    norm = np.sqrt(dx**2 + dy**2) + 1e-8
    dx /= norm
    dy /= norm

    # --------------------------------------------------------
    # Channel behavior
    # --------------------------------------------------------
    if channel == "grey":
        dx *= 1.15
        dy *= 1.15
    else:
        dx *= 0.55
        dy *= 0.55

    # --------------------------------------------------------
    # Active strand oscillation
    # --------------------------------------------------------
    osc = np.sin(osc_freq * t + 0.15 * x)
    dy += osc_strength * osc

    # --------------------------------------------------------
    # Collapse avoidance
    # --------------------------------------------------------
    if signals["collapse"] > 0.5:
        dx *= -0.7
        dy *= -0.7

    # --------------------------------------------------------
    # Final step
    # --------------------------------------------------------
    new_x = x + step_size * dx
    new_y = y + step_size * dy

    return new_x, new_y, channel, switch, signals


# ------------------------------------------------------------
# SIMULATION
# ------------------------------------------------------------
def run_kernel_simulation(
    start: tuple[float, float] = (-6.0, -5.0),
    steps: int = n_steps,
) -> tuple[np.ndarray, list[str], list[str], list[dict]]:
    x, y = start
    prev_x, prev_y = x, y

    traj = []
    channels = []
    switches = []
    signals = []

    for t in range(steps):
        new_x, new_y, ch, sw, sig = nexah_kernel_step(x, y, prev_x, prev_y, t)

        traj.append((new_x, new_y))
        channels.append(ch)
        switches.append(sw)
        signals.append(sig)

        prev_x, prev_y = x, y
        x, y = new_x, new_y

    return np.array(traj), channels, switches, signals


# ------------------------------------------------------------
# VISUALIZATION
# ------------------------------------------------------------
def plot_kernel_results(
    traj: np.ndarray,
    channels: list[str],
    switches: list[str],
    signals: list[dict],
) -> None:
    x = traj[:, 0]
    y = traj[:, 1]

    # masks
    grey_mask = np.array([c == "grey" for c in channels])
    upper_mask = np.array([s == "upper" for s in switches])
    lower_mask = np.array([s == "lower" for s in switches])
    neutral_mask = np.array([s == "neutral" for s in switches])

    # axis
    xx = np.linspace(np.min(x) - 1, np.max(x) + 1, 300)
    yy = axis_slope * xx + axis_intercept

    # --------------------------------------------------------
    # Plot 1: trajectory in field
    # --------------------------------------------------------
    plt.figure(figsize=(10, 7))
    plt.plot(xx, yy, color="goldenrod", linewidth=2, label="NEXAH axis")
    plt.scatter(x[grey_mask], y[grey_mask], s=8, c="black", label="grey channel")
    plt.scatter(x[upper_mask], y[upper_mask], s=10, c="deepskyblue", label="upper")
    plt.scatter(x[lower_mask], y[lower_mask], s=10, c="magenta", label="lower")
    plt.scatter(x[neutral_mask], y[neutral_mask], s=5, c="orange", alpha=0.6, label="neutral")

    plt.title("NEXAH Navigation Kernel v1 — Trajectory")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # --------------------------------------------------------
    # Plot 2: switch timeline
    # --------------------------------------------------------
    switch_values = []
    for s in switches:
        if s == "upper":
            switch_values.append(1)
        elif s == "lower":
            switch_values.append(-1)
        else:
            switch_values.append(0)

    plt.figure(figsize=(10, 3))
    plt.plot(switch_values, linewidth=1.0)
    plt.title("Switch Timeline")
    plt.yticks([-1, 0, 1], ["lower", "neutral", "upper"])
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    # --------------------------------------------------------
    # Plot 3: coherence / drift / collapse
    # --------------------------------------------------------
    coherence = [s["coherence"] for s in signals]
    drift = [s["drift"] for s in signals]
    collapse = [s["collapse"] for s in signals]

    fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    axs[0].plot(coherence)
    axs[0].set_title("Coherence")
    axs[0].grid(True, alpha=0.3)

    axs[1].plot(drift)
    axs[1].set_title("Drift")
    axs[1].grid(True, alpha=0.3)

    axs[2].plot(collapse)
    axs[2].set_title("Collapse")
    axs[2].grid(True, alpha=0.3)
    axs[2].set_xlabel("Step")

    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
if __name__ == "__main__":
    traj, channels, switches, signals = run_kernel_simulation(
        start=(-6.0, -5.0),
        steps=800,
    )

    print("=== NEXAH Kernel v1 ===")
    print("Trajectory length:", len(traj))
    print("Grey count:", channels.count("grey"))
    print("Upper switches:", switches.count("upper"))
    print("Lower switches:", switches.count("lower"))
    print("Neutral states:", switches.count("neutral"))

    plot_kernel_results(traj, channels, switches, signals)
