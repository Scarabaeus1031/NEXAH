import numpy as np


def compute_gradient_field(landscape):
    """
    Computes gradient field and magnitude.
    """
    gx, gy = np.gradient(landscape)
    grad_mag = np.sqrt(gx**2 + gy**2)
    return gx, gy, grad_mag


def extract_dynamic_boundary(landscape, threshold=0.7, band=0.02):
    """
    Extract boundary around a voltage threshold.
    """
    boundary = np.logical_and(
        landscape > threshold - band,
        landscape < threshold + band
    )
    return boundary


def compute_boundary_strength(grad_mag, boundary):
    """
    Boundary intensity = gradient magnitude restricted to boundary.
    """
    return grad_mag * boundary


def compute_signed_boundary_field(landscape, threshold=0.7):
    """
    Signed scalar field relative to boundary threshold.
    Positive = stable side
    Negative = collapse side
    Zero = boundary
    """
    return landscape - threshold


def normalize_field(field):
    """
    Normalize to [-1, 1] if possible.
    """
    fmin = np.min(field)
    fmax = np.max(field)

    if np.isclose(fmax, fmin):
        return np.zeros_like(field)

    scaled = 2 * (field - fmin) / (fmax - fmin) - 1
    return scaled


def mirror_field_vertical(field):
    """
    Mirror field vertically (flip left-right).
    """
    return np.fliplr(field)


def mirror_field_horizontal(field):
    """
    Mirror field horizontally (flip up-down).
    """
    return np.flipud(field)


def combine_fields(field_a, field_b, mode="difference"):
    """
    Combine two fields.
    Modes:
    - difference
    - sum
    - product
    - average
    """
    if mode == "difference":
        return field_a - field_b
    elif mode == "sum":
        return field_a + field_b
    elif mode == "product":
        return field_a * field_b
    elif mode == "average":
        return 0.5 * (field_a + field_b)
    else:
        raise ValueError(f"Unknown mode: {mode}")
