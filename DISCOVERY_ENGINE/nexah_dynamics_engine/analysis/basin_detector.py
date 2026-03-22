import numpy as np


# --------------------------------------------------
# FLOW MAGNITUDE
# --------------------------------------------------

def compute_flow_magnitude(flow_x, flow_y):
    return np.sqrt(flow_x**2 + flow_y**2)


# --------------------------------------------------
# SIMPLE SMOOTHING (3x3 MEAN FILTER)
# --------------------------------------------------

def smooth_field(field):
    padded = np.pad(field, 1, mode='edge')
    smoothed = np.zeros_like(field)

    for i in range(field.shape[0]):
        for j in range(field.shape[1]):
            window = padded[i:i+3, j:j+3]
            smoothed[i, j] = np.mean(window)

    return smoothed


# --------------------------------------------------
# BASIN DETECTION (IMPROVED)
# --------------------------------------------------

def detect_basins(flow_x, flow_y, threshold=0.2, smooth=True):
    """
    Detect basins (low flow regions)
    → "eye of the storm"
    """

    magnitude = compute_flow_magnitude(flow_x, flow_y)

    # optional smoothing
    if smooth:
        magnitude = smooth_field(magnitude)

    basins = np.zeros_like(magnitude)

    for i in range(magnitude.shape[0]):
        for j in range(magnitude.shape[1]):
            if magnitude[i, j] < threshold:
                basins[i, j] = 1

    return basins


# --------------------------------------------------
# BASIN STRENGTH
# --------------------------------------------------

def compute_basin_strength(flow_x, flow_y):
    """
    Strong basin = low movement
    """

    magnitude = compute_flow_magnitude(flow_x, flow_y)

    strength = 1.0 / (magnitude + 1e-6)

    return strength


# --------------------------------------------------
# OPTIONAL: BASIN LABELING (CONNECTED COMPONENTS)
# --------------------------------------------------

def label_basins(basins):
    """
    Label connected basin regions
    """

    labels = np.zeros_like(basins, dtype=int)
    current_label = 1

    rows, cols = basins.shape

    def flood_fill(i, j, label):
        stack = [(i, j)]

        while stack:
            x, y = stack.pop()

            if (
                x < 0 or x >= rows or
                y < 0 or y >= cols or
                basins[x, y] == 0 or
                labels[x, y] != 0
            ):
                continue

            labels[x, y] = label

            stack.extend([
                (x+1, y), (x-1, y),
                (x, y+1), (x, y-1)
            ])

    for i in range(rows):
        for j in range(cols):
            if basins[i, j] == 1 and labels[i, j] == 0:
                flood_fill(i, j, current_label)
                current_label += 1

    return labels


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":
    print("Basin Detection Ready")
