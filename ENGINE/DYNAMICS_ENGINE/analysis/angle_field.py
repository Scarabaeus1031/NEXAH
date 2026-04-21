import numpy as np


# --------------------------------------------------
# ANGLE COMPUTATION
# --------------------------------------------------

def compute_local_angles(trajectory):
    """
    Compute turning angles along trajectory
    """
    angles = []

    for i in range(1, len(trajectory) - 1):

        p1 = trajectory[i - 1]
        p2 = trajectory[i]
        p3 = trajectory[i + 1]

        v1 = p2 - p1
        v2 = p3 - p2

        # normalize
        v1_norm = np.linalg.norm(v1)
        v2_norm = np.linalg.norm(v2)

        if v1_norm == 0 or v2_norm == 0:
            continue

        v1 = v1 / v1_norm
        v2 = v2 / v2_norm

        dot = np.clip(np.dot(v1, v2), -1.0, 1.0)
        angle = np.arccos(dot)

        angles.append(angle)

    return np.array(angles)


# --------------------------------------------------
# ANGLE METRICS
# --------------------------------------------------

def analyze_angle_distribution(trajectory):

    angles = compute_local_angles(trajectory)

    if len(angles) == 0:
        return {
            "mean_angle": 0.0,
            "std_angle": 0.0,
            "dominant_angle": 0.0,
            "angle_histogram": {}
        }

    mean_angle = float(np.mean(angles))
    std_angle = float(np.std(angles))

    # histogram (degrees)
    deg = np.degrees(angles)
    hist, bins = np.histogram(deg, bins=12, range=(0, 180))

    dominant_idx = np.argmax(hist)
    dominant_angle = float((bins[dominant_idx] + bins[dominant_idx + 1]) / 2)

    angle_profile = {
        int((bins[i] + bins[i + 1]) / 2): float(hist[i])
        for i in range(len(hist))
    }

    return {
        "mean_angle": mean_angle,
        "std_angle": std_angle,
        "dominant_angle": dominant_angle,
        "angle_profile": angle_profile
    }
