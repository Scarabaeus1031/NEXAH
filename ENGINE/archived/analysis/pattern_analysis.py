import numpy as np
from scipy.ndimage import maximum_filter

# --------------------------------------------------
# SYMMETRY
# --------------------------------------------------

def symmetry_score(field):
    flipped = np.flipud(np.fliplr(field))
    return np.mean(np.abs(field - flipped))


# --------------------------------------------------
# QUADRANTS
# --------------------------------------------------

def quadrant_energy(field):
    h, w = field.shape
    q1 = field[:h//2, :w//2].mean()
    q2 = field[:h//2, w//2:].mean()
    q3 = field[h//2:, :w//2].mean()
    q4 = field[h//2:, w//2:].mean()

    return {
        "Q1": q1,
        "Q2": q2,
        "Q3": q3,
        "Q4": q4
    }


# --------------------------------------------------
# HOTSPOTS (LOCAL MAXIMA)
# --------------------------------------------------

def detect_hotspots(field, size=3):
    local_max = (field == maximum_filter(field, size=size))
    coords = np.argwhere(local_max)
    values = [field[x, y] for x, y in coords]

    return list(zip(coords, values))


# --------------------------------------------------
# FLOW ALIGNMENT
# --------------------------------------------------

def flow_alignment(flow_x, flow_y):
    angles = np.arctan2(flow_y, flow_x)
    return np.std(angles)


# --------------------------------------------------
# MOTIF DETECTION (PAIRS)
# --------------------------------------------------

def detect_pairs(field, threshold=0.7):
    pairs = []
    h, w = field.shape

    for i in range(h-1):
        for j in range(w-1):

            if field[i,j] > threshold and field[i+1,j] > threshold:
                pairs.append(((i,j), (i+1,j)))

            if field[i,j] > threshold and field[i,j+1] > threshold:
                pairs.append(((i,j), (i,j+1)))

    return pairs


# --------------------------------------------------
# RANDOM BASELINE
# --------------------------------------------------

def random_field(shape):
    return np.random.rand(*shape)


# --------------------------------------------------
# FULL ANALYSIS
# --------------------------------------------------

def analyze_field(field, flow_x=None, flow_y=None):

    results = {}

    results["symmetry"] = symmetry_score(field)
    results["quadrants"] = quadrant_energy(field)

    hotspots = detect_hotspots(field)
    results["hotspots"] = len(hotspots)

    pairs = detect_pairs(field)
    results["pairs"] = len(pairs)

    if flow_x is not None and flow_y is not None:
        results["flow_alignment"] = flow_alignment(flow_x, flow_y)

    return results


# --------------------------------------------------
# COMPARISON AGAINST RANDOM
# --------------------------------------------------

def compare_with_random(field):

    rand = random_field(field.shape)

    real = analyze_field(field)
    rnd  = analyze_field(rand)

    return {
        "real": real,
        "random": rnd
    }
