def analyze(time, voltage, collapse_threshold=0.7):

    collapse_idx = None
    collapse_indices = np.where(voltage < collapse_threshold)[0]
    if len(collapse_indices) > 0:
        collapse_idx = collapse_indices[0]

    # ----------------------------------------
    # Features
    # ----------------------------------------

    dv = np.diff(voltage, prepend=voltage[0])
    acc = compute_acceleration(voltage)

    # Normierung
    slope = np.abs(dv)
    distance = np.maximum(voltage - collapse_threshold, 0)

    # ----------------------------------------
    # Hybrid Score
    # ----------------------------------------

    # Wichtig: Gewichtung
    score = (
        1.0 * acc +
        0.5 * slope +
        0.5 * (1.0 / (distance + 1e-3))
    )

    # Glätten
    kernel = np.ones(5) / 5
    score = np.convolve(score, kernel, mode='same')

    # ----------------------------------------
    # Detection
    # ----------------------------------------

    min_idx = int(0.1 * len(time))
    max_idx = int(0.9 * len(time))

    valid = np.arange(len(time))
    valid = valid[(valid >= min_idx) & (valid <= max_idx)]

    phi_idx = valid[np.argmax(score[valid])]

    # ----------------------------------------
    # Output
    # ----------------------------------------

    print("\n--- RESULTS ---")

    if collapse_idx is not None:
        print(f"Collapse at t = {time[collapse_idx]}")
    else:
        print("No collapse detected")

    print(f"Phi-Split (hybrid) at t = {time[phi_idx]}")

    if collapse_idx is not None:
        lead_time = time[collapse_idx] - time[phi_idx]
        print(f"Lead Time = {lead_time}")
    else:
        print("Lead Time not computable")

    print(f"Max score = {np.max(score):.6f}")

    return phi_idx, collapse_idx, acc, score
