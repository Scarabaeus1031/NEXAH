# nexah_navigation_kernel_v1.py

import numpy as np


# ============================================================
# NEXAH Navigation Kernel v1
# ------------------------------------------------------------
# Purpose:
# - take field position + signals
# - detect channel + switch state
# - propose next movement step
#
# This is NOT full control yet.
# It is a first decision layer.
# ============================================================


# ------------------------------------------------------------
# PARAMETERS
# ------------------------------------------------------------
axis_slope = 0.53
axis_intercept = -0.2

grey_threshold = 2.0
switch_offset = 1.0

step_size = 0.15


# ------------------------------------------------------------
# GEOMETRY HELPERS
# ------------------------------------------------------------
def line_projection(x, y, m, b):
    """
    Project point onto line y = m x + b
    """
    x_proj = (x + m * (y - b)) / (1 + m * m)
    y_proj = m * x_proj + b
    return x_proj, y_proj


def signed_distance(x, y, m, b):
    """
    Signed distance to line
    """
    return (m * x - y + b) / np.sqrt(m * m + 1)


# ------------------------------------------------------------
# CHANNEL DETECTION (v8)
# ------------------------------------------------------------
def detect_channel(x, y):
    dist = abs(signed_distance(x, y, axis_slope, axis_intercept))

    if dist < grey_threshold:
        return "grey"
    else:
        return "field"


# ------------------------------------------------------------
# SWITCH DETECTION (v9)
# ------------------------------------------------------------
def detect_switch(x, y):
    d = signed_distance(x, y, axis_slope, axis_intercept)

    if d > switch_offset:
        return "lower"
    elif d < -switch_offset:
        return "upper"
    else:
        return "neutral"


# ------------------------------------------------------------
# SIGNALS (simple first version)
# ------------------------------------------------------------
def compute_signals(x, y, prev_x, prev_y):
    dx = x - prev_x
    dy = y - prev_y

    drift = np.sqrt(dx**2 + dy**2)

    # coherence = how aligned we are with axis
    x_proj, y_proj = line_projection(x, y, axis_slope, axis_intercept)
    dist = np.sqrt((x - x_proj)**2 + (y - y_proj)**2)

    coherence = 1.0 / (1.0 + dist)

    collapse = max(0.0, dist - grey_threshold)

    return {
        "drift": drift,
        "coherence": coherence,
        "collapse": collapse
    }


# ------------------------------------------------------------
# KERNEL STEP
# ------------------------------------------------------------
def nexah_kernel_step(x, y, prev_x, prev_y):

    # detect structures
    channel = detect_channel(x, y)
    switch = detect_switch(x, y)

    signals = compute_signals(x, y, prev_x, prev_y)

    # --------------------------------------------------------
    # BASE DIRECTION: follow axis
    # --------------------------------------------------------
    x_proj, y_proj = line_projection(x, y, axis_slope, axis_intercept)

    dx = x_proj - x
    dy = y_proj - y

    # normalize
    norm = np.sqrt(dx**2 + dy**2) + 1e-8
    dx /= norm
    dy /= norm

    # --------------------------------------------------------
    # CHANNEL BEHAVIOR
    # --------------------------------------------------------
    if channel == "grey":
        dx *= 1.2
        dy *= 1.2
    else:
        dx *= 0.6
        dy *= 0.6

    # --------------------------------------------------------
    # SWITCH MODULATION
    # --------------------------------------------------------
    if switch == "upper":
        dy -= 0.2
    elif switch == "lower":
        dy += 0.2

    # --------------------------------------------------------
    # COLLAPSE AVOIDANCE
    # --------------------------------------------------------
    if signals["collapse"] > 0.5:
        dx *= -0.7
        dy *= -0.7

    # --------------------------------------------------------
    # STEP
    # --------------------------------------------------------
    new_x = x + step_size * dx
    new_y = y + step_size * dy

    return new_x, new_y, channel, switch, signals


# ------------------------------------------------------------
# SIMPLE SIMULATION
# ------------------------------------------------------------
def run_kernel_simulation(start=(0.0, 0.0), steps=500):

    x, y = start
    prev_x, prev_y = x, y

    traj = []
    channels = []
    switches = []

    for _ in range(steps):

        new_x, new_y, ch, sw, sig = nexah_kernel_step(x, y, prev_x, prev_y)

        traj.append((new_x, new_y))
        channels.append(ch)
        switches.append(sw)

        prev_x, prev_y = x, y
        x, y = new_x, new_y

    return np.array(traj), channels, switches


# ------------------------------------------------------------
# TEST RUN
# ------------------------------------------------------------
if __name__ == "__main__":

    traj, channels, switches = run_kernel_simulation(start=(-6.0, -5.0), steps=600)

    print("=== NEXAH Kernel v1 ===")
    print("Trajectory length:", len(traj))
    print("Grey count:", channels.count("grey"))
    print("Upper switches:", switches.count("upper"))
    print("Lower switches:", switches.count("lower"))
