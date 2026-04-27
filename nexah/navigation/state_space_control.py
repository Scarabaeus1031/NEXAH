# ============================================================
# 🧭 NEXAH — State Space Control (v7 FINAL)
# Transition Probability Control
# ============================================================

import numpy as np


# ------------------------------------------------------------
# SIGNAL
# ------------------------------------------------------------

def generate_signal(n=500):
    t = np.linspace(0, 20, n)
    return np.sin(t) + 0.3 * np.sin(5 * t)


# ------------------------------------------------------------
# STATE SPACE
# ------------------------------------------------------------

def build_state_space(x):
    v = np.gradient(x)
    return np.stack([x, v], axis=1)


# ------------------------------------------------------------
# BASINS
# ------------------------------------------------------------

def assign_basins(x, levels=None):
    if levels is None:
        levels = [-0.6, 0.0, 0.6]
    return np.digitize(x, levels)


def compute_transition_matrix(basins):
    unique = np.unique(basins)
    n = len(unique)

    index = {b: i for i, b in enumerate(unique)}
    P = np.zeros((n, n))

    for i in range(len(basins) - 1):
        a = index[basins[i]]
        b = index[basins[i + 1]]
        P[a, b] += 1

    P = P / (P.sum(axis=1, keepdims=True) + 1e-8)

    return P, index


# ------------------------------------------------------------
# CONTROL (v7)
# ------------------------------------------------------------

def apply_transition_control(
    x,
    risk,
    strength=0.08,
    threshold=0.8,
    target_transition=(0, 1)
):
    """
    Control by increasing probability of specific transition.
    """

    states = build_state_space(x)
    basins = assign_basins(x)

    P, index = compute_transition_matrix(basins)

    x_ctrl = x.copy()
    events = []

    for t in range(2, len(x) - 1):

        if risk[t] < threshold:
            continue

        b_now = basins[t]
        b_next = basins[t + 1]

        # --- target condition ---
        if (b_now, b_next) == target_transition:
            continue

        # --- if we're in source basin, steer toward target ---
        if b_now == target_transition[0]:

            # desired direction: upward shift
            direction = 1

            dx = x_ctrl[t] - x_ctrl[t - 1]
            dx = np.clip(dx, -1.0, 1.0)

            # push toward transition
            correction = strength * direction * (1.0 - abs(dx))

            correction = np.clip(correction, -0.12, 0.12)

            new_dx = dx + correction

            x_ctrl[t + 1] = x_ctrl[t] + new_dx

            events.append({
                "t": int(t),
                "basin": int(b_now),
                "target": target_transition,
                "corr": float(correction),
            })

    return x_ctrl, basins, events


# ------------------------------------------------------------
# DEMO
# ------------------------------------------------------------

def demo():
    import matplotlib.pyplot as plt

    x = generate_signal()

    flow = np.abs(np.gradient(x))
    accel = np.abs(np.gradient(flow))
    risk = flow * accel
    risk = (risk - np.min(risk)) / (np.max(risk) + 1e-8)

    x_ctrl, basins, events = apply_transition_control(
        x,
        risk,
        strength=0.08,
        threshold=0.8,
        target_transition=(0, 1)
    )

    peaks = np.where(risk > 0.8)[0]

    plt.figure(figsize=(12, 5))
    plt.plot(x, label="Original", alpha=0.7)
    plt.plot(x_ctrl, "--", label="Controlled v7")

    plt.scatter(peaks, x[peaks], color="red", s=20, label="High Risk")

    for e in events:
        plt.axvline(e["t"], color="gray", alpha=0.1)

    plt.title(f"NEXAH v7 — Transition Control | events={len(events)}")
    plt.legend()
    plt.tight_layout()
    plt.show()

    print("\n--- Events ---")
    for e in events[:20]:
        print(e)


if __name__ == "__main__":
    demo()
