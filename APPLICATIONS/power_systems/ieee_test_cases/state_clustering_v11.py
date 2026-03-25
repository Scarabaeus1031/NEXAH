import numpy as np
from scipy.ndimage import label


def extract_states_from_recurrence(M, threshold=0.2):
    """
    Extract connected high-density regions as states.
    """
    if np.max(M) == 0:
        return [], np.zeros_like(M)

    norm = M / np.max(M)
    mask = norm > threshold

    labeled, num = label(mask)

    states = []
    for i in range(1, num + 1):
        coords = np.column_stack(np.where(labeled == i))
        if len(coords) < 5:
            continue
        center = coords.mean(axis=0)
        states.append({
            "id": i,
            "center": center,
            "points": coords
        })

    return states, labeled
