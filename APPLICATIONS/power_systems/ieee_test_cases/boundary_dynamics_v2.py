import numpy as np


def compute_gradient_field(landscape):
    """
    Gradient field (Flow)
    """
    gx, gy = np.gradient(landscape)
    grad_mag = np.sqrt(gx**2 + gy**2)

    return gx, gy, grad_mag


def extract_dynamic_boundary(landscape, threshold=0.7):
    """
    Boundary around voltage threshold
    """
    boundary = np.logical_and(
        landscape > threshold - 0.02,
        landscape < threshold + 0.02
    )

    return boundary


def compute_boundary_strength(grad_mag, boundary):
    """
    Boundary intensity (sharpness)
    """
    strength = grad_mag * boundary
    return strength
