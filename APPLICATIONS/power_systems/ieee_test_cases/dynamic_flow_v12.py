import numpy as np


def compute_dynamic_flow(gx, gy, strength=0.6, rotation=0.5, noise=0.02, rng_seed=42):
    """
    Combine gradient drift + rotational flow + small stochastic exploration.

    Parameters
    ----------
    gx, gy : 2D arrays
        Gradient field components.
    strength : float
        Weight of the gradient/drift component.
    rotation : float
        Weight of the rotational/curl-like component.
    noise : float
        Small random perturbation to allow regime switching.
    rng_seed : int
        Seed for reproducibility.

    Returns
    -------
    Fx, Fy : 2D arrays
        Dynamic flow field components.
    """
    rng = np.random.default_rng(rng_seed)

    # Drift component
    Ix = gx.copy()
    Iy = gy.copy()

    # Rotational component: perpendicular to gradient
    Rx = -gy
    Ry = gx

    Fx = strength * Ix + rotation * Rx
    Fy = strength * Iy + rotation * Ry

    if noise > 0:
        Fx = Fx + noise * rng.standard_normal(Fx.shape)
        Fy = Fy + noise * rng.standard_normal(Fy.shape)

    return Fx, Fy
