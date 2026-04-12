import numpy as np


def classify_states(c, dc, d2c, frag, labels, gh_clusters):
    states = []

    valid = (
        np.isfinite(c) &
        np.isfinite(dc) &
        np.isfinite(d2c) &
        np.isfinite(frag)
    )

    if np.sum(valid) < 10:
        return ["UNKNOWN"] * len(c)

    # --- adaptive thresholds ---
    frag_valid = frag[valid]
    d2c_valid = np.abs(d2c[valid])

    frag_warn_thr = np.percentile(frag_valid, 60)
    frag_crit_thr = np.percentile(frag_valid, 80)

    d2c_warn_thr = np.percentile(d2c_valid, 70)
    d2c_crit_thr = np.percentile(d2c_valid, 90)

    for i in range(len(c)):

        # =========================================
        # 1. COLLAPSED
        # =========================================
        if not valid[i]:
            states.append("COLLAPSED")
            continue

        label = labels[i]

        in_gh = (
            label in gh_clusters
            if isinstance(gh_clusters, (list, tuple, np.ndarray))
            else label == gh_clusters
        )

        frag_i = frag[i]
        d2c_i = abs(d2c[i])

        # =========================================
        # 2. CRITICAL (FIXED)
        # =========================================
        if (
            (d2c_i >= d2c_crit_thr and in_gh)
            or (frag_i >= frag_crit_thr)
        ):
            states.append("CRITICAL")
            continue

        # =========================================
        # 3. WARNING
        # =========================================
        if (
            (frag_i >= frag_warn_thr and in_gh)
            or (d2c_i >= d2c_warn_thr and frag_i >= frag_warn_thr)
        ):
            states.append("WARNING")
            continue

        # =========================================
        # 4. SAFE
        # =========================================
        states.append("SAFE")

    return states
