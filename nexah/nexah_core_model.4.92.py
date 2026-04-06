import numpy as np


def detect_nexah_v492(t, v):
    dv = np.gradient(v, t)
    d2v = np.gradient(dv, t)

    window = 10

    for i in range(window, len(v)):

        # ---- Core score ----
        score = -dv[i] + 0.5 * (-d2v[i])

        # ---- Lotus (soft) ----
        phi_window = np.arctan2(d2v[i-window:i], dv[i-window:i] + 1e-8)
        lotus = 1 / (1 + np.std(phi_window))

        final_score = score * lotus

        # ---- NEW: activation guard ----
        if abs(dv[i]) < 0.001:
            continue

        # ---- NEW: trend filter ----
        trend = np.mean(dv[i-5:i])
        if trend > -0.002:
            continue

        # ---- Threshold ----
        if final_score > 0.015:
            return t[i]

    return None
