import numpy as np


# --------------------------------------------------
# NORMALIZATION
# --------------------------------------------------

def normalize(field):
    min_val = np.min(field)
    max_val = np.max(field)

    if max_val - min_val < 1e-8:
        return np.zeros_like(field)

    return (field - min_val) / (max_val - min_val)


# --------------------------------------------------
# META FIELD BUILDER
# --------------------------------------------------

def compute_meta_field(
    gradient,
    transition_overlay,
    basin_strength,
    flow_x=None,
    flow_y=None,
    rotation=None
):
    """
    Combine all fields into one meta field
    """

    # --------------------------------------------------
    # NORMALIZE INPUTS
    # --------------------------------------------------

    grad_n = normalize(gradient)
    trans_n = normalize(transition_overlay)
    basin_n = normalize(basin_strength)

    # flow magnitude (optional)
    if flow_x is not None and flow_y is not None:
        flow_mag = np.sqrt(flow_x**2 + flow_y**2)
        flow_n = normalize(flow_mag)
    else:
        flow_n = 0

    # rotation influence (optional)
    if rotation is not None:
        rot_n = normalize(np.abs(rotation))
    else:
        rot_n = 0

    # --------------------------------------------------
    # BUILD COMPONENTS
    # --------------------------------------------------

    # instability = gradient + transitions
    instability = 0.6 * grad_n + 0.8 * trans_n

    # stability = basin inverse
    stability = 1.0 - basin_n

    # flow influence
    flow_component = 0.3 * flow_n

    # rotation influence
    rotation_component = 0.2 * rot_n

    # --------------------------------------------------
    # FINAL META FIELD
    # --------------------------------------------------

    meta = (
        instability
        + flow_component
        + rotation_component
        - 0.5 * stability
    )

    return normalize(meta)


# --------------------------------------------------
# HOT / STABLE ZONES
# --------------------------------------------------

def extract_meta_zones(meta_field, threshold_hot=0.7, threshold_stable=0.3):
    """
    Extract zones from meta field
    """

    hot = (meta_field > threshold_hot).astype(int)
    stable = (meta_field < threshold_stable).astype(int)

    return hot, stable


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":
    print("Meta Field Ready")
